from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
# from .models_dataset import Dataset as DatasetModel


class Hyperparameter(models.Model):
    use_if = models.BooleanField(default=False)
    # dataset = models.ForeignKey(
    #     DatasetModel, on_delete=models.CASCADE, default=1)
    default_hyperparameter = models.BooleanField(default=False)
    n_tree = models.IntegerField(default=100)
    sample = models.IntegerField(default=256)
    kontaminasi = models.FloatField(default=0.001,max_length=10)
    # max_fitur = models.CharField(
    #     max_length=10, default='sqrt', validators=[validate_max_fitur])
    # max_kedalaman = models.CharField(max_length=255, default=10)

    def __str__(self):
        # return "[{}] -> n_tree({}) ,max_fitur({}), max_kedalaman({})".format(self.id, self.n_tree, self.max_fitur, self.max_kedalaman)
        return "[{}] -> n_tree({}) ,sample({}),kontaminasi({})".format(self.id, self.n_tree, self.sample, self.kontaminasi)
