import streamlit as st 
import pandas as pd 
import numpy as np 
import streamlit_actions as st_actions 
import load_data as ld 

import utils

test_data    =  ld.load_raw_data()
train_data   =  ld.load_raw_data(False)

st.set_page_config(layout='wide')
_,col,_ = st.columns(3)


with col:
    st.title('Rossman Predict Sales')
    utils.skip_lines(2)

_,col1, col2, _ = st.columns([1,3,2,1])
if 'all_stores_selected' not in st.session_state:
    st.session_state.all_stores_selected = False

with col2:
# Inicializando o estado da sessão para armazenar o estado do checkbox

   # Atualizando o estado da sessão e o multiselect quando o checkbox é alterado
    utils.skip_lines(2)
    ALL_STORES = st.checkbox('Select All Stores')
    print(ALL_STORES)

    if ALL_STORES:
        st.session_state.all_stores_selected = True

    
    else:
        st.session_state.all_stores_selected = False


    utils.skip_lines(2)
    predict_btn = st.button(label = 'Executar Previsão')
    # Criando o multiselect

with col1:
    option = st.multiselect(
        'Selecione uma ou mais Lojas',
        test_data['store'].unique(),
        disabled=st.session_state.all_stores_selected
    )

if ALL_STORES:
    option = test_data['store'].unique().tolist()



if predict_btn:
    st_actions.predict_button(test_data, train_data, option)
    

