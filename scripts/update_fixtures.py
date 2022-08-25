import datetime as dt
import django # type: ignore
from django.core.mail import send_mail # type: ignore
from django.conf import settings # type: ignore
from django.test.utils import get_runner # type: ignore
import sys

from data_sourcing.db_population.db_population import DBPopulator
from my_secrets import EMAIL_ADDRESS # type: ignore
from params import PARAMS
from supported_comps import PREDICTION_COMPS


def run(on_date:str=None):
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    num_failures = test_runner.run_tests([])
    if num_failures > 0:
        now = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        subject = f'FAILED TESTS | {now}'
        msg = f'{num_failures} tests failed.\ntime: {now}'
        send_mail(subject, msg, '', [EMAIL_ADDRESS])
        sys.exit(bool(num_failures))
    
    print('\n-----------------------------------' * 3)
    print('all tests passed, updating fixtures')
    
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
    three_before = on_date - dt.timedelta(days=3)

    print(f'updating fixtures for {three_before}')
    populator.update_settled_fixtures(three_before)
    print(f'updating fixtures for {two_before}')
    populator.update_settled_fixtures(two_before)
    print(f'updating fixtures for {day_before}')
    populator.update_settled_fixtures(day_before)
    print(f'updated fixtures for {on_date}')
    populator.update_settled_fixtures(on_date)
    print('updated settled fixtures')