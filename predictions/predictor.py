from cmath import e
import datetime as dt
from decimal import Decimal
from turtle import home
from django.db.models import Q
import math

from data_sourcing.models import Fixture
from supported_comps import COMP_CODES


class Predictor:

    def __init__(self):
        self.upcoming_fixtures = []

    def _get_upcoming_fixtures(self, date: dt.date, competition, within_days=2):
        if competition not in COMP_CODES:
            valid_comps = [k for k in COMP_CODES]
            raise ValueError(f'competion must be one of {valid_comps} – {competition} is invalid')
        if date > dt.date.today():
            raise ValueError(f'date must be in the past – {date} is invalid')
        end_date = date + dt.timedelta(days=within_days)
        fixtures = Fixture.objects.filter(
            competition=competition,
            date__gte=date,
            date__lte=end_date
        ).order_by('date')
        return fixtures

    def _calculate_base_forecast_xG(self, fixture):
        """gets the average xG of the last 5 games for each team involced in a
        given fixture. if there is no past xG data, then goals scored is used instead.

        Args:
            fixture (data_sourcing.models.Fixture): fixture to forecast xG for.

        Returns:
            dict: {'home': home_forecast_xG, 'away': away_forecast_xG}
        """
        home_past_5 = self._get_home_team_past_n_fixtures(fixture)
        home_past_5_xGs = []
        for f in home_past_5:
            if f.home == fixture.home:
                if f.xG_home is not None:
                    home_past_5_xGs.append(f.xG_home)
                else:
                    home_past_5_xGs.append(f.goals_home)
            else:
                if f.xG_away is not None:
                    home_past_5_xGs.append(f.xG_away)
                else:
                    home_past_5_xGs.append(f.goals_away)
            try:
                home_avg_xG = sum(home_past_5_xGs) / len(home_past_5_xGs)
            except ZeroDivisionError:
                home_avg_xG = float(0)
        
        away_past_5 = self._get_away_team_past_n_fixtures(fixture)
        away_past_5_xGs = []
        for f in away_past_5:
            if f.home == fixture.away:
                if f.xG_home is not None:
                    away_past_5_xGs.append(f.xG_home)
                else:
                    away_past_5_xGs.append(f.goals_home)
            else:
                if f.xG_away is not None:
                    away_past_5_xGs.append(f.xG_away)
                else:
                    away_past_5_xGs.append(f.goals_away)
            try:
                away_avg_xG = sum(away_past_5_xGs) / len(away_past_5_xGs)
            except ZeroDivisionError:
                away_avg_xG = Decimal('0.0')
        return {'home': home_avg_xG, 'away': away_avg_xG}

    def _calculate_chance_suppression_scores(self, fixture, past_games=5, weight=1):
        """calculates the chance suppression scores for a given fixture. chance suppression
        represents a team's ability to defend their opponents' goal scoring chances. the process is:
            1. get the past n games for each team involved in the fixture
            2. get the total GA and xGA for the past n games
            3. get unweighted score with GA/floor(xGA)
        To weight score:
            1. get the difference between 1 and the unweighted score
            2. multiply the difference by the weight
            3. subtract the multiplied difference from 1

        note that this is an inverted score, so < 1 = good, > 1 = bad.

        Args:
            fixture (data_sourcing.models.Fixture): fixture to calculate suppression scores for.
            past_games (int): number of past games to use to calculate suppression scores.
            weight (int): weight to apply to the chance suppression scores.

        Returns:
            dict: {'home': home_chance_suppression_score, 'away': away_chance_suppression_score}
        """
        unweighted_home_score = self._suppression_score_helper(fixture, past_games, 'home')
        home_weighting_delta = 1 - unweighted_home_score
        home_weighted_delta = home_weighting_delta * weight
        home_weighted_score = round((1 - home_weighted_delta), 2)

        unweighted_away_score = self._suppression_score_helper(fixture, past_games, 'away')
        away_weighting_delta = 1 - unweighted_away_score
        away_weighted_delta = away_weighting_delta * weight
        away_weighted_score = round((1 - away_weighted_delta), 2)
        return {'home': home_weighted_score, 'away': away_weighted_score}

    def _suppression_score_helper(self, fixture, n_games, home_or_away: str):
        """helper function for calculating chance suppression scores.

        Args:
            fixture (data_sourcing.models.Fixture): fixture to calculate suppression scores for.
            home_or_away (str): 'home' or 'away'.

        Returns:
            float: suppression score for the given team.
        """
        h_or_a = {'home': fixture.home, 'away': fixture.away}
        if home_or_away == 'home':
            past_games = self._get_home_team_past_n_fixtures(fixture, n_games)
        else:
            past_games = self._get_away_team_past_n_fixtures(fixture, n_games)
        past_games_ga = []
        past_games_xga = []
        for f in past_games:
            if f.away == h_or_a[home_or_away]:
                if f.xG_home is not None:
                    past_games_ga.append(f.goals_home)
                    past_games_xga.append(float(f.xG_home))
                else:
                    past_games_ga.append(f.goals_home)
                    past_games_xga.append(f.goals_home)
            else:
                if f.xG_away is not None:
                    past_games_ga.append(f.goals_away)
                    past_games_xga.append(float(f.xG_away))
                else:
                    past_games_ga.append(f.goals_away)
                    past_games_xga.append(f.goals_away)
        total_ga = sum(past_games_ga)
        total_xga = sum(past_games_xga)
        try:
            unweighted_score = total_ga / math.floor(total_xga)
        except ZeroDivisionError:
            unweighted_score = 1
        return unweighted_score

    def _calculate_chance_conversion_scores(self, fixture, past_games=5, weight=1):
        """calculates the chance conversion scores for a given fixture. chance conversion
        represents a team's ability to convert their goal scoring chances. the process is:
            1. get the past n games for each team involved in the fixture
            2. get the total G and xG for the past n games
            3. get unweighted score with G/xG
        To weight score:
            1. get the difference between 1 and the unweighted score
            2. multiply the difference by the weight
            3. subtract the multiplied difference from 1

        scores > 1 = good, < 1 = bad.

        Args:
            fixture (data_sourcing.models.Fixture): fixture to calculate conversion scores for.
            past_games (int): number of past games to use to calculate conversion scores.
            weight (int): weight to apply to the chance conversion scores.

        Returns:
            dict: {'home': home_chance_conversion_score, 'away': away_chance_conversion_score}
        """
        unweighted_home_score = self._conversion_score_helper(fixture, past_games, 'home')
        home_weighting_delta = unweighted_home_score - 1
        home_weighted_delta = home_weighting_delta * weight
        home_weighted_score = round((1 + home_weighted_delta), 2)

        unweighted_away_score = self._conversion_score_helper(fixture, past_games, 'away')
        away_weighting_delta = unweighted_away_score - 1
        away_weighted_delta = away_weighting_delta * weight
        away_weighted_score = round((1 + away_weighted_delta), 2)
        return {'home': home_weighted_score, 'away': away_weighted_score}

    def _conversion_score_helper(self, fixture, n_games, home_or_away: str):
        """helper function for calculating chance conversion scores.

        Args:
            fixture (data_sourcing.models.Fixture): fixture to calculate conversion scores for.
            home_or_away (str): 'home' or 'away'.

        Returns:
            float: conversion score for the given team.
        """
        h_or_a = {'home': fixture.home, 'away': fixture.away}
        if home_or_away == 'home':
            past_games = self._get_home_team_past_n_fixtures(fixture, n_games)
        else:
            past_games = self._get_away_team_past_n_fixtures(fixture, n_games)
        past_games_g = []
        past_games_xg = []
        for f in past_games:
            if f.home == h_or_a[home_or_away]:
                if f.xG_home is not None:
                    past_games_g.append(f.goals_home)
                    past_games_xg.append(float(f.xG_home))
                else:
                    past_games_g.append(f.goals_home)
                    past_games_xg.append(f.goals_home)
            else:
                if f.xG_away is not None:
                    past_games_g.append(f.goals_away)
                    past_games_xg.append(float(f.xG_away))
                else:
                    past_games_g.append(f.goals_away)
                    past_games_xg.append(f.goals_away)
        total_g = sum(past_games_g)
        total_xg = sum(past_games_xg)
        try:
            unweighted_score = total_g / math.floor(total_xg)
        except ZeroDivisionError:
            unweighted_score = 1
        return unweighted_score

    def _get_home_team_past_n_fixtures(self, fixture, n=5):
        past_n_fixtures = Fixture.objects.filter(
            Q(home=fixture.home) | Q(away=fixture.home),
            date__lt=fixture.date,
        ).order_by('-date')[:n]
        if len(past_n_fixtures) < n:
            raise(ValueError(f'fixture {fixture.id} has fewer than {n} past fixtures'))
        return list(past_n_fixtures)

    def _get_away_team_past_n_fixtures(self, fixture, n=5):
        past_n_fixtures = Fixture.objects.filter(
            Q(home=fixture.away) | Q(away=fixture.away),
            date__lt=fixture.date,
        ).order_by('-date')[:n]
        if len(past_n_fixtures) < n:
            raise(ValueError(f'fixture {fixture.id} has fewer than {n} past fixtures'))
        return list(past_n_fixtures)