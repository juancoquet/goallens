from datetime import date, time as dt_time
from unittest import TestCase, skip
from unittest.mock import patch, Mock

from data_sourcing.models import Team, Fixture
from data_sourcing.scrapers.teams.teams_scraper import TeamsScraper
from data_sourcing.scrapers.fixtures.fixtures_scraper import FixturesScraper
from .expected_test_results import (
    EXPECTED_FIXTURE_IDS, EXPECTED_FIXTURE_DATES, EXPECTED_FIXTURE_TIMES,
    EXPECTED_FIXTURE_TEAM_IDS, EXPECTED_FIXTURE_GOALS, EXPECTED_FIXTURE_XG,
    EXPECTED_NO_XG_DATA,
)
from supported_comps import COMP_CODES


class TestTeamIDScraper(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scraper = TeamsScraper()

    def test_get_team_ids(self):
        output = self.scraper.get_team_ids('2019-2020', competition='Premier League')
        expected = [
            '822bd0ba', 'b8fd03ef', '19538871', 'cff3d9bb', 'a2d435b3', # liv, mci, mutd, che, lei
            '361ca564', '8cec06e1', '18bb7c10', '1df6b87e', '943e8050', # tot, wol, ars, shef, bur
            '33c895d4', 'd3fd31cc', 'b2b47a98', '47c64c55', 'd07537b9', # sou, eve, newc, cry, bri
            '7c21e445', '8602292d', '4ba7cbea', '2abfe087', '1c781004', # wham, av, bou, wat, nor
        ]
        self.assertEqual(len(output), 20)
        self.assertEqual(output, expected)

    def test_unsupported_competition_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.get_team_ids('2019-2020', competition='fantasy league')

    def test_incorrect_season_format_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.get_team_ids('2019-20', competition='Premier League')

    def test_incorrect_season_range_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.get_team_ids('2010-2019', competition='Premier League')
        with self.assertRaises(ValueError):
            self.scraper.get_team_ids('2019-2010', competition='Premier League')
        with self.assertRaises(ValueError):
            self.scraper.get_team_ids('2019-2019', competition='Premier League')

    def test_incorrect_season_year_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.get_team_ids('2002-2003', competition='Premier League')
        with self.assertRaises(ValueError):
            self.scraper.get_team_ids('2998-2999', competition='Premier League')


class TestTeamShortNameScraper(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scraper = TeamsScraper()

    def test_get_team_short_names(self):
        output = self.scraper.get_team_short_names('2019-2020', competition='Premier League')
        expected = [
            'Liverpool', 'Manchester City', 'Manchester Utd', 'Chelsea', 'Leicester City',
            'Tottenham', 'Wolves', 'Arsenal', 'Sheffield Utd', 'Burnley',
            'Southampton', 'Everton', 'Newcastle Utd', 'Crystal Palace', 'Brighton',
            'West Ham', 'Aston Villa', 'Bournemouth', 'Watford', 'Norwich City'
        ]
        self.assertEqual(len(output), 20)
        self.assertEqual(output, expected)

    def test_unsupported_competition_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.get_team_short_names('2019-2020', competition='fantasy league')

    def test_incorrect_season_format_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.get_team_short_names('2019-20', competition='Premier League')

    def test_incorrect_season_range_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.get_team_short_names('2010-2019', competition='Premier League')
        with self.assertRaises(ValueError):
            self.scraper.get_team_short_names('2019-2010', competition='Premier League')
        with self.assertRaises(ValueError):
            self.scraper.get_team_short_names('2019-2019', competition='Premier League')

    def test_incorrect_season_year_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.get_team_short_names('2002-2003', competition='Premier League')
        with self.assertRaises(ValueError):
            self.scraper.get_team_short_names('2998-2999', competition='Premier League')



class TestTeamNameScraper(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scraper = TeamsScraper()

    def test_get_team_names(self):
        output = self.scraper.get_team_names(['822bd0ba', 'e2d8892c', 'd07537b9']) # liv, mutd, bri
        expected = {
            '822bd0ba': 'Liverpool',
            'e2d8892c': 'Paris Saint-Germain',
            'd07537b9': 'Brighton & Hove Albion'
        }
        self.assertEqual(len(output), 3)
        self.assertEqual(output, expected)

    def test_invalid_team_id_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.get_team_names(['invalid'])



class TestFixtureIDsScraper(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scraper = FixturesScraper()

    def test_get_fixture_ids(self):
        output = self.scraper.scrape_fixture_ids('2019-2020', competition='Premier League')
        expected = EXPECTED_FIXTURE_IDS
        self.assertEqual(len(output), 380)
        self.assertEqual(output.sort(), expected.sort())

    @patch('data_sourcing.scrapers.base_scraper.session.get')
    def test_get_future_fixture_ids(self, mock_get):
        with open('data_sourcing/tests/mock_response', 'r') as f:
            mock_get.return_value = Mock(text=f.read())
        output = self.scraper.scrape_fixture_ids('2022-2023', competition='Premier League')
        self.assertEqual(len(output), 380)
        self.assertEqual(output[0], '9-47c64c55-18bb7c10')
        self.assertEqual(output[15], '9-d07537b9-b2b47a98')
        self.assertEqual(output[-1], '9-cd051869-b8fd03ef')

    def test_unsupported_competition_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_ids('2019-2020', competition='fantasy league')

    def test_incorrect_season_format_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_ids('2019-20', competition='Premier League')

    def test_incorrect_season_range_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_ids('2010-2019', competition='Premier League')
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_ids('2019-2010', competition='Premier League')
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_ids('2019-2019', competition='Premier League')

    def test_incorrect_season_year_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_ids('2002-2003', competition='Premier League')
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_ids('2998-2999', competition='Premier League')


class TestFixtureDatesScraper(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.scraper = FixturesScraper()

    def test_get_fixture_dates(self):
        output = self.scraper.scrape_fixture_dates('2019-2020', competition='Premier League')
        expected = EXPECTED_FIXTURE_DATES
        self.assertEqual(len(output), 380)
        self.assertEqual(output, expected)

    def test_unsupported_competition_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_dates('2019-2020', competition='fantasy league')

    def test_incorrect_season_format_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_dates('2019-20', competition='Premier League')

    def test_incorrect_season_range_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_dates('2010-2019', competition='Premier League')
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_dates('2019-2010', competition='Premier League')
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_dates('2019-2019', competition='Premier League')

    def test_incorrect_season_year_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_dates('2002-2003', competition='Premier League')
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_dates('2998-2999', competition='Premier League')


class TestFixtureTimesScraper(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scraper = FixturesScraper()

    def test_get_fixture_times(self):
        output = self.scraper.scrape_fixture_times('2019-2020', competition='Premier League')
        expected = EXPECTED_FIXTURE_TIMES
        self.assertEqual(len(output), 380)
        self.assertEqual(output, expected)

    def test_unsupported_competition_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_times('2019-2020', competition='fantasy league')

    def test_incorrect_season_format_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_times('2019-20', competition='Premier League')

    def test_incorrect_season_range_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_times('2010-2019', competition='Premier League')
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_times('2019-2010', competition='Premier League')
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_times('2019-2019', competition='Premier League')

    def test_incorrect_season_year_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_times('2002-2003', competition='Premier League')
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_times('2998-2999', competition='Premier League')


class TestFixtureTeamIDsScraper(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scraper = FixturesScraper()

    def test_get_fixture_team_ids(self):
        output = self.scraper.scrape_fixture_team_ids('2019-2020', competition='Premier League')
        expected = EXPECTED_FIXTURE_TEAM_IDS
        self.assertEqual(len(output), 380)
        self.assertEqual(output, expected)

    def test_unsupported_competition_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_team_ids('2019-2020', competition='fantasy league')

    def test_incorrect_season_format_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_team_ids('2019-20', competition='Premier League')

    def test_incorrect_season_range_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_team_ids('2010-2019', competition='Premier League')
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_team_ids('2019-2010', competition='Premier League')
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_team_ids('2019-2019', competition='Premier League')

    def test_incorrect_season_year_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_team_ids('2002-2003', competition='Premier League')
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_team_ids('2998-2999', competition='Premier League')


class TestFixtureGoalsScraper(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scraper = FixturesScraper()

    def test_get_fixture_goals(self):
        output = self.scraper.scrape_fixture_goals('2019-2020', competition='Premier League')
        expected = EXPECTED_FIXTURE_GOALS
        self.assertEqual(len(output), 380)
        self.assertEqual(output, expected)

    @patch('data_sourcing.scrapers.base_scraper.session.get')
    def test_get_future_fixture_goals(self, mock_get):
        with open('data_sourcing/tests/mock_response', 'r') as f:
            mock_get.return_value = Mock(text=f.read())
        output = self.scraper.scrape_fixture_goals('2022-2023', competition='Premier League')
        self.assertEqual(len(output), 380)
        self.assertEqual(output[list(output.keys())[0]], {'home': None, 'away': None})
        self.assertEqual(output[list(output.keys())[-1]], {'home': None, 'away': None})

    def test_unsupported_competition_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_goals('2019-2020', competition='fantasy league')

    def test_incorrect_season_format_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_goals('2019-20', competition='Premier League')

    def test_incorrect_season_range_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_goals('2010-2019', competition='Premier League')
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_goals('2019-2010', competition='Premier League')
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_goals('2019-2019', competition='Premier League')

    def test_incorrect_season_year_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_goals('2002-2003', competition='Premier League')
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_goals('2998-2999', competition='Premier League')


class TestFixturexGsScraper(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scraper = FixturesScraper()

    def test_get_fixture_xGs(self):
        output = self.scraper.scrape_fixture_xGs('2019-2020', competition='Premier League')
        expected = EXPECTED_FIXTURE_XG
        self.assertEqual(len(output), 380)
        self.assertEqual(output, expected)

    @patch('data_sourcing.scrapers.base_scraper.session.get')
    def test_get_future_fixture_xGs(self, mock_get):
        with open('data_sourcing/tests/mock_response', 'r') as f:
            mock_get.return_value = Mock(text=f.read())
        output = self.scraper.scrape_fixture_xGs('2022-2023', competition='Premier League')
        self.assertEqual(len(output), 380)
        self.assertEqual(output[list(output.keys())[0]], {'home': None, 'away': None})
        self.assertEqual(output[list(output.keys())[-1]], {'home': None, 'away': None})

    def test_no_xG_data_returns_none_in_dict(self):
        output = self.scraper.scrape_fixture_xGs('2019-2020', competition='Ligue 2')
        expeced = EXPECTED_NO_XG_DATA
        self.assertEqual(len(output), 380)
        self.assertEqual(output, expeced)

    def test_unsupported_competition_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_xGs('2019-2020', competition='fantasy league')

    def test_incorrect_season_format_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_xGs('2019-20', competition='Premier League')

    def test_incorrect_season_range_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_xGs('2010-2019', competition='Premier League')
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_xGs('2019-2010', competition='Premier League')
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_xGs('2019-2019', competition='Premier League')

    def test_incorrect_season_year_fails(self):
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_xGs('2002-2003', competition='Premier League')
        with self.assertRaises(ValueError):
            self.scraper.scrape_fixture_xGs('2998-2999', competition='Premier League')


class TestUpcomingFixturesScraper(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scraper = FixturesScraper()

    def test_scrape_upcoming_fixtures(self):
        output = self.scraper.scrape_upcoming_fixtures(from_date=date(2022, 8, 4), lookahead=2, competition='Premier League')
        expected = [
            '9-47c64c55-18bb7c10',
            '9-fd962109-822bd0ba',
            '9-4ba7cbea-8602292d',
            '9-5bfb9659-8cec06e1',
            '9-b2b47a98-e4a775cb',
            '9-361ca564-33c895d4',
            '9-d3fd31cc-cff3d9bb'
        ]
        self.assertEqual(len(output), len(expected))
        self.assertEqual(output, expected)

    def test_scrape_upcoming_fixtures_datetimes(self):
        output = self.scraper.scrape_upcoming_fixtures_datetimes(from_date=date(2022, 8, 4), lookahead=2, competition='Premier League')
        expected = {
            '9-47c64c55-18bb7c10': {'date': date(2022, 8, 5), 'time': dt_time(20, 0)},
            '9-fd962109-822bd0ba': {'date': date(2022, 8, 6), 'time': dt_time(12, 30)},
            '9-4ba7cbea-8602292d': {'date': date(2022, 8, 6), 'time': dt_time(15, 0)},
            '9-5bfb9659-8cec06e1': {'date': date(2022, 8, 6), 'time': dt_time(15, 0)},
            '9-b2b47a98-e4a775cb': {'date': date(2022, 8, 6), 'time': dt_time(15, 0)},
            '9-361ca564-33c895d4': {'date': date(2022, 8, 6), 'time': dt_time(15, 0)},
            '9-d3fd31cc-cff3d9bb': {'date': date(2022, 8, 6), 'time': dt_time(17, 30)}
        }
        self.assertEqual(output, expected)


class TestUpdateSettledFixtures(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scraper = FixturesScraper()

    def test_scrape_settled_fixtures(self):
        output = self.scraper.scrape_settled_fixtures(date(2022, 4, 3))
        expected_a =  {
            'fixture_id': 'b22e54c4',
            'date': date(2022, 4, 3),
            'time': dt_time(14, 0),
            'home': '7c21e445',
            'away': 'd3fd31cc',
            'goals_home': 2,
            'goals_away': 1,
            'xG_home': 1.2,
            'xG_away': 0.8,
        }
        expected_b = {
            'fixture_id': '6f8a2207',
            'date': date(2022, 4, 3),
            'time': dt_time(16, 30),
            'home': '361ca564',
            'away': 'b2b47a98',
            'goals_home': 5,
            'goals_away': 1,
            'xG_home': 3.1,
            'xG_away': 0.6,
        }
        self.assertEqual(output['9-7c21e445-d3fd31cc'], expected_a)
        self.assertEqual(output['9-361ca564-b2b47a98'], expected_b)
        self.assertEqual(len(output), 34)

class TestUpdateSettledFixtures(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scraper = FixturesScraper()

    def test_scrape_settled_fixtures(self):
        output = self.scraper.scrape_settled_fixtures(date(2022, 4, 3))
        expected_a =  {
            'fixture_id': 'b22e54c4',
            'date': date(2022, 4, 3),
            'time': dt_time(14, 0),
            'home': '7c21e445',
            'away': 'd3fd31cc',
            'goals_home': 2,
            'goals_away': 1,
            'xG_home': 1.2,
            'xG_away': 0.8,
        }
        expected_b = {
            'fixture_id': '6f8a2207',
            'date': date(2022, 4, 3),
            'time': dt_time(16, 30),
            'home': '361ca564',
            'away': 'b2b47a98',
            'goals_home': 5,
            'goals_away': 1,
            'xG_home': 3.1,
            'xG_away': 0.6,
        }
        self.assertEqual(output['9-7c21e445-d3fd31cc'], expected_a)
        self.assertEqual(output['9-361ca564-b2b47a98'], expected_b)
        self.assertEqual(len(output), 34)

class TestUpdateSettledFixtures(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scraper = FixturesScraper()

    def test_scrape_settled_fixtures(self):
        output = self.scraper.scrape_settled_fixtures(date(2022, 4, 3))
        expected_a =  {
            'fixture_id': 'b22e54c4',
            'date': date(2022, 4, 3),
            'time': dt_time(14, 0),
            'home': '7c21e445',
            'away': 'd3fd31cc',
            'goals_home': 2,
            'goals_away': 1,
            'xG_home': 1.2,
            'xG_away': 0.8,
        }
        expected_b = {
            'fixture_id': '6f8a2207',
            'date': date(2022, 4, 3),
            'time': dt_time(16, 30),
            'home': '361ca564',
            'away': 'b2b47a98',
            'goals_home': 5,
            'goals_away': 1,
            'xG_home': 3.1,
            'xG_away': 0.6,
        }
        self.assertEqual(output['9-7c21e445-d3fd31cc'], expected_a)
        self.assertEqual(output['9-361ca564-b2b47a98'], expected_b)
        self.assertEqual(len(output), 34)

class TestUpdateSettledFixtures(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scraper = FixturesScraper()

    def test_scrape_settled_fixtures(self):
        output = self.scraper.scrape_settled_fixtures(date(2022, 4, 3))
        expected_a =  {
            'fixture_id': 'b22e54c4',
            'date': date(2022, 4, 3),
            'time': dt_time(14, 0),
            'home': '7c21e445',
            'away': 'd3fd31cc',
            'goals_home': 2,
            'goals_away': 1,
            'xG_home': 1.2,
            'xG_away': 0.8,
        }
        expected_b = {
            'fixture_id': '6f8a2207',
            'date': date(2022, 4, 3),
            'time': dt_time(16, 30),
            'home': '361ca564',
            'away': 'b2b47a98',
            'goals_home': 5,
            'goals_away': 1,
            'xG_home': 3.1,
            'xG_away': 0.6,
        }
        self.assertEqual(output['9-7c21e445-d3fd31cc'], expected_a)
        self.assertEqual(output['9-361ca564-b2b47a98'], expected_b)
        self.assertEqual(len(output), 34)

class TestUpdateSettledFixtures(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scraper = FixturesScraper()

    def test_scrape_settled_fixtures(self):
        output = self.scraper.scrape_settled_fixtures(date(2022, 4, 3))
        expected_a =  {
            'fixture_id': 'b22e54c4',
            'date': date(2022, 4, 3),
            'time': dt_time(14, 0),
            'home': '7c21e445',
            'away': 'd3fd31cc',
            'goals_home': 2,
            'goals_away': 1,
            'xG_home': 1.2,
            'xG_away': 0.8,
        }
        expected_b = {
            'fixture_id': '6f8a2207',
            'date': date(2022, 4, 3),
            'time': dt_time(16, 30),
            'home': '361ca564',
            'away': 'b2b47a98',
            'goals_home': 5,
            'goals_away': 1,
            'xG_home': 3.1,
            'xG_away': 0.6,
        }
        self.assertEqual(output['9-7c21e445-d3fd31cc'], expected_a)
        self.assertEqual(output['9-361ca564-b2b47a98'], expected_b)
        self.assertEqual(len(output), 34)

class TestUpdateSettledFixtures(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scraper = FixturesScraper()

    def test_scrape_settled_fixtures(self):
        output = self.scraper.scrape_settled_fixtures(date(2022, 4, 3))
        expected_a =  {
            'fixture_id': 'b22e54c4',
            'date': date(2022, 4, 3),
            'time': dt_time(14, 0),
            'home': '7c21e445',
            'away': 'd3fd31cc',
            'goals_home': 2,
            'goals_away': 1,
            'xG_home': 1.2,
            'xG_away': 0.8,
        }
        expected_b = {
            'fixture_id': '6f8a2207',
            'date': date(2022, 4, 3),
            'time': dt_time(16, 30),
            'home': '361ca564',
            'away': 'b2b47a98',
            'goals_home': 5,
            'goals_away': 1,
            'xG_home': 3.1,
            'xG_away': 0.6,
        }
        self.assertEqual(output['9-7c21e445-d3fd31cc'], expected_a)
        self.assertEqual(output['9-361ca564-b2b47a98'], expected_b)
        self.assertEqual(len(output), 34)

class TestUpdateSettledFixtures(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scraper = FixturesScraper()

    def test_scrape_settled_fixtures(self):
        output = self.scraper.scrape_settled_fixtures(date(2022, 4, 3))
        expected_a =  {
            'fixture_id': 'b22e54c4',
            'date': date(2022, 4, 3),
            'time': dt_time(14, 0),
            'home': '7c21e445',
            'away': 'd3fd31cc',
            'goals_home': 2,
            'goals_away': 1,
            'xG_home': 1.2,
            'xG_away': 0.8,
        }
        expected_b = {
            'fixture_id': '6f8a2207',
            'date': date(2022, 4, 3),
            'time': dt_time(16, 30),
            'home': '361ca564',
            'away': 'b2b47a98',
            'goals_home': 5,
            'goals_away': 1,
            'xG_home': 3.1,
            'xG_away': 0.6,
        }
        self.assertEqual(output['9-7c21e445-d3fd31cc'], expected_a)
        self.assertEqual(output['9-361ca564-b2b47a98'], expected_b)
        self.assertEqual(len(output), 34)

class TestUpdateSettledFixtures(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scraper = FixturesScraper()

    def test_scrape_settled_fixtures(self):
        output = self.scraper.scrape_settled_fixtures(date(2022, 4, 3))
        expected_a =  {
            'fixture_id': 'b22e54c4',
            'date': date(2022, 4, 3),
            'time': dt_time(14, 0),
            'home': '7c21e445',
            'away': 'd3fd31cc',
            'goals_home': 2,
            'goals_away': 1,
            'xG_home': 1.7,
            'xG_away': 0.8,
        }
        expected_b = {
            'fixture_id': '6f8a2207',
            'date': date(2022, 4, 3),
            'time': dt_time(16, 30),
            'home': '361ca564',
            'away': 'b2b47a98',
            'goals_home': 5,
            'goals_away': 1,
            'xG_home': 3.2,
            'xG_away': 0.6,
        }
        self.assertEqual(output['9-7c21e445-d3fd31cc'], expected_a)
        self.assertEqual(output['9-361ca564-b2b47a98'], expected_b)
        self.assertEqual(len(output), 34)