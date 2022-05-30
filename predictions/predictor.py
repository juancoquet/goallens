import datetime as dt
from decimal import Decimal
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

    def _calculate_defensive_scores(self, fixture, past_games=5, weight=1):
        """calculates the defensive scores for a given fixture. the process is:
            1. get the past n games for each team involved in the fixture
            2. get the total GA and xGA for the past n games
            3. get unweighted score with GA/floor(xGA)
        To weight score:
            1. get the difference between 1 and the unweighted score
            2. multiply the difference by the weight
            3. subtract the multiplied difference from 1

        Args:
            fixture (data_sourcing.models.Fixture): fixture to calculate defensive scores for.
            past_games (int): number of past games to use to calculate defensive scores.
            weight (int): weight to apply to the defensive scores.

        Returns:
            dict: {'home': home_defensive_score, 'away': away_defensive_score}
        """
        home_past_games = self._get_home_team_past_n_fixtures(fixture, n=past_games)
        away_past_games = self._get_away_team_past_n_fixtures(fixture, n=past_games)

        home_past_games_ga = []
        home_past_games_xga = []
        for f in home_past_games:
            if f.away == fixture.home: # if was away in the fixture, append home team's stats
                if f.xG_home is not None:
                    home_past_games_ga.append(f.goals_home)
                    home_past_games_xga.append(float(f.xG_home))
                else: # if no xG data, use goals scored (renders a neutral defensive score)
                    home_past_games_ga.append(f.goals_home)
                    home_past_games_xga.append(f.goals_home)
            else: # if was home in the fixture, append away team's stats
                if f.xG_away is not None:
                    home_past_games_ga.append(f.goals_away)
                    home_past_games_xga.append(float(f.xG_away))
                else: # if no xG data, use goals scored (renders a neutral defensive score)
                    home_past_games_ga.append(f.goals_away)
                    home_past_games_xga.append(f.goals_away)
        total_home_ga = sum(home_past_games_ga)
        total_home_xga = sum(home_past_games_xga)
        unweighted_home_score = total_home_ga / math.floor(total_home_xga)
        weighting_delta = 1 - unweighted_home_score
        weighted_delta = weighting_delta * weight
        weighted_home_score = 1 - weighted_delta

        away_past_games_ga = []
        away_past_games_xga = []
        for f in away_past_games:
            if f.away == fixture.away: # if was away in the fixture, append home team's stats
                if f.xG_home is not None:
                    away_past_games_ga.append(f.goals_home)
                    away_past_games_xga.append(float(f.xG_home))
                else: # if no xG data, use goals scored (renders a neutral defensive score)
                    away_past_games_ga.append(f.goals_home)
                    away_past_games_xga.append(f.goals_home)
            else: # if was home in the fixture, append away team's stats
                if f.xG_away is not None:
                    away_past_games_ga.append(f.goals_away)
                    away_past_games_xga.append(float(f.xG_away))
                else: # if no xG data, use goals scored (renders a neutral defensive score)
                    away_past_games_ga.append(f.goals_away)
                    away_past_games_xga.append(f.goals_away)
        total_away_ga = sum(away_past_games_ga)
        total_away_xga = sum(away_past_games_xga)
        unweighted_away_score = total_away_ga / math.floor(total_away_xga)
        weighting_delta = 1 - unweighted_away_score
        weighted_delta = weighting_delta * weight
        weighted_away_score = 1 - weighted_delta
        
        weighted_home_score = round(weighted_home_score, 2)
        weighted_away_score = round(weighted_away_score, 2)
        return {'home': weighted_home_score, 'away': weighted_away_score}

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