from data_sourcing.db_population.db_population import DBPopulator
from supported_comps import COMP_CODES


def run():
    populator = DBPopulator()

    seasons = ['2022-2023']
    competitions = list(COMP_CODES.keys())

    populator.add_teams_to_db(seasons, competitions)