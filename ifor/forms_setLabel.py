# membuat form
from django import forms

from .models_setLabel import SetLabel as SetLabelModel


class SetLabelForm(forms.ModelForm):
    error_css_class = 'error'

    class Meta:
        model = SetLabelModel
        fields = (
            'dataset',
            'kolom_label',
            'nilai_label_fraud',
        )

        labels = {
            'kolom_label': 'Kolom Label/Target',
            'nilai_label_fraud': 'Nilai Label Kelas Fraud',
        }

        widgets = {
            'dataset': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'kolom_label': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': 'required',
                }
            ),
            'nilai_label_fraud': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': 'required',

                }
            ),

        }
