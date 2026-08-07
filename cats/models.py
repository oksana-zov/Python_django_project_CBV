from django.db import models
from django.conf import settings

NULLABLE = {'blank': True, 'null': True}

class Breed(models.Model):
    name = models.CharField(max_length=100, verbose_name='Порода')
    description = models.CharField(max_length=1000, verbose_name='Описание', **NULLABLE)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Порода'
        verbose_name_plural = 'Породы'


class Cat(models.Model):
    name = models.CharField(max_length=250, verbose_name='Кличка')
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, verbose_name='Порода')
    photo = models.ImageField(upload_to='cats/', **NULLABLE, verbose_name='Фото')
    birth_date = models.DateField(**NULLABLE, verbose_name='Дата рождения')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Ссылка на кастомную модель User
        on_delete=models.SET_NULL,  # При удалении пользователя кошка НЕ удаляется, хозяин становится NULL
        null=True,  # Разрешаем NULL в базе данных
        blank=True,  # Разрешаем пустое значение при валидации форм
        verbose_name='Хозяин'
    )

    def __str__(self):
        return f'{self.name} ({self.breed})'

    class Meta:
        verbose_name = 'Кошка'
        verbose_name_plural = 'Кошки'