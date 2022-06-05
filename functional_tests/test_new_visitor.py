from selenium.webdriver.common.by import By # type: ignore

from .ft_base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_home_page(self):
        # a new user visits the site and is greeted by a welcome message
        welcome = self.driver.find_element(By.TAG_NAME, 'h1')
        self.assertEqual(welcome.text, 'Welcome to')