import streamlit as st
import pandas as pd 
import numpy as np
import json 
import requests
import load_data as ld
import utils
import sys 
sys.path.append('../API')

from API import model_pipeline as mp
import plotly.graph_objects as go
from datetime import timedelta
# Controla se o modelo sera executado em uma API ou "localmente" com a aplicação 
API = False 

day_of_week_map = {
    1 : 'Segunda',
    2 : 'Terça' ,   
    3 : 'Quarta',
    4 : 'Quinta',
    5 : 'Sexta',
    6 : 'Sabado',
    7 : 'Domingo'
    
}


def call_api(predict_data) -> pd.Series:
    url = 'http://192.168.100.40:5000/rossmann/predict'
    header = {'Content-type' : 'application/json'}
    data = json.dumps(predict_data.to_dict(orient = 'records')) 
    r = requests.post(url, data = data, headers = header)

    #print(f'O retorno foi: {r.decode().json()}')
    
    return_data = pd.DataFrame(r.json())
    
    return  return_data['sales']


def run_model_locally(predict_data):
    return_data = mp.run_model_pipeline(predict_data)
    
    return  return_data['sales']


def run_prediction(data_to_predict):
    if API:
        return  call_api(data_to_predict)
            
    else: 
        return run_model_locally(data_to_predict)


def line_chart(
        predict_data, 
        historical_data):
    
    predict_data.date = pd.to_datetime(predict_data.date)
    historical_data.date = pd.to_datetime(historical_data.date)
    
    first_prediction        = predict_data.date.min()
    last_historical         = historical_data.date.max()
    thresholding_historical = first_prediction - timedelta(days=120)
    print(first_prediction)
    print(thresholding_historical)
    print(last_historical)

    _predict_data = predict_data[['store','date']]

    _predict_data['sales'] = np.nan
    _predict_data['predict_sales'] = run_prediction(predict_data)
    _predict_data = _predict_data[['date','predict_sales']].groupby(['date']).sum().reset_index()

    _historical_data  = historical_data[['store','date','sales']]
    
    _historical_data  = _historical_data[_historical_data.date >= thresholding_historical]

    _historical_data = _historical_data[['date','sales']].groupby(['date']).sum().reset_index()
    
    df_chart = pd.concat([_predict_data, _historical_data])
    df_chart = df_chart.sort_values(by = 'date' , ascending = True)

    fig = go.Figure()

    # Traço com as vendas reais
    fig.add_trace(
        go.Scatter(
            x    = df_chart['date'], 
            y    = df_chart['sales'],
            mode = 'lines',
            name = 'Vendas Reais',
            line = dict(color='blue', width = 3) 
            )
        )
    
    # Traço com as vendas preditas
    fig.add_trace(
        go.Scatter(
            x    = df_chart['date'], 
            y    = df_chart['predict_sales'],
            mode = 'lines',
            name = 'Previsão',
            line = dict(color='red', width = 3) 
            )
        )
    
    fig.update_layout(
        title="Vendas Reais e Previsões de Vendas",
        xaxis_title="Data",
        yaxis_title="Valor de Vendas",
        legend_title="Legenda",
        showlegend=True
    )

    st.plotly_chart(fig)

    
    ...
    
def predict_button( predict_data,
                    historical_data,
                    idx_store):

    data_to_predict = predict_data[predict_data.store.isin(idx_store)].reset_index(drop=True)
    historical_data = historical_data[historical_data.store.isin(idx_store)].reset_index(drop=True)
    print('olha que tanto')
    print(len(data_to_predict))
    columns_to_show = ['store', 'day_of_week', 'date', 'predict_sales']
    if len(data_to_predict) > 0:
        
        return_data = run_prediction(data_to_predict)
        data_to_predict['predict_sales'] = return_data
        total_prediction = round(data_to_predict.predict_sales.sum() , 2)
        mean_prediction  = round(data_to_predict.predict_sales.mean(), 2)
        data_to_predict.predict_sales  = data_to_predict.predict_sales.apply(lambda x: round(x,2))
        data_to_predict.day_of_week = data_to_predict.day_of_week.map(day_of_week_map)

        utils.skip_lines(2)

        #cols to centralize indicator cards

        #_,col,_ = st.columns(3)

        #with col:
        #    st.title(f'Loja {idx_store}')
                
        _,col3,col4,_ = st.columns([1,3,3,1])

        # ------------- INDICADORES ---------------------------
        
        with col3:
            
            st.text('='*60)
            _,sub_col,_ = st.columns([1,2,1])
            
            with sub_col:
                st.subheader(' '*5 + 'Previsão Total')
                st.metric(label = '', value = f"$ {total_prediction:.2f}".replace(',',' ').replace('.',','))
            
            st.text('='*60)
        with col4:
            st.text('='*60)
            _,sub_col,_ = st.columns([1,2,1])
            
            with sub_col:
                st.subheader(' '*5 + 'Ticket Médio')
                st.metric(label = '', value = f"$ {mean_prediction:.2f}".replace(',',' ').replace('.',',') )
            
            st.text('='*60)

        utils.skip_lines(2)
        
        # ---------------------- CHART AND TABLE ----------------------------- 

        #st.line_chart(data_to_predict, x = 'date', y = 'predict_sales')
        st.title('Vendas e Valor Previsto')
        line_chart(data_to_predict, historical_data)
        
        st.title('Previsões')
        st.table(data_to_predict[columns_to_show].head(200))


    else:
        st.warning(f'A LOJA {idx_store} NÃO FOI ENCONTRADA')
