from django.urls import path

from recipes import api, views

app_name = 'recipes'

urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),
    path('recipes/search/', views.SearchListView.as_view(), name='search'),
    path('recipes/tags/<slug:slug>', views.TagListView.as_view(), name='tag'),
    path(
        'recipes/category/<int:category_id>/',
        views.CategoryListView.as_view(),
        name='category',
    ),
    path('recipes/<int:pk>/', views.RecipeDetail.as_view(), name='recipe'),
    path(
        'recipes/api/v1/',
        views.HomeListViewAPI.as_view(),
        name='recipes_api_v1',
    ),
    path(
        'recipes/api/v1/<int:pk>/',
        views.RecipeDetailAPI.as_view(),
        name='recipes_api_v1_detail',
    ),
    path('recipes/api/v2/', api.recipe_api_list, name='recipes_api_v2'),
    path(
        'recipes/api/v2/<int:pk>/',
        api.recipe_api_detail,
        name='recipes_api_v2_detail',
    ),
]
