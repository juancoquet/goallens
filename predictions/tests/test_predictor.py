import csv
from datetime import date, time
from decimal import Decimal
from unittest import skip
from django.test import TestCase # type: ignore

from ..predictor import NotEnoughDataError, Predictor
from data_sourcing.db_population.db_population import DBPopulator
from data_sourcing.models import Fixture, Team


class TestPredictor(TestCase):

    maxDiff = None

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
        fixtures = self.predictor.get_upcoming_fixtures(
            date=date(year=2022, month=4, day=30),
            competition='Premier League',
            within_days=2
        )
        self.assertEqual(len(fixtures), 10)
        fixtures = self.predictor.get_upcoming_fixtures(
            date=date(year=2022, month=5, day=1),
            competition='Premier League',
            within_days=0
        )
        self.assertEqual(len(fixtures), 3)

    def test_get_upcoming_fixtures_cannot_be_future_date(self):
        with self.assertRaises(ValueError):
            self.predictor.get_upcoming_fixtures(
                date=date(year=2999, month=5, day=1),
                competition='Premier League',
                within_days=2
            )

    def test_get_upcoming_fixtures_raises_invalid_comp(self):
        with self.assertRaises(ValueError):
            self.predictor.get_upcoming_fixtures(
                date=date(year=2022, month=4, day=30),
                competition='invalid',
                within_days=2
            )

    def test_calculate_base_forecast_xG(self):
        xGs = self.predictor._calculate_base_forecast_xGs(self.fixture)
        expected = {'home': 2.88, 'away': 1.48}
        self.assertEqual(xGs, expected)
        fixture = Fixture.objects.get(id='620ebbfd')
        xGs = self.predictor._calculate_base_forecast_xGs(fixture)
        expected = {'home': 0.48, 'away': 1.18}
        self.assertEqual(xGs, expected)
        fixture = Fixture.objects.get(id='37e2fe92')
        xGs = self.predictor._forecast_xGs(fixture)
        expected = {'home': 2.56, 'away': 2.08}

    def test_calculate_base_forecast_xG_with_no_past_xG_data(self):
        fixture = Fixture.objects.get(id='ae30a29c')
        xGs = self.predictor._calculate_base_forecast_xGs(fixture)
        expected = {'home': 1.0, 'away': 2.0}
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

    
    def test_calculate_home_performance_score(self):
        home_perfomance = self.predictor._calculate_home_away_performance(self.fixture, 'home', past_games=10)
        expected = 1.25
        self.assertEqual(home_perfomance, expected)

    def test_calculate_away_performance_score(self):
        away_perfomance = self.predictor._calculate_home_away_performance(self.fixture, 'away', past_games=10)
        expected = 1.0
        self.assertEqual(away_perfomance, expected)

    def test_calculate_h_a_performance_no_goals_scored(self):
        fixture = Fixture.objects.get(id='63496f6c')
        perf = self.predictor._calculate_home_away_performance(fixture, 'away', past_games=10)
        expected = 1.0
        self.assertEqual(perf, expected)

    def test_calculate_home_away_performance_weighted(self):
        home_perfomance = self.predictor._calculate_home_away_performance(self.fixture, 'home', past_games=10, weight=0.5)
        expected = 1.13
        self.assertEqual(home_perfomance, expected)

    def test_forecast_xGs(self):
        xGs = self.predictor._forecast_xGs(self.fixture)
        expected = {'home': 2.87, 'away': 1.22}
        self.assertEqual(xGs, expected)
        
    def test_forecast_xG_with_not_enough_past_game_data(self):
        with self.assertRaises(NotEnoughDataError):
            fixture = Fixture.objects.get(id='b015cd93')
            xGs = self.predictor._forecast_xGs(fixture)

    def test_generate_predictions(self):
        predictions = self.predictor.generate_prediction(self.fixture)
        expected = {
            'fixture': self.fixture,
            'forecast_xGs': {'home': 2.87, 'away': 1.22},
            'prob_0_goals': {'home': 0.0567, 'away': 0.2952},
            'prob_1_goals': {'home': 0.1627, 'away': 0.3602},
            'prob_2_goals': {'home': 0.2335, 'away': 0.2197},
            'prob_3_goals': {'home': 0.2234, 'away': 0.0893},
            'prob_4_goals': {'home': 0.1603, 'away': 0.0273},
            'prob_5_goals': {'home': 0.092, 'away': 0.0066},
            'prob_6_goals': {'home': 0.044, 'away': 0.0014},
            'prob_7_goals': {'home': 0.018, 'away': 0.0002},
            'likely_scoreline': {'home': 2, 'away': 1}
        }
        self.assertEqual(predictions, expected)

    # def test_generate_upcoming_predictions(self):
    #     predictions = self.predictor.generate_upcoming_predictions(['Premier League'], date=date(2022, 5, 16))
    #     self.assertEqual(len(predictions), 2)
    #     self.assertEqual(predictions[0]['fixture'].id, 'a3b3a0d5')
    #     self.assertEqual(predictions[1]['fixture'].id, '733409b2')


