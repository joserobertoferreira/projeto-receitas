from django.core.exceptions import ValidationError

from tests.test_recipe_base import RecipeBaseTest


class CategoryModelTest(RecipeBaseTest):
    def setUp(self) -> None:
        self.category = self.create_category(name='Teste Categoria')
        return super().setUp()

    def test_category_name_max_length(self):
        self.category.name = 'a' * 66

        with self.assertRaises(ValidationError):  # noqa: PT027
            self.category.full_clean()  # a validação do campo ocorre aqui

    def test_category_string_representation(self):
        self.assertEqual(str(self.category), self.category.name)  # noqa: PT009
