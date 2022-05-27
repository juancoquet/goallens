from unittest import TestCase, skip

from data_sourcing.scrapers.teams.teams_scraper import TeamsScraper
from data_sourcing.scrapers.fixtures.fixtures_scraper import FixturesScraper
from .expected_test_results import (
    EXPECTED_FIXTURE_IDS, EXPECTED_FIXTURE_DATES, EXPECTED_FIXTURE_TIMES,
    EXPECTED_FIXTURE_TEAM_IDS, EXPECTED_FIXTURE_GOALS, EXPECTED_FIXTURE_XG
)


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
        self.assertEqual(output, expected)

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

    def test_get_fixture_ids(self):
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

    def test_get_fixture_ids(self):
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

    def test_get_fixture_ids(self):
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

    def test_get_fixture_ids(self):
        output = self.scraper.scrape_fixture_goals('2019-2020', competition='Premier League')
        expected = EXPECTED_FIXTURE_GOALS
        self.assertEqual(len(output), 380)
        self.assertEqual(output, expected)

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


# TODO: scrape fixture home xG
# TODO: scrape fixture away xG
class TestFixturexGsScraper(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scraper = FixturesScraper()

    def test_get_fixture_ids(self):
        output = self.scraper.scrape_fixture_xGs('2019-2020', competition='Premier League')
        expected = EXPECTED_FIXTURE_XG
        self.assertEqual(len(output), 380)
        self.assertEqual(output, expected)

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




# TODO: scrape fixture competition
    # dont need to, competition baked into get_fixture_ids call
# TODO: scrape fixture season
    # dont need to, season baked into get_fixture_ids call