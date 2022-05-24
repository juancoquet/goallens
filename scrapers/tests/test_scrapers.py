# from unittest import TestCase
# from scrapers.teams_scraper import TeamScraper


# class TestTeamScraper(TestCase):

#     # go to pl page
#     # (get list of all teams' ids from pl table for a given season)
#     # go to each team's url
#     # get full team name
#     # add team name and id to db

#     # can 

#     def test_get_all_team_ids(self):
#         output = TeamScraper.get_all_team_ids('2019-2020', league='Premier League')
#         expected = [
#             '822bd0ba', 'b8fd03ef', '19538871', 'cff3d9bb', 'a2d435b3', # liv, mci, mutd, che, lei
#             '361ca564', '8cec06e1', '18bb7c10', '1df6b87e', '943e8050', # tot, wol, ars, shef, bur
#             '33c895d4', 'd3fd31cc', 'b2b47a98', '47c64c55', 'd07537b9', # sou, eve, newc, cry, bri
#             '7c21e445', '8602292d', '4ba7cbea', '2abfe087', '1c781004', # wham, av, bou, wat, nor
#         ]
#         self.assertEqual(len(output), 20)
#         self.assertEqual(output, expected)

#     def test_get_team_names(self):
#         output = TeamScraper.get_team_names(['822bd0ba', '19538871', 'd07537b9']) # liv, mutd, bri
#         expected = ['Liverpool', 'Manchester United', 'Brighton & Hove Albion']
#         self.assertEqual(len(output), 3)
#         self.assertEqual(output, expected)

#     def test_names_and_ids_added_to_db(self):
#         self.fail('write test and function')