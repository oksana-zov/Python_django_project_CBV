from django.urls import path
from users.apps import UsersConfig
from users.views import (
    UserRegisterView, UserLoginView, UserProfileView,
    UserLogoutView, UserUpdateView, UserPasswordChangeView,
    user_generate_new_password_view
)

app_name = UsersConfig.name

urlpatterns = [
    path('', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('update/', UserUpdateView.as_view(), name='user_update'),
    path('change_password/', UserPasswordChangeView.as_view(), name='user_change_password'),
    path('generate-password/', user_generate_new_password_view, name='user_generate_password'),
]