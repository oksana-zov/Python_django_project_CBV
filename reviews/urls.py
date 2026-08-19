from django.urls import path
from reviews.views import (
    ReviewListView, ReviewDeactivatedListView, ReviewCreateView,
    ReviewDetailView, ReviewUpdateView, ReviewDeleteView, ReviewSearchListView,
    review_toggle_activity)


app_name = 'reviews'


urlpatterns = [
    path('', ReviewListView.as_view(), name='reviews_list'),
    path('deactivated/', ReviewDeactivatedListView.as_view(), name='reviews_deactivated'),
    path('create/', ReviewCreateView.as_view(), name='review_create'),
    path('detail/<slug:slug>/', ReviewDetailView.as_view(), name='review_detail'),
    path('update/<slug:slug>/', ReviewUpdateView.as_view(), name='review_update'),
    path('delete/<slug:slug>/', ReviewDeleteView.as_view(), name='review_delete'),
    path('toggle/<slug:slug>/', review_toggle_activity, name='review_toggle'),
    path('search/', ReviewSearchListView.as_view(), name='reviews_search'),
]
