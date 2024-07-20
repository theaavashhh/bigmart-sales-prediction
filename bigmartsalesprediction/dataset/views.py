from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import transform, translated 
import pandas 
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score

# Create your views here.
def createDB(file_path):
    df_train=pd.read_csv(file_path,delimiter=',')
    val=df_train.describe()

    


def dataset(request):
    if request.method == "POST":
        file=request.FILES['file']
        
        obj=File.objects.create(file=file)
        createDB(obj.file)

        return HttpResponseRedirect('/dashboard')

        

    return render(request,"dataset.html")




def predict(request):
    if request.method=='POST':

        global val,Y,Ys

        item_weight= float(request.POST['item_weight'])
        item_fat_content=float(request.POST['item_fat_content'])
        item_visibility= float(request.POST['item_visibility'])
        item_type= float(request.POST['item_type'])
        item_mrp = float(request.POST['item_mrp'])
        outlet_establishment_year= float(request.POST['outlet_establishment_year'])
        outlet_size= float(request.POST['outlet_size'])
        outlet_location_type= float(request.POST['outlet_location_type'])
        outlet_type= float(request.POST['outlet_type'])

        X= np.array([[ item_weight,item_fat_content,item_visibility,item_type,item_mrp,
                outlet_establishment_year,outlet_size,outlet_location_type,outlet_type ]])

        # scaler_path= '../bigmartsalesprediction/models/sc.sav'

        # sc=joblib.load(scaler_path)

        # X_std= sc.transform(X)

        # model_path='../bigmartsalesprediction/models/lr.sav'

        # model= joblib.load(model_path)

        # Y_pred=model.predict(X_std)

        # val=abs(Y_pred)
        linear=joblib.load('../bigmartsalesprediction/models/linearRegression')
        Y_pred=linear.predict(X)
        val=abs(Y_pred-30000)

        

        xgb=joblib.load('../bigmartsalesprediction/models/XGBoostRegression')
        Y=xgb.predict(X)
      

       
        rf=joblib.load('../bigmartsalesprediction/models/RandomForestRegression')
        Ys=rf.predict(X)
    
      

        return render(request,'accuracy.html',context={'c':val,'a':abs(Y),'b':abs(Ys)})

    
   
        


    return render(request,"predict.html")

def visualization(request):
    lists=[]
    lists.append(Y)
    lists.append(Ys)
    lists.append(val)

    if(Y!=""):

        return render(request,'visualization.html',context={'a':lists})


    

   
    

