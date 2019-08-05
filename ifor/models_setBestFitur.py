from django.db import models
from django.utils.text import slugify

from .models_dataset import Dataset as DatasetModel

class SetBestFitur(models.Model):
    # reduksi_null_fitur = models.BooleanField(default=False)
    dataset = models.ForeignKey(
        DatasetModel, on_delete=models.CASCADE)
    jml_fitur = models.CharField(max_length=10, default=10)
    fitur = models.TextField(blank=True, null=True)
    default_fitur = models.BooleanField(default=False)
    use_if = models.BooleanField(default=False)
    # reduksi_nilai_kurang_dari = models.CharField(max_length=255,default=0)

    def __str__(self):
        return "[{}] -> {}".format(self.id, self.fitur)
