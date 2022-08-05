from data_sourcing.db_population.db_population import DBPopulator
from predictions.models import Prediction
from data_sourcing.models import Fixture

from supported_comps import PREDICTION_COMPS


def run():

    populator = DBPopulator()

    # seasons = ['2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022']
    # competitions = list(PREDICTION_COMPS.keys())

    fixture = Fixture.objects.all().filter(season='2022-2023', competition='Premier League').order_by('date')[0]
    print(fixture)

    params = {
        'xGs_past_games': 10,
        'suppression_range': 0.75,
        'conversion_range': 1.25,
        'sup_con_past_games': 10,
        'h_a_weight': 0.5,
        'h_a_past_games': 10
    }

    # populator._add_prediction_to_db(fixture, **params)
    prediciton = Prediction.objects.all().filter(fixture=fixture)[0]
    print(prediciton)