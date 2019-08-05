from django.contrib import admin

from .models_dataset import Dataset
from .models_setLabel import SetLabel
from .models_setFitur import SetFitur
from .models_hyperparameter import Hyperparameter
from .models_iForest import IsolationForest

# Register your models here.
admin.site.register([Dataset, SetLabel, SetFitur, Hyperparameter, IsolationForest
	])
