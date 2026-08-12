from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    slug = forms.SlugField(max_length=20, initial='temp_slug', widget=forms.HiddenInput())

    class Meta:
        model = Review
        fields = ('cat', 'title', 'content', 'slug')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }
