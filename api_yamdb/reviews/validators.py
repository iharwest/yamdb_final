import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    """
    Проверка года выпуска произведения.
    """
    year = dt.datetime.now().year
    if year < value:
        raise ValidationError('Год выпуска произведения'
                              'не может быть больше текущего!')
    return value
