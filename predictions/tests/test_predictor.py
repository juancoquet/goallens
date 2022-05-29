import csv
from datetime import date, time
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

    def setUp(self):
        self.predictor = Predictor()
        self.populator = DBPopulator()
        with open('predictions/tests/teams.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.populator.add_team_to_db(
                    team_id=row['id'],
                    team_name=row['team_name'],
                    team_short_name=row['team_short_name'],
                )
        with open('predictions/tests/fixtures.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.populator.add_fixture_to_db(
                    fixture_id=row['id'],
                    competition=row['competition'],
                    season=row['season'],
                    date=date.fromisoformat(row['date']),
                    time=time(int(row['time'].split(':')[0]), int(row['time'].split(':')[1])),
                    home_team_id=row['home'],
                    away_team_id=row['away'],
                    goals_home=row['goals_home'],
                    goals_away=row['goals_away'],
                    xG_home=row['xG_home'],
                    xG_away=row['xG_away'],
                )
    
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