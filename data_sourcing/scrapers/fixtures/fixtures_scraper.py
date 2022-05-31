from datetime import date, time
import re

from ..base_scraper import BaseScraper


class FixturesScraper(BaseScraper):
    # TODO: modify all methods to handle seasons that have not been fully scheduled
    # at the moment the methods expect every fixture to have all data available
    # and will raise an error if a fixture is missing data (like if a match is yet to be played)
    # TODO: consider edge cases

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

    def scrape_fixture_notes(self, season: str, competition: str):
        """scrapes all notes for a given season and competition.
        
        Args:
            season (str): the season to scrape, e.g. '2019-2020'
            competition (str): the competition to scrape, e.g. 'Premier League'
        Returns:
            dict: a dict of fixture ids mapped to strings {fixture_id: str}
        """
        self._validate_season(season)
        self._validate_competition(competition)

        comp_code = self.comp_codes[competition]
        url = f'https://fbref.com/en/comps/{comp_code}/schedule/'
        self._request_url(url)
        self._go_to_season(season)
        table = self.soup.select("table[id^='sched_'][id$='_1']")[0]
        match_report_cells = table.select('td.left[data-stat="match_report"]')
        notes_cells = table.select('td.left[data-stat="notes"]')
        notes_cells = [c for i, c in enumerate(notes_cells) if not 'iz' in match_report_cells[i].get('class')]
        match_report_cells = [c for c in match_report_cells if not 'iz' in c.get('class')]
        notes = [cell.get_text() for cell in notes_cells]
        fixture_ids = [cell.find('a').get('href').split('/')[3] for cell in match_report_cells]
        ids_notes = dict(zip(fixture_ids, notes))
        return ids_notes

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
        def _parse_time(time_str: str):
            try:
                hhmmss = time_str.split(':')
            except AttributeError:
                hhmmss = [None] * 3
            try:
                hh = int(hhmmss[0])
                mm = int(hhmmss[1])
                t = time(hh, mm)
            except (ValueError, TypeError):
                t = None
            return t

        self._validate_season(season)
        self._validate_competition(competition)

        comp_code = self.comp_codes[competition]
        url = f'https://fbref.com/en/comps/{comp_code}/schedule/'
        self._request_url(url)
        self._go_to_season(season)
        table = self.soup.select("table[id^='sched_'][id$='_1']")[0]
        match_report_cells = table.select('td.left[data-stat="match_report"]')
        time_cells = table.select('td.right[data-stat="time"]')
        time_cells = [c for i, c in enumerate(time_cells) if not 'iz' in match_report_cells[i].get('class')]
        match_report_cells = [c for c in match_report_cells if not 'iz' in c.get('class')]
        times = [cell.get('csk') for cell in time_cells]
        times = [_parse_time(t) for t in times]
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


    def scrape_fixture_goals(self, season: str, competition: str):
        """scrapes home and away goals for each fixture in a given season and competition.
        
        Args:
            season (str): the season to scrape, e.g. '2019-2020'
            competition (str): the competition to scrape, e.g. 'Premier League'
        Returns:
            dict: a dict of fixture ids mapped to another dict containing home and away goals with format:
            {fixture_id: {'home': int, 'away': int}}
        """
        self._validate_season(season)
        self._validate_competition(competition)

        comp_code = self.comp_codes[competition]
        url = f'https://fbref.com/en/comps/{comp_code}/schedule/'
        self._request_url(url)
        self._go_to_season(season)
        table = self.soup.select("table[id^='sched_'][id$='_1']")[0]
        score_cells = table.select('td.center[data-stat="score"]:not(.iz)')
        scores = [cell.find('a').get_text() for cell in score_cells]
        home_goals = [int(s.split('–')[0]) for s in scores]
        away_goals = [int(s.split('–')[1]) for s in scores]
        match_report_cells = table.select('td.left[data-stat="match_report"]:not(.iz)')
        fixture_ids = [cell.find('a').get('href').split('/')[3] for cell in match_report_cells]
        fid_hg_ag = zip(fixture_ids, home_goals, away_goals)
        goals = {fid: {'home': hg, 'away': ag} for fid, hg, ag in fid_hg_ag}
        return goals

    def scrape_fixture_xGs(self, season: str, competition: str):
        """scrapes home and away xGs for each fixture in a given season and competition.
        
        Args:
            season (str): the season to scrape, e.g. '2019-2020'
            competition (str): the competition to scrape, e.g. 'Premier League'
        Returns:
            dict: a dict of fixture ids mapped to another dict containing home and away xGs with format:
            {fixture_id: {'home': float, 'away': float}}
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
        return xGs