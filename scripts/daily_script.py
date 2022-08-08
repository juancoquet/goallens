import datetime as dt
from data_sourcing.db_population.db_population import DBPopulator
import os
from params import PARAMS
from supported_comps import PREDICTION_COMPS

def run():
    populator = DBPopulator()
    comps = list(PREDICTION_COMPS.keys())
    populator.add_upcoming_predictions_to_db(comps, **PARAMS, within_days=2)
    print('added predictions')
    today = dt.date.today()
    today = dt.date(2022, 8, 6)
    yesterday = today - dt.timedelta(days=1)
    populator.update_settled_fixtures(yesterday)
    populator.update_settled_fixtures(today)
    print('updated settled fixtures')