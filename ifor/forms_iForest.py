# membuat form
from django import forms

from .models_iForest import IsolationForest as IForestModel


class IForestForm(forms.ModelForm):
    error_css_class = 'error'

    class Meta:
        model = IForestModel
        fields = (
            'dataset',
            'setlabel',
            'setfitur',
            'hyperparameter',
            'setTrain',
            # 'setVal',
            # 'setTest',

            
            
            # 'k_cv',
            # 'splitdata'
        )

        labels = {
            'setlabel': ' Label(y)',
            'setfitur': 'Fitur(X)',
            'hyperparameter': 'Hyperparameter Isolation Forest',
            'setTrain': ' Train Rasio',
            # 'setVal': ' Validasi Rasio',
            # 'setTest': ' Test Rasio',
            # 'splitdata': ' Split Data'
            # 'setfitur': 'Fitur(X)',
            
            # 'k_cv': 'Nilai " k " dalam K-Fold Cross Validation',
        }

        widgets = {
            'dataset': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'setlabel': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'setfitur': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'hyperparameter': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'setTrain': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            # 'setVal': forms.Select(
            #     attrs={
            #         'class': 'form-control',
            #     }
            # ),
            # 'setTest': forms.Select(
            #     attrs={
            #         'class': 'form-control',
            #     }
            # ),
            # 'splitdata': forms.Select(
            #     attrs={
            #         'class': 'form-control',
            #     }
            # ),
            
        }
