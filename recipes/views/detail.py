from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.generic import DetailView

from recipes.models import Recipe


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({'is_detail_page': True})

        return context


class RecipeDetailAPI(RecipeDetail):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = (
                self.request.build_absolute_uri()
                + recipe_dict['cover'].url[1:]
            )
        else:
            recipe_dict['cover'] = ''

        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)

        del recipe_dict['is_published']
        del recipe_dict['preparation_steps_is_html']

        return JsonResponse(recipe_dict, safe=False)
