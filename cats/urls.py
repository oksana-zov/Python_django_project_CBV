from django.urls import path
from cats.views import (
    index, breeds_list, breeds_cats_list, cats_list_view,
    cat_detail_view, cat_create_view, cat_update_view, cat_delete_view
)
from cats.apps import CatsConfig

app_name = CatsConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('breeds/', breeds_list, name='breeds'),
    path('breeds/<int:pk>/cats/', breeds_cats_list, name='breeds_cats'),
    path('cats/', cats_list_view, name='cats_list'),
    path('cats/create/', cat_create_view, name='cat_create'),       # Добавить кошку
    path('cats/<int:pk>/', cat_detail_view, name='cat_detail'),     # Детальная страница кошки
    path('cats/<int:pk>/update/', cat_update_view, name='cat_update'), # Редактировать
    path('cats/<int:pk>/delete/', cat_delete_view, name='cat_delete'), # Удалить
]