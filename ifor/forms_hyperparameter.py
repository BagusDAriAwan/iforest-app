# membuat form
from django import forms

from .models_hyperparameter import Hyperparameter as HyperparameterModel


class HyperparameterForm(forms.ModelForm):
    error_css_class = 'error'

    class Meta:
        model = HyperparameterModel
        fields = (
            # 'dataset',
            'n_tree',
            'sample',
            'kontaminasi',
            # 'max_kedalaman',
        )

        labels = {
            'n_tree': 'Jumlah Pohon dalam Isolation Forest',
            'sample': 'Jumlah Sample',
            # 'max_kedalaman': 'Maksimal Kedalaman Pohon dalam Random Forest',
        }

        widgets = {
            # 'dataset': forms.Select(
            #     attrs={
            #         'class': 'form-control',
            #     }
            # ),
            'n_tree': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 1,
                }
            ),
            'sample': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 1,
                }
            ),
            'kontaminasi': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0,
                    'max': 1,
                    'step': 0.001
                }

            ),
            # 'max_kedalaman': forms.NumberInput(
            #     attrs={
            #         'class': 'form-control',
            #         'placeholder': '50',
            #         'min': 1

            #     }
            # ),
        }
