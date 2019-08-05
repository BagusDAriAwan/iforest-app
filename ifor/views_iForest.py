import random
import io
from pylab import savefig

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse

from .models_dataset import Dataset as DatasetModel
from .models_setLabel import SetLabel as SetLabelModel
from .models_setFitur import SetFitur as SetFiturModel
from .models_hyperparameter import Hyperparameter as HyperparameterModel
from .models_iForest import IsolationForest as IForestModel
from .forms_iForest import IForestForm
from . import views
from . import views_if_model

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpld3
import json
# from IPython.display import Image  
from sklearn.externals.six import StringIO
from sklearn import tree  
import pydotplus
import pickle
import seaborn as sns
sns.set()


class IForestListView(ListView):
    model = IForestModel
    ordering = ['id']
    template_name = "ifor/iForest/index.html"
    context_object_name = 'iforests'


    extra_context = {
        'page_judul': 'Tabel Perhitungan',
        'page_deskripsi': 'mengelola Perhitungan Isolation Forest berdasarkan dataset default',
        'page_role': 'Perhitungan',
    }

    def get_queryset(self):
        count_default_dataset = DatasetModel.objects.filter(
            default_dataset=True).count()
        count_default_hyperparameter = HyperparameterModel.objects.filter(
            default_hyperparameter=True).count()
        queryset = IForestModel()
        if count_default_dataset == 1:
            default_dataset = DatasetModel.objects.get(
                default_dataset=True)
            queryset = IForestModel.objects.filter(
                dataset_id=default_dataset.id)
        return queryset

    def get_context_data(self, *args, **kwargs):
        count_default_dataset = DatasetModel.objects.filter(
            default_dataset=True).count()
        count_default_hyperparameter = HyperparameterModel.objects.filter(
            default_hyperparameter=True).count()

        kwargs.update(self.extra_context)
        context = super(IForestListView,
                        self).get_context_data(*args, **kwargs)


        # if count_default_dataset == 1 and count_default_hyperparameter == 1:
        #     default_dataset = DatasetModel.objects.get(
        #         default_dataset=True)

        context['set_hyperparameter'] = count_default_hyperparameter
        return context


