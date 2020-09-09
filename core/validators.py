from django.core.exceptions import ValidationError


def account_number_validator(value):
    if not value.strip().isdigit():
        raise ValidationError('Только цифры')

    if len(value) < 16:
        raise ValidationError('Минимум 16 символов')


def isdigit_validator(value):
    if not value.strip().isdigit():
        raise ValidationError('Только цифры')
