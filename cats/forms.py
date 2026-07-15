from django import forms
from cats.models import Cat

class CatForm(forms.ModelForm):
    class Meta:
        model = Cat
        fields = '__all__'  # Берет все поля из модели Cat (name, breed, photo, birth_date)
