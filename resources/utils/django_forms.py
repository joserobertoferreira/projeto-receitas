# from django.core.exceptions import ValidationError


def add_attribute(field, attr_name, attr_value):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_value}'.strip()


def add_placeholder(field, value):
    add_attribute(field, 'placeholder', value)
