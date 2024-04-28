import datetime

from django.core.exceptions import ValidationError

__all__ = []


def birthday_validator(value):
    max_date = datetime.date.today()
    if value > max_date:
        raise ValidationError("введите коректный день рождения")
