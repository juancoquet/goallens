from ast import Delete
import csv
import datetime as dt
from decimal import Decimal
from django.test import TestCase # type: ignore
from unittest import skip

from data_sourcing.db_population.db_population import DBPopulator
from data_sourcing.models import Team, Fixture
from .expected_test_results import EXPECTED_FIXTURES_DICT, EXPECTED_UPLOAD_DICT
from predictions.models import Prediction


class TestCreateSeasonsTeamDict(TestCase):

    def setUp(self):
        self.populator = DBPopulator()

    def test_valid_params_creates_dict(self):
        d = self.populator._create_seasons_teams_dict(
            seasons=['2018-2019', '2019-2020'],
            competitions=['Premier League', 'Championship'],
        )
        self.assertEqual(d, EXPECTED_UPLOAD_DICT)
        
    def test_unsupported_competition_fails(self):
        with self.assertRaises(ValueError):
            self.populator._create_seasons_teams_dict(
                seasons=['2018-2019', '2019-2020'],
                competitions=['Premier League', 'Championship', 'Invalid'],
            )
    
    def test_invalid_season_format_fails(self):
        with self.assertRaises(ValueError):
            self.populator._create_seasons_teams_dict(
                seasons=['2018-2019', '2019-20'],
                competitions=['Premier League', 'Championship'],
            )

    def test_invalid_season_range_fails(self):
        with self.assertRaises(ValueError):
            self.populator._create_seasons_teams_dict(
                seasons=['2010-2019', '2019-2010'],
                competitions=['Premier League', 'Championship'],
            )
        with self.assertRaises(ValueError):
            self.populator._create_seasons_teams_dict(
                seasons=['2019-2019', '2019-2019'],
                competitions=['Premier League', 'Championship'],
            )
    
    def test_invalid_season_year_fails(self):
        with self.assertRaises(ValueError):
            self.populator._create_seasons_teams_dict(
                seasons=['2002-2003',],
                competitions=['Premier League', 'Championship'],
            )
        with self.assertRaises(ValueError):
            self.populator._create_seasons_teams_dict(
                seasons=['2998-2999',],
                competitions=['Premier League', 'Championship'],
            )


class TestAddTeamsToDB(TestCase):

    def setUp(self):
        self.populator = DBPopulator()

    def test_add_valid_team_to_db(self):
        self.assertEqual(Team.objects.count(), 0)
        
        self.populator.add_team_to_db(
            team_id='361ca564',
            team_name='Tottenham Hotspur',
            team_short_name='Tottenham',
        )
        self.assertEqual(Team.objects.count(), 1)
        self.assertEqual(Team.objects.get(id='361ca564').name, 'Tottenham Hotspur')

    def test_add_duplicate_team_to_db_does_not_raise_error(self):
        self.assertEqual(Team.objects.count(), 0)
        
        self.populator.add_team_to_db(
            team_id='361ca564',
            team_name='Tottenham Hotspur',
            team_short_name='Tottenham',
        )
        self.assertEqual(Team.objects.count(), 1)
        self.populator.add_team_to_db(
            team_id='361ca564',
            team_name='Tottenham Hotspur',
            team_short_name='Tottenham',
        )
        self.assertEqual(Team.objects.count(), 1)
        self.assertEqual(Team.objects.get(id='361ca564').name, 'Tottenham Hotspur')

    def test_add_teams_from_season_to_db(self):
        self.assertEqual(Team.objects.count(), 0)
        
        self.populator.add_teams_to_db(
            season=['2018-2019'],
            competition=['Premier League'],
        )
        self.assertEqual(Team.objects.count(), 20)

    def test_add_teams_from_season_to_db_args_must_be_lists(self):
        with self.assertRaises(TypeError):
            self.populator.add_teams_to_db(
                season='2018-2019',
                competition=['Premier League'],
            )
        with self.assertRaises(TypeError):
            self.populator.add_teams_to_db(
                season=['2018-2019'],
                competition='Premier League',
            )


