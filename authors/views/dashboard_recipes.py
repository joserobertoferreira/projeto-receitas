from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from authors.forms.recipe import AuthorsRecipeForm
from recipes.models import Recipe
from resources.utils.strings import is_number


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch',
)
class DashboardRecipes(View):
    def get_recipe(self, id):
        recipe = None

        if id:
            recipe = Recipe.objects.filter(
                pk=id,
                is_published=False,
                author=self.request.user,
            ).first()

            if not recipe:
                raise Http404

        return recipe

    def render_recipe(self, form):
        return render(
            self.request,
            'authors/pages/dashboard_recipe.html',
            context={
                'form': form,
            },
        )

    def get(self, request, id=None):  # noqa: PLR6301
        recipe = self.get_recipe(id)

        form = AuthorsRecipeForm(instance=recipe)

        return self.render_recipe(form)

    def post(self, request, id=None):
        recipe = self.get_recipe(id)

        form = AuthorsRecipeForm(
            request.POST or None, files=request.FILES or None, instance=recipe
        )

        if form.is_valid():
            recipe = form.save(commit=False)

            recipe.author = request.user
            recipe.is_published = False
            recipe.preparation_steps_is_html = False

            if is_number(recipe.preparation_time):
                recipe.preparation_time = int(form.data['preparation_time'])
            if is_number(recipe.servings):
                recipe.servings = int(form.data['servings'])

            recipe.save()

            messages.success(request, 'Recipe updated successfully.')

            return redirect(
                reverse('authors:dashboard_recipe_edit', args=(recipe.id,))
            )

        return self.render_recipe(form)


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch',
)
class DashboardRecipesDelete(DashboardRecipes):
    def post(self, *args, **kwargs):
        recipe = self.get_recipe(self.request.POST.get('id'))
        recipe.delete()
        messages.success(self.request, 'Recipe was deleted successfully.')

        return redirect(reverse('authors:dashboard'))
