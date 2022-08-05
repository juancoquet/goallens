from data_sourcing.db_population.db_population import DBPopulator
from params import PARAMS
from supported_comps import PREDICTION_COMPS

def run():
    populator = DBPopulator()
    comps = list(PREDICTION_COMPS.keys())
    populator.add_upcoming_predictions_to_db(comps, **PARAMS, within_days=2)
    print('added predictions')
    populator.update_settled_fixtures()
    print('updated settled fixtures')