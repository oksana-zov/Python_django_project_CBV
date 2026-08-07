from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
import string

from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserChangePasswordForm
from users.services import send_register_email, send_new_password_email


# РЕГИСТРАЦИЯ
def user_register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

            # Отправка письма при регистрации
            send_register_email(new_user.email)

            return HttpResponseRedirect(reverse('users:user_login'))

    context = {
        'title': 'Создать аккаунт',
        'form': UserRegisterForm()
    }
    return render(request, 'users/register_update.html', context=context)


# ВХОД
def user_login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(email=cd['email'], password=cd['password'])

            if user is not None and user.is_active:
                login(request, user)
                return redirect('cats:index')
            else:
                return HttpResponse("Неверный логин/пароль или аккаунт неактивен")

    context = {'title': 'Авторизация', 'form': UserLoginForm()}
    return render(request, 'users/login.html', context)


# ПРОФИЛЬ
@login_required
def user_profile_view(request):
    user_object = request.user
    context = {
        'title': f'Ваш профиль {user_object}',
        'object': user_object
    }
    return render(request, 'users/user_profile_read_only.html', context)


# ОБНОВЛЕНИЕ ПРОФИЛЯ
@login_required
def user_update_view(request):
    user_object = request.user
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=user_object)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:user_profile'))

    context = {
        'object': user_object,
        'title': f'Изменить профиль {user_object}',
        'form': UserUpdateForm(instance=user_object)
    }
    return render(request, 'users/register_update.html', context=context)


# СМЕНА ПАРОЛЯ
@login_required
def user_change_password_view(request):
    user_object = request.user
    # Передаем пользователя в форму (обязательно для PasswordChangeForm)
    form = UserChangePasswordForm(user_object, request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user_object = form.save()

            # Обновляем хеш сессии (чтобы не выкинуло из аккаунта)
            update_session_auth_hash(request, user_object)

            messages.success(request, 'Пароль был успешно изменен!')

            # отправка письма
            send_new_password_email(user_object.email, form.cleaned_data['new_password1'])

            return HttpResponseRedirect(reverse('users:user_profile'))
        else:
            messages.error(request, 'Не удалось изменить пароль!')

    context = {
        'form': form,
        'title': f'Изменить пароль {user_object}'
    }
    return render(request, 'users/change_password.html', context)


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


# ВЫХОД
def user_logout_view(request):
    logout(request)
    return redirect('cats:index')
