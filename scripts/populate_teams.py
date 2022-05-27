from data_sourcing.db_population.db_population import DBPopulator


def run():
    populator = DBPopulator()

    seasons = ['2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022']
    competitions = ['Premier League', 'Championship']

    populator.add_teams_to_db(seasons, competitions)