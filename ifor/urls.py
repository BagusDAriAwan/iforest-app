from django.urls import path, include
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic import ListView, DetailView, FormView

from . import views_dataset, views_setLabel
from . import views_setFitur, views_eda
from . import views_iForest, views_hyperparameter

app_name = 'ifor'

urlpatterns = [
    
    # path('random-forest/pohon/<int:pk>/<int:no_pohon>',
    #      views_randomForest.get_pohon, name='random-forest-pohon'),
    # path('random-forest/fitur_importance/<int:pk>',
    #      views_randomForest.get_fitur_importance, name='random-forest-fitur-importance'),
    path('iforest/default/<int:pk>',
         views_iForest.set_default, name='iforest-set-default'),
    path('iforest/result/<int:pk>',
         views_iForest.get_result, name='iforest-result'),
    #     path('random-forest/detail-tree/<int:pk>',
    #          views_randomForest.RandomForestDetailTreeView.as_view(), name='random-forest-detail-tree'),
    path('iforest/detail/<int:pk>',
         views_iForest.IForestDetailView.as_view(), name='iforest-detail'),
    path('iforest/delete/<int:pk>',
         views_iForest.IForestDeleteView.as_view(), name='iforest-delete'),
    path('iforest/create/', views_iForest.IForestCreateView.as_view(),
         name='iforest-create'),
    path('iforest/', views_iForest.IForestListView.as_view(),
         name='iforest-index'),

    # -------------------set hyperparameter
    path('hyperparameter/default/<int:pk>',
         views_hyperparameter.set_default, name='hyperparameter-set-default'),
    path('hyperparameter/detail/<int:pk>',
         views_hyperparameter.HyperparameterDetailView.as_view(), name='hyperparameter-detail'),
    path('hyperparameter/update/<int:pk>',
         views_hyperparameter.HyperparameterUpdateView.as_view(), name='hyperparameter-update'),
    path('hyperparameter/delete/<int:pk>',
         views_hyperparameter.HyperparameterDeleteView.as_view(), name='hyperparameter-delete'),
    path('hyperparameter/create/', views_hyperparameter.HyperparameterCreateView.as_view(),
         name='hyperparameter-create'),
    path('hyperparameter/', views_hyperparameter.HyperparameterListView.as_view(),
         name='hyperparameter-index'),

	# -------------------set fitur
    path('set-fitur/default/<int:pk>',
         views_setFitur.set_default, name='set-fitur-set-default'),
    path('set-fitur/detail/<int:pk>',
         views_setFitur.SetFiturDetailView.as_view(), name='set-fitur-detail'),
    path('set-fitur/update/<int:pk>',
         views_setFitur.SetFiturUpdateView.as_view(), name='set-fitur-update'),
    path('set-fitur/delete/<int:pk>',
         views_setFitur.SetFiturDeleteView.as_view(), name='set-fitur-delete'),
    path('set-fitur/create/', views_setFitur.SetFiturCreateView.as_view(),
         name='set-fitur-create'),
    path('set-fitur/', views_setFitur.SetFiturListView.as_view(),
         name='set-fitur-index'),

	# -------------------EDA

    path('eda/pca/',
         views_eda.pca, name='eda-pca'),
    path('eda/plot/<int:pk>/boxplot/<str:list_fitur>',
         views_eda.get_boxplot, name='eda-plot-get-boxplot'),
    # path('eda/detail/<int:pk>/boxplot',
    #      views_eda.boxplot, name='eda-detail-boxplot'),
    # path('eda/detail-swarm-box/<int:pk>/<str:list_fitur>',
    #      views_eda.get_swarm_box, name='eda-detail-swarm-box'),
    path('eda/plot/<str:list_fitur>',
         views_eda.plot, name='eda-plot'),
    path('eda/eksplore-data/',
         views_eda.eksploreData, name='eda-eksplore-data'),

    # -------------------set label
    path('set-label/create/label-fraud/<int:id_dataset>/<str:kolom_label>',
         views_setLabel.get_label_fraud, name='set-label-get-label-fraud'),
    path('set-label/create/label/<int:id_dataset>',
         views_setLabel.get_label, name='set-label-get-label'),
    path('set-label/default/<int:pk>',
         views_setLabel.set_default, name='set-label-set-default'),
    path('set-label/detail/<int:pk>',
         views_setLabel.SetLabelDetailView.as_view(), name='set-label-detail'),
    path('set-label/update/<int:pk>',
         views_setLabel.SetLabelUpdateView.as_view(), name='set-label-update'),
    path('set-label/delete/<int:pk>',
         views_setLabel.SetLabelDeleteView.as_view(), name='set-label-delete'),
    path('set-label/create/', views_setLabel.SetLabelCreateView.as_view(),
         name='set-label-create'),
    path('set-label/', views_setLabel.SetLabelListView.as_view(),
         name='set-label-index'),

    # -------------------dataset
    path('dataset/default/<int:pk>',
         views_dataset.set_default, name='dataset-set-default'),
    # path('dataset/detail/<int:pk>/boxplot/<str:list_fitur>',
    #      views_dataset.get_boxplot, name='dataset-detail-get-boxplot'),
    # path('dataset/detail/<int:pk>/boxplot',
    #      views_dataset.boxplot, name='dataset-detail-boxplot'),
    # path('dataset/detail-swarm-box/<int:pk>/<str:list_fitur>',
    #      views_dataset.get_swarm_box, name='dataset-detail-swarm-box'),
    path('dataset/detail/<int:pk>',
         views_dataset.DatasetDetailView.as_view(), name='dataset-detail'),
    path('dataset/update/<int:pk>',
         views_dataset.DatasetUpdateView.as_view(), name='dataset-update'),
    path('dataset/delete/<int:pk>',
         views_dataset.DatasetDeleteView.as_view(), name='dataset-delete'),
    path('dataset/create/', views_dataset.DatasetCreateView.as_view(),
         name='dataset-create'),
    path('dataset/', views_dataset.DatasetListView.as_view(), name='dataset-index'),
]