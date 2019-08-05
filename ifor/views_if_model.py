
from .models_dataset import Dataset as DatasetModel
from .models_setLabel import SetLabel as SetLabelModel
from .models_setFitur import SetFitur as SetFiturModel
# from .models_hyperparameterRF import HyperparameterRF as HyperparameterRFModel
from .models_iForest import IsolationForest as IForestModel

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
from . import views

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random as rn
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
import seaborn as sns
sns.set()

def get_x_y (df,get_label,get_fitur):
    # print(df[get_label.kolom_label])
    # if df[get_label.kolom_label].dtype == 'object':
    #     df[get_label.kolom_label] = np.where(df.Class == str(get_label.nilai_label_fraud), 1, 0)
    # print(df[get_label.kolom_label])
    # if get_fitur.all_fitur == 0:
    #     # set fitur dan label
    #     fitur = get_fitur.fitur
    #     fitur = fitur.replace('[', '')
    #     fitur = fitur.replace(']', '')
    #     fitur = fitur.replace(' ', '')
    #     fitur = fitur.replace("'", '')
    #     fitur = fitur.split(',')
    #     if fitur[0] == '':
    #         fitur.remove('')
    # X = df.drop([get_label.kolom_label], axis=1)
    # for m in X.columns:
    #     if df[m].dtype == 'object':
    #         df = df.drop(m, axis=1)
    #         if get_fitur.all_fitur == 0:
    #             if m in fitur:
    #                 fitur.remove(m)

    # if get_fitur.subs_median_group_by_class == 1 :
    # if get_fitur.delete_fitur_with_null_val == 1 :
    #     # for m in df.columns:
    #     #     df[m].fillna(df.groupby("Class")[m].transform("median"), inplace=True)
    #     for m in df.columns:
    #         if(df[m].isnull().sum() > 0):
    #             df = df.drop(m, axis=1)
        

    y = df[get_label.kolom_label]
    X = df.drop([get_label.kolom_label], axis=1)

    if get_fitur.all_fitur == 0 :
        fitur = get_fitur.fitur
        fitur = fitur.replace('[', '')
        fitur = fitur.replace(']', '')
        fitur = fitur.replace(' ', '')
        fitur = fitur.replace("'", '')
        fitur = fitur.split(',')
        if fitur[0] == '':
            fitur.remove('')
        # if fitur == ['miR-10b', 'miR-143', 'miR-199a', 'miR-21', 'miR-23b', 'miR-335'] :
        #     fitur = ['miR-143', 'miR-199a', 'miR-23b', 'miR-21', 'miR-335', 'miR-10b']
        X=X[fitur]
        
    for m in X.columns:
        if(X[m].isnull().sum() > 0):
            X = X.drop(m, axis=1)
            
    # print(y)
    return X,y

# def predict(ifor, X_test, cont):
#     skor = ifor.compute_paths(X_in=X_test)
#     skor_rsort = np.sort(skor)[::-1]
#     maks = int(int(skor_rsort.size)*cont)
#     data1 = skor_rsort[:maks]
#     th = data1.mean()
#     y_pred=[]
#     for w in skor:
#         if(w<th):
#             y_pred.append(0)
#         else:
#             y_pred.append(1)
#     return y_pred
def confussion_matrik(actual,predict):
    TP,FP,FN,TN = 0,0,0,0
    for i,val in enumerate(actual):
        if val == 0:
            if val == predict[i]:
                TN += 1
            else:
                FP += 1
        if val == 1:
            if val == predict[i]:
                TP += 1
            else:
                FN += 1
    return TP,FP,FN,TN

def acc_sens_spec(actual,predict):
    TP,FP,FN,TN = confussion_matrik(actual,predict)
    df_heatmap = pd.DataFrame([[TN,FP],[FN,TP]],['Aktual Normal','Aktual Fraud'],['Prediksi Normal','Prediksi Fraud'])
    plt.figure(figsize=(8,8))
    plot = sns.set(font_scale =1.4)
    plot = sns.heatmap(df_heatmap,annot=True, annot_kws={'size':16},fmt='g')
    figure = plot.get_figure() 
# akurasi
    if (TP+FP+FN+TN) == 0 :
        accuracy = 0 
    else :
        accuracy = (TP+TN)/(TP+FP+FN+TN)
        
# sensitivity
    if (TP+FN) == 0 :
        sensitivity = 0
    else :
        sensitivity = TP/(TP+FN)
        
# specifity    
    if (TN +FP) == 0 :
        specifity = 0
    else :
        specifity = TN/(TN +FP)
        
# precision
    if (TP+FP) == 0 :
        precision = 0
    else :
        precision = TP/(TP+FP)

# recall
    recall = sensitivity

# f1_score
    if (precision+recall) == 0 :
        f1_score = 0
    else :
        f1_score = 2*((precision*recall)/(precision+recall))  
    
    return figure,precision,recall,f1_score

