from django.db import models
from django.utils.text import slugify

from .models_dataset import Dataset as DatasetModel
from .models_setLabel import SetLabel as SetLabelModel
from .models_setFitur import SetFitur as SetFiturModel
from .models_hyperparameter import Hyperparameter as HyperparameterModel


class IsolationForest(models.Model):
    dataset = models.ForeignKey(
        DatasetModel, on_delete=models.CASCADE)
    setlabel = models.ForeignKey(
        SetLabelModel, on_delete=models.CASCADE)
    setfitur = models.ForeignKey(
        SetFiturModel, on_delete=models.CASCADE,default=3)
    setTrain = models.IntegerField(default=4)
    setVal = models.IntegerField(default=3)
    setTest = models.IntegerField(default=3)
    default = models.BooleanField(default=False)
    hyperparameter = models.ForeignKey(
        HyperparameterModel, on_delete=models.CASCADE,default=3)
    # k_cv = models.IntegerField(default=5,
    #                         validators=[validate_k_cv])
    if_result = models.FileField(
        upload_to='iForest/result/', default='coba.csv')
    # rf_fitur_importance = models.FileField(
    #     upload_to='ranForest/fiturImportance/', default='coba.csv')
    if_model = models.FileField(
        upload_to='iForest/model/', default='coba.pkl')

    if_cmval = models.FileField(
        upload_to='iforest/cm/val/', default='coba.png')
    if_cmtest = models.FileField(
        upload_to='iforest/cm/test/', default='coba.png')

    tanggal_running = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        self.if_result.delete()
        # self.rf_fitur_importance.delete()
        self.if_model.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return "[{}] 'IF-'{}".format(self.id, str(self.tanggal_running)[1:18])
