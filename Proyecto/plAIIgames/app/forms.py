from django import forms
from app.models import Library, Game


class LibraryForm(forms.ModelForm):

    class Meta:
        model = Library

        fields = ['title', 'description', 'user']
        labels = {
            'title': 'Título',
            'description': 'Descripción',
            'user': 'User'}

        widgets = {
            'title': forms.TextInput(),
            'description': forms.Textarea(),
            'user': forms.HiddenInput()
        }
