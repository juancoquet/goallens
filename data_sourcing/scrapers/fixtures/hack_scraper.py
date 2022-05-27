from bs4 import BeautifulSoup # type: ignore
from datetime import date
import requests # type: ignore


# url = 'https://fbref.com/en/comps/9/schedule/'
url = 'https://fbref.com/en/comps/9/3232/schedule/'
table_id = 'sched_3232_1'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table', id=table_id)
date_cells = table.select('td.left[data-stat="date"]:not(.iz)')
dates = [cell.get('csk') for cell in date_cells]
dates = [date(int(d[:4]), int(d[4:6]), int(d[6:])) for d in dates]
match_report_cells = table.select('td.left[data-stat="match_report"]:not(.iz)')
fixture_ids = [cell.find('a').get('href').split('/')[3] for cell in match_report_cells]
ids_dates = dict(zip(fixture_ids, dates))
assert len(ids_dates) == 380
