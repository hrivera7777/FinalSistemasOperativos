from django import forms
from .models import ArchivosCh


class ArchivoForm(forms.ModelForm):
    class Meta:
        model = ArchivosCh
        fields = ['archivo']