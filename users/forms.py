from django import forms
from django.contrib.auth.forms import PasswordChangeForm

from users.models import User
from users.validators import validate_password


# МИКСИН ДЛЯ СТИЛЕЙ
class StyleFormMixin:
    """Автоматически добавляет Bootstrap-класс ко всем полям формы"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


# 1. Форма регистрации
class UserRegisterForm(StyleFormMixin, forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, validators=[validate_password])
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        cd = self.cleaned_data
        # Безопасно получаем значения (не вызовет ошибку, если поля нет)
        password = cd.get('password')
        password2 = cd.get('password2')
        # Если одно из полей пустое (из-за ошибки валидации),
        # просто выходим, чтобы не сравнивать несуществующие данные
        if not password or not password2:
            return password2
        # Проверяем совпадение только если оба пароля существуют
        if password != password2:
            raise forms.ValidationError('Пароли не совпадают!')

        return password2


# 2. Форма входа
class UserLoginForm(StyleFormMixin, forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


# 3. Форма обновления профиля
class UserUpdateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'telegram', 'avatar')


# 4. ФОРМА СМЕНЫ ПАРОЛЯ
class UserChangePasswordForm(StyleFormMixin, PasswordChangeForm):
    pass