# membuat form
from django import forms

from .models_setFitur import SetFitur as SetFiturModel


class SetFiturForm(forms.ModelForm):
    error_css_class = 'error'

    class Meta:
        model = SetFiturModel
        fields = (
            'dataset',
            'all_fitur',
            'fitur',
        )

        labels = {
            'all_fitur': 'Gunakan Semua Fitur',
        }

        widgets = {
            'dataset': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'all_fitur': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'fitur': forms.SelectMultiple(
                attrs={
                    'class': 'form-control',
                }
            ),
        }