class IForestCreateView(SuccessMessageMixin, CreateView):
    # model = RandomForestModel
    form_class = IForestForm
    template_name = "ifor/iForest/create.html"
    success_url = reverse_lazy('if:iforest-index')
    context_object_name = 'forms'

    extra_context = {
        'page_judul': 'Tambah Perhitungan',
        'page_deskripsi': 'untuk menambah data Perhitungan Isolation Forest',
        'page_role': 'Perhitungan',
    }

    

    def get_context_data(self, *args, **kwargs):
        count_default_dataset = DatasetModel.objects.filter(
            default_dataset=True).count()
        count_default_hyperparameter = HyperparameterModel.objects.filter(
            default_hyperparameter=True).count()

        kwargs.update(self.extra_context)
        context = super(IForestCreateView,
                        self).get_context_data(*args, **kwargs)

        if count_default_dataset == 1:
            get_dataset = DatasetModel.objects.get(
                default_dataset=True)
            get_label = SetLabelModel.objects.filter(
                validate_label=True).filter(
                dataset_id=get_dataset.id).first()
            get_fitur = SetFiturModel.objects.filter(
                default_fitur=True).filter(
                dataset_id=get_dataset.id).first()
            get_hyperparameter = HyperparameterModel.objects.get(
                default_hyperparameter=True)
            
            df = views.dataframe(
                get_dataset.file_dataset, get_dataset.separator)

            # X, y = views_rf_model.get_x_y(df, get_label, get_fitur)
            
            context['get_dataset'] = get_dataset
            context['get_label'] = get_label
            context['train_rasio'] = [40,50,60,70,80] 
            context['get_fitur'] = get_fitur
            context['get_hyperparameter'] = get_hyperparameter
            # context['count_row_x'] = df.shape[0]

        return context

    def post(self, request, **kwargs):
        dataset_id = request.POST.get('dataset')
        setlabel_id = request.POST.get('setlabel')
        train_id = request.POST.get('setTrain')
        train = int(train_id)
        val_id = int((100 - train)/2)
        test_id = int((100 - train)/2)
        setfitur_id = request.POST.get('setfitur')
        hyperparameter_id = request.POST.get('hyperparameter')
        # hyperparameter_id = request.POST.get('hyperparameter')
        # k_cv = request.POST.get('k_cv')

        # print('dt_id', dataset_id)
        # print('sl_id', setlabel_id)
        # print('st_id', setfitur_id)
        # print('hp_id', hyperparameter_id)

        get_dataset = DatasetModel.objects.get(
            pk=dataset_id)
        get_label = SetLabelModel.objects.get(
            pk=setlabel_id)
        get_fitur = SetFiturModel.objects.get(
            pk=setfitur_id)
        get_hyperparameter = HyperparameterModel.objects.get(
            pk=hyperparameter_id)

        get_label.use_if = True
        get_label.save()
        get_fitur.use_if = True
        get_fitur.save()
        get_hyperparameter.use_if = True
        get_hyperparameter.save()


        ifo = IForestModel()
        ifo.dataset_id = dataset_id
        ifo.setlabel_id = setlabel_id
        ifo.setTrain = train_id
        ifo.setVal = str(val_id)
        ifo.setTest = str(test_id)
        ifo.setfitur_id = setfitur_id
        ifo.hyperparameter_id = hyperparameter_id
        # ifo.k_cv = k_cv
        ifo.save()

        views_if_model.isolationForest(ifo.id)

        file_result = 'iForest/result/coba.csv'
        # file_fitur_importance = 'randomForest/fiturImportance/coba.csv'
        file_model = 'iForest/model/coba.pkl'

        file_cmval = 'iforest/cm/val/coba.png'
        file_cmtest = 'iforest/cm/test/coba.png'

        file_result = file_result.replace('coba',str(ifo.id))
        # file_fitur_importance = file_fitur_importance.replace('coba',str(rf.id))
        file_model = file_model.replace('coba',str(ifo.id))

        file_cmval = file_cmval.replace('coba',str(ifo.id))
        file_cmtest = file_cmtest.replace('coba',str(ifo.id))

        ifo.if_result = file_result
        # rf.rf_fitur_importance = file_fitur_importance
        ifo.if_model = file_model
        ifo.if_cmval = file_cmval
        ifo.if_cmtest = file_cmtest


        ifo.save()

        # success_url = self.get_success_url()
        return HttpResponseRedirect(reverse_lazy('if:iforest-index'))

        # return super(RandomForestCreateView,
                    #  self).post(request, **kwargs)

    def get_success_message(self, cleaned_data):
        return 'Perhitungan Isolation Forest berhasil'


class IForestDeleteView(DeleteView):
    model = IForestModel
    # template_name = "random_forest/randomForest/create.html"
    success_url = reverse_lazy('if:iforest-index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        count_label = IForestModel.objects.filter(
            setlabel_id=self.object.setlabel_id).count()
        if count_label == 1:
            get_label = SetLabelModel.objects.get(
                pk=self.object.setlabel_id)
            get_label.use_if = False
            get_label.save()
            # print('label')

        count_fitur = IForestModel.objects.filter(
            setfitur_id=self.object.setfitur_id).count()
        if count_fitur == 1:
            get_fitur = SetFiturModel.objects.get(
                pk=self.object.setfitur_id)
            get_fitur.use_if = False
            get_fitur.save()
        #     # print('fitur')

        count_hyperparameter = IForestModel.objects.filter(
            hyperparameter_id=self.object.hyperparameter_id).count()
        if count_hyperparameter == 1:
            get_hyperparameter = HyperparameterModel.objects.get(
                pk=self.object.hyperparameter_id)
            get_hyperparameter.use_if = False
            get_hyperparameter.save()
            # print('hyperparameter')

        self.object.delete()
        return HttpResponseRedirect(success_url)



