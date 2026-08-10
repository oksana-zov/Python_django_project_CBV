from django.urls import path
from cats.views import (
    IndexView, BreedsListView, BreedCatsListView, CatsListView,
    CatDetailView, CatCreateView, CatUpdateView, CatDeleteView,
    PedigreeView
)
from cats.apps import CatsConfig

app_name = CatsConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'), # Главная страница (список пород)
    path('breeds/', BreedsListView.as_view(), name='breeds'),# Список всех пород
    path('breeds/<int:pk>/cats/', BreedCatsListView.as_view(), name='breeds_cats'),# Кошки конкретной породы
    path('cats/', CatsListView.as_view(), name='cats_list'),# Общий список кошек
    path('cats/<int:pk>/pedigree/', PedigreeView.as_view(), name='cat_pedigree'),# Родословная
    path('cats/<int:pk>/', CatDetailView.as_view(), name='cat_detail'),# Детальная страница кошки
    path('cats/create/', CatCreateView.as_view(), name='cat_create'),# Создание кошки
    path('cats/<int:pk>/update/', CatUpdateView.as_view(), name='cat_update'),# Редактирование кошки
    path('cats/<int:pk>/delete/', CatDeleteView.as_view(), name='cat_delete'),# Удаление кошки
]