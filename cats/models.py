from django.db import models

NULLABLE = {'blank': True, 'null': True}

class Breed(models.Model):
    name = models.CharField(max_length=100, verbose_name='Порода')
    description = models.CharField(max_length=1000, verbose_name='Описание', **NULLABLE)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Порода'
        verbose_name_plural = 'Породы'


class Cat(models.Model):  # <-- Замени Dog на Cat
    name = models.CharField(max_length=250, verbose_name='Кличка')
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, verbose_name='Порода')
    photo = models.ImageField(upload_to='cats/', **NULLABLE, verbose_name='Фото')
    birth_date = models.DateField(**NULLABLE, verbose_name='Дата рождения')

    def __str__(self):
        return f'{self.name} ({self.breed})'

    class Meta:
        verbose_name = 'Кошка'
        verbose_name_plural = 'Кошки'