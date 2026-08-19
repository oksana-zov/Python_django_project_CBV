from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

NULLABLE = {'blank': True, 'null': True}


class UserRoles(models.TextChoices):
    ADMIN = 'admin', _('Администратор')
    MODERATOR = 'moderator', _('Модератор')
    USER = 'user', _('Пользователь')


class User(AbstractUser):
    username = None  # Отключаем стандартное поле логина

    email = models.EmailField(unique=True, verbose_name='email')
    first_name = models.CharField(max_length=150, verbose_name='first name', default='Anonymous')
    last_name = models.CharField(max_length=150, verbose_name='last name', default='Anonymous')
    avatar = models.ImageField(upload_to='users/', verbose_name='avatar', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='phone number', **NULLABLE)
    telegram = models.CharField(max_length=150, verbose_name='telegram username', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='active')
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.USER, verbose_name='Роль')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email} {self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id']
