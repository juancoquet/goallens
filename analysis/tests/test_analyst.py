import csv
from decimal import Decimal
from datetime import date, time
from django.test import TestCase # type: ignore

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
        outcomes = self.analyst.check_prediction_outcomes(prediction)
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
        
    def test_combine_predictions_and_outcomes(self):
        prediction = self.predictor.generate_prediction(self.fixture)
        pred_copy = prediction.copy()
        outcomes = self.analyst.check_prediction_outcomes(prediction)
        combined = self.analyst._combine_predictions_and_outcomes(pred_copy, outcomes)
        expected = {
            0.0567: 0, 0.2952: 0,
            0.1627: 0, 0.3602: 0,
            0.2335: 0, 0.2197: 1,
            0.2234: 1, 0.0893: 0,
            0.1603: 0, 0.0273: 0,
            0.092:  0, 0.0066: 0,
            0.044:  0, 0.0014: 0,
            0.018:  0, 0.0002: 0
        }
        self.assertEqual(combined, expected)