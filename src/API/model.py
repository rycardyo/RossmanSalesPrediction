import joblib as jbl
import xgboost as xgb
import pandas as pd
import os 
import numpy as np
curr_path = os.path.dirname(__file__)

class XGB_sales_prediction():
    
    def __init__(self, model_path: str = curr_path + '/models/xgb_tunned.pkl'):
        
        self.model = jbl.load(model_path)

    def run_prediction(self, input_data : pd.DataFrame):
        self.predictions = np.expm1(self.model.predict(input_data))
        
        return self.predictions

