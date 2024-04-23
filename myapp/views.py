from django.shortcuts import render,redirect
from .models import contact, users
from django.contrib import messages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
# Create your views here.

def index(request):
    if 'email' in request.session:
        current=request.session['email']
        user=users.objects.get(email=current)
        return render(request,"index.html",{'current_user':current,'user':user})
    return render(request,'index.html')

def login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=users.objects.filter(email=email,password=password)
        if user:
            request.session['email']=email
            return redirect('/')
        else:
            messages.error(request,"username and password doesnt match")
    return render(request,'login.html')

def register(request):
    if request.method=='POST':
        name=request.POST['name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirmpassword=request.POST['confirmpassword']
        mobilenumber=request.POST['mobilenumber']
        emailexists=users.objects.filter(email=email)
        if emailexists:
            messages.error(request,"Email ID already exists")
        elif password!=confirmpassword:
            messages.error(request,"Password doesnt match")
        else:
            users.objects.create(name=name,username=username,email=email,password=password,confirmpassword=confirmpassword,mobilenumber=mobilenumber)
            return redirect('/')
    return render(request,'register.html')
def logout(request):
    del request.session['email']
    return redirect('/')  

def prediction(request):
    if 'email' in request.session:
        current=request.session['email']
        user=users.objects.get(email=current)
        data=pd.read_csv('static/csv/loan_approval_dataset.csv')
        data[' loan_status'] = data.apply(lambda row: 1 if row[' loan_status']!= ' Rejected' else 0, axis=1)
        data[' loan_status'] 
        data=data.drop(['loan_id',' loan_amount',' loan_term',' residential_assets_value',' commercial_assets_value',' luxury_assets_value',' bank_asset_value'],axis=1)
        le=LabelEncoder()
        data[' self_employed']=le.fit_transform(data[' self_employed'])
        data[' education']=data.apply(lambda row:0 if row[' education']!=' Graduate' else 1 ,axis=1)
        x=data.iloc[:,0:5].values
        y=data.iloc[:,-1].values
        x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=.5,random_state=0)
        rfc=RandomForestClassifier()
        rfc.fit(x_train,y_train)
        if request.method=='POST':
            no_of_dependents = int(request.POST['dependents'])
            education = int(request.POST['education'])
            self_employed = int(request.POST['employment'])
            income_annum = int(request.POST['income'])
            cibil_score = int(request.POST['cibil'])

            # Reshaping the input for prediction
            input_values = np.array([[no_of_dependents, education, self_employed, income_annum, cibil_score]])

            # Making prediction
            prediction = rfc.predict(input_values)
            print(prediction)

            # Checking prediction result
            if prediction == 1:
                messages.success(request," got a loan from the bank.")
                return render(request,"prediction1.html",{'current_user':current,'user':user,'prediction':prediction})
            else:
                messages.success(request," didn't get a loan from the bank.")
                return render(request,"prediction1.html",{'current_user':current,'user':user,'prediction':prediction})
        return render(request,"prediction1.html",{'current_user':current,'user':user})
    return render(request,'prediction1.html') 
def contactus(request):
    if request.method=='POST':
        name=request.POST['name']
        message=request.POST['feedback']
        email=request.POST['email']
        contact.objects.create(Name=name,Message=message,Email=email)
        return redirect('/')  
    return render(request,'contactus.html') 
def bank_function(request):
    return render(request,'banks.html')
def myprofile(request):
    if 'email' in request.session:
        current=request.session['email']
        user=users.objects.get(email=current)
        return render(request,"myprofile.html",{'current_user':current,'user':user})
    return render(request,'myprofile.html')
def updateprofile(request):
    if 'email' in request.session:
        current=request.session['email']
        user=users.objects.get(email=current)
        if request.method=='POST':
            name=request.POST['name']
            username=request.POST['username']
            password=request.POST['password']
            confirmpassword=request.POST['confirmpassword']
            mobilenumber=request.POST['mobilenumber']
            if password!=confirmpassword:
                messages.error(request,"Password doesnt match")
            else:
                user.name=name
                user.username=username
                user.password=password
                user.mobilenumber=mobilenumber
                user.save()
                return redirect('myprofile')
        return render(request,"updateprofile.html",{'current_user':current,'user':user})
    return render(request,'updateprofile.html')
def about(request):
    return render(request,"about.html")