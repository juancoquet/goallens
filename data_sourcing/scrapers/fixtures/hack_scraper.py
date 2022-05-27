from bs4 import BeautifulSoup # type: ignore
from datetime import date, time
import requests # type: ignore


# url = 'https://fbref.com/en/comps/9/schedule/'
url = 'https://fbref.com/en/comps/9/3232/schedule/'
table_id = 'sched_3232_1'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table', id=table_id)
home_cells = table.select('td.right[data-stat="squad_a"]:not(.iz)')
home_ids = [cell.find('a').get('href').split('/')[3] for cell in home_cells]
away_cells = table.select('td.left[data-stat="squad_b"]:not(.iz)')
away_ids = [cell.find('a').get('href').split('/')[3] for cell in away_cells]
match_report_cells = table.select('td.left[data-stat="match_report"]:not(.iz)')
fixture_ids = [cell.find('a').get('href').split('/')[3] for cell in match_report_cells]
# ids_dates = dict(zip(fixture_ids, times))
fid_hid_aid = zip(fixture_ids, home_ids, away_ids)
fixture_teams = {fid: {'home': hid, 'away': aid} for fid, hid, aid in fid_hid_aid}
assert len(fixture_teams) == 380
print(fixture_teams)
