import random
import io
from pylab import savefig
from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.http import JsonResponse

from .models_dataset import Dataset as DatasetModel
from .models_setLabel import SetLabel as SetLabelModel
from .models_setFitur import SetFitur as SetFiturModel
from .models_hyperparameterRF import HyperparameterRF as HyperparameterRFModel
from .models_randomForest import RandomForest as RandomForestModel
from .forms_dataset import DatasetForm
from . import views

from sklearn.decomposition import PCA
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpld3
import json

import seaborn as sns
sns.set()

def eksploreData(request):
    template_name = "random_forest/eda/eksplore_data.html"
    context = {
        'page_judul': 'Eksplorasi Dataset',
        'page_deskripsi': 'untuk memperoleh pengetahuan awal mengenai data',
        'page_role': 'Dataset'

    }
    context['count_validate_label'] = 0

    count_default_dataset = DatasetModel.objects.filter(
        default_dataset=True).count()

    if count_default_dataset == 1:
        get_dataset = DatasetModel.objects.get(
            default_dataset=True)
        # count_validate_label = SetLabelModel.objects.filter(
        #     dataset_id=get_dataset.id).filter(
        #     validate_label=True).count()
        # if count_validate_label == 1:

        df = views.dataframe(get_dataset.file_dataset, get_dataset.separator)

        null = []
        for i in list(df.columns[:]):
            if df[i].isnull().sum() > 0 :
                null.append([i,df[i].isnull().sum()])
        df_null = pd.DataFrame(data=null,columns=['fitur','count_null'])

        context['df_null'] = df_null.to_html(
            classes='dataframe-style table')
        context['df_null_count'] = df_null.shape[0]
        context['df_head'] = df.head(10).to_html(
            classes='dataframe-style table')
        context['df_tail'] = df.tail(10).to_html(
            classes='dataframe-style table')
        context['df_describe'] = df.describe().to_html(
            classes='dataframe-style table')
        context['df_info'] = df.info()
        context['df_shape'] = df.shape

        context['dataset'] = get_dataset

            # context['count_validate_label'] = count_validate_label

    return render(request,template_name, context)


def plot(request,list_fitur):
    template_name = "random_forest/eda/plot.html"
    context = {
        'page_judul': 'Eksploratory Data Analysis',
        'page_deskripsi': 'untuk memperoleh pengetahuan awal mengenai data',
        'page_role': 'Dataset'

    }
    context['count_validate_label'] = 0

    count_default_dataset = DatasetModel.objects.filter(
        default_dataset=True).count()

    if count_default_dataset == 1:
        get_dataset = DatasetModel.objects.get(
            default_dataset=True)
        count_validate_label = SetLabelModel.objects.filter(
            dataset_id=get_dataset.id).filter(
            validate_label=True).count()
        if count_validate_label == 1:
            get_label = SetLabelModel.objects.filter(
                dataset_id=get_dataset.id).filter(
                validate_label=True).first()
            df = views.dataframe(get_dataset.file_dataset, get_dataset.separator)
            # df = df.fillna(value=0)

            X = df.drop([get_label.kolom_label], axis=1)
            for m in X.columns:
                if df[m].dtype == 'object':
                    df = df.drop(m, axis=1)

            X = df.drop([get_label.kolom_label], axis=1)
            y = df[get_label.kolom_label]

            context['dataset'] = get_dataset
            context['fiturs'] = list(X.columns)

            context['count_validate_label'] = count_validate_label

            if list_fitur == 'default':
                # for i in list(df.columns[:]):
                #     if df[i].dtypes == 'O' :
                #         df = df.drop(i, axis=1)

                if df.shape[1] >= 5:
                    random = np.random.choice(df.columns, 5, replace=False)
                else:
                    random = np.random.choice(df.columns, df.shape[1], replace=False)
                kolom = list(random)
            else:
                fitur = list_fitur
                fitur = fitur.replace('[', '')
                fitur = fitur.replace(']', '')
                fitur = fitur.replace(' ', '')
                fitur = fitur.replace("'", '')
                fitur = fitur.split(",")
                kolom = fitur
                print(kolom)

            plt.figure(999,figsize=(15, len(kolom)), dpi=100)
            plt.title("Swarm-Box-Plot")
            # plt.grid(color='b', linestyle='-', linewidth=0.2)
            plot = sns.boxplot(data=df[kolom], orient="h", palette="Set2")
            plot = sns.swarmplot(data=df[kolom], orient="h")
            print(kolom)
            figure = plot.get_figure() 
            figure.savefig("random_forest/static/random_forest/plot/swarm-box-plot.png")

            # nilai_label = y.unique()
            # validate_kolom = []
            # for i,m in enumerate(kolom) :
            #     validate_index = {}
            #     validate = 0
            #     try :
            #         plt.figure(i,figsize=(5, 3), dpi=80)
            #         plt.title("Kernel Density Plot - fitur {}".format(m))
            #         # plt.grid(color='b', linestyle='-', linewidth=0.2)
            #         plot2 = sns.kdeplot(df[m][df[get_label.kolom_label]==nilai_label[0]], shade=True, color="r")
            #         plot2 = sns.kdeplot(df[m][df[get_label.kolom_label]==nilai_label[1]], shade=True, color="b")
            #         plt.legend((nilai_label[0],nilai_label[1]),loc='upper right')

            #         figure = plot2.get_figure()
            #         nama_file = 'random_forest/static/random_forest/plot/kde-plot-999.png'
            #         nama_file = nama_file.replace('999',str(i))
            #         figure.savefig(nama_file)
            #         validate = 1
            #     except Exception as e:
            #         pass
            #     validate_index['validate'] = validate
            #     validate_index['index'] = i
            #     validate_index['fitur'] = m

                # validate_kolom.append(validate_index)


            # context['validate_kolom'] = validate_kolom
            # context['count_kolom'] = list(range(len(kolom)))
            # context['kolom'] = kolom

    # context['url_plot'] = "/ML/eda/plot/"+str(get_dataset.id)+"/boxplot/"+str(list_fitur)

            
    return render(request,template_name, context)

