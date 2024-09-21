from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from authors.forms import LoginForm, RegisterForm
from recipes.models import Recipe


def register(request):
    register_form_data = request.session.get('register_form_data', None)

    form = RegisterForm(register_form_data)

    return render(
        request,
        'authors/pages/register.html',
        {'form': form, 'form_action': reverse('authors:register_create')},
    )


def register_create(request):
    if not request.POST:
        raise Http404

    POST = request.POST
    request.session['register_form_data'] = POST

    form = RegisterForm(POST)

    if form.is_valid():
        # Save the form data to the memory cache
        user = form.save(commit=False)

        user.set_password(user.password)

        # Save the form data to the database
        user.save()

        messages.success(request, 'User created successfully. Please log in.')

        del request.session['register_form_data']
        return redirect(reverse('authors:login'))

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()

    return render(
        request,
        'authors/pages/login.html',
        {'form': form, 'form_action': reverse('authors:login_create')},
    )


def login_create(request):
    if not request.POST:
        raise Http404

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated:
            messages.success(request, 'Logged.')
            login(request, authenticated)
        else:
            messages.error(request, 'Invalid credentials')
            # Redirect the user to the dashboard
    else:
        messages.error(request, 'Error: Invalid form')

    return redirect(reverse('authors:dashboard'))


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request) -> None:
    if not request.POST:
        messages.error(request, 'Invalid logout request.')
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user.')
        return redirect(reverse('authors:login'))

    logout(request)

    messages.error(request, 'Logout success.')

    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request) -> None:
    recipes = Recipe.objects.filter(is_published=False, author=request.user)

    return render(
        request,
        'authors/pages/dashboard.html',
        context={
            'recipes': recipes,
        },
    )


# @login_required(login_url='authors:login', redirect_field_name='next')
# def dashboard_recipe_edit(request, id) -> None:
#    recipe = Recipe.objects.filter(
#        pk=id,
#        is_published=False,
#        author=request.user,
#    ).first()

#    if not recipe:
#        raise Http404

#    form = AuthorsRecipeForm(
#        request.POST or None, files=request.FILES or None, instance=recipe
#    )

#    if form.is_valid():
#        recipe = form.save(commit=False)

#        recipe.author = request.user
#        recipe.is_published = False
#        recipe.preparation_steps_is_html = False

#        recipe.save()

#        messages.success(request, 'Recipe updated successfully.')

#        return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))

#    return render(
#        request,
#        'authors/pages/dashboard_recipe.html',
#        context={
#            'form': form,
#        },
#    )


# @login_required(login_url='authors:login', redirect_field_name='next')
# def dashboard_recipe_create(request):
#    form = AuthorsRecipeForm(request.POST or None, files=request.FILES or None)
#    if form.is_valid():
#        recipe: Recipe = form.save(commit=False)
#        recipe.author = request.user
#        recipe.is_published = False
#        recipe.preparation_steps_is_html = False
#        if is_number(recipe.preparation_time):
#            recipe.preparation_time = int(form.data['preparation_time'])
#        if is_number(recipe.servings):
#            recipe.servings = int(form.data['servings'])
#        recipe.save()
#        messages.success(request, 'Recipe created successfully.')
#        return redirect(
#            reverse('authors:dashboard_recipe_edit', args=(recipe.id,))
#        )
#    return render(
#        request,
#        'authors/pages/dashboard_recipe.html',
#        context={
#            'form': form,
#            'form_action': reverse('authors:dashboard_recipe_create'),
#        },
#    )


# @login_required(login_url='authors:login', redirect_field_name='next')
# def dashboard_recipe_delete(request) -> None:
#    if not request.POST:
#        raise Http404

#    POST = request.POST
#    id = POST.get('id')

#    recipe = Recipe.objects.filter(
#        pk=id,
#        is_published=False,
#        author=request.user,
#    ).first()

#    if not recipe:
#        raise Http404

#    recipe.delete()

#    messages.success(request, 'Recipe was deleted successfully.')

#    return redirect(reverse('authors:dashboard'))
