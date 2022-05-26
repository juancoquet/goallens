from datetime import date
import re

from ..base_scraper import BaseScraper


class TeamsScraper(BaseScraper):

    def _capture_html(self, filename):
        filepath = f'data_sourcing/scrapers/teams/captured_html/{filename}.html'
        return super()._capture_html(filepath)

    def get_team_ids(self, season, competition):
        """scrapes team ids from fbref.com.
        
        Args:
            season (str): the season to scrape, e.g. '2019-2020'
            competition (str): the competition to scrape, e.g. 'Premier League'
        """
        season_re = r'\d{4}-\d{4}'
        if competition not in self.comp_codes:
            raise ValueError(f'competion must be one of {self.comp_codes.keys()}')
        if not re.match(season_re, season):
            raise ValueError('season must be in format yyyy-yyyy')
        else:
            start_yr = int(season[:4])
            end_yr = int(season[-4:])
            if end_yr - start_yr != 1:
                raise ValueError('season must be a one year period, e.g. 2019-2020')
            if start_yr < 2010 or end_yr > date.today().year:
                raise ValueError(f'season must be between 2010 and {date.today().year}')

        comp_code = self.comp_codes[competition]
        url = f'https://fbref.com/en/comps/{comp_code}/'
        self._request_url(url)
        self._go_to_season(season)
        table = self.soup.select("table[id^='results'][id$='_overall']")[0]
        team_name_cells = table.select('td.left[data-stat="squad"]')
        team_ids = [cell.find('a').get('href').split('/')[3] for cell in team_name_cells]
        return team_ids

    def get_team_short_names(self, season, competition):
        """scrapes team short names from fbref.com.
        
        Args:
            season (str): the season to scrape, e.g. '2019-2020'
            competition (str): the competition to scrape, e.g. 'Premier League'
        """
        season_re = r'\d{4}-\d{4}'
        if competition not in self.comp_codes:
            raise ValueError(f'competion must be one of {self.comp_codes.keys()}')
        if not re.match(season_re, season):
            raise ValueError('season must be in format yyyy-yyyy')
        else:
            start_yr = int(season[:4])
            end_yr = int(season[-4:])
            if end_yr - start_yr != 1:
                raise ValueError('season must be a one year period, e.g. 2019-2020')
            if start_yr < 2010 or end_yr > date.today().year:
                raise ValueError(f'season must be between 2010 and {date.today().year}')

        comp_code = self.comp_codes[competition]
        url = f'https://fbref.com/en/comps/{comp_code}/'
        self._request_url(url)
        self._go_to_season(season)
        table = self.soup.select("table[id^='results'][id$='_overall']")[0]
        team_name_cells = table.select('td.left[data-stat="squad"]')
        team_short_names = [cell.find('a').text for cell in team_name_cells]
        return team_short_names