from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.functional.recipes.base import RecipeBaseTest


@pytest.mark.selenium
class TestHomePage(RecipeBaseTest):
    def test_home_page_with_no_recipes_message(self):
        self.browser.get(self.live_server_url)

        body = self.browser.find_element(By.TAG_NAME, 'body').text

        assert 'Não existem receitas' in body

    def test_recipe_search_input(self):
        # create a recipes to test search input
        recipes = self.recipe_factory()

        # open page
        self.browser.get(self.live_server_url)

        # find search input
        search_input = self.browser.find_element(
            By.XPATH, '//input[@placeholder="Search for recipes..."]'
        )

        # search for a recipe
        search_input.send_keys(recipes[0].title)
        search_input.send_keys(Keys.ENTER)

        body = self.browser.find_element(By.TAG_NAME, 'body').text

        assert recipes[0].title in body

    @patch('recipes.views.base.PER_PAGE', new=2)
    def test_recipe_home_pagination(self):
        # create a recipes to test search input
        self.recipe_factory()

        # open page
        self.browser.get(self.live_server_url)

        # identify pagination e click page 2
        page = self.browser.find_element(
            By.XPATH, '//a[@aria-label="Go to page 2"]'
        )

        page.click()

        # verify page 2 recipes
        assert 2 == len(self.browser.find_elements(By.CLASS_NAME, 'recipe'))  # noqa: PLR2004

        self.waitFor(5)
