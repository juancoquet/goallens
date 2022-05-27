from bs4 import BeautifulSoup # type: ignore
from datetime import date
import re
import requests # type: ignore
from time import sleep


class BaseScraper():

    def __init__(self):
        self.comp_codes = {
            'Premier League': 9,
            'Championship': 10,
        }
        self.response = None
        self.html = None
        self.soup = None

    def _request_url(self, url, wait=3):
        response = requests.get(url)
        self.html = response.text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        sleep(wait) # wait to avoid rate limits
        return response

    def _capture_html(self, filepath):
        with open(filepath, 'w') as f:
            f.write(self.html)

    def _go_to_season(self, season):
        season_re = r'\d{4}-\d{4}'
        page_heading = self.soup.find('h1').text
        matched_season = re.search(season_re, page_heading).group()

        while matched_season != season:
            prev_ssn_btn = self.soup.find('a', class_='button2 prev')
            prev_ssn_href = prev_ssn_btn.get('href')
            url = f'https://fbref.com{prev_ssn_href}'
            self._request_url(url)
            page_heading = self.soup.find('h1').text
            matched_season = re.search(season_re, page_heading).group()

    def _validate_competition(self, competition):
        if competition not in self.comp_codes:
            valid_comps = [k for k in self.comp_codes.keys()]
            raise ValueError(f'competion must be one of {valid_comps} – {competition} is invalid')

    def _validate_season(self, season):
        season_re = r'\d{4}-\d{4}'
        if not re.match(season_re, season):
            raise ValueError(f'season must be in format yyyy-yyyy – {season} is invalid')
        else:
            start_yr = int(season[:4])
            end_yr = int(season[-4:])
            if end_yr - start_yr != 1:
                raise ValueError(f'season must be a one year period, e.g. 2019-2020 – {season} is invalid')
            if start_yr < 2010 or end_yr > date.today().year:
                raise ValueError(f'season must be between 2010 and {date.today().year} – {season} is invalid')