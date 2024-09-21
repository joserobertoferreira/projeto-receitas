import os

from django.views.generic import ListView

from recipes.models import Recipe
from resources.utils.pagination import pagination

PER_PAGE = int(os.getenv('PER_PAGE', 6))  # noqa: PLW1508


class RecipeBaseListView(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        page_obj, pagination_range = pagination(
            self.request, context.get('recipes'), PER_PAGE
        )

        context.update({
            'recipes': page_obj,
            'pagination_range': pagination_range,
        })

        return context
