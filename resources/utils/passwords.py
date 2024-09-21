import re

from django.core.exceptions import ValidationError


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(
            (
                'Password is not strong enough'
                # 'Password must have at least one uppercase letter,'
                # ' and at least one lowercase letter'
            ),
            code='invalid',
        )
