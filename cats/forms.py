from django import forms
from cats.models import Cat
from users.forms import StyleFormMixin
from datetime import datetime

class CatForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Cat
        #fields = '__all__'  # Берет все поля из модели Cat (name, breed, photo, birth_date)
        exclude = ('owner',) # Важно: исключаем владельца, чтобы пользователь не выбирал его сам

    # --- ВАЛИДАЦИЯ Даты рождения ---
    def clean_birth_date(self):
        cleaned_data = self.cleaned_data['birth_date']
        now_year = datetime.now().year
        if now_year - cleaned_data.year > 32:
            raise forms.ValidationError('Кошка должна быть моложе 32 лет')
        return cleaned_data


