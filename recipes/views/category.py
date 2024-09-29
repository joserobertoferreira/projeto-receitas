from django.http import Http404
from django.utils.translation import gettext as _

from recipes.views.base import RecipeBaseListView


class CategoryListView(RecipeBaseListView):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            category__id=self.kwargs.get('category_id'), is_published=True
        )

        if not queryset:
            raise Http404

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        category_translation = _('Category')

        context.update({
            'title': f'{category_translation} - {context.get("recipes")[0].category.name} |'  # noqa: E501
        })

        return context
