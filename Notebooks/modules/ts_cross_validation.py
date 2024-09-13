import pandas as pd
import datetime 
import numpy as np 

class time_series_k_fold_validation():
    def __init__(self,
                k_fold : int,
                dict_models : dict,
                train_data : pd.DataFrame,
                week_split_time : int,
                features_train : list, 
                target : str,
                loss_function):
        '''
        k_fold : number of k_folds for separeted the dataset 
        dict_models: dict in the format: key = model_name, value = model in from sklearn (or similar)
        train_data: train_dataset
        wee_split_time: size of split time in weeks for data validation 
        '''
        self.k_fold = k_fold
        self.dict_models = dict_models
        self.train_data = train_data
        self.week_split_time = week_split_time
        self.features_train = features_train
        self.target = target
        self.loss_function = loss_function

    def train_models(self, train_data, models : dict):
        ''' 
        model: dict in the format: 
            key = model_name, value = model
        '''
        
        x_train = train_data[self.features_train].values
        y_train = train_data[self.target].values

        for model in models.keys(): 
            models[model].fit(x_train, y_train)
        
        return models 


    def evaluate_models(self, models, validation_data):

        x_validation = validation_data[self.features_train].values
        y_validation = validation_data['sales'].values

        predictions = {}
        errors = {}

        for model in models.keys():
            predictions[model]  = models[model].predict(x_validation)
            errors[model] = self.loss_function(np.expm1(predictions[model]), np.expm1(y_validation), model)
        
        errors_df = [errors[model] for model in models.keys()]

        return pd.concat(errors_df)


    def cross_validation_time_series(self):
        
        start_date = self.train_data.date.min()
        end_date = self.train_data.date.max()
        
        results = []
        weeks = int( (end_date - start_date).days / 7)
        rest = (end_date - start_date).days % 7

        for k in range(0, self.k_fold):

            current_start_date = end_date - datetime.timedelta(days = 7 * (self.week_split_time * (k + 1)) )
            current_end_date = current_start_date + datetime.timedelta(days = 7 * self.week_split_time)

            current_train = self.train_data[self.train_data.date <= current_start_date]
            current_validation = self.train_data[(self.train_data.date > current_start_date) & (self.train_data.date <= current_end_date)]

            print(f'Kfold --> {k}')
            models = self.train_models(current_train, self.dict_models)

            results.append(self.evaluate_models(models, current_validation))


        final_result = pd.concat(results)
        
        final_result_mean = final_result.groupby('Model_name').agg({
                                                                'RMSE' : 'mean',
                                                                'MAPE' : 'mean',
                                                                'MAE'  : 'mean'
        }).reset_index()

        final_result_std = final_result.groupby('Model_name').agg({
                                                                'RMSE' : 'std',
                                                                'MAPE' : 'std',
                                                                'MAE'  : 'std'
        }).reset_index()

        final_result_mean['STD_RMSE']  =  final_result_std['RMSE']
        final_result_mean['STD_MAPE']  =  final_result_std['MAPE']
        final_result_mean['STD_MAE']   =  final_result_std['MAE']

        return final_result_mean