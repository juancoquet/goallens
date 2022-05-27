from datetime import date
import re

from ..base_scraper import BaseScraper


class FixturesScraper(BaseScraper):

    def scrape_fixture_ids(self, season: str, competition: str):
        """scrapes all fixture ids for a given season and competition.
        
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
        url = f'https://fbref.com/en/comps/{comp_code}/schedule/'
        self._request_url(url)
        self._go_to_season(season)
        table = self.soup.select("table[id^='sched_'][id$='_1']")[0]
        match_report_cells = table.select('td.left[data-stat="match_report"]:not(.iz)')
        fixture_ids = [cell.find('a').get('href').split('/')[3] for cell in match_report_cells]
        return fixture_ids

    def scrape_fixture_dates(self, season: str, competition: str):
        """scrapes all fixture dates for a given season and competition.
        
        Args:
            season (str): the season to scrape, e.g. '2019-2020'
            competition (str): the competition to scrape, e.g. 'Premier League'
        Returns:
            dict: a dict of fixture ids mapped to datetime.date objects {fixture_id: datetime.date}
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
        url = f'https://fbref.com/en/comps/{comp_code}/schedule/'
        self._request_url(url)
        self._go_to_season(season)
        table = self.soup.select("table[id^='sched_'][id$='_1']")[0]
        date_cells = table.select('td.left[data-stat="date"]:not(.iz)')
        dates = [cell.get('csk') for cell in date_cells]
        dates = [date(int(d[:4]), int(d[4:6]), int(d[6:])) for d in dates]
        match_report_cells = table.select('td.left[data-stat="match_report"]:not(.iz)')
        fixture_ids = [cell.find('a').get('href').split('/')[3] for cell in match_report_cells]
        ids_dates = dict(zip(fixture_ids, dates))
        return ids_dates