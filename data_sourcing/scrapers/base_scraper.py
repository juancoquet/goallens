from bs4 import BeautifulSoup # type: ignore
from datetime import date
import re
import requests # type: ignore
import requests_cache # type: ignore
from time import sleep

from supported_comps import COMP_CODES

EXPIRE_AFTER = 60 * 60 * 24 # expire value in seconds
session = requests_cache.CachedSession(cache_name='req_cache', backend='sqlite', expire_after=EXPIRE_AFTER)

class BaseScraper():

    def __init__(self):
        self.comp_codes = COMP_CODES
        self.response = None
        self.html = None
        self.soup = None

    def _request_url(self, url, wait=3, expire_after=None):
        """requests a url using requests_cache and returns the response object.
        saves the html and bs4 soup to self.html and self.soup. if the request is not cached,
        a wait time is added to avoid hitting rate limits. if expire_after is specified, the request is
        cached for the specified amount of time (fallback to EXPIRE_AFTER if not specified).

        Args:
            url (str): the url to request.
            wait (int, optional): wait time after uncached request, in seconds. Defaults to 3.
            expire_after (int, optional): cache duration, in seconds.

        Returns:
            _type_: _description_
        """
        if expire_after is None:
            response = session.get(url)
        else:
            response = session.get(url, expire_after=expire_after)
        self.html = response.text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        if not(response.from_cache):
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
            start_yr = int(season[:4])
            matched_start_yr = int(matched_season[:4])
            if matched_start_yr > start_yr:
                prev_ssn_btn = self.soup.find('a', class_='button2 prev')
                ssn_href = prev_ssn_btn.get('href')
            else:
                next_ssn_btn = self.soup.find('a', class_='button2 next')
                ssn_href = next_ssn_btn.get('href')
            url = f'https://fbref.com{ssn_href}'
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
            if start_yr < 2010 or end_yr > date.today().year + 1:
                raise ValueError(f'season must be between 2010 and {date.today().year + 1} – {season} is invalid')