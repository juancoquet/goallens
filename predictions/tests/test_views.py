import csv
import datetime
from decimal import Decimal
from unittest import TestCase
from urllib import response
from django.core.paginator import Paginator # type: ignore
from django.test import TestCase # type: ignore

from data_sourcing.db_population.db_population import DBPopulator
from data_sourcing.models import Fixture, Team
from predictions.models import Prediction


class TestPredictionDetailView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.populator = DBPopulator()

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
                    date=datetime.date.fromisoformat(row['date']),
                    time=datetime.time(int(row['time'].split(':')[0]), int(row['time'].split(':')[1])),
                    home=Team.objects.get(id=row['home']),
                    away=Team.objects.get(id=row['away']),
                    goals_home=int(row['goals_home']),
                    goals_away=int(row['goals_away']),
                    xG_home=Decimal(row['xG_home']) if row['xG_home'] else None,
                    xG_away=Decimal(row['xG_away']) if row['xG_away'] else None,
                )

        cls.fixture = Fixture.objects.get(id='ffb4946c')
        cls.home = Team.objects.get(id='8602292d')
        cls.away = Team.objects.get(id='b8fd03ef')

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

        self.prev_pred_home = self.populator._add_prediction_to_db(
            fixture=Fixture.objects.get(id='ac409026'),
            xGs_past_games=5,
            suppression_range=1.0,
            conversion_range=1.0,
            sup_con_past_games=5,
            h_a_weight=1.0,
            h_a_past_games=5,
        )
        self.next_pred_home = self.populator._add_prediction_to_db(
            fixture=Fixture.objects.get(id='bd044bad'),
            xGs_past_games=5,
            suppression_range=1.0,
            conversion_range=1.0,
            sup_con_past_games=5,
            h_a_weight=1.0,
            h_a_past_games=5,
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

    def test_context_contains_prev_prediction_for_team(self):
        response = self.client.get('/predictions/ffb4946c')
        self.assertEqual(response.context['prev_prediction_home'], self.prev_pred_home)

    def test_context_contains_next_prediction_for_team(self):
        response = self.client.get('/predictions/ffb4946c')
        self.assertEqual(response.context['next_prediction_home'], self.next_pred_home)


class TestPredictionListView(TestCase):

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
        response = self.client.get('/predictions/')
        self.assertTemplateUsed(response, 'prediction_list.html')

    def test_context_contains_predictions(self):
        response = self.client.get('/predictions/')
        self.assertEqual(len(response.context['predictions']), 1)

    def test_response_contains_table(self):
        response = self.client.get('/predictions/')
        self.assertContains(response, 'id="prediction-table"')

    def test_table_has_9_columns(self):
        response = self.client.get('/predictions/')
        self.assertContains(response, '<th>Open</th>')
        self.assertContains(response, '<th>Date</th>')
        self.assertContains(response, '<th>Comp</th>')
        self.assertContains(response, '<th>Home</th>')
        self.assertContains(response, '<th>FxG-H</th>')
        self.assertContains(response, '<th>Away</th>')
        self.assertContains(response, '<th>FxG-A</th>')
        self.assertContains(response, '<th>Result</th>')

    def test_response_contains_table_rows(self):
        response = self.client.get('/predictions/')
        html = response.content.decode('utf-8')
        num_preds = len(response.context['predictions'])
        self.assertEqual(html.count('<tr'), num_preds + 1) # +1 for header row

    def test_context_contains_queries(self):
        url = '/predictions/?'
        season = '2019-2020'
        competition = 'Premier League'
        team = 'Aston Villa'
        url += 'season=' + season + '&'
        url += 'competition=' + competition + '&'
        url += 'team=' + team
        response = self.client.get(url)
        self.assertEqual(response.context['season_q'], season)
        self.assertEqual(response.context['competition_q'], competition)
        self.assertEqual(response.context['team_q'], team)


class UpcomingPredictionsViewTest(TestCase):

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
        this_yr = datetime.date.today().year
        next_yr = this_yr + 1
        next_week = datetime.date.today() + datetime.timedelta(days=7)
        cls.fixture = cls.populator.add_fixture_to_db(
            fixture_id='ffb4946c',
            competition='Premier League',
            season=f'{this_yr}-{next_yr}',
            date=next_week,
            time=datetime.time(16, 30),
            home_team_id=cls.home.id,
            away_team_id=cls.away.id,
            goals_home=1,
            goals_away=6,
            xG_home=1.0,
            xG_away=2.5,
        )
        cls.prediction = Prediction.objects.create(
            fixture=cls.fixture,
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

    def test_uses_upcoming_predictions_template(self):
        response = self.client.get('/predictions/upcoming/')
        self.assertTemplateUsed(response, 'prediction_upcoming.html')
    
    def test_fixture_in_context(self):
        response = self.client.get('/predictions/upcoming/')
        self.assertEqual(response.context['predictions']['Premier League'][0], self.prediction)

    def test_response_contains_tables(self):
        response = self.client.get('/predictions/upcoming/')
        self.assertContains(response, 'id="premier-league-table"')
        self.assertContains(response, 'id="la-liga-table"')
        self.assertContains(response, 'id="ligue-1-table"')
        self.assertContains(response, 'id="bundesliga-table"')
        self.assertContains(response, 'id="serie-a-table"')
