import datetime
from decimal import Decimal
from unittest import TestCase
from urllib import response
from django.test import TestCase # type: ignore

from data_sourcing.db_population.db_population import DBPopulator
from data_sourcing.models import Fixture
from predictions.models import Prediction


class TestPredictionDetailView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.populator = DBPopulator()
        cls.home = cls.populator.add_team_to_db(
            team_id='8602292d',
            team_name='Aston Villa',
            team_short_name='Aston Villa',
        )
        cls.away = cls.populator.add_team_to_db(
            team_id='b8fd03ef',
            team_name='Manchester City',
            team_short_name='Mancheseter City',
        )
        cls.fixture = cls.populator.add_fixture_to_db(
            fixture_id='ffb4946c',
            competition='Premier League',
            season='2019-2020',
            date=datetime.date(2020, 1, 12),
            time=datetime.time(16, 30),
            home_team_id=cls.home.id,
            away_team_id=cls.away.id,
            goals_home=1,
            goals_away=6,
            xG_home=1.0,
            xG_away=2.5,
        )

    def setUp(self):
        self.prediction = Prediction.objects.create(
            fixture=self.fixture,
            forecast_hxG=Decimal('0.96'),
            forecast_axG=Decimal('2.06'),
            prob_hg_0=Decimal('0.3829'),
            prob_hg_1=Decimal('0.3676'),
            prob_hg_2=Decimal('0.1764'),
            prob_hg_3=Decimal('0.0565'),
            prob_hg_4=Decimal('0.0136'),
            prob_hg_5=Decimal('0.0026'),
            prob_hg_6=Decimal('0.0004'),
            prob_hg_7=Decimal('0.0001'),

            prob_ag_0=Decimal('0.1275'),
            prob_ag_1=Decimal('0.2626'),
            prob_ag_2=Decimal('0.2704'),
            prob_ag_3=Decimal('0.1857'),
            prob_ag_4=Decimal('0.0956'),
            prob_ag_5=Decimal('0.0394'),
            prob_ag_6=Decimal('0.0135'),
            prob_ag_7=Decimal('0.004'),
            likely_hg=0,
            likely_ag=2,
        )


    def test_uses_prediction_detail_template(self):
        response = self.client.get('/predictions/ffb4946c')
        self.assertTemplateUsed(response, 'prediction_detail.html')

    def test_correct_fixture_retrieved(self):
        response = self.client.get('/predictions/ffb4946c')
        self.assertEqual(response.context['fixture'], self.fixture)

    def test_correct_related_prediction_retrieved(self):
        response = self.client.get('/predictions/ffb4946c')
        self.assertEqual(response.context['prediction'], self.prediction)

    def test_team_logos_in_page(self):
        response = self.client.get('/predictions/ffb4946c')
        self.assertContains(response, '/static/images/team_logos/8602292d.png')
        self.assertContains(response, '/static/images/team_logos/b8fd03ef.png')

    def test_context_contains_home_win_probability(self):
        response = self.client.get('/predictions/ffb4946c')
        self.assertEqual(response.context['home_win_prob'], 17)

    def test_context_contains_away_win_probability(self):
        response = self.client.get('/predictions/ffb4946c')
        self.assertEqual(response.context['away_win_prob'], 63)

    def test_context_contains_draw_probability(self):
        response = self.client.get('/predictions/ffb4946c')
        self.assertEqual(response.context['draw_prob'], 20)