def get_boxplot(request, pk,list_fitur):
    get_dataset = DatasetModel.objects.get(pk=pk)
    df = views.dataframe(get_dataset.file_dataset, get_dataset.separator)
    # X = df.drop([get_label.kolom_label], axis=1)
    if list_fitur == 'default':
        # for i in list(df.columns[:]):
        #     if df[i].dtypes == 'O' :
        #         df = df.drop(i, axis=1)

        if df.shape[1] >= 5:
            random = np.random.choice(df.columns, 5, replace=False)
        else:
            random = np.random.choice(df.columns, df.shape[1], replace=False)
        kolom = list(random)
    else:
        fitur = list_fitur
        fitur = fitur.replace('[', '')
        fitur = fitur.replace(']', '')
        fitur = fitur.replace(' ', '')
        fitur = fitur.replace("'", '')
        fitur = fitur.split(",")
        kolom = fitur

    df1 = df[kolom].transpose()
    fig, axes = plt.subplots(1, 1, figsize=(12, 4))
    bplot=axes.boxplot(df1,labels=kolom ,vert=False)
    # bplot=df.boxplot(column=kolom ,vert=False, notch=True, patch_artist=True)

    axes.set_title('Box-Plot', fontsize=14)

    html_fig = mpld3.fig_to_html(fig)

    return HttpResponse(html_fig)

    
def pca(request):

    template_name = "random_forest/eda/pca.html"
    context = {
        'page_judul': 'Eksploratory Data Analysis',
        'page_deskripsi': 'untuk memperoleh pengetahuan awal mengenai data',
        'page_role': 'Dataset'

    }
    context['count_validate_label'] = 0

    count_default_dataset = DatasetModel.objects.filter(
        default_dataset=True).count()

    if count_default_dataset == 1:
        get_dataset = DatasetModel.objects.get(
            default_dataset=True)
        count_validate_label = SetLabelModel.objects.filter(
            dataset_id=get_dataset.id).filter(
            validate_label=True).count()
        if count_validate_label == 1:
            get_label = SetLabelModel.objects.filter(
                dataset_id=get_dataset.id).filter(
                validate_label=True).first()
            df = views.dataframe(get_dataset.file_dataset, get_dataset.separator)

          # cleaning----------------------------------------------------
            if df[get_label.kolom_label].dtype == 'object':
                df[get_label.kolom_label] = np.where(df.Class == str(get_label.nilai_label_kanker), 1, 0)
                
            df = df.fillna(value=0)

            X = df.drop([get_label.kolom_label], axis=1)
            for m in X.columns:
                if df[m].dtype == 'object':
                    df = df.drop(m, axis=1)

            # for m in df.columns:
            #     df[m].fillna(df.groupby("Class")[m].transform("median"), inplace=True)

            y = df[get_label.kolom_label]
            X = df.drop([get_label.kolom_label], axis=1)

            # for m in X.columns:
            #     if(X[m].isnull().sum() > 0):
            #         X = X.drop(m, axis=1)

          # create PCA----------------------------------------------------
            target_names = y.unique()
            pca = PCA(n_components=2)
            X_r = pca.fit(X).transform(X)

            plt.figure(figsize=(10, 5))
            colors = ['navy', 'turquoise', 'darkorange']
            lw = 2

            for color, i, target_name in zip(colors, [0, 1, 2], target_names):
                plot = plt.scatter(X_r[y == i, 0], X_r[y == i, 1], color=color, alpha=.8, lw=lw,
                            label=target_name)
            plt.legend(loc='best', shadow=False, scatterpoints=1)
            plt.title('PCA')
            # plt.grid(color='b', linestyle='-', linewidth=0.2)

            figure = plot.get_figure() 
            figure.savefig("random_forest/static/random_forest/pca/pca.png")


            context['dataset'] = get_dataset
            context['fiturs'] = list(X.columns)

            context['count_validate_label'] = count_validate_label

    return render(request,template_name, context)

