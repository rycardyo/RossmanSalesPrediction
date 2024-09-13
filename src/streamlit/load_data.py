import pandas as pd
import sys
sys.path.append('../')
import inflection 
import os 

CURR_PATH = os.path.dirname(__file__)

def load_raw_data(predict : bool = True):

    source = 'test' if predict else 'train'
    df_sales_raw = pd.read_csv(CURR_PATH + f'/../../Data/{source}.csv', low_memory=False)
    df_store_raw = pd.read_csv(CURR_PATH + '/../../Data/store.csv', low_memory=False)

    df_test_raw = pd.merge(df_sales_raw, df_store_raw, on = 'Store', how = 'left')
    df_test_raw = df_test_raw[df_test_raw.Open == 1]

    try:
        df_test_raw.drop(columns=['Id'], inplace=True)
    except:
        pass
    
    raw_columns = df_test_raw.columns.values 

    snake_case = lambda x: inflection.underscore(x)

    new_columns = list(map(snake_case, raw_columns))
    df_test_raw.columns = new_columns

    return df_test_raw



