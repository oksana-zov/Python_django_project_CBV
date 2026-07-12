from django.urls import path
from cats.views import index, breeds_list, breeds_cats_list, cats_list_view
from cats.apps import CatsConfig

app_name = CatsConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('breeds/', breeds_list, name='breeds'),
    path('breeds/<int:pk>/cats/', breeds_cats_list, name='breeds_cats'), # <-- Изменили URL
    path('cats/', cats_list_view, name='cats_list'),
]