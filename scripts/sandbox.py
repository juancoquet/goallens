from data_sourcing.db_population.db_population import DBPopulator
from data_sourcing.scrapers.fixtures.fixtures_scraper import FixturesScraper
from supported_comps import COMP_CODES

comps = list(COMP_CODES.keys())

def run():
    s = FixturesScraper()
    s.scrape_upcoming_fixtures('Premier League')
