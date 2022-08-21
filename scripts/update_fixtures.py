import datetime as dt
from data_sourcing.db_population.db_population import DBPopulator
import os
from params import PARAMS
from supported_comps import PREDICTION_COMPS

def run(on_date:str=None):
    populator = DBPopulator()
    comps = list(PREDICTION_COMPS.keys())
    populator.add_upcoming_predictions_to_db(comps, **PARAMS, within_days=2)
    print('added predictions')
    if on_date is not None:
        on_date = dt.datetime.strptime(on_date, '%Y-%m-%d').date()
    else:
        on_date = dt.date.today()
    day_before = on_date - dt.timedelta(days=1)
    two_before = on_date - dt.timedelta(days=2)
    print(f'updating fixtures for {two_before}')
    populator.update_fixtures_for_date(two_before)
    print(f'updating fixtures for {day_before}')
    populator.update_settled_fixtures(day_before)
    print(f'updated fixtures for {on_date}')
    populator.update_settled_fixtures(on_date)
    print('updated settled fixtures')