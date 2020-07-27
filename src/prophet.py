
from fbprophet import Prophet
from hypertune import tunning
import pandas as pd

def prophet_model(prophet_data,Prediction_period):
    # a = tunning(prophet_data,Prediction_period,Test)     uncomment it to use hypertune file to adjust fourier_order

    m = Prophet(growth='linear',
                changepoint_prior_scale = 0.5,
                n_changepoints = 200,

                seasonality_mode= 'additive',
                daily_seasonality = False,
                weekly_seasonality = True,
                yearly_seasonality= True,
            ).add_seasonality(
                name='daily',
                period=30.5,
                fourier_order= 10                    # Parameter that can be tuned
                )
        
    m.fit(prophet_data)
    future = m.make_future_dataframe(periods=Prediction_period, freq='D')
    forecast = m.predict(future).round(2)
    forecast.ds = pd.to_datetime(forecast['ds'])
    result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    print(result.tail())
    result = result.iloc[len(prophet_data):]
    result.to_csv('Prediction.csv')     # Saving the predicted values in file
    






