from django.core.exceptions import ValidationError
from parameterized import parameterized

from tests.test_recipe_base import Recipe, RecipeBaseTest


class RecipeModelTest(RecipeBaseTest):
    def setUp(self) -> None:
        self.recipe = self.create_recipe()
        return super().setUp()

    def create_recipe_without_default_values(self):
        recipe = Recipe(
            category=self.create_category(name='Categoria'),
            author=self.create_author(username='newuser'),
            title='Título da Receita',
            description='Descrição da receita',
            slug='recipe-slug-default',
            preparation_time=10,
            preparation_time_unit='minutos',
            servings=5,
            servings_unit='porções',
            preparation_steps='Passos para a preparação da receita',
        )
        recipe.full_clean()
        recipe.save()

        return recipe

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 35),
        ('servings_unit', 35),
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(
            self.recipe, field, 'a' * (max_length + 1)
        )  # um caractere a mais do que o limite

        with self.assertRaises(ValidationError):  # noqa: PT027
            self.recipe.full_clean()  # a validação do campo ocorre aqui

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.create_recipe_without_default_values()
        self.assertFalse(recipe.preparation_steps_is_html)  # noqa: PT009

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.create_recipe_without_default_values()
        self.assertFalse(recipe.is_published)  # noqa: PT009

    def test_recipe_string_representation(self):
        self.recipe.title = 'Test Title'
        self.recipe.full_clean()
        self.recipe.save()

        self.assertEqual(str(self.recipe), 'Test Title')  # noqa: PT009
