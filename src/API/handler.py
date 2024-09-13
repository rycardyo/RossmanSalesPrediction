import data_preparation 
#import model
import pandas as pd 
import os 
from flask import Flask, request, Response
import json 
import model_pipeline

#modelo = model.XGB_sales_prediction()
app = Flask(__name__)

@app.route('/rossmann/predict', methods = ['POST'])
def rossman_predict():
    test_json = request.get_json()

    if test_json: #There is data
        if isinstance(test_json, dict): # unique input
            test_raw = pd.DataFrame(test_json, index = [0])
        
        else: #multiple inputs
            test_raw = pd.DataFrame(test_json, columns = test_json[0].keys())

        # Instancia classe de preparacao dos dados
        data_to_return = model_pipeline.run_model_pipeline(test_raw)

        return json.dumps(data_to_return.to_dict(orient = 'records'))

        
    else:
        return Response('{}', status = 200, mimetype = 'application/json')

if __name__ == '__main__':
    app.run('0.0.0.0')







'''
CURRENT_PATH = os.path.abspath(__file__)

df_sales_raw = pd.read_csv('../Data/train.csv', low_memory=False)
df_store_raw = pd.read_csv('../Data/store.csv', low_memory=False)
df_raw = pd.merge(df_sales_raw, df_store_raw, on = 'Store', how = 'left')

print('Data_Preparation')
picareta_dos_dados = data_preparation.Data_preprocessing(df_raw.sample(20), path_scallers='../scallers/')


dados_tinindo = picareta_dos_dados.df_gold
print(dados_tinindo.sample(2))

print('Model_Runnig...')
bolaCristal = model.XGB_sales_prediction()

predicoes = bolaCristal.run_prediction(dados_tinindo)

print(predicoes)'''

