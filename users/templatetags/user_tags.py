from django import template


register = template.Library()


@register.filter
def user_media(val):
    if val:
        return f'/media/{val}'
    return '/static/img/noavatar.png'  # Путь к заглушке аватара
