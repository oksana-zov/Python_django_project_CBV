# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from users.models import User
from users.validators import validate_password


# МИКСИН ДЛЯ СТИЛЕЙ (оставляем твой, он отличный!)
class StyleFormMixin:
    """Автоматически добавляет Bootstrap-класс ко всем полям формы"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


# 1. ФОРМА РЕГИСТРАЦИИ (адаптированная UserCreationForm)
class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

    # Переопределяем поле username на email (так как у нас кастомная модель)
    username = None  # Убираем поле username
    email = forms.EmailField(label='Email', max_length=254)

    def clean_password2(self):
        cd = self.cleaned_data
        password1 = cd.get('password1')
        password2 = cd.get('password2')

        if not password1 or not password2:
            return password2

        validate_password(password1)  # Валидатор
        if password1 != password2:
            raise forms.ValidationError('Пароли не совпадают!')
        return password2


# 2. ФОРМА ВХОДА (адаптированная AuthenticationForm)
class UserLoginForm(StyleFormMixin, AuthenticationForm):
    # Переопределяем поле username на email
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))


# 3. ФОРМА ОБНОВЛЕНИЯ ПРОФИЛЯ
class UserUpdateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'telegram', 'avatar')


# 4. ФОРМА СМЕНЫ ПАРОЛЯ
class UserChangePasswordForm(StyleFormMixin, PasswordChangeForm):
    def clean_new_password2(self):
        cd = self.cleaned_data
        password1 = cd.get('new_password1')
        password2 = cd.get('new_password2')

        if not password1 or not password2:
            return password2

        validate_password(password1)  # валидатор
        if password1 != password2:
            raise forms.ValidationError('Пароли не совпадают!')
        return password2