from datetime import date, time, timedelta
import json
import re

from ..base_scraper import BaseScraper
from data_sourcing.models import Fixture
from supported_comps import COMP_CODES


class FixturesScraper(BaseScraper):

    def __init__(self):
        super().__init__()

    def scrape_fixture_ids(self, season: str, competition: str):
        """scrapes all fixture ids for a given season and competition.
        
        Args:
            season (str): the season to scrape, e.g. '2019-2020'
            competition (str): the competition to scrape, e.g. 'Premier League'
        Returns:
            list: a list of fixture ids
        """
        self._validate_season(season)
        self._validate_competition(competition)

        comp_code = self.comp_codes[competition]
        url = f'https://fbref.com/en/comps/{comp_code}/schedule/'
        self._request_url(url)
        self._go_to_season(season)
        table = self.soup.select("table[id^='sched_'][id$='_1']")[0]
        rows = table.select('tbody')[0].select('tr:not(.spacer):not(.thead)')
        fixture_ids = []
        for row in rows:
            match_report_cell = row.select('td.left[data-stat="match_report"]')[0]
            if match_report_cell.text != 'Match Report': # game is yet to be played, create temp ids
                home = row.select('td[data-stat="squad_a"]')[0].find('a').get('href').split('/')[3]
                away = row.select('td[data-stat="squad_b"]')[0].find('a').get('href').split('/')[3]
                fixture_ids.append(f'{comp_code}-{home}-{away}')
            else:
                fixture_ids.append(match_report_cell.find('a').get('href').split('/')[3])
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
        rows = table.select('tbody')[0].select('tr:not(.spacer):not(.thead)')
        fixture_ids = self.scrape_fixture_ids(season, competition)
        notes = [row.select('td[data-stat="notes"]')[0].text for row in rows]
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
        fixture_ids = self.scrape_fixture_ids(season, competition)
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
        rows = table.select('tbody')[0].select('tr:not(.spacer):not(.thead)')
        fixture_ids = self.scrape_fixture_ids(season, competition)
        times = [_parse_time(row.select('td[data-stat="time"]')[0].get('csk')) for row in rows]
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
        fixture_ids = self.scrape_fixture_ids(season, competition)
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
        rows = table.select('tbody')[0].select('tr:not(.spacer):not(.thead)')
        score_cells = [row.select('td[data-stat="score"]')[0] for row in rows]
        scores = []
        for cell in score_cells:
            try:
                scores.append(cell.find('a').get_text())
            except AttributeError:
                scores.append(None)
        home_goals, away_goals = [], []
        for score in scores:
            if score is None:
                home_goals.append(None)
                away_goals.append(None)
            else:
                home_goals.append(int(score.split('–')[0]))
                away_goals.append(int(score.split('–')[1]))
        fixture_ids = self.scrape_fixture_ids(season, competition)
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
        fixture_ids = self.scrape_fixture_ids(season, competition)
        rows = table.select('tbody')[0].select('tr:not(.spacer):not(.thead)')
        home_xGs, away_xGs = [], []
        for row in rows:
            try:
                home_xG_cell = row.select('td[data-stat="xg_a"]')[0]
                away_xG_cell = row.select('td[data-stat="xg_b"]')[0]
                home_xG = float(home_xG_cell.get_text()) if home_xG_cell.get_text() else None
                away_xG = float(away_xG_cell.get_text()) if away_xG_cell.get_text() else None
            except IndexError:
                home_xG = None
                away_xG = None
            home_xGs.append(home_xG)
            away_xGs.append(away_xG)
        fid_hxG_axG = zip(fixture_ids, home_xGs, away_xGs)
        xGs = {fid: {'home': hxG, 'away': axG} for fid, hxG, axG in fid_hxG_axG}
        return xGs

    def scrape_upcoming_fixtures(self, competition: str, from_date=date.today(), lookahead=2):
        """scrapes upcoming fixtures temporary ids after given date from the given competition.
        
        Args:
            comps (list[str]): the competitions to scrape, e.g. ['Premier League', 'La Liga']
            from_date (date): the date to start scraping from, e.g. date(2019, 1, 1)
            lookahead (int): the number of days to look ahead, e.g. 2
        Returns:
            list[str]: a list of temporary ids with format ['{comp_code}-{home_id}-{away_id}']
        """
        curr_date = from_date
        upcoming_ids = []
        while curr_date <= from_date + timedelta(days=lookahead):
            url = f'https://fbref.com/en/matches/{curr_date.strftime("%Y-%m-%d")}'
            self._request_url(url, expire_after=60*2)
            table_containers = self.soup.select('div.table_wrapper')

            for table_container in table_containers:
                # get comp code
                ## couldn't find a clean way of doing this due to poor html formatting on fbref
                ## hacky regex solution, but it works
                sched_id = table_container.get('id').split('_')[-1]
                # match an href which contains the comp code related to the schedule id
                # (id of the schedule for a comp & season)
                href_re = re.compile(f'id="sched_{sched_id}_link" data-label="' + r'<a href="(?P<href>[-a-zA-Z0-9@:%_\+.~#?&//=]*)">')
                href = href_re.search(self.html).group('href')
                comp_code = int(href.split('/')[3])

                if comp_code == self.comp_codes[competition]:
                    table = self.soup.select(f'table[id="sched_{sched_id}"]')[0]
                    rows = table.select('tbody')[0].select('tr:not(.spacer):not(.thead)')
                    for row in rows:
                        home = row.select('td[data-stat="squad_a"]')[0].find('a').get('href').split('/')[3]
                        away = row.select('td[data-stat="squad_b"]')[0].find('a').get('href').split('/')[3]
                        temp_id = f'{self.comp_codes[competition]}-{home}-{away}'
                        upcoming_ids.append(temp_id)
            curr_date += timedelta(days=1)
        return upcoming_ids

    def scrape_settled_fixtures(self, on_date=date.today()):
        """scrapes data for fixtures that were played on a given date for all supported competitions. ignores
        fixtures that have not yet been played.
        
        Returns:
            dict: a dict of fixture ids mapped to another dict containing the fixture's data with format:
            {temp_fixture_id:
                {
                    'fixture_id': str,
                    'date': datetime.date,
                    'time': datetime.time,
                    'home': home_team_id,
                    'away': away_team_id,
                    'goals_home': int,
                    'goals_away: int,
                    'xG_home': float,
                    'xG_away': float
                }
            }
        """
        if on_date > date.today():
            raise ValueError('on_date must be less than or equal to today')
        new_data = {}
        url = f'https://fbref.com/en/matches/{on_date.strftime("%Y-%m-%d")}'
        self._request_url(url)
        table_containers = self.soup.select('div.table_wrapper')
        for table_container in table_containers:
            # get comp code
            ## couldn't find a clean way of doing this due to poor html formatting on fbref
            ## hacky regex solution, but it works
            sched_id = table_container.get('id').split('_')[-1]
            # match an href which contains the comp code related to the schedule id
            # (id of the schedule for a comp & season)
            href_re = re.compile(f'id="sched_{sched_id}_link" data-label="' + r'<a href="(?P<href>[-a-zA-Z0-9@:%_\+.~#?&//=]*)">')
            href = href_re.search(self.html).group('href')
            comp_code = int(href.split('/')[3])

            if comp_code in list(COMP_CODES.values()):
                table = self.soup.select(f'table[id="sched_{sched_id}"]')[0]
                rows = table.select('tbody')[0].select('tr:not(.spacer):not(.thead)')

                for row in rows:
                    match_report_cell = row.select('td.left[data-stat="match_report"]')[0]
                    if match_report_cell.text != 'Match Report': # game is yet to be played, skip
                        continue
                        # home = row.select('td[data-stat="squad_a"]')[0].find('a').get('href').split('/')[3]
                        # away = row.select('td[data-stat="squad_b"]')[0].find('a').get('href').split('/')[3]
                        # fixture_id = (f'{comp_code}-{home}-{away}')
                    else:
                        fixture_id = (match_report_cell.find('a').get('href').split('/')[3])

                    time_str = row.select('td[data-stat="time"]')[0].get('csk')
                    hh, mm, _ = time_str.split(':')
                    time_ = time(int(hh), int(mm))
                    home = row.select('td[data-stat="squad_a"]')[0].find('a').get('href').split('/')[3]
                    away = row.select('td[data-stat="squad_b"]')[0].find('a').get('href').split('/')[3]
                    score = row.select('td[data-stat="score"]')[0].get_text().split('–')
                    try:
                        goals_home = int(score[0])
                        goals_away = int(score[1])
                    except ValueError: # no score yet
                        goals_home = None
                        goals_away = None
                    try:
                        home_xG_cell = row.select('td[data-stat="xg_a"]')[0]
                        away_xG_cell = row.select('td[data-stat="xg_b"]')[0]
                        home_xG = float(home_xG_cell.get_text()) if home_xG_cell.get_text() else None
                        away_xG = float(away_xG_cell.get_text()) if away_xG_cell.get_text() else None
                    except IndexError: # no xG data
                        home_xG = None
                        away_xG = None
                    temp_id = f'{comp_code}-{home}-{away}'
                    new_data[temp_id] = {
                        'fixture_id': fixture_id,
                        'date': on_date,
                        'time': time_,
                        'home': home,
                        'away': away,
                        'goals_home': goals_home,
                        'goals_away': goals_away,
                        'xG_home': home_xG,
                        'xG_away': away_xG
                    }
        return new_data