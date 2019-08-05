from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views import View
from django.core.files.storage import FileSystemStorage

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
# import os
import matplotlib.pyplot as plt
import math
import collections
import time


def dataframe(file_dataset, separator):
    pd.set_option('colheader_justify', 'center')
    df = pd.DataFrame()
    if separator == 'koma':
        df = pd.read_csv(file_dataset, sep=',')
    elif separator == 'titik_koma':
        df = pd.read_csv(file_dataset, sep=';')
    elif separator == 'tab':
        df = pd.read_csv(file_dataset, sep='\t')
    elif separator == 'enter':
        df = pd.read_csv(file_dataset, sep='\n')

    return df



# Calculate accuracy percentage
def accuracy_metric(actual, predicted):
    #how many correct predictions?
    correct = 0
    #for each actual label
    for i in range(len(actual)):
        #if actual matches predicted label
        if actual[i] == predicted[i]:
            #add 1 to the correct iterator
            correct += 1
    #return percentage of predictions that were correct
    return correct / float(len(actual)) * 100.0