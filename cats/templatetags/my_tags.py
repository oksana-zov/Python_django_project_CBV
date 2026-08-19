from django import template


register = template.Library()


@register.filter
def cats_media(value):
    """Возвращает путь к медиа или заглушку, если фото нет"""
    if value:
        return f'/media/{value}'
    return '/static/img/dummy_cat.jpg'  # Убедись, что такая картинка есть в static/img/