class TestCreateSeasonsFixturesDict(TestCase):

    def setUp(self):
        self.populator = DBPopulator()

    def test_valid_params_creates_dict(self):
        d = self.populator._create_season_fixtures_dict(
            seasons=['2019-2020'], competitions=['Premier League']
        )
        self.assertEqual(d, EXPECTED_FIXTURES_DICT)

    def test_unsupported_competition_fails(self):
        with self.assertRaises(ValueError):
            self.populator._create_season_fixtures_dict(
                seasons=['2018-2019', '2019-2020'],
                competitions=['Premier League', 'Championship', 'Invalid'],
            )
    
    def test_invalid_season_format_fails(self):
        with self.assertRaises(ValueError):
            self.populator._create_season_fixtures_dict(
                seasons=['2018-2019', '2019-20'],
                competitions=['Premier League', 'Championship'],
            )

    def test_invalid_season_range_fails(self):
        with self.assertRaises(ValueError):
            self.populator._create_season_fixtures_dict(
                seasons=['2010-2019', '2019-2010'],
                competitions=['Premier League', 'Championship'],
            )
        with self.assertRaises(ValueError):
            self.populator._create_season_fixtures_dict(
                seasons=['2019-2019', '2019-2019'],
                competitions=['Premier League', 'Championship'],
            )
    
    def test_invalid_season_year_fails(self):
        with self.assertRaises(ValueError):
            self.populator._create_season_fixtures_dict(
                seasons=['2002-2003',],
                competitions=['Premier League', 'Championship'],
            )
        with self.assertRaises(ValueError):
            self.populator._create_season_fixtures_dict(
                seasons=['2998-2999',],
                competitions=['Premier League', 'Championship'],
            )


class TestAddFixturesToDB(TestCase):

    def setUp(self):
        self.populator = DBPopulator()
        self.home = Team.objects.create(
            id='822bd0ba', name='Liverpool', short_name='Liverpool'
        )
        self.away = Team.objects.create(
            id='1c781004', name='Norwich City', short_name='Norwich City'
        )

    def test_add_valid_fixture_to_db(self):
        self.assertEqual(Fixture.objects.count(), 0)
        
        self.populator.add_fixture_to_db(
            fixture_id='928467bd',
            competition='Premier League',
            season='2019-2020',
            date=dt.date(2019, 8, 9),
            time=dt.time(20, 0),
            home_team_id='822bd0ba',
            away_team_id='1c781004',
            goals_home=4,
            goals_away=1,
            xG_home=1.7,
            xG_away=1.0,
        )
        self.assertEqual(Fixture.objects.count(), 1)
        self.assertEqual(Fixture.objects.get(id='928467bd').date, dt.date(2019, 8, 9))
        self.assertEqual(Fixture.objects.get(id='928467bd').home, self.home)

    def test_add_duplicate_fixture_to_db_updates_record(self):
        self.assertEqual(Fixture.objects.count(), 0)
        
        self.populator.add_fixture_to_db(
            fixture_id='928467bd',
            competition='Premier League',
            season='2019-2020',
            date=dt.date(2019, 8, 9),
            time=dt.time(20, 0),
            home_team_id='822bd0ba',
            away_team_id='1c781004',
            goals_home=None,
            goals_away=None,
            xG_home=None,
            xG_away=None,
        )
        self.assertEqual(Fixture.objects.count(), 1)
        self.populator.add_fixture_to_db(
            fixture_id='928467bd',
            competition='Premier League',
            season='2019-2020',
            date=dt.date(2019, 8, 9),
            time=dt.time(20, 0),
            home_team_id='822bd0ba',
            away_team_id='1c781004',
            goals_home=5,
            goals_away=2,
            xG_home=1.7,
            xG_away=1.0,
        )
        self.assertEqual(Fixture.objects.count(), 1)
        self.assertEqual(Fixture.objects.get(id='928467bd').goals_home, 5)
        self.assertEqual(Fixture.objects.get(id='928467bd').goals_away, 2)
        self.assertEqual(Fixture.objects.get(id='928467bd').xG_home, Decimal('1.70'))
        self.assertEqual(Fixture.objects.get(id='928467bd').xG_away, Decimal('1.00'))

    def test_add_fixtures_from_season_to_db(self):
        with open('data_sourcing/tests/teams.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.populator.add_team_to_db(
                    team_id=row['id'],
                    team_name=row['team_name'],
                    team_short_name=row['team_short_name'],
                )
        
        self.assertEqual(Fixture.objects.count(), 0)
        self.populator.add_fixtures_to_db(
            seasons=['2019-2020', '2020-2021'],
            competitions=['Premier League', 'Championship']
        )
        self.assertEqual(Fixture.objects.count(), 380+380+552+552) # 380x2 pl fixtures, 552x2 championship fixtures

    def test_add_fixtures_from_season_to_db_args_must_be_lists(self):
        with self.assertRaises(TypeError):
            self.populator.add_fixtures_to_db(
                seasons='2018-2019',
                competitions=['Premier League'],
            )
        with self.assertRaises(TypeError):
            self.populator.add_fixtures_to_db(
                seasons=['2018-2019'],
                competitions='Premier League',
            )

    # TODO: test input data validation:
        # - invalid competition
        # - invalid season
        # - do for teams population too


