from datetime import date
import re

from .models import Team
from .scrapers.teams.teams_scraper import TeamsScraper

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
        season_re = r'\d{4}-\d{4}'
        for competition in competitions:
            if competition not in scraper.comp_codes:
                valid_comps = [k for k in scraper.comp_codes.keys()]
                raise ValueError(f'competion must be one of {valid_comps} – "{competition}" is invalid')
        for season in seasons:
            if not re.match(season_re, season):
                raise ValueError(f'season must be in format yyyy-yyyy – "{season}" is invalid')
            else:
                start_yr = int(season[:4])
                end_yr = int(season[-4:])
                if end_yr - start_yr != 1:
                    raise ValueError(f'season must be a one year period, e.g. 2019-2020 – "{season}" is invalid')
                if start_yr < 2010 or end_yr > date.today().year:
                    raise ValueError(f'season must be between 2010 and {date.today().year} – "{season}" is invalid')

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

    def add_teams_from_season_to_db(self, season: list[str], competition: list[str]):
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

