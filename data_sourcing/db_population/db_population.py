from datetime import date, time
import re

from ..models import Team, Fixture
from ..scrapers.teams.teams_scraper import TeamsScraper
from ..scrapers.fixtures.fixtures_scraper import FixturesScraper

class DBPopulator:

    def __init__(self):
        self.teams = {}
    
    def _create_seasons_teams_dict(self, seasons: list[str], competitions: list[str]) -> dict:
        """Scrapes all teams involved in the given seasons and competitions.

        Args:
            seasons (list[str]): a list containing season strings in the format 'YYYY-YYYY'
            competitions (list[str]): a list containing competition names

        Raises:
            ValueError: if any of the given seasons or competitions are invalid

        Returns:
            dict: a dictionary that maps scraped teams with format:
            {'team_id': {
                'id': 'team_id',
                'name': 'team_name',
                'short_name': 'team_short_name'
                }
            } 
        """
        scraper = TeamsScraper()
        for season in seasons:
            scraper._validate_season
        for competition in competitions:
            scraper._validate_competition(competition)

        teams = {}
        for season in seasons:
            for competition in competitions:
                team_ids = scraper.get_team_ids(season, competition)
                team_short_names = scraper.get_team_short_names(season, competition)
                unique_indexes = [i for i in range(len(team_ids)) if team_ids[i] not in teams]
                team_ids = [team_ids[i] for i in unique_indexes]
                team_short_names = [team_short_names[i] for i in unique_indexes]
                team_names = scraper.get_team_names(team_ids, print_progress=True) # {'team_id': 'team_name'} dict
                for _id, short_name in zip(team_ids, team_short_names):
                    teams[_id] = {
                        'id': _id,
                        'name': team_names[_id],
                        'short_name': short_name
                    }
        self.teams = teams
        return teams

    def add_teams_to_db(self, season: list[str], competition: list[str]):
        """adds all teams involved in the given season and competition to the database.
        
        Args:
            season (list[str]): a list containing season strings in the format 'YYYY-YYYY'
            competition (list[str]): a list containing competition names
        """
        if type(season) != list:
            raise TypeError('seasons must be passed as a list')
        if type(competition) != list:
            raise TypeError('competitions must be passed as a list')

        teams = self._create_seasons_teams_dict(season, competition)
        for team in teams.values():
            self.add_team_to_db(team['id'], team['name'], team['short_name'])
        return teams

    def add_team_to_db(self, team_id: str, team_name: str, team_short_name: str):
        """adds a team to the database and returns the created team object. if the team already
        exists in the database, it returns the existing team object instead.

        Args:
            team_id (str): the id of the team to be added
            team_name (str): the name of the team to be added
            team_short_name (str): the short name of the team to be added

        Returns:
            data_sourcing.models.Team: the created or existing team object
        """
        exists = Team.objects.filter(id=team_id).exists()
        if not exists:
            team = Team.objects.create(
                id=team_id,
                name=team_name,
                short_name=team_short_name
            )
        else:
            team = Team.objects.get(id=team_id)
        return team

    def _create_season_fixtures_dict(self, seasons: list[str], competitions: list[str]) -> dict:
        """scrapes all fixtures for the given seasons and competitions.

        Args:
            seasons (list[str]): seasons to scrape, passed as a list of strings in the format yyyy-yyyy
            competitions (list[str]): a list containing competition names

        Returns:
            dict: a dictionary that maps a fixture id to its pertinent data with format:
            {fixture_id: {
                'competition': comp_name,
                'sesaon', yyyy-yyyy,
                'date': datetime.date,
                'time': datetime.time,
                'home': home_team_id,
                'away': away_team_id,
                'goals_home': int,
                'goals_away': int,
                'xG_home': float,
                'xG_away': 'float
                }
            }
        """
        scraper = FixturesScraper()
        for season in seasons:
            scraper._validate_season(season)
        for competition in competitions:
            scraper._validate_competition(competition)

        fixtures = {}
        for season in seasons:
            for competition in competitions:
                print(f'Scraping fixtures for {competition} in {season}')
                print('-' * 50)
                print('scraping ids...')
                ids = scraper.scrape_fixture_ids(season, competition)
                print('scraping dates...')
                dates = scraper.scrape_fixture_dates(season, competition)
                print('scraping times...')
                times = scraper.scrape_fixture_times(season, competition)
                print('scraping team ids...')
                team_ids = scraper.scrape_fixture_team_ids(season, competition)
                print('scraping goals...')
                goals = scraper.scrape_fixture_goals(season, competition)
                print('scraping xG...')
                xG = scraper.scrape_fixture_xGs(season, competition)
                print(f'finished scraping for {competition} in {season}')
                print(f'scraped {len(ids)} fixtures')
                print('-' * 50)
                for _id in ids:
                    fixtures[_id] = {
                        'competition': competition,
                        'season': season,
                        'date': dates[_id],
                        'time': times[_id],
                        'home': team_ids[_id]['home'],
                        'away': team_ids[_id]['away'],
                        'goals_home': goals[_id]['home'],
                        'goals_away': goals[_id]['away'],
                        'xG_home': xG[_id]['home'],
                        'xG_away': xG[_id]['away']
                    }
        self.fixtures = fixtures
        return fixtures

    def add_fixtures_to_db(self, seasons: list[str], competitions: list[str]):
        """adds all fixtures for the given seasons and competitions to the database.

        Args:
            seasons (list[str]): seasons to scrape, passed as a list of strings in the format yyyy-yyyy
            competitions (list[str]): a list containing competition names
        """
        if type(seasons) != list:
            raise TypeError('seasons must be passed as a list')
        if type(competitions) != list:
            raise TypeError('competitions must be passed as a list')

        fixtures = self._create_season_fixtures_dict(seasons, competitions)
        for id_, data in fixtures.items():
            self.add_fixture_to_db(
                fixture_id=id_,
                competition=data['competition'],
                season=data['season'],
                date=data['date'],
                time=data['time'],
                home_team_id=data['home'],
                away_team_id=data['away'],
                goals_home=data['goals_home'],
                goals_away=data['goals_away'],
                xG_home=data['xG_home'],
                xG_away=data['xG_away']
            )
        return fixtures

    def add_fixture_to_db(self, fixture_id: str, competition: str, season: str, date: date, time: time,
                          home_team_id: str, away_team_id: str, goals_home: int, goals_away: int,
                          xG_home: float, xG_away: float):
        """adds a fixture to the database and returns the created fixture object. if the fixture already
        exists in the database, it returns the existing fixture object instead.

        Args:
            fixture_id (str): the id of the fixture to be added
            competition (str): the name of the competition the fixture belongs to
            season (str): the season the fixture belongs to
            date (datetime.date): the date of the fixture
            time (datetime.time): the time of the fixture
            home_team_id (str): the id of the home team
            away_team_id (str): the id of the away team
            goals_home (int): the number of goals scored by the home team
            goals_away (int): the number of goals scored by the away team
            xG_home (float): the home team's xG
            xG_away (float): the away team's xG

        Returns:
            data_sourcing.models.Fixture: the created or existing fixture object
        """
        exists = Fixture.objects.filter(id=fixture_id).exists()
        home_team = Team.objects.get(id=home_team_id)
        away_team = Team.objects.get(id=away_team_id)
        if not exists:
            fixture = Fixture.objects.create(
                id=fixture_id,
                competition=competition,
                season=season,
                date=date,
                time=time,
                home=home_team,
                away=away_team,
                goals_home=goals_home,
                goals_away=goals_away,
                xG_home=xG_home,
                xG_away=xG_away
            )
        else:
            fixture = Fixture.objects.get(id=fixture_id)
            fixture.competition = competition
            fixture.season = season
            fixture.date = date
            fixture.time = time
            fixture.home = home_team
            fixture.away = away_team
            fixture.goals_home = goals_home
            fixture.goals_away = goals_away
            fixture.xG_home = xG_home
            fixture.xG_away = xG_away
            fixture.save()
            fixture = Fixture.objects.get(id=fixture_id)
        return fixture