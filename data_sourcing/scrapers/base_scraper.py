import re
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from time import sleep


class BaseScraper():
    """base scraper class with shared functionality."""

    def __init__(self):
        self.comp_codes = {
            'Premier League': 9,
        }

        profile = webdriver.FirefoxProfile()
        profile.set_preference("javascript.enabled", False)
        self.driver = webdriver.Remote(
            'http://selenium:4444/wd/hub',
            desired_capabilities=webdriver.common.desired_capabilities.DesiredCapabilities.FIREFOX,
            browser_profile=profile
        )
        self.driver.get('https://fbref.com/en/')
        sleep(1)
        self._accept_cookies()

    def terminate(self):
        self.driver.quit()

    def _accept_cookies(self):
        try:
            cookie_bts = self.driver.find_element(By.CSS_SELECTOR,'.qc-cmp2-summary-buttons')
            accept = cookie_bts.find_element(By.CSS_SELECTOR,'button.css-1hy2vtq')
            accept.click()
        except:
            pass

    def _screenshot(self, file_path):
        self.driver.save_screenshot(file_path)

    def _capture_html(self, file_path):
        with open(file_path, 'w') as f:
            f.write(self.driver.page_source)

    def _go_to_season(self, season):
        season_re = r'\d{4}-\d{4}'
        page_heading = self.driver.find_element(By.TAG_NAME, 'h1').text
        matched_season = re.search(season_re, page_heading).group()

        while matched_season != season:
            # self._screenshot(matched_season)
            # self._capture_html(matched_season)
            prev_ssn_btn = self.driver.find_element_by_css_selector('a.button2.prev')
            prev_ssn_btn.click()
            sleep(1)
            page_heading = self.driver.find_element(By.TAG_NAME, 'h1').text
            matched_season = re.search(season_re, page_heading).group()