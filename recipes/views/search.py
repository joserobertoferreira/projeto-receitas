from django.db.models import Q
from django.http import Http404

from recipes.views.base import RecipeBaseListView


class SearchListView(RecipeBaseListView):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('search', '').strip()

        if not search_term:
            raise Http404

        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            Q(
                Q(title__icontains=search_term)
                | Q(description__icontains=search_term)
            ),
            is_published=True,
        )

        return queryset

    def get_context_data(self, *args, **kwargs):
        search_term = self.request.GET.get('search', '').strip()
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'url_query': f'&search={search_term}',
        })

        return context
