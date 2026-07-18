from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm


# РЕГИСТРАЦИЯ
def user_register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return redirect('users:user_login')

    context = {'title': 'Создать аккаунт', 'form': UserRegisterForm()}
    return render(request, 'users/register_update.html', context)


# ВХОД
def user_login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(email=cd['email'], password=cd['password'])

            if user is not None and user.is_active:
                login(request, user)
                return redirect('cats:index')  # Перенаправляем на главную кошек после входа
            else:
                return HttpResponse("Неверный логин/пароль или аккаунт неактивен")

    context = {'title': 'Авторизация', 'form': UserLoginForm()}
    return render(request, 'users/login.html', context)


# ПРОФИЛЬ (Только для авторизованных!)
@login_required
def user_profile_view(request):
    user_object = request.user
    context = {
        'title': f'Ваш профиль {user_object}',
        'object': user_object
    }
    return render(request, 'users/user_profile_read_only.html', context)


# ОБНОВЛЕНИЕ ПРОФИЛЯ (Только для авторизованных!)
@login_required
def user_update_view(request):
    user_object = request.user
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=user_object)
        if form.is_valid():
            form.save()
            return redirect('users:user_profile')

    context = {
        'object': user_object,
        'title': f'Изменить профиль {user_object}',
        'form': UserUpdateForm(instance=user_object)
    }
    return render(request, 'users/register_update.html', context)


# ВЫХОД
def user_logout_view(request):
    logout(request)
    return redirect('cats:index')  # После выхода тоже на главную кошек