def iForest(X, ntree, sample, th):
    ifor = IsolationForest(n_estimators=ntree, max_samples=sample, contamination=th, random_state=1)
    ifor.fit(X)
    return ifor

def convert(y):
    for i in range(y.shape[0]):
        if y[i]==-1:
            y[i]=1;
        else:
            y[i]=0
    return y

def eval_model(ifor,X,y):
#     ts = time.time()
    y_pred=ifor.predict(X)
#     tf = time.time()
    y_pred=convert(y_pred)
    figure,precision,recall,f1_score = acc_sens_spec(y,y_pred)
    return figure,precision,recall,f1_score

def isolationForest(ifo_id):
    get_if = IForestModel.objects.get(
        pk=ifo_id)
    get_dataset = get_if.dataset
    get_label = get_if.setlabel
    trainras = get_if.setTrain
    valras = get_if.setVal
    testras = get_if.setTest
    get_fitur = get_if.setfitur
    get_hyperparameter = get_if.hyperparameter

    ntree = get_hyperparameter.n_tree
    sample = get_hyperparameter.sample
    kontaminasi = get_hyperparameter.kontaminasi
    file_result = 'media/iForest/result/coba.csv'
    # file_fitur_importance = 'media/iForest/fiturImportance/coba.csv'
    file_model = 'media/iForest/model/coba.pkl'

    file_cmval = 'ifor/static/iforest/cm/val/coba.png'
    file_cmtest = 'ifor/static/iforest/cm/test/coba.png'

    file_result = file_result.replace('coba',str(get_if.id))
    # file_fitur_importance = file_fitur_importance.replace('coba',str(get_rf.id))
    file_model = file_model.replace('coba',str(get_if.id))

    file_cmval = file_cmval.replace('coba',str(get_if.id))
    file_cmtest = file_cmtest.replace('coba',str(get_if.id))

    # To Dataframe
    df = views.dataframe(get_dataset.file_dataset, get_dataset.separator)
    print(df.shape)
    # Preprocessing
    X,y = get_x_y(df,get_label,get_fitur)

    y_ab = len(y[y==1])
    th = y_ab/len(y)

    train_size = trainras/100
    val_size = valras/100
    test_size = testras/100
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=1, stratify=y)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=val_size/(train_size+test_size), random_state=1, stratify=y_train)
    
    # #training
    ifor  = iForest(X_train, ntree, sample, kontaminasi)

    # #pred
    # yval_pred = predict(ifor,X_val,th)
    # ytest_pred = predict(ifor,X_test,th)



    #eval
    hasil=[]
    val_cm,val_prec,val_rec,val_f1 = eval_model(ifor,X_val,y_val)
    hasil.append(['Validasi', val_prec, val_rec, val_f1])
    test_cm,test_prec,test_rec,test_f1 = eval_model(ifor,X_test,y_test)
    hasil.append(['Test', test_prec, test_rec, test_f1])

    df_result = pd.DataFrame(data= hasil, columns=['hasil','Precision','Recall','F1_Score'])
    df_result.to_csv(file_result, index=False)

    val_cm.savefig(file_cmval)
    test_cm.savefig(file_cmtest)
    # pemodelan
    # maks_fitur = get_hyperparameter.max_fitur
    # try:
    #     if isinstance(int(maks_fitur), int) == True:
    #         maks_fitur = int(maks_fitur)
    # except:
    #     try:
    #         if isinstance(float(maks_fitur), float) == True:
    #             maks_fitur = float(maks_fitur)
    #     except Exception as e:
    #         pass

    # clf = RandomForestClassifier(criterion='gini', max_depth=int(get_hyperparameter.max_kedalaman),
    # clf = RandomForestClassifier(criterion='gini',
    #                              max_features=maks_fitur, n_estimators=int(get_hyperparameter.n_tree), random_state=1)
    # clf = clf.fit(X, y)
    # pred = clf.predict(X)

    # acc = accuracy_score(y, pred)
    # cm_model = confusion_matrix(y, pred)

    # --K-FOld Cross Validation
    # kfolds_cv = views.kfold_cross_validation(clf,X,y,n_fold=int(get_rf.k_cv),n_seed=1)
    # df_result = pd.DataFrame(data= kfolds_cv, columns=['Akurasi','Sensitivity','Specifity','Waktu'])
    # df_result.to_csv(file_result, index=False)
    
    # -- fitur importance
    # importances = clf.feature_importances_
    # indices = np.argsort(importances)[::-1]
    # fitur_importance = []
    # for f in range(X.shape[1]):
    #     if  importances[indices[f]] > 0 :
    #         fitur_importance.append(
    #             [X.columns[indices[f]], importances[indices[f]]])

    # df_FI = pd.DataFrame(data=fitur_importance, columns=['fitur', 'nilai importance'])
    # df_FI.to_csv(file_fitur_importance, index=False)

    #model
    IFFile = open(file_model, 'wb')
    pickle.dump(ifor, IFFile)
    IFFile.close()
