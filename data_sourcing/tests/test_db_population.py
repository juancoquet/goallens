from django.test import TestCase # type: ignore
from unittest import skip

from data_sourcing.db_population import DBPopulator
from .expected_test_results import EXPECTED_UPLOAD_DICT


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