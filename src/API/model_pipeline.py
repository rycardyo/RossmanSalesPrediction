import data_preparation 
import model
import pandas as pd 

modelo = model.XGB_sales_prediction()

def run_model_pipeline(raw_data):

    data_preparator = data_preparation.Data_preprocessing(df_raw = raw_data)

    # Executa o pipeline de transformações
    data_preparator.pipeline()
    data_to_predict = data_preparator.df_gold

    # Realiza as predições com o modelo 
    prediction = modelo.run_prediction(data_to_predict)
    data_to_return = pd.DataFrame(data_to_predict['store'])
    data_to_return['sales'] = prediction

    return data_to_return
