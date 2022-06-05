import datetime as dt
from django.contrib.staticfiles.testing import StaticLiveServerTestCase # type: ignore
from selenium import webdriver # type: ignore
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities # type: ignore
import os


class FunctionalTest(StaticLiveServerTestCase):

    host="web"
    
    def setUp(self):
        self.driver = webdriver.Remote(
            'http://selenium:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.FIREFOX,
        )
        self.error_capture_path = None
        self.driver.get(self.live_server_url)
        self.driver.save_screenshot('screenshot.png')

    def tearDown(self):
        if self._test_has_failed:
            self.capture_error_data()
        self.driver.quit()

        
    def capture_error_data(self):
        self._create_error_capture_path()
        self._capture_html(f'{self.error_capture_path}/page_source.html')
        self.driver.save_screenshot(f'{self.error_capture_path}/screenshot.png')

    @property
    def _test_has_failed(self):
        # check if there was an error
        return len(self._outcome.errors) > 0

    def _create_error_capture_path(self):
        timestamp = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.error_capture_path = f'functional_tests/error_captures/{timestamp}'
        os.makedirs(self.error_capture_path)
        with open(f'{self.error_capture_path}/_metadata.txt', 'w') as f:
            f.write(f'{timestamp}\n')
            f.write(f'{self.__class__.__name__}.{self._testMethodName}\n\n')
            for error in self._outcome.errors:
                f.write(f'{error}\n')

    def _capture_html(self, filepath):
        with open(filepath, 'w') as f:
            f.write(self.driver.page_source)