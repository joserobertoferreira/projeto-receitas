from django.test import TestCase

from recipes.models import Category, Recipe, User


class RecipeMixin:
    def create_category(self, name='Outros') -> Category:  # noqa: PLR6301
        return Category.objects.create(name=name)

    def create_author(  # noqa: PLR6301
        self,
        first_name='John',
        last_name='Smith',
        username='john_smith',
        password='23444',
        email='john@smith.com',
    ) -> User:
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def create_recipe(  # noqa: PLR0913, PLR0917
        self,
        category_data=None,
        author_data=None,
        title='Title',
        description='Description',
        slug='recipe-slug',
        preparation_time=10,
        preparation_time_unit='minutes',
        servings=5,
        servings_unit='portions',
        preparation_steps='steps',
        preparation_steps_is_html=False,
        is_published=True,
    ):
        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
            category=self.create_category(**category_data),
            author=self.create_author(**author_data),
        )

    def recipe_factory(self, recipes_number=10):
        recipes = []

        for i in range(recipes_number):
            kwargs = {
                'title': f'Recipe Title {i}',
                'slug': f'r{i}',
                'author_data': {'username': f'u{i}'},
            }
            recipe = self.create_recipe(**kwargs)
            recipes.append(recipe)

        return recipes


class RecipeBaseTest(TestCase, RecipeMixin):
    def setUp(self) -> None:
        return super().setUp()
