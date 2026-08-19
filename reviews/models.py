from django.db import models
from django.conf import settings
from cats.models import Cat


class Review(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.SlugField(max_length=25, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(verbose_name='Текст отзыва')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    sign_of_review = models.BooleanField(default=False, verbose_name='Опубликован')  # False = на модерации

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='reviews', verbose_name='Кошка')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('reviews:review_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created']
