from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError

from recipes.models import Recipe
from resources.utils.django_forms import add_attribute
from resources.utils.strings import is_positive_number


class AuthorsRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attribute(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'preparation_time',
            'preparation_time_unit',
            'servings',
            'servings_unit',
            'preparation_steps',
            'cover',
        ]
        widgets = {
            'cover': forms.FileInput(attrs={'class': 'span-2'}),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Unidade', 'Unidade'),
                    ('Pedaço', 'Pedaço'),
                    ('Litros', 'Litros'),
                    ('Fatias', 'Fatias'),
                    ('Pessoas', 'Pessoas'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            ),
        }

    def clean_description(self):
        description = self.cleaned_data.get('description')

        if description is None or len(description) < 20:  # noqa: PLR2004
            self._my_errors['description'].append(
                'Descrição precisa ter no mínimo 20 caracteres',
            )

        return description

    def clean_preparation_time(self):
        preparation_time = self.cleaned_data.get('preparation_time')

        if not is_positive_number(preparation_time):
            self._my_errors['preparation_time'].append(
                'Tempo de preparo precisa ser positivo',
            )

        return preparation_time

    def clean_servings(self):
        servings = self.cleaned_data.get('servings')

        if not is_positive_number(servings):
            self._my_errors['servings'].append(
                'Quantidade de porções precisa ser positivo',
            )

        return servings

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)

        clean_data = self.cleaned_data

        title = clean_data.get('title')

        if title is None or len(title) < 5:  # noqa: PLR2004
            self._my_errors['title'].append(
                'Título precisa ter no mínimo 5 caracteres',
            )

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean
