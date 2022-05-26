from unittest import TestCase, skip
from data_sourcing.scrapers.teams.teams_scraper import TeamsScraper


# need to get:
# - team id
# - team name
# - team short name

# keep scrapers separate from data handlers (modules/functions that send data to the database)

# for a given league on a given season:
# - scrape all team ids from league table
# - scrape all team short names from league table
# - scrape all team names from league table
    # - take list of team ids as argument
    # - go to each team's page
    # - scrape team name


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