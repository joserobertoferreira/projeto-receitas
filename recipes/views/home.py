from django.http import JsonResponse

from recipes.views.base import RecipeBaseListView


class HomeListView(RecipeBaseListView):
    template_name = 'recipes/pages/home.html'


class HomeListViewAPI(RecipeBaseListView):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):  # noqa: PLR6301
        recipes_dict = self.get_context_data()['recipes']
        recipes_list = recipes_dict.object_list.values()

        return JsonResponse(list(recipes_list), safe=False)
