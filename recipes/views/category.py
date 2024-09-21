from django.http import Http404

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

        context.update({
            'title': f'Categoria - {context.get("recipes")[0].category.name} |'
        })

        return context
