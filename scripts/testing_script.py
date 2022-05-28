from data_sourcing.scrapers.base_scraper import BaseScraper


def run():
    s = BaseScraper()
    for i in range(10):
        s._request_url('https://www.google.com')
        print(i)