from datetime import date
import re

from ..base_scraper import BaseScraper
from data_sourcing.models import Team


class TeamsScraper(BaseScraper):

    def _capture_html(self, filename):
        filepath = f'data_sourcing/scrapers/teams/captured_html/{filename}.html'
        return super()._capture_html(filepath)

    def get_team_ids(self, season: str, competition: str):
        """scrapes team ids for all teams in a competitin on a given season.
        
        Args:
            season (str): the season to scrape, e.g. '2019-2020'
            competition (str): the competition to scrape, e.g. 'Premier League'
        """
        self._validate_season(season)
        self._validate_competition(competition)

        comp_code = self.comp_codes[competition]
        url = f'https://fbref.com/en/comps/{comp_code}/'
        self._request_url(url)
        self._go_to_season(season)
        table = self.soup.select("table[id^='results'][id$='_overall']")[0]
        team_name_cells = table.select('td.left[data-stat="team"]')
        team_ids = [cell.find('a').get('href').split('/')[3] for cell in team_name_cells]
        return team_ids

    def get_team_short_names(self, season, competition):
        """scrapes team short names.
        
        Args:
            season (str): the season to scrape, e.g. '2019-2020'
            competition (str): the competition to scrape, e.g. 'Premier League'
        """
        self._validate_season(season)
        self._validate_competition(competition)

        comp_code = self.comp_codes[competition]
        url = f'https://fbref.com/en/comps/{comp_code}/'
        self._request_url(url)
        self._go_to_season(season)
        table = self.soup.select("table[id^='results'][id$='_overall']")[0]
        # team_name_cells = table.select('td.left[data-stat="squad"]') # old solution
        team_name_cells = table.select('td.left[data-stat="team"]')
        team_short_names = [cell.find('a').text for cell in team_name_cells]
        return team_short_names


    def get_team_names(self, team_ids: list[str], print_progress=False):
        """scrapes team names.
        
        Args:
            team_ids (list[str]): list of team ids to scrape.
            print_progress (bool): whether to print progress to console.
        Returns:
            dict: a dictionary of team names keyed by team id. {team_id: team_name}
        """
        team_names = {}
        for _id in team_ids:
            if Team.objects.filter(id=_id).exists():
                team_names[_id] = Team.objects.get(id=_id).name
                continue
            url = f'https://fbref.com/en/squads/{_id}/'
            if print_progress:
                print(f'Scraping team name for {_id}')
            self._request_url(url)
            page_heading = self.soup.find('h1').text
            team_name_season_re = r'\d{4}-\d{4} (?P<team_name>.+?) Stats'
            match = re.search(team_name_season_re, page_heading)
            if match is None:
                team_name_re = r'(?P<team_name>.+?) Stats'
                match = re.search(team_name_re, page_heading)
                if match is None:
                    raise ValueError(f'could not find team name for team id {_id}: {url}')
            team_names[_id] = match.group('team_name')
            if print_progress:
                print(f'Team name for {_id}: {team_names[_id]}\n')
        return team_names