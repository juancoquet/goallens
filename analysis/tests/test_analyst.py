from cmath import nan
import csv
from decimal import Decimal
from datetime import date, time
from django.test import TestCase # type: ignore
import pandas as pd # type: ignore

from ..analyst import Analyst
from data_sourcing.models import Fixture, Team
from predictions.predictor import Predictor


class TestAnalyst(TestCase):

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
        cls.analyst = Analyst()

    def test_check_prediction_outcomes(self):
        prediction = self.predictor.generate_prediction(self.fixture)
        outcomes = self.analyst._check_prediction_outcomes(prediction)
        expected = {
            '0_goals': {'home': 0, 'away': 0},
            '1_goals': {'home': 0, 'away': 0},
            '2_goals': {'home': 0, 'away': 1},
            '3_goals': {'home': 1, 'away': 0},
            '4_goals': {'home': 0, 'away': 0},
            '5_goals': {'home': 0, 'away': 0},
            '6_goals': {'home': 0, 'away': 0},
            '7_goals': {'home': 0, 'away': 0},
        }
        self.assertEqual(outcomes, expected)
        fixture = Fixture.objects.get(id='ad903480')
        prediction = self.predictor.generate_prediction(fixture)
        outcomes = self.analyst._check_prediction_outcomes(prediction)
        expected = {
            '0_goals': {'home': 0, 'away': 0},
            '1_goals': {'home': 0, 'away': 1},
            '2_goals': {'home': 1, 'away': 0},
            '3_goals': {'home': 0, 'away': 0},
            '4_goals': {'home': 0, 'away': 0},
            '5_goals': {'home': 0, 'away': 0},
            '6_goals': {'home': 0, 'away': 0},
            '7_goals': {'home': 0, 'away': 0},
        }
        self.assertEqual(outcomes, expected)
        
    def test_combine_predictions_and_outcomes(self):
        prediction = self.predictor.generate_prediction(self.fixture)
        pred_copy = prediction.copy()
        outcomes = self.analyst._check_prediction_outcomes(prediction)
        combined = self.analyst._combine_predictions_and_outcomes(pred_copy, outcomes)
        expected = [
            (0.0567, 0), (0.2952, 0),
            (0.1627, 0), (0.3602, 0),
            (0.2335, 0), (0.2197, 1),
            (0.2234, 1), (0.0893, 0),
            (0.1603, 0), (0.0273, 0),
            (0.092,  0), (0.0066, 0),
            (0.044,  0), (0.0014, 0),
            (0.018,  0), (0.0002, 0)
        ]
        self.assertEqual(combined, expected)
                
    def test_create_analysis_df(self):
        self.assertEqual(self.analyst.df, None)
        df = self.analyst.create_analysis_df(seasons=['2020-2021', '2021-2022'], competitions=['Premier League'])
        self.assertEqual(df.shape, (380*16*2, 2)) # 380 fixtures per season, 16 predictions per fx, 2 seasons
        self.assertEqual(type(self.analyst.df), type(df))

    def test_create_analysis_df_only_accepts_lists_as_args(self):
        with self.assertRaises(TypeError):
            self.analyst.create_analysis_df(seasons=['2019-2020'], competitions='Premier League')
        with self.assertRaises(TypeError):
            self.analyst.create_analysis_df(seasons='2019-2020', competitions=['Premier League'])

    def test_invalid_season_or_competition_raises_error(self):
        with self.assertRaises(ValueError):
            self.analyst.create_analysis_df(seasons=['2019-2020'], competitions=['Premier League', 'Serie A', 'Invalid'])
        with self.assertRaises(ValueError):
            self.analyst.create_analysis_df(seasons=['2019-2020', 'Invalid'], competitions=['Premier League'])
        with self.assertRaises(ValueError):
            self.analyst.create_analysis_df(seasons=['2019-2019'], competitions=['Premier League'])
        with self.assertRaises(ValueError):
            self.analyst.create_analysis_df(seasons=['2017-2020'], competitions=['Premier League'])
        with self.assertRaises(ValueError):
            self.analyst.create_analysis_df(seasons=['2003-2004'], competitions=['Premier League'])
        with self.assertRaises(ValueError):
            self.analyst.create_analysis_df(seasons=['2998-2999'], competitions=['Premier League'])

    def test_calculate_strike_rates(self):
        data = {
            'probability': [0.0001, 0.024, 0.12, 0.31, 0.324],
            'outcome': [0, 0, 1, 0, 1]
        }
        df = pd.DataFrame(data)
        result = self.analyst.calculate_strikerates(df)
        expected = {
            '0.0-2.5': {'mean_prediction': 0.01205, 'strikerate': 0.0},
            '2.5-5.0': {'mean_prediction': None, 'strikerate': None},
            '5.0-7.5': {'mean_prediction': None, 'strikerate': None},
            '7.5-10.0': {'mean_prediction': None, 'strikerate': None},
            '10.0-12.5': {'mean_prediction': 0.12, 'strikerate': 1.0},
            '12.5-15.0': {'mean_prediction': None, 'strikerate': None},
            '15.0-17.5': {'mean_prediction': None, 'strikerate': None},
            '17.5-20.0': {'mean_prediction': None, 'strikerate': None},
            '20.0-22.5': {'mean_prediction': None, 'strikerate': None},
            '22.5-25.0': {'mean_prediction': None, 'strikerate': None},
            '25.0-27.5': {'mean_prediction': None, 'strikerate': None},
            '27.5-30.0': {'mean_prediction': None, 'strikerate': None},
            '30.0-32.5': {'mean_prediction': 0.317, 'strikerate': 0.5},
            '32.5-35.0': {'mean_prediction': None, 'strikerate': None},
            '35.0-37.5': {'mean_prediction': None, 'strikerate': None},
            '37.5-40.0': {'mean_prediction': None, 'strikerate': None},
            '40.0-42.5': {'mean_prediction': None, 'strikerate': None},
            '42.5-45.0': {'mean_prediction': None, 'strikerate': None},
            '45.0-47.5': {'mean_prediction': None, 'strikerate': None},
            '47.5-50.0': {'mean_prediction': None, 'strikerate': None},
            '50.0-52.5': {'mean_prediction': None, 'strikerate': None},
            '52.5-55.0': {'mean_prediction': None, 'strikerate': None},
            '55.0-57.5': {'mean_prediction': None, 'strikerate': None},
            '57.5-60.0': {'mean_prediction': None, 'strikerate': None},
            '60.0-62.5': {'mean_prediction': None, 'strikerate': None},
            '62.5-65.0': {'mean_prediction': None, 'strikerate': None},
            '65.0-67.5': {'mean_prediction': None, 'strikerate': None},
            '67.5-70.0': {'mean_prediction': None, 'strikerate': None},
            '70.0-72.5': {'mean_prediction': None, 'strikerate': None},
            '72.5-75.0': {'mean_prediction': None, 'strikerate': None},
            '75.0-77.5': {'mean_prediction': None, 'strikerate': None},
            '77.5-80.0': {'mean_prediction': None, 'strikerate': None},
            '80.0-82.5': {'mean_prediction': None, 'strikerate': None},
            '82.5-85.0': {'mean_prediction': None, 'strikerate': None},
            '85.0-87.5': {'mean_prediction': None, 'strikerate': None},
            '87.5-90.0': {'mean_prediction': None, 'strikerate': None},
            '90.0-92.5': {'mean_prediction': None, 'strikerate': None},
            '92.5-95.0': {'mean_prediction': None, 'strikerate': None},
            '95.0-97.5': {'mean_prediction': None, 'strikerate': None},
            '97.5-100.0': {'mean_prediction': None, 'strikerate': None},
        }
        self.assertEqual(result, expected)

    def test_mean_squared_error(self):
        data = {
            'probability': [0.0001, 0.024, 0.12, 0.31, 0.324],
            'outcome': [0, 0, 1, 0, 1]
        }
        df = pd.DataFrame(data)
        result = self.analyst.mean_squared_error(df)
        expected = 0.2656
        self.assertEqual(result, expected)

    def test_calculate_strikerates_defaults_to_self_df(self):
        data = {
            'probability': [0.0001, 0.024, 0.12, 0.31, 0.324],
            'outcome': [0, 0, 1, 0, 1]
        }
        df = pd.DataFrame(data)
        self.analyst.df = df
        try:
            self.analyst.calculate_strikerates()
        except Exception as e:
            self.fail(e)
        self.assertNotEqual(self.analyst.strikerates, None)

    def test_weighted_mean_squared_error_defaults_to_self_strikerates_and_df(self):
        data = {
            'probability': [0.0001, 0.024, 0.12, 0.31, 0.324],
            'outcome': [0, 0, 1, 0, 1]
        }
        df = pd.DataFrame(data)
        self.analyst.df = df
        self.analyst.calculate_strikerates()
        try:
            self.analyst.mean_squared_error()
        except Exception as e:
            self.fail(e)
        self.assertNotEqual(self.analyst.mean_squared_error, None)