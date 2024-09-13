import inflection 
import pandas as pd
import pickle as pkl
import numpy as np
import joblib as jb
import datetime 
import os 

curr_path = os.path.dirname(__file__)

class Data_preprocessing():
    def __init__(self, 
                 df_raw : pd.DataFrame,
                 path_scallers : str = curr_path + '/scallers/'):

        self.path_scallers = path_scallers
        self.df_raw = df_raw
        self._load_scallers()
    
    
    def pipeline(self):
        
        self.df_processing = self._data_cleaning(self.df_raw)
        self.df_processing = self._change_dtypes(self.df_processing)
        self.df_processing = self._feature_enginnering(self.df_processing)
        self.df_processing = self._feature_transformation(self.df_processing)
        self.df_gold = self._feature_selection(self.df_processing) 
        

    def _load_scallers(self):

        self.robust_scaller  =  jb.load(self.path_scallers + 'robustScaller.pkl')
        self.label_enconder  =  jb.load(self.path_scallers + 'labelEncoder.pkl')
        self.minMax_scaller  =  jb.load(self.path_scallers + 'minmaxScaller.pkl')
    
    
    def _data_cleaning(self,
                      df_step):
        

        __current_df = df_step.copy()
        raw_columns = __current_df.columns.values 

        snake_case = lambda x: inflection.underscore(x)

        new_columns = list(map(snake_case, raw_columns))
        __current_df.columns = new_columns

        __current_df.loc[:, 'date'] = pd.to_datetime(__current_df['date'])

        __current_df['date'] = pd.to_datetime(__current_df.date)

        # Assumption: Se o dado está nulo, é devido podemos considerar que ou esqueceram de anotar,
        # ou não há competidor proximo, para o segundo então o valor pode ser um valor abitrariamente alto
        # competition_distance  
        __current_df.loc[__current_df['competition_distance'].isna(), 'competition_distance'] = __current_df.competition_distance.max() * 3

        # competition_open_since_year    
        # Assumption: Aqui estamos pensando na etapa de feature enginnering 
        # onde o tempo desde que um competidor foi aberto impacta na quantidade de vendas, de modo que cria-se um regime 
        # transitorio em que a loja tem suas vendas diminuidas no inicio e posteriomente suas vendas voltam a subir
        # aqui a variavel é QUANTO TEMPO tem DESDE QUE O COMPETIDODR FOI ABERTO 
        # bem quando esta variavel for calculada para estes casos o retorno será zero. 
        # porém TUDO É CICLICO E TUDO pode mudar se necessário. 
        __current_df.loc[__current_df['competition_open_since_year'].isna(), 'competition_open_since_year'] = \
            __current_df.loc[__current_df['competition_open_since_year'].isna(), 'date'].dt.year 

        # competition_open_since_month    

        __current_df.loc[__current_df['competition_open_since_month'].isna(), 'competition_open_since_month'] = \
                __current_df.loc[__current_df['competition_open_since_month'].isna(), 'date'].dt.month 

                                
        # promo2_since_week               
        # Caso o valor seja nulo, siginifica que a loja não aderiu a promo2 
        # logo podemos usar a mesma ideia da anterior, uma vez que o "tempo nesta promoção" também será nulo
        __current_df.loc[__current_df['promo2_since_week'].isna(), 'promo2_since_week'] = \
                __current_df.loc[__current_df['promo2_since_week'].isna(), 'date'].dt.isocalendar().week 


        # promo2_since_year    
        # Caso o valor seja nulo, siginifica que a loja não aderiu a promo2 
        # logo podemos usar a mesma ideia da anterior, uma vez que o "tempo nesta promoção" também será nulo
        __current_df.loc[__current_df['promo2_since_year'].isna(), 'promo2_since_year'] = \
                __current_df.loc[__current_df['promo2_since_year'].isna(), 'date'].dt.year 
                
        # promo_interval
        # Indica os meses em que a promoção reiniciou 
        map_month = { 
            1 : 'Jan',
            2 : 'Feb',
            3 : 'Mar',
            4 : 'Apr',
            5 : 'May',
            6 : 'Jun',
            7 : 'Jul',
            8 : 'Aug',
            9 : 'Sep',
            10 : 'Oct',
            11 : 'Nov',
            12 : 'Dec',
        }
        __current_df['date_month'] = __current_df['date'].dt.month.map(map_month)
        __current_df.promo_interval.fillna("0", inplace=True)

        __current_df['is_promo'] = __current_df.apply(lambda x: 1 if x['date_month'] in str(x['promo_interval']).split(',') else 0, axis = 1)

        return __current_df

    def _change_dtypes(self, current_df : pd.DataFrame):
        __current_df = current_df.copy()
        
        __current_df['competition_open_since_month'] = current_df['competition_open_since_month'].astype(int)
        __current_df['competition_open_since_year'] = __current_df['competition_open_since_year'].astype(int)  
        __current_df['promo2_since_week'] = __current_df['promo2_since_week'].astype(int) 
        __current_df['promo2_since_year'] = __current_df['promo2_since_year'].astype(int) 

        return __current_df
    

    def _feature_enginnering(self, 
                            current_df : pd.DataFrame):

        __current_df = current_df.copy()

        # year 
        __current_df['year'] = __current_df.date.dt.year

        # month 
        __current_df['month'] = __current_df.date.dt.month 

        # day
        __current_df['day'] = __current_df.date.dt.day

        # week of year 
        __current_df['week_year'] = __current_df.date.dt.isocalendar().week

        # year-week
        __current_df['year_week'] = __current_df.date.dt.strftime('%Y-%W')

        # competition since 
        __current_df['competion_open_date_temp'] = pd.to_datetime(__current_df.apply(lambda x:  datetime.date( x['competition_open_since_year'], \
                                                                        x['competition_open_since_month'],1), axis = 1))



        __current_df['competion_since_days'] = (__current_df['date'] - __current_df['competion_open_date_temp']).dt.days 
        __current_df['competion_since_month'] = ( (__current_df['date'] - __current_df['competion_open_date_temp']).dt.days/30).astype('int') 


        # promo since


        __current_df['promo2_since_year_week_temp'] = (__current_df.apply(lambda x: str(x['promo2_since_year']) + '-' + str(x['promo2_since_week']), axis = 1))


        __current_df['promo2_since'] = __current_df['promo2_since_year_week_temp'].apply( lambda x: datetime.datetime.strptime(x + '-1', '%Y-%W-%w') - datetime.timedelta(days = 7))

        __current_df['promo2_time_week'] = ( ( __current_df['date'] - __current_df['promo2_since'] )/7 ).apply(lambda x: x.days ).astype( int )

        # assortment 
        assortment_map = {
            'a' : 'basic',
            'b' : 'extra',
            'c' : 'etended'
        }

        __current_df.loc[:,'assortment'] = __current_df['assortment'].apply(lambda x: assortment_map[x])

        # state holiday

        state_holiday_map = {
            'a' : 'public_holiday',
            'b' : 'easter_holiday',
            'c' : 'christmas',
            '0' : 'regular_day'
        }

        __current_df.loc[:, 'state_holiday'] = __current_df.state_holiday.apply(lambda x: state_holiday_map[x])

        return __current_df 
    

    def _feature_selection(self, 
                          current_df):

        __current_df = current_df.copy()
        cols_drop_base = ['customers', 'open', 'competion_open_date_temp', 'promo2_since_year_week_temp']
        cols_drop = [x for x in cols_drop_base if x in __current_df.columns]
       # __current_df = __current_df[(__current_df.open != 0) & (__current_df.sales) > 0]
        __current_df = __current_df[(__current_df.open != 0)]
        __current_df = __current_df.drop(cols_drop, axis= 1)

        cols_selected = [
            'store',
            'promo',
            'school_holiday',
            'store_type',
            'assortment',
            'competition_distance',
            'competition_open_since_year',
            'promo2',
            'promo2_since_year',
            'competion_since_month',
            'promo2_time_week'

         ]
        

        return __current_df[cols_selected]
        

    def _feature_transformation(self, current_df):
        __current_df = current_df.copy()

        continuous_data = ['competition_distance',  'competition_open_since_year',  
                           'competion_since_days',  'year','promo2_time_week']
        
        robust_scallers = ['competition_distance', 'competion_since_days', 
                           'competion_since_month', 'promo2_since_year']
        
        outros_continuos = list(set(continuous_data) - set(robust_scallers))
        
        X = __current_df[robust_scallers].values
        __current_df[robust_scallers] =  self.robust_scaller.transform(X)

        X = __current_df[outros_continuos].values
        __current_df[outros_continuos] =  self.minMax_scaller.transform(X)


        __current_df = pd.get_dummies(__current_df, prefix = ['state_holiday'], columns = ['state_holiday'], dtype=float)
        store_type = self.label_enconder.transform(__current_df.store_type)
        __current_df.loc[:, 'store_type'] = store_type
        

        # assortment 
        # O sortimento possui uma caracteristica ordinal
        # extended > extra > basic
        dict_assortment = {
            'basic' : 0,
            'extra' : 1,
            'extended' : 2
        }
        __current_df.loc[:, 'assortment'] = __current_df.assortment.apply(lambda x: 'extended' if x == 'etended' else x)
        __current_df.loc[:, 'assortment'] = __current_df.assortment.apply(lambda x: dict_assortment[x])


       # __current_df.loc[:, 'sales'] = np.log1p(__current_df.sales.values)
        __current_df[['store_type', 'assortment']] = __current_df[['store_type', 'assortment']].astype('int16')


        return __current_df