
# Need to used with Test Data only

# we need to send thre requied paramters

from fbprophet import Prophet
import pandas as pd
import random
import numpy as np
from sklearn.metrics import mean_squared_error
def tunning(prophet_data,Prediction_period,Test):
    a = [12,13,15,16,18,19,20,21,22,23,25,27,29,30,32,35,38]
    # sklearn.metrics.mean_absolute_error
    model_parameters = pd.DataFrame(columns = ['MAPE','Parameters'])
    for p in a:
        test = pd.DataFrame()
        print(p)
        random.seed(0)
        train_model =Prophet(changepoint_prior_scale = 0.5,
    #                          holidays_prior_scale = p['holidays_prior_scale'],
                            n_changepoints = 300,
                            seasonality_mode = 'additive',
                            weekly_seasonality=True,
                            daily_seasonality = False,
                            yearly_seasonality = True).add_seasonality(
                                    name='daily',
                                    period=30.5,
                                    fourier_order=p,
                                )
        train_model.fit(prophet_data)
        train_forecast = train_model.make_future_dataframe(periods=Prediction_period, freq='D',include_history = False)
        train_forecast = train_model.predict(train_forecast)
        test=train_forecast[['ds','yhat']]
    #     Actual = df[(df['ds']>strt) & (df['ds']<=end)]
        MAPE = np.sqrt(mean_squared_error(Test['new_cases'],abs(test['yhat'])))
        print('Mean Absolute Percentage Error(MAPE)------------------------------------',MAPE)
        model_parameters = model_parameters.append({'MAPE':MAPE,'Parameters':p},ignore_index=True)


    parameters = model_parameters.sort_values(by=['MAPE'])
    parameters = parameters.reset_index(drop=True)
    print(parameters.head())

    a = parameters['Parameters'][0]
    return a 