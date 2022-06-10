from data_sourcing.db_population.db_population import DBPopulator

from supported_comps import PREDICTION_COMPS


def run():
    populator = DBPopulator()

    seasons = ['2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022']
    competitions = list(PREDICTION_COMPS.keys())

    params = {
        'xGs_past_games': 10,
        'suppression_range': 0.5,
        'conversion_range': 1.0,
        'sup_con_past_games': 7,
        'h_a_weight': 0.5,
        'h_a_past_games': 10
    }

    populator.add_predictions_to_db(seasons, competitions, **params)