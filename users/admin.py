from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Выводим ID, Фамилию и Имя
    list_display = ('pk', 'last_name', 'first_name','role', 'is_active')
