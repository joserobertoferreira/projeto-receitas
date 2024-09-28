from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from tag.models import Tag

from .models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin): ...


class TagInline(GenericStackedInline):
    model = Tag
    fields = ('name',)
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'is_published', 'author']
    list_display_links = 'title', 'created_at'
    list_filter = [
        'category',
        'author',
        'is_published',
        'created_at',
        'preparation_steps_is_html',
    ]
    list_per_page = 15
    list_editable = [
        'is_published',
    ]

    ordering = ['-id']

    prepopulated_fields = {'slug': ('title',)}

    search_fields = ['id', 'title', 'description', 'slug', 'preparation_steps']

    inlines = [TagInline]


admin.site.register(Category, CategoryAdmin)
