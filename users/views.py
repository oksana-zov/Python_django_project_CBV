from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
import string

from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserChangePasswordForm
from users.services import send_register_email, send_new_password_email

from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin

from users.models import User
from users.forms import (
    UserRegisterForm, UserLoginForm, UserUpdateForm,
    UserChangePasswordForm
)
from users.services import send_register_email


# РЕГИСТРАЦИЯ
class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register_update.html'
    success_url = reverse_lazy('users:user_login')  # <-- reverse_lazy обязательно!

    extra_context = {'title': 'Создать аккаунт'}

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_password(form.cleaned_data['password1'])
        self.object.save()
        send_register_email(self.object.email)
        return super().form_valid(form)


# ВХОД
class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    extra_context = {'title': 'Авторизация'}

    # После входа кидаем на главную кошек
    def get_success_url(self):
        return reverse_lazy('cats:index')


# СПИСОК ВСЕХ ПОЛЬЗОВАТЕЛЕЙ
class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'users_list'
    paginate_by = 3

    def get_queryset(self):
        # Показываем только активных пользователей
        return super().get_queryset().filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все пользователи питомника'
        return context


# ПРОСМОТР ЧУЖОГО ПРОФИЛЯ (Публичный)
class UserPublicProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_profile_read_only.html'  # Используем тот же шаблон
    context_object_name = 'object'  # Важно! Чтобы {{ object.telegram }} работал

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_obj = self.object
        name = user_obj.get_full_name() or user_obj.email
        context['title'] = f'Профиль: {name}'
        return context


# ПРОФИЛЬ (DetailView)
class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_profile_read_only.html'

    def get_object(self, queryset=None):
        return self.request.user  # <-- Показываем текущего юзера, а не по ID

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Профиль {self.object}'
        return context


# РЕДАКТИРОВАНИЕ (UpdateView)
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/register_update.html'
    success_url = reverse_lazy('users:user_profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Изменить профиль: {self.object}'
        return context


# СМЕНА ПАРОЛЯ
class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = UserChangePasswordForm
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('users:user_profile')
    extra_context = {'title': 'Изменить пароль'}


# ВЫХОД
class UserLogoutView(LogoutView):
    template_name = 'users/logout.html'
    extra_context = {'title': 'Выход'}


@login_required
def user_generate_new_password_view(request):
    # Генерируем случайный пароль из 12 символов (буквы + цифры)
    new_password = ''.join(random.sample(string.ascii_letters + string.digits, k=12))
    # Устанавливаем новый пароль пользователю
    request.user.set_password(new_password)
    request.user.save()
    # Обязательно обновляем сессию, иначе пользователя выкинет!
    update_session_auth_hash(request, request.user)
    # Отправляем письмо с новым паролем
    send_new_password_email(request.user.email, new_password)
    messages.success(request, 'Новый пароль сгенерирован и отправлен вам на почту!')
    return redirect(reverse('users:user_profile'))

