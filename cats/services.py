from django.core.mail import send_mail
from django.conf import settings


def send_views_mail(cat_object, owner_email, views_count):
    """Отправляет письмо владельцу при достижении кратного 20 просмотрам"""
    send_mail(
        subject=f'{views_count} просмотров у кошки {cat_object.name}!',
        message=f'Поздравляем! Карточка вашей кошки "{cat_object.name}" набрала уже {views_count} просмотров.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[owner_email],
        fail_silently=False,
    )
