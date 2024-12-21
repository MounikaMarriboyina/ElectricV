from django.shortcuts import render, redirect
from . import views
# Create your views here.
import pandas as pd
from django.contrib import messages
import pandas as pd
from catboost import CatBoostClassifier
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from django.http import HttpResponse
from sklearn.tree import DecisionTreeClassifier
from keras.models import Sequential, load_model
from keras.layers import Conv1D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import MaxPooling2D,Dropout
import matplotlib.pyplot as plt
import tensorflow as tf
import os
from xgboost import XGBClassifier
from .models import *
from sklearn.svm import SVC
from django.contrib.auth.models import User

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

# Register function
def registration(request):
    if request.method=='POST':
        Name = request.POST['username']
        email=request.POST['email1']
        password=request.POST['password']
        conpassword=request.POST['cpassword']
        contact=request.POST['contact']
        print(Name,email,password,conpassword,contact)
        if password==conpassword:
            dc = User.objects.filter(email=email,password=password)
            if dc:
                msg='Account already exists'
                return render(request,'registration.html',{'msg':msg})
            else:
                user=User(username=Name,email=email,password=password)
                user.save()
                return render(request,'login.html')
                
        else:
            msg='passwords not matched '
            return render(request,'registration.html',{'msg':msg})
    return render(request,'registration.html')


def login(request):
    if request.method=='POST':
        lemail=request.POST['email']
        lpassword=request.POST['password']

        d=User.objects.filter(email=lemail,password=lpassword).exists()
        if d:

            return redirect('upload')
        else:
            msg='login failed'
            return render(request,'login.html',{'msg':msg})

    return render(request,'login.html')

def userhome(request):
    
    return render(request,'userhome.html')


def upload(request):
    global data, path
    if (request.method == 'POST'):
        file = request.FILES['file']
        d = dataset(data=file)
        fn = d.filename()
        path = 'home\static\dataset'+fn

        data = pd.read_csv('home\static\dataset\EV-Charging-Raw-Data.csv')
        datas = data.iloc[:100,:]
        x = datas.to_html()

        return render(request, 'upload.html', {'table':x})
    return render(request, 'upload.html')

def split(request):
    global x_train,x_test,y_train,y_test,x,y,data,path
    if request.method == "POST":
        size = request.POST['split']
        size = int(request.POST['split'])
        size = size / 100
        df = pd.read_csv('home\static\dataset\EV-Charging-Raw-Data.csv')
        
        le=LabelEncoder()
        x=['Org Name','Start Date','Start Time Zone','End Date','End Time Zone','Transaction Date (Pacific Time)','Total Duration (hh:mm:ss)','Charging Time (hh:mm:ss)','Port Type','Plug Type','Country','Currency','Ended By','Driver Postal Code']
        for xd in x:

            df[xd]=le.fit_transform(df[xd]) 

        df=df.drop(columns=(['Label 01','Lable 02','Label 03','Label 04','Label 05','Label 06','Label 07','Label 08','Gasoline Savings (gallons)']))
        numeric_data=df.select_dtypes(include=[np.number])
        catagorical_data=df.select_dtypes(exclude=[np.number])
        x=df.iloc[:,:-4]
        y=df.iloc[:,-4]
        x_train,x_test,y_train,y_test= train_test_split(x,y,test_size=0.3,random_state=41)
        messages.info(request,"Data Splits Succesfully")
    return render(request,'split.html',{'msg':messages})

