from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validate(value):
    if value > timezone.now().year:
        raise ValidationError(
              ('%(value)s год еще не наступил'),
              params={'value': value},
              )