class TestSuppressionScores(TestCase):
    
    maxDiff = None

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

    
    def test_calculate_suppression_scores(self):
        fixture = Fixture.objects.get(id='79b8fb6e')
        suppression_scores = self.predictor._calculate_chance_suppression_scores(fixture)
        expected = {'home': 1.17, 'away': 1.1} # values for new function implementation
        self.assertEqual(suppression_scores, expected)
        fixture = Fixture.objects.get(id='37e2fe92')
        suppression_scores = self.predictor._calculate_chance_suppression_scores(fixture, past_games=5)
        expected = {'home': 1.0, 'away': 0.5} # values for new function implementation
        self.assertEqual(suppression_scores, expected)

    def test_calculate_suppression_score_no_xG_data(self):
        fixture = Fixture.objects.get(id='ae30a29c')
        defensive_scores = self.predictor._calculate_chance_suppression_scores(fixture, past_games=5)
        expected = {'home': 1.0, 'away': 1.0}
        self.assertEqual(defensive_scores, expected)

    def test_calculate_suppression_scores_custom_range(self):
        fixture = Fixture.objects.get(id='79b8fb6e')
        defensive_scores = self.predictor._calculate_chance_suppression_scores(fixture, past_games=5, range_=0.5)
        expected = {'home': 1.08, 'away': 1.05}
        self.assertEqual(defensive_scores, expected)


class TestConversionScores(TestCase):

    maxDiff = None

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

    def test_calculate_chance_conversion_scores(self):
        fixture = Fixture.objects.get(id='59b3ee40')
        conversion_scores = self.predictor._calculate_chance_conversion_scores(fixture, past_games=5)
        expected = {'home': 0.67, 'away': 1.18}
        self.assertEqual(conversion_scores, expected)

    def test_calculate_chance_conversion_scores_no_xG_data(self):
        fixture = Fixture.objects.get(id='ae30a29c')
        conversion_scores = self.predictor._calculate_chance_conversion_scores(fixture, past_games=5)
        expected = {'home': 1.0, 'away': 1.0}
        self.assertEqual(conversion_scores, expected)

    def test_calculate_chance_conversion_scores_custom_range(self):
        fixture = Fixture.objects.get(id='59b3ee40')
        conversion_scores = self.predictor._calculate_chance_conversion_scores(fixture, past_games=5, range_=0.5)
        expected = {'home': 0.83, 'away': 1.09}
        self.assertEqual(conversion_scores, expected)


class TestForecastxGA(TestCase):

    maxDiff = None

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

    def test_calculate_base_forecast_xGA(self):
        xGAs = self.predictor._calculate_base_forecast_xGAs(self.fixture)
        expected = {'home': 0.88, 'away': 1.42}
        self.assertEqual(xGAs, expected)
        
    def test_calculate_base_forecast_xGA_with_no_past_xG_data(self):
        fixture = Fixture.objects.get(id='ae30a29c')
        xGAs = self.predictor._calculate_base_forecast_xGAs(fixture)
        expected = {'home': 1.2, 'away': 1.2}
        self.assertEqual(xGAs, expected)