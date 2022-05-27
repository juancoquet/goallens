from datetime import date
import re

from .scrapers.teams.teams_scraper import TeamsScraper

class DBPopulator:

    def __init__(self):
        self.teams = {}
    
    def _create_seasons_teams_dict(self, seasons: list[str], competitions: list[str]) -> dict:
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