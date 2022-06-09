import datetime
from decimal import Decimal
from django.test import TestCase # type: ignore


from predictions.models import Prediction
from data_sourcing.db_population.db_population import DBPopulator


class TestPredictionModel(TestCase):

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

    def test_create_new_model(self):
        self.assertEqual(Prediction.objects.count(), 1)

    def test_fk_fixture(self):
        self.assertEqual(self.prediction.fixture, self.fixture)

    def test_string_representation(self):
        expected = f'prediction 0-2 {self.fixture.id}: {self.fixture}'
        self.assertEqual(str(self.prediction), expected)

    def test_home_win_prob(self):
        self.assertEqual(self.prediction.home_win_prob, Decimal('0.16744984'))

    def test_away_win_prob(self):
        self.assertEqual(self.prediction.away_win_prob, Decimal('0.62639951'))

    def test_draw_prob(self):
        self.assertEqual(self.prediction.draw_prob, Decimal('0.20495052'))

    def test_win_draw_probs_sum_to_1(self):
        home_win_prob = self.prediction.home_win_prob
        away_win_prob = self.prediction.away_win_prob
        draw_prob = self.prediction.draw_prob
        self.assertAlmostEqual(home_win_prob + away_win_prob + draw_prob, 1, places=2)