class IForestDetailView(DetailView):
    model = IForestModel
    template_name = "ifor/iForest/detail.html"
    context_object_name = 'iforest'

    extra_context = {
        'page_judul': 'Detail Perhitungan',
        'page_deskripsi': 'untuk melihat detail data Perhitungan Isolation Forest',
        'page_role': 'Perhitungan'
    }

    def get_context_data(self, *args, **kwargs):
        ifo = IForestModel.objects.get(
            pk=self.kwargs.get('pk'))


        kwargs.update(self.extra_context)
        context = super(IForestDetailView,
                        self).get_context_data(*args, **kwargs)


        # get_dataset = rf.dataset
        get_label = ifo.setlabel
        get_fitur = ifo.setfitur
        dataset = ifo.dataset

        df = views.dataframe(dataset.file_dataset, dataset.separator)
        # df = views.dataframe(
        #     get_dataset.file_dataset, get_dataset.separator)

        context['dataset_shape'] = df.shape
        context['label_label'] = list(df[ifo.setlabel.kolom_label].unique())
        context['label_frekuensi'] = list(df[ifo.setlabel.kolom_label].value_counts())
        context['cm_val'] = str(ifo.if_cmval)
        context['cm_test'] = str(ifo.if_cmtest)
        # print('static/'+str(ifo.if_cmtest))
        # context['count_x_before'] = int(df.shape[1]) -  1
        # context['count_x_delete'] = int(df.shape[1]) - (int(get_fitur.count_after_preparation) + 1)
        # context['count_x_after'] = int(get_fitur.count_after_preparation)

        if get_fitur.all_fitur == 0:
            # set fitur dan label
            fitur = get_fitur.fitur
            fitur = fitur.replace('[', '')
            fitur = fitur.replace(']', '')
            fitur = fitur.replace(' ', '')
            fitur = fitur.replace("'", '')
            fitur = fitur.split(',')
            if fitur[0] == '':
                fitur.remove('')
        #     context['count_x_before'] = len(fitur)
        #     context['count_x_delete'] = len(fitur) - int(get_fitur.count_after_preparation)


        df_result = views.dataframe(ifo.if_result,'koma')
        # df_result.insert(loc=0, column='No', value=list(range(1,df_result.shape[0]+1)))
        # df_result = df_result.set_index('No')
        # df_result = df_result.append(df_result.describe()[1:2])
        context['df_result'] = df_result.to_html(
             classes='dataframe-style table')

        # df_FI = views.dataframe(rf.rf_fitur_importance,'koma')
        # df_FI.insert(loc=0, column='No', value=list(range(1,df_FI.shape[0]+1)))
        # df_FI = df_FI.set_index('No')
        # del df_FI.index.name
        # context['df_FI'] = df_FI.to_html(
        #      classes='dataframe-style table')
        return context

def get_result(request, pk):
    ifo = IForestModel.objects.get(pk=pk)
    df = views.dataframe(ifo.if_result,'koma')
    # df = df.set_index('No')
    # df = df.append(df.describe()[1:2])
    data = df.to_html(
        classes='table table-striped text-center')
    return JsonResponse(data, safe=False)

# def get_fitur_importance(request, pk):
#     rf = RandomForestModel.objects.get(pk=pk)
#     df = views.dataframe(rf.rf_fitur_importance,'koma')
#     df.insert(loc=0, column='No', value=list(range(1,df.shape[0]+1)))
#     df = df.set_index('No')
#     del df.index.name
#     data = df.to_html(
#         classes='table table-striped text-center')
#     return JsonResponse(data, safe=False)

# def get_pohon(request, pk,no_pohon):
#     get_rf = RandomForestModel.objects.get(
#         pk=pk)
#     context = {
#         'page_judul': 'Melihat Hasil Pohon',
#         'page_deskripsi': 'untuk melihat hasil pohon pada Random Forest',
#         'page_role': 'Perhitungan RF',
#         'no_pohon' : no_pohon,
#         'randomforest': get_rf,
#         'n_pohon' : list(range(int(get_rf.hyperparameter.n_tree)))
#     }

#     get_dataset = get_rf.dataset
#     get_label = get_rf.setlabel
#     # get_fitur = get_rf.setfitur
#     df = views.dataframe(get_dataset.file_dataset, get_dataset.separator)

#     X,y = views_rf_model.get_x_y(df,get_label)
#     # print(str(get_rf.rf_model))
#     # from pathlib import Path
#     file_model = "media/"+str(get_rf.rf_model)
#     RFFile = open(file_model,"rb")
#     clf_rf = pickle.load(RFFile)

#     dot_data = StringIO()  
#     tree.export_graphviz(clf_rf.estimators_[no_pohon], out_file=dot_data,  
#                                 feature_names=X.columns)  
#     graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
#     # Image(graph.create_png()) 
#     graph.write_pdf("random_forest/static/random_forest/tree/tree.pdf")
#     RFFile.close()

#     return render(request, 'random_forest/randomForest/detail_tree.html', context)
def set_default(request, pk):
    if request.method == 'POST':
        setmodel = IForestModel.objects.get(pk=pk)
        all_set_model = IForestModel.objects.all()
        all_set_model.update(default=False)
        setmodel.default = True
        setmodel.save()

        return JsonResponse('success', safe=False)