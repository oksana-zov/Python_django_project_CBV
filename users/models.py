from django.db import models
from django.contrib.auth.models import AbstractUser


NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None # Удаляем стандартное поле логина

    # Делаем email уникальным идентификатором
    email = models.EmailField(unique=True, verbose_name='email')

    # Добавляем свои поля (телефон и телеграм)
    phone = models.CharField(max_length=35, verbose_name='phone number', **NULLABLE)
    telegram = models.CharField(max_length=150, verbose_name='telegram username', **NULLABLE)

    # Говорим Django использовать email для входа
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id']