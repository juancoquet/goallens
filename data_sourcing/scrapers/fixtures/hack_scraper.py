from bs4 import BeautifulSoup # type: ignore
from datetime import date, time
import requests # type: ignore


# url = 'https://fbref.com/en/comps/9/schedule/'
url = 'https://fbref.com/en/comps/9/3232/schedule/'
table_id = 'sched_3232_1'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table', id=table_id)
score_cells = table.select('td.center[data-stat="score"]:not(.iz)')
scores = [cell.find('a').get_text() for cell in score_cells]
home_goals = [int(s.split('–')[0]) for s in scores]
away_goals = [int(s.split('–')[1]) for s in scores]
match_report_cells = table.select('td.left[data-stat="match_report"]:not(.iz)')
fixture_ids = [cell.find('a').get('href').split('/')[3] for cell in match_report_cells]
# ids_dates = dict(zip(fixture_ids, times))
fid_hg_ag = zip(fixture_ids, home_goals, away_goals)
goals = {fid: {'home': hg, 'away': ag} for fid, hg, ag in fid_hg_ag}
assert len(goals) == 380
print(goals)
