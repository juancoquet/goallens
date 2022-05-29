import datetime
from decimal import Decimal
from django.test import TestCase


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
        self.pediction = Prediction.objects.create(
            fixture=self.fixture,
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

    def test_create_new_model(self):
        self.assertEqual(Prediction.objects.count(), 1)

    # TODO: implement remaining tests
    def test_fk_fixture(self):
        self.assertEqual(self.pediction.fixture, self.fixture)

    def test_string_representation(self):
        expected = f'prediction 2-3 {self.fixture.id}: {self.fixture}'
        self.assertEqual(str(self.pediction), expected)