class TestPredictionPopulation(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with open('data_sourcing/tests/teams.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Team.objects.create(
                    id=row['id'],
                    name=row['team_name'],
                    short_name=row['team_short_name'],
                )
        with open('data_sourcing/tests/fixtures.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Fixture.objects.create(
                    id=row['id'],
                    competition=row['competition'],
                    season=row['season'],
                    date=dt.date.fromisoformat(row['date']),
                    time=dt.time(int(row['time'].split(':')[0]), int(row['time'].split(':')[1])),
                    home=Team.objects.get(id=row['home']),
                    away=Team.objects.get(id=row['away']),
                    goals_home=row['goals_home'],
                    goals_away=row['goals_away'],
                    xG_home=Decimal(row['xG_home']) if row['xG_home'] else None,
                    xG_away=Decimal(row['xG_away']) if row['xG_away'] else None,
                )
        cls.populator = DBPopulator()
        cls.fixture = Fixture.objects.get(id='928467bd')
        cls.params = {
            'xGs_past_games': 5,
            'suppression_range': 1.0,
            'conversion_range': 1.0,
            'sup_con_past_games': 5,
            'h_a_weight': 1.0,
            'h_a_past_games': 5,
        }

    def test_populate_prediction(self):
        self.assertEqual(Prediction.objects.count(), 0)
        self.populator._add_prediction_to_db(self.fixture, **self.params)
        self.assertEqual(Prediction.objects.count(), 1)

    def test_populate_prediction_overwrites_existing_record(self):
        self.assertEqual(Prediction.objects.count(), 0)
        self.populator._add_prediction_to_db(self.fixture, **self.params)
        self.assertEqual(Prediction.objects.count(), 1)
        self.params['h_a_weight'] = 1.5
        self.populator._add_prediction_to_db(self.fixture, **self.params)
        self.assertEqual(Prediction.objects.count(), 1)

    def test_add_predictions_to_db(self):
        self.assertEqual(Prediction.objects.count(), 0)
        self.populator.add_predictions_to_db(
            seasons=['2020-2021', '2021-2022'],
            competitions=['Premier League'],
            **self.params
        )
        self.assertEqual(Prediction.objects.count(), 380*2) # 380 games per season, 2 competitions

    def test_add_predictions_with_not_enough_data_does_not_raise(self):
        self.populator.add_predictions_to_db(
            seasons=['2017-2018'],
            competitions=['Premier League'],
            **self.params
        )

    def test_add_predictions_to_db_args_must_be_lists(self):
        with self.assertRaises(TypeError):
            self.populator.add_predictions_to_db(
                seasons='2018-2019',
                competitions=['Premier League'],
                **self.params
            )
        with self.assertRaises(TypeError):
            self.populator.add_predictions_to_db(
                seasons=['2018-2019'],
                competitions='Premier League',
                **self.params
            )

    def test_add_upcoming_predictions_to_db(self):
        Fixture.objects.create(
            id='9-b2b47a98-18bb7c10',
            competition='Premier League',
            season='2021-2022',
            date=dt.date(2022, 5, 16),
            home=Team.objects.get(id='b2b47a98'),
            away=Team.objects.get(id='18bb7c10'),
        )
        Fixture.objects.create(
            id='9-33c895d4-822bd0ba',
            competition='Premier League',
            season='2021-2022',
            date=dt.date(2022, 5, 17),
            home=Team.objects.get(id='33c895d4'),
            away=Team.objects.get(id='822bd0ba'),
        )
        self.populator.add_upcoming_predictions_to_db(
            competitions=['Premier League'],
            date=dt.date(2022, 5, 16),
            **self.params
        )
        self.assertEqual(Prediction.objects.count(), 2)
        self.assertEqual(Prediction.objects.all()[0].fixture.id, '9-b2b47a98-18bb7c10')
        self.assertEqual(Prediction.objects.all()[1].fixture.id, '9-33c895d4-822bd0ba')

    def test_update_settled_fixtures(self):
        # delete existing fixtures on the same day as the one we're testing
        # (previously added as part of the test setup)
        Fixture.objects.filter(id='a3b3a0d5').delete()
        Fixture.objects.filter(id='4216543d').delete()

        # create fixtures with temp ids and missing data (as if the games have not yet been played)
        Fixture.objects.create(
            id='9-b2b47a98-18bb7c10',
            competition='Premier League',
            season='2021-2022',
            date=dt.date(2022, 5, 16),
            home=Team.objects.get(id='b2b47a98'),
            away=Team.objects.get(id='18bb7c10'),
        )
        Fixture.objects.create(
            id='10-f5922ca5-e297cd13',
            competition='Championship',
            season='2021-2022',
            date=dt.date(2022, 5, 16),
            home=Team.objects.get(id='f5922ca5'),
            away=Team.objects.get(id='e297cd13'),
        )
        Fixture.objects.create(
            id='17-ab358912-800303a0',
            competition='Segunda Division',
            season='2021-2022',
            date=dt.date(2022, 5, 16),
            home=Team.objects.get(id='ab358912'),
            away=Team.objects.get(id='800303a0'),
        )
        Fixture.objects.create(
            id='11-8ff9e3b3-421387cf',
            competition='Serie A',
            season='2021-2022',
            date=dt.date(2022, 5, 16),
            home=Team.objects.get(id='8ff9e3b3'),
            away=Team.objects.get(id='421387cf'),
        )
        Fixture.objects.create(
            id='11-e0652b02-7213da33',
            competition='Serie A',
            season='2021-2022',
            date=dt.date(2022, 5, 16),
            home=Team.objects.get(id='e0652b02'),
            away=Team.objects.get(id='7213da33'),
        )

        # add predictions for fixtures
        f_ids= [
            '9-b2b47a98-18bb7c10', '10-f5922ca5-e297cd13', '17-ab358912-800303a0',
            '11-8ff9e3b3-421387cf', '11-e0652b02-7213da33'
        ]
        for f_id in f_ids:
            Prediction.objects.create(
                fixture=Fixture.objects.get(id=f_id),
                forecast_hxG=Decimal('1.5'),
                forecast_axG=Decimal('1.5'),
                prob_hg_0=Decimal('0.5'),
                prob_hg_1=Decimal('0.5'),
                prob_hg_2=Decimal('0.5'),
                prob_hg_3=Decimal('0.5'),
                prob_hg_4=Decimal('0.5'),
                prob_hg_5=Decimal('0.5'),
                prob_hg_6=Decimal('0.5'),
                prob_hg_7=Decimal('0.5'),
                prob_ag_0=Decimal('0.5'),
                prob_ag_1=Decimal('0.5'),
                prob_ag_2=Decimal('0.5'),
                prob_ag_3=Decimal('0.5'),
                prob_ag_4=Decimal('0.5'),
                prob_ag_5=Decimal('0.5'),
                prob_ag_6=Decimal('0.5'),
                prob_ag_7=Decimal('0.5'),
                likely_hg=1,
                likely_ag=1,
            )

        # check that fixtures were added correctly
        fixture = Fixture.objects.get(id='9-b2b47a98-18bb7c10')
        self.assertEqual(fixture.id, '9-b2b47a98-18bb7c10')
        self.assertEqual(fixture.goals_home, None)
        self.assertEqual(fixture.goals_away, None)
        self.assertEqual(fixture.xG_home, None)
        self.assertEqual(fixture.xG_away, None)

        # check that predictions were added correctly
        prediction = Prediction.objects.get(fixture=fixture)
        self.assertEqual(prediction.fixture.id, '9-b2b47a98-18bb7c10')
        
        # update fixtures with real data from fbref
        self.populator.update_settled_fixtures(on_date=dt.date(2022, 5, 16))
        
        # test that fixture ids were updated correctly
        self.assertEqual(Fixture.objects.filter(id='a3b3a0d5').count(), 1)
        self.assertEqual(Fixture.objects.filter(id='9-b2b47a98-18bb7c10').count(), 0)

        # test that fixture data was updated correctly
        fixture = Fixture.objects.get(id='a3b3a0d5')
        self.assertEqual(fixture.goals_home, 2)
        self.assertEqual(fixture.goals_away, 0)
        self.assertEqual(fixture.xG_home, Decimal('1.6'))
        self.assertEqual(fixture.xG_away, Decimal('0.6'))

        # test that related predictions were updated correctly
        pred = Prediction.objects.filter(fixture__id='9-b2b47a98-18bb7c10')
        self.assertEqual(pred.count(), 0)
        pred = Prediction.objects.filter(fixture__id='a3b3a0d5')
        self.assertEqual(pred.count(), 1)

    def test_update_upcoming_fixtures_datetimes(self):
        Fixture.objects.create(
            id='9-b2b47a98-18bb7c10',
            competition='Premier League',
            season='2021-2022',
            date=dt.date(2022, 5, 17), # wrong date to simulate date change
            home=Team.objects.get(id='b2b47a98'),
            away=Team.objects.get(id='18bb7c10'),
        )
        Fixture.objects.create(
            id='9-33c895d4-822bd0ba',
            competition='Premier League',
            season='2021-2022',
            date=dt.date(2022, 5, 17),
            home=Team.objects.get(id='33c895d4'),
            away=Team.objects.get(id='822bd0ba'),
        )
        self.populator.update_upcoming_fixtures_datetimes(['Premier League'], from_date=dt.date(2022, 5, 15))
        fixture = Fixture.objects.get(id='9-b2b47a98-18bb7c10')
        self.assertEqual(fixture.date, dt.date(2022, 5, 16))
