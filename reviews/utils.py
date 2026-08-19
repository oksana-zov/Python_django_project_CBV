import string
import random


def generate_slug():
    """Генерирует случайную строку из 20 букв и цифр"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))
