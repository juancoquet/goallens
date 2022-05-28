from django.test import TestCase # type: ignore
from unittest import skip

from data_sourcing.db_population.db_population import DBPopulator
from data_sourcing.models import Team
from .expected_test_results import EXPECTED_FIXTURES_DICT, EXPECTED_UPLOAD_DICT


class TestCreateSeasonsTeamDict(TestCase):

    maxDiff = None

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
        self.assertAlmostEquals(Team.objects.count(), 0)
        
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

    maxDiff = None

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