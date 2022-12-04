import json
import random
from flask import Flask ,render_template, request, send_file, jsonify
import numpy as np
import pickle
import pandas as pd
import os

def transform(adult):
    df=pd.DataFrame([adult])
    cols = df.columns.values
    large_data = [i for i in cols if df[i].mean() > 10000]

    df_std =np.log1p(df[large_data])
    df[large_data]= df_std
    return df

def predict_single(adult,model):
    df=transform(adult)
    X=df.values
    y_pred=model.predict_proba(X)[:, 1]
    return y_pred[0]

with open('/home/olfa/Downloads/Tunihack/for_olfa/stress-model.bin', 'rb') as f_in:
    model = pickle.load(f_in)
    
STATIC_DIR=os.path.abspath('./static')

app = Flask(__name__,static_folder=STATIC_DIR)
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')



@app.route("/prediction", methods=['GET','POST'])
def prediction():
    city=request.form['city']
    gender=request.form['gender']
    age= request.form['age']
    married = request.form['married']
    nbrchildren= request.form['nbrchildren']
    educ = request.form['educ']
    fam= request.form['fam']
    gasset= request.form['gasset']
    dasset = request.form['dasset']
    sasset = request.form['sasset']
    liasset= request.form['liasset']
    oexpenses= request.form['oexpenses']
    insalary = request.form['insalary']
    inoform = request.form['inoform']
    inbusiness = request.form['inbusiness']
    innobusiness = request.form['innobusiness']
    inagri= request.form['inagri']
    farmexpenses = request.form['farmexpenses']
    laprimary = request.form['laprimary']
    lainvestment = request.form['lainvestment']
    nolainvestment = request.form['nolainvestment']
    if( gender== 'Male'):
        gender = 1
    elif(gender== 'Female'):
        gender = 0
        
    if( married== 'YES'):
        married = 1
    elif(married== 'NO'):
        married = 0
        
    random.seed(2)
    city = random.random()
    
    
    
    
    
    adult={
    
   
    'age':int(age) ,
    'number_children':int(nbrchildren),
    'education_level':int(educ),
    'total_members ':int(fam),
    'gained_asset ':int(gasset),
    'durable_asset':int(dasset), 
    'save_asset':int(sasset),
    'living_expenses ':int(liasset),
    'other_expenses':int(oexpenses), 
    'incoming_salary ':int(insalary),
    'incoming_own_farm':int(inoform), 
    'incoming_business':int(inbusiness), 
    'incoming_no_business':int(innobusiness),
    'incoming_agricultural':int(inagri),
    'farm_expenses':int(farmexpenses),
    'labor_primary':int(laprimary),
    'lasting_investment':int(lainvestment),
    'no_lasting_investmen':int(nolainvestment),
    'ville_id ':int(city),
    'sex':int(gender),
    'married ':int(married),
     
    } 
   
    json_object = json.dumps(adult, indent=4)
 
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)
    

   
  
    return render_template('page2.html', pred =  predict_single(adult,model) )



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696) 