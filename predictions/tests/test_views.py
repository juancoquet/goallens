import datetime
from decimal import Decimal
from unittest import TestCase
from django.test import TestCase # type: ignore

from data_sourcing.db_population.db_population import DBPopulator
from data_sourcing.models import Fixture
from predictions.models import Prediction


class TestPredictionDetailView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.populator = DBPopulator()
        cls.home = cls.populator.add_team_to_db(
            team_id='b8fd03ef',
            team_name='Manchester City',
            team_short_name='Mancheseter City',
        )
        cls.away = cls.populator.add_team_to_db(
            team_id='822bd0ba',
            team_name='Liverpool',
            team_short_name='Liverpool',
        )
        cls.fixture = cls.populator.add_fixture_to_db(
            fixture_id='37e2fe92',
            competition='Premier League',
            season='2021-2022',
            date=datetime.date(2022, 4, 10),
            time=datetime.time(16, 30),
            home_team_id=cls.home.id,
            away_team_id=cls.away.id,
            goals_home=2,
            goals_away=2,
            xG_home=2.0,
            xG_away=1.0
        )
        cls.prediction = Prediction.objects.create(
            fixture=cls.fixture,
            forecast_hxG=Decimal('1.5'),
            forecast_axG=Decimal('2.3'),
            prob_hg_0=Decimal('0.1'),
            prob_hg_1=Decimal('0.15'),
            prob_hg_2=Decimal('0.25'),
            prob_hg_3=Decimal('0.15'),
            prob_hg_4=Decimal('0.1'),
            prob_hg_5=Decimal('0.05'),
            prob_hg_6=Decimal('0.03'),
            prob_ag_0=Decimal('0.1'),
            prob_ag_1=Decimal('0.15'),
            prob_ag_2=Decimal('0.2'),
            prob_ag_3=Decimal('0.25'),
            prob_ag_4=Decimal('0.1'),
            prob_ag_5=Decimal('0.05'),
            prob_ag_6=Decimal('0.03'),
            likely_hg=2,
            likely_ag=3,
        )


    def test_uses_prediction_detail_template(self):
        response = self.client.get('/predictions/37e2fe92')
        self.assertTemplateUsed(response, 'prediction_detail.html')

    def test_correct_fixture_retrieved(self):
        response = self.client.get('/predictions/37e2fe92')
        self.assertEqual(response.context['fixture'], self.fixture)

    def test_correct_related_prediction_retrieved(self):
        response = self.client.get('/predictions/37e2fe92')
        self.assertEqual(response.context['prediction'], self.prediction)
