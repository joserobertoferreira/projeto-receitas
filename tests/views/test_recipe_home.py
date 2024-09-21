from http import HTTPStatus
from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views
from tests.test_recipe_base import RecipeBaseTest


class HomeViewsTest(RecipeBaseTest):
    def test_recipe_home_view_function_is_ok(self):  # noqa: PLR6301
        view = resolve(reverse('recipes:home'))

        assert view.func.view_class is views.HomeListView

    def test_recipe_home_view_returns_status_code_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, HTTPStatus.OK)  # noqa: PT009

    def test_recipe_home_view_load_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')  # noqa: PT009

    def test_recipe_home_template_shows_not_found_message(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(  # noqa: PT009
            '<h1>Não existem receitas</h1>', response.content.decode('utf-8')
        )

    def test_recipe_home_template_load_recipes(self):
        self.create_recipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        recipe_context = response.context['recipes']

        self.assertIn('Title', content)  # noqa: PT009
        self.assertEqual(len(recipe_context), 1)  # noqa: PT009

    def test_recipe_home_template_not_published(self):
        self.create_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        self.assertIn(  # noqa: PT009
            '<h1>Não existem receitas</h1>', response.content.decode('utf-8')
        )

    @patch('recipes.views.base.PER_PAGE', new=3)
    def test_recipe_home_pagination(self):
        self.recipe_factory(8)

        response = self.client.get(reverse('recipes:home'))

        recipes = response.context['recipes']
        paginator = recipes.paginator

        assert paginator.num_pages == 3  # noqa: PLR2004
        assert len(paginator.get_page(1)) == 3  # noqa: PLR2004
        assert len(paginator.get_page(2)) == 3  # noqa: PLR2004
        assert len(paginator.get_page(3)) == 2  # noqa: PLR2004

    #        self.assertEqual(len(paginator.get_page(3)), 3)  # noqa: PT009

    @patch('recipes.views.base.PER_PAGE', new=3)
    def test_send_recipe_invalid_page(self):
        self.recipe_factory(8)

        response = self.client.get(reverse('recipes:home') + '?page=1a')

        assert response.context['recipes'].number == 1

        response = self.client.get(reverse('recipes:home') + '?page=2')

        assert response.context['recipes'].number == 2  # noqa: PLR2004
