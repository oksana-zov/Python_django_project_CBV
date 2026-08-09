import re
from django.conf import settings
from django.core.exceptions import ValidationError


def validate_password(field):
    # Получаем текущий язык из настроек
    language = settings.LANGUAGE_CODE

    # Словарь с переводами ошибок
    error_messages = [
        {
            'ru-ru': 'Пароль должен содержать только латинские буквы и цифры',
            'en-us': 'Password must contain A-Z a-z letters and 0-9 numbers'
        },
        {
            'ru-ru': 'Пароль должен содержать от 8 до 16 символов',
            'en-us': 'Password length must be between 8 and 16 characters'
        }
    ]

    # Регулярное выражение: только латиница и цифры
    pattern = re.compile(r'^[A-Za-z0-9]+$')

    # Проверка 1: символы
    if not bool(re.match(pattern, field)):
        message = error_messages[0].get(language, error_messages[0]['en-us'])
        raise ValidationError(message)

    # Проверка 2: длина
    if not 8 <= len(field) <= 16:
        message = error_messages[1].get(language, error_messages[1]['en-us'])
        raise ValidationError(message)
