from django.conf import settings
from django.core.mail import send_mail


def send_register_email(email):
    send_mail('Регистрация', 'Вы успешно зарегистрировались', settings.EMAIL_HOST_USER, [email], fail_silently=False)


def send_new_password_email(email, new_password):
    send_mail('Сброс пароля', f'Ваш новый пароль: {new_password}', settings.EMAIL_HOST_USER, [email])


def send_cat_creation(email, cat_obj):
    send_mail('Новый питомец', f'Вы добавили: {cat_obj}', settings.EMAIL_HOST_USER, [email])
