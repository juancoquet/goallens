import csv
from datetime import date, time
from decimal import Decimal
from unittest import skip
from django.test import TestCase

from ..predictor import Predictor
from data_sourcing.db_population.db_population import DBPopulator
from data_sourcing.models import Fixture, Team


class TestPredictor(TestCase):

    # get fixtures within next n days
        # take a date (default tot today) as an argument
        # take n as an argument, default to 2 (passed date + 2 days)
        # return list of fixtures within that period
    # use fixture data to make necessary calculations

    # test date fri 2022-04-30

    @classmethod
    def setUpTestData(cls):
        with open('predictions/tests/teams.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Team.objects.create(
                    id=row['id'],
                    name=row['team_name'], 
                    short_name=row['team_short_name']
                )
        with open('predictions/tests/fixtures.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Fixture.objects.create(
                    id=row['id'],
                    competition=row['competition'],
                    season=row['season'],
                    date=date.fromisoformat(row['date']),
                    time=time(int(row['time'].split(':')[0]), int(row['time'].split(':')[1])),
                    home=Team.objects.get(id=row['home']),
                    away=Team.objects.get(id=row['away']),
                    goals_home=row['goals_home'],
                    goals_away=row['goals_away'],
                    xG_home=Decimal(row['xG_home']) if row['xG_home'] else None,
                    xG_away=Decimal(row['xG_away']) if row['xG_away'] else None,
                )
        cls.predictor = Predictor()
        cls.fixture = Fixture.objects.get(id='7b4b63d0')
    
    def test_get_upcoming_fixtures(self):
        fixtures = self.predictor._get_upcoming_fixtures(
            date=date(year=2022, month=4, day=30),
            competition='Premier League',
            within_days=2
        )
        self.assertEqual(len(fixtures), 10)
        fixtures = self.predictor._get_upcoming_fixtures(
            date=date(year=2022, month=5, day=1),
            competition='Premier League',
            within_days=0
        )
        self.assertEqual(len(fixtures), 3)

    def test_get_upcoming_fixtures_cannot_be_future_date(self):
        with self.assertRaises(ValueError):
            self.predictor._get_upcoming_fixtures(
                date=date(year=2999, month=5, day=1),
                competition='Premier League',
                within_days=2
            )

    def test_get_upcoming_fixtures_raises_invalid_comp(self):
        with self.assertRaises(ValueError):
            self.predictor._get_upcoming_fixtures(
                date=date(year=2022, month=4, day=30),
                competition='invalid',
                within_days=2
            )

    def test_calculate_base_forecast_xG(self):
        xGs = self.predictor._calculate_base_forecast_xG(self.fixture)
        expected = {'home': Decimal('2.88'), 'away': Decimal('1.48')}
        self.assertEqual(xGs, expected)
        fixture = Fixture.objects.get(id='620ebbfd')
        xGs = self.predictor._calculate_base_forecast_xG(fixture)
        expected = {'home': Decimal('0.48'), 'away': Decimal('1.18')}
        self.assertEqual(xGs, expected)

    def test_calculate_base_forecast_xG_with_no_past_xG_data(self):
        fixture = Fixture.objects.get(id='ae30a29c')
        xGs = self.predictor._calculate_base_forecast_xG(fixture)
        expected = {'home': Decimal('1.0'), 'away': Decimal('2.0')}
        self.assertEqual(xGs, expected)

    def test_get_past_5_home_fixtures(self):
        fixtures = self.predictor._get_home_team_past_n_fixtures(self.fixture)
        ids = ['f94c5f85', 'a93c0c92', 'd1bcaf2b', '5ce80a04', 'af522ca3']
        expected = [Fixture.objects.get(id=id) for id in ids]
        self.assertEqual(fixtures, expected)

    def test_get_past_5_away_fixtures(self):
        fixtures = self.predictor._get_away_team_past_n_fixtures(self.fixture)
        ids = ['bc4f902e', 'd2e9e9e3', '1016efad', 'c1dc9202', 'bf7873f2']
        expected = [Fixture.objects.get(id=id) for id in ids]
        self.assertEqual(fixtures, expected)

    def test_not_enough_past_fixtures_raises(self):
        with self.assertRaises(ValueError):
            fixture = Fixture.objects.get(id='f34dd009')
            fixtures = self.predictor._get_away_team_past_n_fixtures(fixture)
        with self.assertRaises(ValueError):
            fixture = Fixture.objects.get(id='072bfc99')
            fixtures = self.predictor._get_home_team_past_n_fixtures(fixture)

    def test_calculate_defensive_scores(self):
        defensive_scores = self.predictor._calculate_defensive_scores(self.fixture, past_games=5)
        expected = {'home': 1.0, 'away': 0.71}
        self.assertEqual(defensive_scores, expected)

    def test_calculate_defesive_score_no_xG_data(self):
        fixture = Fixture.objects.get(id='ae30a29c')
        defensive_scores = self.predictor._calculate_defensive_scores(fixture, past_games=5)
        expected = {'home': 1.0, 'away': 1.0}

    # TODO: test weighted
    def test_calculate_defensive_scores_weighted(self):
        defensive_scores = self.predictor._calculate_defensive_scores(self.fixture, past_games=5, weight=0.5)
        expected = {'home': 1.0, 'away': 0.86}
        self.assertEqual(defensive_scores, expected)