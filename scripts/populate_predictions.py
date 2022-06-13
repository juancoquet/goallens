from data_sourcing.db_population.db_population import DBPopulator
from predictions.models import Prediction

from supported_comps import PREDICTION_COMPS


def run():

    populator = DBPopulator()

    seasons = ['2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022']
    competitions = list(PREDICTION_COMPS.keys())

    params = {
        'xGs_past_games': 10,
        'suppression_range': 0.75,
        'conversion_range': 1.25,
        'sup_con_past_games': 10,
        'h_a_weight': 0.5,
        'h_a_past_games': 10
    }

    populator.add_predictions_to_db(seasons, competitions, **params)