import datetime as dt
from decimal import Decimal
from django.db.models import Q

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
        home_past_5 = self._get_home_team_past_5_fixtures(fixture)
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
        
        away_past_5 = self._get_away_team_past_5_fixtures(fixture)
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

    def _get_home_team_past_5_fixtures(self, fixture):
        home_past_5_fixtures = Fixture.objects.filter(
            Q(home=fixture.home) | Q(away=fixture.home),
            date__lt=fixture.date,
        ).order_by('-date')[:5]
        if len(home_past_5_fixtures) < 5:
            raise(ValueError(f'fixture {fixture.id} has fewer than 5 past fixtures'))
        return list(home_past_5_fixtures) 

    def _get_away_team_past_5_fixtures(self, fixture):
        away_past_5_fixtures = Fixture.objects.filter(
            Q(home=fixture.away) | Q(away=fixture.away),
            date__lt=fixture.date,
        ).order_by('-date')[:5]
        if len(away_past_5_fixtures) < 5:
            raise(ValueError(f'fixture {fixture.id} has fewer than 5 past fixtures'))
        return list(away_past_5_fixtures)