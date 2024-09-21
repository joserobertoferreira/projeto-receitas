import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from resources.utils.browser import chrome_browser
from tests.test_recipe_base import RecipeMixin


class RecipeBaseTest(StaticLiveServerTestCase, RecipeMixin):
    def setUp(self) -> None:
        self.browser = chrome_browser('--headless')

        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()

        return super().tearDown()

    def waitFor(self, timeout=5) -> None:  # noqa: PLR6301
        time.sleep(timeout)
