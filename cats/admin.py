from django.contrib import admin
from cats.models import Breed, Cat


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')  # Показываем ID и название в списке
    ordering = ('pk',)  # Сортируем по ID (новые породы внизу)


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'breed')  # Показываем ID, кличку и породу
    list_filter = ('breed',)  # Добавляем фильтр справа по породам
    ordering = ('name',)  # Сортируем кошек по алфавиту

