import random
import io
from pylab import savefig
from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse

from django.http import JsonResponse
from .models_dataset import Dataset as DatasetModel
from .models_setLabel import SetLabel as SetLabelModel
from .models_setFitur import SetFitur as SetFiturModel
from .models_hyperparameter import Hyperparameter as HyperparameterModel
# from .models_randomForest import RandomForest as RandomForestModel
from .forms_hyperparameter import HyperparameterForm

from . import views
# from . import views_if_model

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpld3
import json

import seaborn as sns
sns.set()


class HyperparameterListView(ListView):
    model = HyperparameterModel
    ordering = ['id']
    template_name = "ifor/hyperparameter/index.html"
    context_object_name = 'hyperparameters'

    extra_context = {
        'page_judul': 'Tabel Hiperparameter IForest',
        'page_deskripsi': 'mengelola Table Set Hiperparameter Isolation Forest',
        'page_role': 'Set Hiperparameter IForest',
    }

    # def get_queryset(self):
    #     count_default_dataset = DatasetModel.objects.filter(
    #         default_dataset=True).count()
    #     queryset = HyperparameterRFModel()
    #     if count_default_dataset == 1:
    #         default_dataset = DatasetModel.objects.get(
    #             default_dataset=True)
    #         queryset = HyperparameterRFModel.objects.filter(
    #             dataset_id=default_dataset.id)
    #     return queryset

    def get_context_data(self, *args, **kwargs):
        count_default_dataset = DatasetModel.objects.filter(
            default_dataset=True).count()

        kwargs.update(self.extra_context)
        context = super(HyperparameterListView,
                        self).get_context_data(*args, **kwargs)

        if count_default_dataset == 1:
            default_dataset = DatasetModel.objects.get(
                default_dataset=True)
            count_fitur = SetFiturModel.objects.filter(
                default_fitur=True).filter(dataset_id=default_dataset.id).count()
            if count_fitur == 1:
                get_label = SetLabelModel.objects.filter(
                    validate_label=True).filter(dataset_id=default_dataset.id).first()
                get_fitur = SetFiturModel.objects.filter(
                    default_fitur=True).filter(dataset_id=default_dataset.id).first()
                # df = views.dataframe(
                #     default_dataset.file_dataset, default_dataset.separator)

                # X, y = views_rf_model.get_x_y(df, get_label, get_fitur)

                # context['count_x'] = int(get_fitur.count_after_preparation)
            context['count_fitur'] = count_fitur
        else: 
            context['count_fitur'] = 0

        return context


class HyperparameterCreateView(SuccessMessageMixin, CreateView):
    # model = HyperparameterRFModel
    form_class = HyperparameterForm
    template_name = "ifor/hyperparameter/create.html"
    success_url = reverse_lazy('if:hyperparameter-index')
    context_object_name = 'forms'

    extra_context = {
        'page_judul': 'Tambah Set Hiperparameter IForest',
        'page_deskripsi': 'untuk menambah data Set Hiperparameter IForest',
        'page_role': 'Set Hiperparameter IForest',
    }

    def post(self, request, **kwargs):
        # self.object = self.get_object()

        count_default_dataset = DatasetModel.objects.filter(
            default_dataset=True).count()

        if count_default_dataset == 1:
            default_dataset = DatasetModel.objects.get(
                default_dataset=True)
            count_fitur = SetFiturModel.objects.filter(
                default_fitur=True).filter(dataset_id=default_dataset.id).count()
            if count_fitur == 1:
                get_label = SetLabelModel.objects.filter(
                    validate_label=True).filter(dataset_id=default_dataset.id).first()
                get_fitur = SetFiturModel.objects.filter(
                    default_fitur=True).filter(dataset_id=default_dataset.id).first()
                # df = views.dataframe(
                #     default_dataset.file_dataset, default_dataset.separator)

                # X, y = views_rf_model.get_x_y(df, get_label, get_fitur)

        # mutable = request.POST._mutable
        # request.POST._mutable = True
        # # print(request.POST)

        # try:
        #     if isinstance(int(request.POST.get('max_fitur')), int) == True:
        #         if int(request.POST.get('max_fitur')) > int(get_fitur.count_after_preparation):
        #             request.POST['max_fitur'] = int(get_fitur.count_after_preparation)
        #         # if int(request.POST.get('max_fitur')) > X.shape[1]:
        #         #     request.POST['max_fitur'] = X.shape[1]
        #             # print('cek')
        # except Exception as e:
        #     pass

        # request.POST._mutable = mutable
        return super(HyperparameterCreateView,
                     self).post(request, **kwargs)

    def get_context_data(self, *args, **kwargs):
        count_default_dataset = DatasetModel.objects.filter(
            default_dataset=True).count()

        kwargs.update(self.extra_context)
        context = super(HyperparameterCreateView,
                        self).get_context_data(*args, **kwargs)

        if count_default_dataset == 1:
            default_dataset = DatasetModel.objects.get(
                default_dataset=True)
            count_fitur = SetFiturModel.objects.filter(
                default_fitur=True).filter(dataset_id=default_dataset.id).count()
            if count_fitur == 1:
                get_label = SetLabelModel.objects.filter(
                    validate_label=True).filter(dataset_id=default_dataset.id).first()
                get_fitur = SetFiturModel.objects.filter(
                    default_fitur=True).filter(dataset_id=default_dataset.id).first()
                # df = views.dataframe(
                #     default_dataset.file_dataset, default_dataset.separator)

                # X, y = views_rf_model.get_x_y(df, get_label, get_fitur)

                # context['count_x'] = X.shape[1]
                # context['count_x'] = int(get_fitur.count_after_preparation)
            context['get_dataset'] = default_dataset
        return context

    def get_success_message(self, cleaned_data):
        return 'Set Hiperparameter berhasil ditambahakan'


