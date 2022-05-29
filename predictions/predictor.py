import datetime as dt

from data_sourcing.models import Fixture
from supported_comps import COMP_CODES


class Predictor:

    def __init__(self):
        self.upcoming_fixtures = []

    def _get_upcoming_fixtures(self, date: dt.date, competition, within_days=2):
        if competition not in COMP_CODES:
            valid_comps = [k for k in COMP_CODES]
            raise ValueError(f'competion must be one of {valid_comps} – {competition} is invalid')
        if date > dt.date.today():
            raise ValueError(f'date must be in the past – {date} is invalid')
        end_date = date + dt.timedelta(days=within_days)
        fixtures = Fixture.objects.filter(
            competition=competition,
            date__gte=date,
            date__lte=end_date
        ).order_by('date')
        return fixtures