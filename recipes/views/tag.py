from recipes.views.base import RecipeBaseListView
from tag.models import Tag


class TagListView(RecipeBaseListView):
    template_name = 'recipes/pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(tags__slug=self.kwargs.get('slug', ''))

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects.filter(
            slug=self.kwargs.get('slug', '')
        ).first()

        if not page_title:
            page_title = 'No recipes found'

        page_title = f'{page_title} - Tag '

        context.update({
            'page_title': page_title,
        })

        return context
