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
            'delete_fitur_with_null_val',
        )

        labels = {
            'all_fitur': 'Gunakan Semua Fitur',
            'delete_fitur_with_null_val': 'Hapus semua fitur yang memiliki nilai NULL',
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
            'delete_fitur_with_null_val': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
        }
