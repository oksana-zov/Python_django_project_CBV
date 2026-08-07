from django.urls import path
from users.views import (
    user_register_view,
    user_login_view,
    user_profile_view,
    user_update_view,
    user_logout_view,
    user_change_password_view,
    user_generate_new_password_view
)

app_name = 'users'

urlpatterns = [
    path('', user_login_view, name='user_login'),
    path('register/', user_register_view, name='user_register'),
    path('profile/', user_profile_view, name='user_profile'),
    path('update/', user_update_view, name='user_update'),
    path('logout/', user_logout_view, name='user_logout'),
    path('change_password/', user_change_password_view, name='user_change_password'),
    path('generate-password/', user_generate_new_password_view, name='user_generate_password'),
]