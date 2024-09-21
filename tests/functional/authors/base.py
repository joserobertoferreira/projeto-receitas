import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By

from resources.utils.browser import chrome_browser


class AuthorsBaseTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = chrome_browser('--headless')

        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()

        return super().tearDown()

    def waitFor(self, timeout=5) -> None:  # noqa: PLR6301
        time.sleep(timeout)

    def get_by_placeholder(self, element, placeholder):  # noqa: PLR6301
        return element.find_element(
            By.XPATH, f'//input[@placeholder="{placeholder}"]'
        )
