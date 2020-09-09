from django.core.exceptions import ValidationError


def filename_validator(value):
    if '.' not in value:
        raise ValidationError('У файла нет расширения')
