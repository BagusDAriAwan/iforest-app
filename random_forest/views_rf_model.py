
from .models_dataset import Dataset as DatasetModel
from .models_setLabel import SetLabel as SetLabelModel
from .models_setFitur import SetFitur as SetFiturModel
from .models_hyperparameterRF import HyperparameterRF as HyperparameterRFModel
from .models_randomForest import RandomForest as RandomForestModel

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
from . import views

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import pickle

def get_x_y (df,get_label,get_fitur):
    # print(df[get_label.kolom_label])
    if df[get_label.kolom_label].dtype == 'object':
        df[get_label.kolom_label] = np.where(df.Class == str(get_label.nilai_label_kanker), 1, 0)
    # print(df[get_label.kolom_label])
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
    X = df.drop([get_label.kolom_label], axis=1)
    for m in X.columns:
        if df[m].dtype == 'object':
            df = df.drop(m, axis=1)
            if get_fitur.all_fitur == 0:
                if m in fitur:
                    fitur.remove(m)

    # if get_fitur.subs_median_group_by_class == 1 :
    # if get_fitur.delete_fitur_with_null_val == 1 :
        # for m in df.columns:
            # df[m].fillna(df.groupby("Class")[m].transform("median"), inplace=True)
        # for m in df.columns:
            # if(df[m].isnull().sum() > 0):
                # df = df.drop(m, axis=1)
        

    y = df[get_label.kolom_label]
    X = df.drop([get_label.kolom_label], axis=1)

    if get_fitur.all_fitur == 0 :
        if fitur == ['miR-10b', 'miR-143', 'miR-199a', 'miR-21', 'miR-23b', 'miR-335'] :
            fitur = ['miR-143', 'miR-199a', 'miR-23b', 'miR-21', 'miR-335', 'miR-10b']
        X=X[fitur]
        
    for m in X.columns:
        if(X[m].isnull().sum() > 0):
            X = X.drop(m, axis=1)
            
    # print(y)
    return X,y

def randomForest(rf_id):
    get_rf = RandomForestModel.objects.get(
        pk=rf_id)
    get_dataset = get_rf.dataset
    get_label = get_rf.setlabel
    get_fitur = get_rf.setfitur
    get_hyperparameter = get_rf.hyperparameter

    file_result = 'media/randomForest/result/coba.csv'
    file_fitur_importance = 'media/randomForest/fiturImportance/coba.csv'
    file_model = 'media/randomForest/model/coba.pkl'

    file_result = file_result.replace('coba',str(get_rf.id))
    file_fitur_importance = file_fitur_importance.replace('coba',str(get_rf.id))
    file_model = file_model.replace('coba',str(get_rf.id))


    # To Dataframe
    df = views.dataframe(get_dataset.file_dataset, get_dataset.separator)

    # Preprocessing
    X,y = get_x_y(df,get_label,get_fitur)

    # pemodelan
    maks_fitur = get_hyperparameter.max_fitur
    try:
        if isinstance(int(maks_fitur), int) == True:
            maks_fitur = int(maks_fitur)
    except:
        try:
            if isinstance(float(maks_fitur), float) == True:
                maks_fitur = float(maks_fitur)
        except Exception as e:
            pass

    # clf = RandomForestClassifier(criterion='gini', max_depth=int(get_hyperparameter.max_kedalaman),
    clf = RandomForestClassifier(criterion='gini',
                                 max_features=maks_fitur, n_estimators=int(get_hyperparameter.n_tree), random_state=1)
    clf = clf.fit(X, y)
    # pred = clf.predict(X)

    # acc = accuracy_score(y, pred)
    # cm_model = confusion_matrix(y, pred)

    # --K-FOld Cross Validation
    kfolds_cv = views.kfold_cross_validation(clf,X,y,n_fold=int(get_rf.k_cv),n_seed=1)
    df_result = pd.DataFrame(data= kfolds_cv, columns=['Akurasi','Sensitivity','Specifity','Waktu'])
    df_result.to_csv(file_result, index=False)
    
    # -- fitur importance
    importances = clf.feature_importances_
    indices = np.argsort(importances)[::-1]
    fitur_importance = []
    for f in range(X.shape[1]):
        if  importances[indices[f]] > 0 :
            fitur_importance.append(
                [X.columns[indices[f]], importances[indices[f]]])

    df_FI = pd.DataFrame(data=fitur_importance, columns=['fitur', 'nilai importance'])
    df_FI.to_csv(file_fitur_importance, index=False)

    #model
    RFFile = open(file_model, 'wb')
    pickle.dump(clf, RFFile)
    RFFile.close()
