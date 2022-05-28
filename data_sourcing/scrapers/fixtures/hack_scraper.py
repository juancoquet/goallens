from bs4 import BeautifulSoup # type: ignore
from datetime import date, time
import requests # type: ignore


# url = 'https://fbref.com/en/comps/9/schedule/'
url = 'https://fbref.com/en/comps/10/3233/schedule/'
table_id = 'sched_3233_1'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table', id=table_id)
match_report_cells = table.select('td.left[data-stat="match_report"]:not(.iz)')
fixture_ids = [cell.find('a').get('href').split('/')[3] for cell in match_report_cells]
home_xG_cells = table.select('td.right[data-stat="xg_a"]')
if len(home_xG_cells) > 0: # xG data exists
    home_xG_cells = [cell for cell in home_xG_cells if cell.get_text() != '']
    home_xGs = [float(cell.get_text()) for cell in home_xG_cells]
    away_xG_cells = table.select('td.right[data-stat="xg_b"]')
    away_xG_cells = [cell for cell in away_xG_cells if cell.get_text() != '']
    away_xGs = [float(cell.get_text()) for cell in away_xG_cells]
    fid_hxg_axg = zip(fixture_ids, home_xGs, away_xGs)
    xGs = {fid: {'home': hxG, 'away': axG} for fid, hxG, axG in fid_hxg_axg}
else:
    xGs = {id_: {'home': None, 'away': None} for id_ in fixture_ids}
assert len(xGs) == 552
print(xGs)
