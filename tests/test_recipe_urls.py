from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_recipe_home_url_is_correct(self):  # noqa: PLR6301
        url = reverse('recipes:home')
        self.assertEqual(url, '/')  # noqa: PT009

    def test_recipe_category_is_correct(self):  # noqa: PLR6301
        url = reverse('recipes:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/recipes/category/1/')  # noqa: PT009

    def test_recipe_detail_url_is_correct(self):  # noqa: PLR6301
        url = reverse('recipes:recipe', kwargs={'pk': 1})
        assert url == '/recipes/1/'

    def test_recipe_search(self):
        url = reverse('recipes:search')
        self.assertEqual(url, '/recipes/search/')  # noqa: PT009
