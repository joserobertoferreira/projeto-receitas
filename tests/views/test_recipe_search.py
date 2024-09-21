from http import HTTPStatus

from django.urls import resolve, reverse

from recipes import views
from tests.test_recipe_base import RecipeBaseTest


class SearchViewsTest(RecipeBaseTest):
    def test_recipe_view_search(self):  # noqa: PLR6301
        url = reverse('recipes:search')
        resolved = resolve(url)

        assert resolved.func.view_class is views.SearchListView

    def test_recipe_search_template_is_loaded(self):
        url = reverse('recipes:search') + '?search=recipe'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/search.html')  # noqa: PT009

    def test_recipe_search_raises_error(self):
        url = reverse('recipes:search')
        response = self.client.get(url)

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_recipe_search_term_is_safe(self):
        url = reverse('recipes:search') + '?search=<recipe>'
        response = self.client.get(url)
        self.assertIn(  # noqa: PT009
            'Search for &quot;&lt;recipe&gt;&quot;',
            response.content.decode('utf-8'),
        )

    def test_recipe_search_recibe_by_title(self):
        recipe1 = self.create_recipe(
            title='Recipe 1',
            slug='recipe-1',
            author_data={'username': 'user 1'},
        )
        recipe2 = self.create_recipe(
            title='Recipe 2',
            slug='recipe-2',
            author_data={'username': 'user 2'},
        )

        url = reverse('recipes:search')

        response = self.client.get(f'{url}?search={recipe1}')
        self.assertIn(recipe1, response.context['recipes'])  # noqa: PT009

        response = self.client.get(f'{url}?search={recipe2}')
        self.assertIn(recipe2, response.context['recipes'])  # noqa: PT009

        response = self.client.get(f'{url}?search=Recipe')
        self.assertIn(recipe1, response.context['recipes'])  # noqa: PT009
        self.assertIn(recipe2, response.context['recipes'])  # noqa: PT009
