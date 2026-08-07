import re
from django.core.exceptions import ValidationError


def validate_password(field):
    # Проверка: только латиница и цифры
    pattern = re.compile(r'^[A-Za-z0-9]+$')
    if not bool(re.match(pattern, field)):
        raise ValidationError("Пароль должен содержать только латинские буквы и цифры")

    # Проверка длины (8-16 символов)
    if not 8 <= len(field) <= 16:
        raise ValidationError('Пароль должен содержать от 8 до 16 символов')
