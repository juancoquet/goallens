from bs4 import BeautifulSoup # type: ignore
from datetime import date, time
import requests # type: ignore
from .fixtures_scraper import FixturesScraper


s = FixturesScraper()
s._request_url('https://fbref.com/en/comps/comp.php?comp=1')
s._go_to_season('2022-2023')
print(s.soup.find('h1').text)
