from django import forms
from cats.models import Cat, Pedigree
from users.forms import StyleFormMixin
from datetime import datetime

class CatForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Cat
        #fields = '__all__'  # Берет все поля из модели Cat (name, breed, photo, birth_date)
        exclude = ('owner', 'is_active', 'views') # Важно: исключаем владельца, чтобы пользователь не выбирал его сам

    # --- ВАЛИДАЦИЯ Даты рождения ---
    def clean_birth_date(self):
        cleaned_data = self.cleaned_data['birth_date']
        now_year = datetime.now().year
        if now_year - cleaned_data.year > 32:
            raise forms.ValidationError('Кошка должна быть моложе 32 лет')
        return cleaned_data

# Форма для СОЗДАНИЯ (наследуется от основной)
class CatCreateForm(CatForm):
    pass

# Форма для записи родословной
class PedigreeForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Pedigree
        fields = '__all__'

class CatAdminForm(CatForm):
    class Meta(CatForm.Meta):
        # Админу показываем ВСЕ поля, кроме owner (владелец назначается при создании)
        exclude = ('owner',)
