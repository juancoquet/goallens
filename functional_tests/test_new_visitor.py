from selenium.webdriver.common.by import By # type: ignore

from .ft_base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_home_page(self):
        # a new user visits the site and is greeted by a welcome message
        welcome = self.driver.find_element(By.TAG_NAME, 'h1')
        self.assertEqual(welcome.text, 'Welcome to')

        # they see a button inviting them to learn more
        learn_more = self.driver.find_element(By.CLASS_NAME, 'btn--primary')

        # they click the button and the page scrolls down
        learn_more.click()
        