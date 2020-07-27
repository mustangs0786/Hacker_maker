import warnings
warnings.filterwarnings('ignore')
import pandas as pd
from prophet import prophet_model
from sklearn.metrics import mean_squared_error
import numpy as np
from plotly_graph import clean

def dataset(data,tr_start,tr_end):
    data = data[(data.location=='United States')]
    data = data[['date','new_cases']]
    data['date'] = pd.to_datetime(data['date'])
    data.index = data.date
    
    train = data[['date','new_cases']][tr_start : tr_end]
    # Test = data[['date','new_cases']][te_start : te_end]       Used only when needed to hypertune
    
    prophet_data =train.rename(columns={'date':'ds',
                        'new_cases':'y'})
  
    return(prophet_data)


def main():
    data = pd.read_csv('/Users/admin/Documents/project/covid-data.csv')    # please change path as per your cloned location
    
    tr_start, tr_end = '2020-03-01','2020-07-24'
    # te_start, te_end = '2020-07-23','2020-07-24'            ####  Test VAlidation data creation
    prophet_data = dataset(data,tr_start,tr_end)
    Prediction_period = 22 # 15 august
    prophet_preds = prophet_model(prophet_data, Prediction_period)
    




if __name__ == "__main__": 
    main()




###################  Only For Test Scenerio in Main function  ###################################
# prophet_preds = prophet_preds.iloc[len(train):]

# print('Prophet model MSE:{}'.format(np.sqrt(mean_squared_error(Test['new_cases'],prophet_preds))))
# data_visaul=pd.read_csv("C:/Users/admin/Downloads/_USA_DATA.csv")
# clean(data)



