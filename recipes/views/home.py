from recipes.views.base import RecipeBaseListView


class HomeListView(RecipeBaseListView):
    template_name = 'recipes/pages/home.html'
