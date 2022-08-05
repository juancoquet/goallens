import datetime as dt
from decimal import Decimal
from django.db.models import Q # type: ignore
import math
from scipy.stats import poisson # type: ignore

from data_sourcing.models import Fixture
from supported_comps import COMP_CODES


class Predictor:

    def generate_prediction(self, fixture, xGs_past_games=5, suppression_range=1, conversion_range=1, sup_con_past_games=5,
                            h_a_weight=1, h_a_past_games=10):
        """generates a prediction for the given fixture.
        
        Args:
            fixture (data_processing.moldels.Fixture): the fixture for which to generate a prediction.
            xGs_past_games (int, optional): the number of past games to use when calculating the base xG. Defaults to 5.
            suppression_range (int, optional): the range around 1 within which to weight the suppression score. Defaults to 1 (0.5-1.5).
            conversion_range (int, optional): the range around 1 within which to weight the conversion score. Defaults to 1 (0.5-1.5).
            sup_con_past_games (int, optional): the number of past games to use when calculating the chance conversion and suppression scores. Defaults to 5.
            h_a_weight (int, optional): value to weight the home/away performance. Defaults to 1.
            h_a_past_games (int, optional): the number of past games to use when calculating h/a performance. Defaults to 10.
        
        Returns:
            dict: a dict that contains the prediction's fixture, forecast xGs, most likely scoreline, and probabilities for eeach number of goals between 0-7. Form is:
                {
                    'fixture': data_sourcing.models.Fixture,
                    'forecast_xGs': {'home': float, 'away': float},
                    'likely_scoreline': {'home': int, 'away': int},
                    'prob_0_goals': {'home': float, 'away': float},
                    ...
                    'prob_7_goals': {'home': float, 'away': float}
        """
        forecast_xGs = self._forecast_xGs(
            fixture,
            xGs_past_games=xGs_past_games,
            suppression_range=suppression_range,
            conversion_range=conversion_range,
            h_a_weight=h_a_weight,
            sup_con_past_games=sup_con_past_games,
            h_a_past_games=h_a_past_games
        )
        prediction = {'fixture': fixture, 'forecast_xGs': forecast_xGs}
        likely_home, likely_away = math.floor(forecast_xGs['home']), math.floor(forecast_xGs['away'])
        prediction['likely_scoreline'] = {'home': likely_home, 'away': likely_away}

        for goals in range(8):
            home = round(poisson.pmf(goals, forecast_xGs['home']), 4)
            away = round(poisson.pmf(goals, forecast_xGs['away']), 4)
            prediction[f'prob_{goals}_goals'] = {'home': home, 'away': away}

        return prediction
    
    def _forecast_xGs(self, fixture: Fixture, xGs_past_games=5, suppression_range=1, conversion_range=1, sup_con_past_games=5,
                    h_a_weight=1, h_a_past_games=10):
        """generates a forecast xG for each team with the following formula:
        fxG = ((bfxG * conversion) + (o_bfxGA * o_suppression)) / 2 * h_a_performance
        where b=base, f=forecast, o=opposition

        Args:
            fixture (Fixture): the fixture for which to generate fxGs
            suppression_weight (int, optional): value to weight the suppression scores. Defaults to 1.
            conversion_weight (int, optional): valus to weight the conversion scores. Defaults to 1.
            h_a_weight (int, optional): value to weight the home/away performance. Defaults to 1.
            past_games (int, optional): the number of past games to use when calculating the base xG. Defaults to 5.
            h_a_past_games (int, optional): the number of past games to use when calculating h/a performance. Defaults to 10.

        Returns:
            dict: {'home': fxG (float), 'away': fxG (float)}
        """
        base_xGs = self._calculate_base_forecast_xGs(fixture, xGs_past_games)
        base_xGAs = self._calculate_base_forecast_xGAs(fixture, xGs_past_games)
        suppression_scores = self._calculate_chance_suppression_scores(fixture, sup_con_past_games, suppression_range)
        conversion_scores = self._calculate_chance_conversion_scores(fixture, sup_con_past_games, conversion_range)
        home_performance = self._calculate_home_away_performance(fixture, 'home', h_a_past_games, h_a_weight)
        away_performance = self._calculate_home_away_performance(fixture, 'away', h_a_past_games, h_a_weight)
        
        home_xG = (
            ((base_xGs['home'] * conversion_scores['home']) + 
            (base_xGAs['away'] * suppression_scores['away'])) / 2
        ) * home_performance

        away_xG = (
            ((base_xGs['away'] * conversion_scores['away']) +
            (base_xGAs['home'] * suppression_scores['home'])) / 2
        ) * away_performance

        home_xG = round(home_xG, 2)
        away_xG = round(away_xG, 2)
        return {'home': home_xG, 'away': away_xG}

    def get_upcoming_fixtures(self, date: dt.date, competition, within_days=2):
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

    def _calculate_base_forecast_xGs(self, fixture, past_games=5):
        """gets the average xG of the last 5 games for each team involced in a
        given fixture. if there is no past xG data, then goals scored is used instead.

        Args:
            fixture (data_sourcing.models.Fixture): fixture to forecast xG for.

        Returns:
            dict: {'home': home_forecast_xG, 'away': away_forecast_xG}
        """
        home_past_5 = self._get_home_team_past_n_fixtures(fixture, past_games)
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
        
        away_past_5 = self._get_away_team_past_n_fixtures(fixture, past_games)
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
        return {'home': float(home_avg_xG), 'away': float(away_avg_xG)}

    def _calculate_base_forecast_xGAs(self, fixture, past_games=5):
        home_past_5 = self._get_home_team_past_n_fixtures(fixture, past_games)
        home_past_5_xGAs = []
        for f in home_past_5:
            if f.home == fixture.home: # if is home team
                if f.xG_away is not None: # opposition xG data (xGA) available
                    home_past_5_xGAs.append(f.xG_away)
                else: # no opposition xG data (xGA) available
                    home_past_5_xGAs.append(f.goals_away)
            else: # if is away team
                if f.xG_home is not None: # opposition xG data (xGA) available
                    home_past_5_xGAs.append(f.xG_home)
                else: # no opposition xG data (xGA) available
                    home_past_5_xGAs.append(f.goals_home)
            try:
                home_avg_xGAs = sum(home_past_5_xGAs) / len(home_past_5_xGAs)
            except ZeroDivisionError:
                home_avg_xGAs = float(0)

        away_past_5 = self._get_away_team_past_n_fixtures(fixture, past_games)
        away_past_5_xGAs = []
        for f in away_past_5:
            if f.home == fixture.away:
                if f.xG_away is not None:
                    away_past_5_xGAs.append(f.xG_away)
                else:
                    away_past_5_xGAs.append(f.goals_away)
            else:
                if f.xG_home is not None:
                    away_past_5_xGAs.append(f.xG_home)
                else:
                    away_past_5_xGAs.append(f.goals_home)
            try:
                away_avg_xGAs = sum(away_past_5_xGAs) / len(away_past_5_xGAs)
            except ZeroDivisionError:
                away_avg_xGAs = float(0)
        return {'home': float(home_avg_xGAs), 'away': float(away_avg_xGAs)}

    def _calculate_chance_suppression_scores(self, fixture, past_games=5, range_=1):
        """calculates the chance suppression scores for a given fixture. chance suppression
        represents a team's ability to defend their opponents' goal scoring chances. values within a given range
        centered at 1 are calculated, e.g from 0.5 to 1.5 (range=1) or from 0.75 to 1.25 (range=0.5). the process is:
            1. get the past n games for each team involved in the fixture
            2. get the total GA and xGA for the past n games
            3. get base score with GA/floor(xGA)
        To weight score:
            if GA/xGA > 1:
                1. turn into a percentage with 1/base score
                2. invert the percentage with 1 - percentage
                3. add 1 to (inverse * 1/2(range))
            else:
                1. invert the percentage with 1 - percentage (GA/xGA is already a percentage if its <= 1)
                2. 1 - (inverse * 1/2(range))

        note that this is an inverted score, so < 1 = good, > 1 = bad.

        Args:
            fixture (data_sourcing.models.Fixture): fixture to calculate suppression scores for.
            past_games (int): number of past games to use to calculate suppression scores.
            range (int/float): the range around 1 within which suppression scores will be calculated. eg a range of 1
            will yield scores between 0.5 and 1.5.

        Returns:
            dict: {'home': home_chance_suppression_score, 'away': away_chance_suppression_score}
        """
        home_base_suppression = self._suppression_score_helper(fixture, past_games, 'home')
        if home_base_suppression > 1:
            percentage = 1 / home_base_suppression
            inverse = 1 - percentage
            home_suppression = 1 + (inverse * (0.5 * range_))
        else:
            inverse = 1 - home_base_suppression
            home_suppression = 1 - (inverse * (0.5 * range_))

        away_base_suppression = self._suppression_score_helper(fixture, past_games, 'away')
        if away_base_suppression > 1:
            percentage = 1 / away_base_suppression
            inverse = 1 - percentage
            away_suppression = 1 + (inverse * (0.5 * range_))
        else:
            inverse = 1 - away_base_suppression
            away_suppression = 1 - (inverse * (0.5 * range_))
        return {'home': round(home_suppression, 2), 'away': round(away_suppression, 2)}

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
        # print(f'{home_or_away} ga: {total_ga}, xga: {total_xga}')
        try:
            base_suppression = total_ga / math.floor(total_xga)
        except ZeroDivisionError:
            base_suppression = 1
        return base_suppression

    def _calculate_chance_conversion_scores(self, fixture, past_games=5, range_=1):
        """calculates the chance conversion scores for a given fixture. chance conversion
        represents a team's ability to convert their goal scoring chances. values within a given
        range centered at 1 are calculated, e.g. from 0.5 to 1.5 (range=1) or from 0.75 to 1.25 
        (range=0.5) the process is:
            1. get the past n games for each team involved in the fixture
            2. get the total G and xG for the past n games
            3. get base score with G/xG
        To weight score:
            if G/xG > 1:
                1. turn into a percentage with 1/base score
                2. invert the percentage with 1 - percentage
                3. add 1 to (inverse * 1/2(range))
            else:
                1. invert the percentage with 1 - percentage (G/xG is already a percentage if its <= 1)
                2. 1 - (inverse * 1/2(range))
        scores > 1 = good, < 1 = bad.

        Args:
            fixture (data_sourcing.models.Fixture): fixture to calculate conversion scores for.
            past_games (int): number of past games to use to calculate conversion scores.
            range (int | float): the range around 1 within which conversion scores will be calculated. eg a range of 1
            will yield scores between 0.5 and 1.5.
        Returns:
            dict: {'home': home_chance_conversion_score, 'away': away_chance_conversion_score}
        """
        home_base_conversion = self._conversion_score_helper(fixture, past_games, 'home')
        if home_base_conversion > 1:
            percentage = 1 / home_base_conversion
            inverse = 1 - percentage
            home_conversion = 1 + (inverse * (0.5 * range_))
        else:
            inverse = 1 - home_base_conversion
            home_conversion = 1 - (inverse * (0.5 * range_))

        away_base_conversion = self._conversion_score_helper(fixture, past_games, 'away')
        if away_base_conversion > 1:
            percentage = 1 / away_base_conversion
            inverse = 1 - percentage
            away_conversion = 1 + (inverse * (0.5 * range_))
        else:
            inverse = 1 - away_base_conversion
            away_conversion = 1 - (inverse * (0.5 * range_))

        return {'home': round(home_conversion, 2), 'away': round(away_conversion, 2)}

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
            base_conversion = total_g / math.floor(total_xg)
        except ZeroDivisionError:
            base_conversion = 1
        return base_conversion

    def _get_home_team_past_n_fixtures(self, fixture, n=5):
        past_n_fixtures = Fixture.objects.filter(
            Q(home=fixture.home) | Q(away=fixture.home),
            date__lt=fixture.date,
        ).order_by('-date')[:n]
        if len(past_n_fixtures) < n:
            raise(NotEnoughDataError(f'fixture {fixture.id} has fewer than {n} past fixtures'))
        return list(past_n_fixtures)

    def _get_away_team_past_n_fixtures(self, fixture, n=5):
        past_n_fixtures = Fixture.objects.filter(
            Q(home=fixture.away) | Q(away=fixture.away),
            date__lt=fixture.date,
        ).order_by('-date')[:n]
        if len(past_n_fixtures) < n:
            raise(NotEnoughDataError(f'fixture {fixture.id} has fewer than {n} past fixtures'))
        return list(past_n_fixtures)

    def _calculate_home_away_performance(self, fixture, home_or_away, past_games=10, weight=1):
        """calculates the recent home/away goalscoring performance for a team in the given fixture.
        e.g. if passed 'home', it will calculate recent home performance for the home team in the
        given fixture.
        
        Args:
            home_or_away (str): 'home' or 'away'.
            past_games (int): number of past games to use to calculate the performance.

        Returns:
            float: recent home/away performance for the given team.
        """
        if home_or_away != 'home' and home_or_away != 'away':
            raise(ValueError(f'home_or_away must be "home" or "away"'))

        if home_or_away == 'home':
            home_team = fixture.home
            past_n_home_fixtures = Fixture.objects.filter(
                home=home_team,
                date__lt=fixture.date,
            ).order_by('-date')[:past_games]
            past_n_away_fixtures = Fixture.objects.filter(
                away=home_team,
                date__lt=fixture.date,
            ).order_by('-date')[:past_games]
            home_goals = [f.goals_home for f in past_n_home_fixtures]
            away_goals = [f.goals_away for f in past_n_away_fixtures]
            agnostic = (sum(home_goals) + sum(away_goals)) / 2
            try:
                result = sum(home_goals) / agnostic
            except ZeroDivisionError:
                result = 1.0
        else:
            away_team = fixture.away
            past_n_home_fixtures = Fixture.objects.filter(
                home=away_team,
                date__lt=fixture.date,
            ).order_by('-date')[:past_games]
            past_n_away_fixtures = Fixture.objects.filter(
                away=away_team,
                date__lt=fixture.date,
            ).order_by('-date')[:past_games]
            home_goals = [f.goals_home for f in past_n_home_fixtures]
            away_goals = [f.goals_away for f in past_n_away_fixtures]
            agnostic = (sum(home_goals) + sum(away_goals)) / 2
            try:
                result = sum(away_goals) / agnostic
            except ZeroDivisionError:
                result = 1.0
        weight_delta = result - 1
        weighted_delta = weight_delta * weight
        weighted_result = round((1 + weighted_delta), 2)
        return weighted_result
        

class NotEnoughDataError(ValueError):
    """raised when there are not enough data points to process a fixture."""
    pass