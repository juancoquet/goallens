from datetime import date
import re
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from time import sleep

from ..base_scraper import BaseScraper


class TeamScraper(BaseScraper):
    """scrapes team ids, names, and short names from fbref.com."""

    def _screenshot(self, filename):
        destination = f'data_sourcing/scrapers/teams/screenshots/{filename}.png'
        super()._screenshot(destination)

    def _capture_html(self, filename):
        destination = f'data_sourcing/scrapers/teams/captured_html/{filename}.html'
        super()._capture_html(destination)

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
        self.driver.get(f'https://fbref.com/en/comps/{comp_code}/')
        self._go_to_season(season)
        sleep(1)
        
        table_selector = "table[id^='results'][id$='_overall']"
        table = self.driver.find_element(By.CSS_SELECTOR, table_selector)
        with open('data_sourcing/scrapers/teams/captured_html/table.html', 'w') as f:
            f.write(table.get_attribute('outerHTML'))