class HyperparameterUpdateView(SuccessMessageMixin, UpdateView):
    model = HyperparameterModel
    form_class = HyperparameterForm
    template_name = "ifor/hiperparameter/create.html"
    context_object_name = 'forms'
    success_url = reverse_lazy('if:hiperparameter-index')

    extra_context = {
        'page_judul': 'Edit Set Hiperparameter IForest',
        'page_deskripsi': 'untuk memperbarui data Set Hiperparameter IForest',
        'page_role': 'Set Hiperparameter IForest',
    }

    def post(self, request, **kwargs):
        # self.object = self.get_object()

        count_default_dataset = DatasetModel.objects.filter(
            default_dataset=True).count()

        if count_default_dataset == 1:
            default_dataset = DatasetModel.objects.get(
                default_dataset=True)
            count_fitur = SetFiturModel.objects.filter(
                default_fitur=True).filter(dataset_id=default_dataset.id).count()
            if count_fitur == 1:
                get_label = SetLabelModel.objects.filter(
                    validate_label=True).filter(dataset_id=default_dataset.id).first()
                get_fitur = SetFiturModel.objects.filter(
                    default_fitur=True).filter(dataset_id=default_dataset.id).first()
                # df = views.dataframe(
                #     default_dataset.file_dataset, default_dataset.separator)

                # X, y = views_rf_model.get_x_y(df, get_label, get_fitur)

        # mutable = request.POST._mutable
        # request.POST._mutable = True

        # try:
        #     if isinstance(int(request.POST.get('max_fitur')), int) == True:
        #         if int(request.POST.get('max_fitur')) > int(get_fitur.count_after_preparation):
        #             request.POST['max_fitur'] = int(get_fitur.count_after_preparation)
        #         # if int(request.POST.get('max_fitur')) > X.shape[1]:
        #         #     request.POST['max_fitur'] = X.shape[1]
        #             # print('cek')
        # except Exception as e:
        #     pass

        # request.POST._mutable = mutable
        return super(HyperparameterUpdateView,
                     self).post(request, **kwargs)

    def get_context_data(self, *args, **kwargs):
        count_default_dataset = DatasetModel.objects.filter(
            default_dataset=True).count()

        kwargs.update(self.extra_context)
        context = super(HyperparameterUpdateView,
                        self).get_context_data(*args, **kwargs)

        if count_default_dataset == 1:
            default_dataset = DatasetModel.objects.get(
                default_dataset=True)
            count_fitur = SetFiturModel.objects.filter(
                default_fitur=True).filter(dataset_id=default_dataset.id).count()
            if count_fitur == 1:
                get_label = SetLabelModel.objects.filter(
                    validate_label=True).filter(dataset_id=default_dataset.id).first()
                get_fitur = SetFiturModel.objects.filter(
                    default_fitur=True).filter(dataset_id=default_dataset.id).first()
                # df = views.dataframe(
                #     default_dataset.file_dataset, default_dataset.separator)

                # X, y = views_rf_model.get_x_y(df, get_label, get_fitur)

                context['count_x'] = int(get_fitur.count_after_preparation)
            context['get_dataset'] = default_dataset
            
        return context

    def get_success_message(self, cleaned_data):
        return 'Set Hiperparameter berhasil diperbarui'


class HyperparameterDeleteView(DeleteView):
    model = HyperparameterModel
    # template_name = "random_forest/hyperparameterRF/create.html"
    success_url = reverse_lazy('if:hyperparameter-index')


class HyperparameterDetailView(DetailView):
    model = HyperparameterModel
    template_name = "ifor/hyperparameter/detail.html"
    context_object_name = 'hyperparameter'

    extra_context = {
        'page_judul': 'Detail Set Hiperparameter IForest',
        'page_deskripsi': 'untuk melihat detai data Set Hiperparameter IForest',
        'page_role': 'Set Hiperparameter IForest'
    }

    def get_context_data(self, *args, **kwargs):

        kwargs.update(self.extra_context)
        context = super(HyperparameterDetailView, self).get_context_data(
            *args, **kwargs)

        return context


def set_default(request, pk):
    if request.method == 'POST':
        set_hyperparameter = HyperparameterModel.objects.get(pk=pk)

        count_default_dataset = DatasetModel.objects.filter(
            default_dataset=True).count()

        if count_default_dataset == 1:
            default_dataset = DatasetModel.objects.get(
                default_dataset=True)
            count_fitur = SetFiturModel.objects.filter(
                default_fitur=True).filter(dataset_id=default_dataset.id).count()
            if count_fitur == 1:
                get_label = SetLabelModel.objects.filter(
                    validate_label=True).filter(dataset_id=default_dataset.id).first()
                get_fitur = SetFiturModel.objects.filter(
                    default_fitur=True).filter(dataset_id=default_dataset.id).first()
                # df = views.dataframe(
                #     default_dataset.file_dataset, default_dataset.separator)

                # X, y = views_rf_model.get_x_y(df, get_label, get_fitur)

        all_set_hyperparameter = HyperparameterModel.objects.all()
        all_set_hyperparameter.update(default_hyperparameter=False)

        set_hyperparameter.default_hyperparameter = True
        set_hyperparameter.save()

        return JsonResponse('success', safe=False)
