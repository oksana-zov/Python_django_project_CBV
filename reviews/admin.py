from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'cat', 'author', 'created', 'sign_of_review')
    list_filter = ('sign_of_review', 'cat', 'author')
    ordering = ('-created',)