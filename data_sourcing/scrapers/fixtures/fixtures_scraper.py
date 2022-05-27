from datetime import date, time
import re

from ..base_scraper import BaseScraper


class FixturesScraper(BaseScraper):
    # TODO: modify all methods to handle seasons that have not been fully scheduled
    # at the moment the methods expect every fixture to have all data available
    # and will raise an error if a fixture is missing data (like if a match is yet to be played)

    def scrape_fixture_ids(self, season: str, competition: str):
        """scrapes all fixture ids for a given season and competition.
        
        Args:
            season (str): the season to scrape, e.g. '2019-2020'
            competition (str): the competition to scrape, e.g. 'Premier League'
        """
        self._validate_season(season)
        self._validate_competition(competition)

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
        self._validate_season(season)
        self._validate_competition(competition)

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

    def scrape_fixture_times(self, season: str, competition: str):
        """scrapes all times for a given season and competition.
        
        Args:
            season (str): the season to scrape, e.g. '2019-2020'
            competition (str): the competition to scrape, e.g. 'Premier League'
        Returns:
            dict: a dict of fixture ids mapped to datetime.time objects {fixture_id: datetime.time}
        """
        self._validate_season(season)
        self._validate_competition(competition)

        comp_code = self.comp_codes[competition]
        url = f'https://fbref.com/en/comps/{comp_code}/schedule/'
        self._request_url(url)
        self._go_to_season(season)
        table = self.soup.select("table[id^='sched_'][id$='_1']")[0]
        time_cells = table.select('td.right[data-stat="time"]:not(.iz)')
        times = [cell.get('csk') for cell in time_cells]
        times = [t.split(':') for t in times]
        times = [time(int(t[0]), int(t[1])) for t in times]
        match_report_cells = table.select('td.left[data-stat="match_report"]:not(.iz)')
        fixture_ids = [cell.find('a').get('href').split('/')[3] for cell in match_report_cells]
        ids_times = dict(zip(fixture_ids, times))
        return ids_times

    def scrape_fixture_team_ids(self, season:str, competition: str):
        """scrapes home and away team ids for each fixture in a given season and competition.
        
        Args:
            season (str): the season to scrape, e.g. '2019-2020'
            competition (str): the competition to scrape, e.g. 'Premier League'
        Returns:
            dict: a dict of fixture ids mapped to another dict of home and away team ids:
            {fixture_id: {'home': home_team_id, 'away': away_team_id}}
        """
        self._validate_season(season)
        self._validate_competition(competition)

        comp_code = self.comp_codes[competition]
        url = f'https://fbref.com/en/comps/{comp_code}/schedule/'
        self._request_url(url)
        self._go_to_season(season)
        table = self.soup.select("table[id^='sched_'][id$='_1']")[0]
        home_cells = table.select('td.right[data-stat="squad_a"]:not(.iz)')
        home_ids = [cell.find('a').get('href').split('/')[3] for cell in home_cells]
        away_cells = table.select('td.left[data-stat="squad_b"]:not(.iz)')
        away_ids = [cell.find('a').get('href').split('/')[3] for cell in away_cells]
        match_report_cells = table.select('td.left[data-stat="match_report"]:not(.iz)')
        fixture_ids = [cell.find('a').get('href').split('/')[3] for cell in match_report_cells]
        fid_hid_aid = zip(fixture_ids, home_ids, away_ids)
        team_ids = {fid: {'home': hid, 'away': aid} for fid, hid, aid in fid_hid_aid}
        return team_ids