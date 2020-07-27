import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import plotly.offline as pyoff
import plotly.express as  px
import numpy as np
import pandas as pd
from fbprophet.plot import plot_plotly
import plotly.offline as py
import streamlit as st
from PIL import Image

################### Cleaning Data ####################
def clean(forecast, who):
    forecast.index = forecast['ds']
    forecast['ds'] = pd.to_datetime(forecast['ds'])
    who.index = forecast.iloc[:len(who)].index
    who['ds'] = forecast['ds']
    who['week'] = forecast['week']
    who['month'] = forecast['month']
    who = who.fillna(0)

    return (forecast,who)



################### Plotting Graphs ###################

def plot(forecast, who):
    print('hello')
    st.header('Prediction challenge: USA COVID-19 positive cases')
    image = Image.open('/Users/admin/Documents/project/images/corona.jpg')
    st.image(image, caption='Source: news.uchicago.edu/',
             use_column_width=True)
    st.header('Data Visualization')

    ##### first Graph
    fig=go.Figure()
    fig.add_trace(go.Scatter(
        x=who.ds,
        y=who.new_cases,
        mode="lines+markers"
    ))

    fig.update_layout(
        title=" PLOT OF NEW CASES , EVERYDAY ",
        xaxis_title="Date",
        yaxis_title="Cases",
        font_color='black',
        plot_bgcolor="#f8f8f8"
    )

    fig.update_xaxes(title_font_family="ARIAL",title_font_color="black",title_font_size=12)
    fig.update_yaxes(title_font_family="ARIAL",title_font_size=12,title_font_color="black")
    st.plotly_chart(fig)

    ##### Second Graph
    fig=go.Figure()
    fig.add_trace(go.Scatter(
        x=who.ds,
        y=who.total_cases,
        mode="markers"
    ))

    fig.update_layout(
        title=" PLOT OF TOTAL CASES PER DAY ",
        xaxis_title="Date",
        yaxis_title="Total_Cases",
        font_color='black',
        plot_bgcolor="#f8f8f8"
    )

    fig.update_xaxes(title_font_family="ARIAL",title_font_color="black",title_font_size=12)
    fig.update_yaxes(title_font_family="ARIAL",title_font_size=12,title_font_color="black")

    st.plotly_chart(fig)

    #### Third Graph
    fig=go.Figure()
    fig.add_trace(go.Scatter(
        x=who.ds,
        y=who.new_deaths,
        mode="lines+markers"
    ))

    fig.update_layout(
        title=" PLOT OF NEW DEATHS PER DAY ",
        xaxis_title="Date",
        yaxis_title="new_deaths",
        font_color='black',
        plot_bgcolor="#f8f8f8"
    )

    fig.update_xaxes(title_font_family="ARIAL",title_font_color="black",title_font_size=12)
    fig.update_yaxes(title_font_family="ARIAL",title_font_size=12,title_font_color="black")

    st.plotly_chart(fig)

    who["active_cases"]=who["new_cases"]-who["new_deaths"]
    who["total_actives"]=who["total_cases"]-who["total_deaths"]

    ###### Fourth Graph
    fig=go.Figure()

    fig.add_trace(go.Scatter(
        x=who.ds,
        y=who.active_cases,
        mode="lines+markers"
    ))

    fig.update_layout(
        title=" PLOT OF NEW ACTIVE CASES PER DAY ",
        xaxis_title="Date",
        yaxis_title="New_actual cases",
        font_color='black',
        plot_bgcolor="#f8f8f8"
    )

    fig.update_xaxes(title_font_family="ARIAL",title_font_color="black",title_font_size=12)
    fig.update_yaxes(title_font_family="ARIAL",title_font_size=12,title_font_color="black")

    st.plotly_chart(fig)

    ##### Fifth Graph
    a = who.groupby(['week'], as_index=False)[['new_cases']].sum()

    plot_data = [
        go.Bar(
            x=a.week,
            y=a.new_cases,
            marker_color='indianred'
            
            ),   
    ]
    plot_layout = go.Layout(
            title='Total number of Cases per week',
            yaxis_title='Cases',
            xaxis_title='Week',
            plot_bgcolor="#f8f8f8"
        )
    fig = go.Figure(data=plot_data, layout=plot_layout)
    st.plotly_chart(fig)

    b = who.groupby(['month'], as_index=False)[['new_cases']].sum()

    ##### Sixth Graph
    plot_data = [
        go.Bar(
            x=b.month,
            y=b.new_cases,
            width = [0.3,0.3,0.3,0.3,0.4],
            marker_color='darkcyan'
            ),   
    ]
    plot_layout = go.Layout(
            title='Total number of Cases per Month',
            yaxis_title='Cases',
            xaxis_title='Month',
            plot_bgcolor="#f8f8f8"
        )
    fig = go.Figure(data=plot_data, layout=plot_layout)
    st.plotly_chart(fig)

    ##### Seventh Graph
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=who.ds,
        y=who.new_cases,
        name=" new cases per day"
    ))


    fig.add_trace(go.Bar(
        x=who.ds,
        y=who.active_cases,
        name=" active cases per day"
    ))

    fig.update_layout(
        title="CUMMULATIVE PLOT OF NEW_ACTIVE AND TOTAL ACTIVE CASES EVERYDAY",
        xaxis_title="Date",
        yaxis_title="cases",
        font_color="black",
        plot_bgcolor="#f8f8f8",
        barmode="group"
    
    )
    fig.update_xaxes(title_font_family="ARIAL",title_font_color="black",title_font_size=12)
    fig.update_yaxes(title_font_family="ARIAL",title_font_size=12,title_font_color="black")

    st.plotly_chart(fig)


  #################################  Forecast Graphs ################################################
    
    image = Image.open('/Users/admin/Documents/project/images/pred.jpg')
    st.image(image, caption='Source: barrons.com/',
             width=300)
    st.header('Prediction Visualization')
    plot_data = [
        go.Scatter(
            x=forecast.ds,
            y=forecast['additive_terms'],
            name='additive_terms',

        ),
        go.Scatter(
            x=forecast.ds,
            y=forecast['weekly'],
            name='weekly',
            marker = dict(color = 'cyan')
        ),
        
    ]
    plot_layout = go.Layout(
            title='Weekly Trend and additive_terms',
            yaxis_title='Values',
            xaxis_title='Week',
            plot_bgcolor="#f8f8f8"
        )
    fig = go.Figure(data=plot_data, layout=plot_layout)
    st.plotly_chart(fig)


    #### Graph two
    plot_data = [
        go.Scatter(
            x=who.ds,
            y=who['new_cases'],
            name='original_cases',
            mode = 'markers',
        ),
            go.Scatter(
            x=forecast.ds,
            y=forecast['yhat'],
            name='prediction',
            mode = 'lines', 
        ),  
    ]
    plot_layout = go.Layout(
            title='Forecast_Graph',
            yaxis_title='Positive_Cases',
            xaxis_title='Month',
            plot_bgcolor="#f8f8f8"
        )
    fig = go.Figure(data=plot_data, layout=plot_layout)
    fig = fig.update_xaxes(rangeslider_visible=True)
    st.plotly_chart(fig)


    ###### Graph Third
    plot_data = [
        go.Scatter(
            x=who.ds,
            y=who['new_cases'],
            name='original_cases',
            mode = 'lines',
        ),
        go.Scatter(
            x=forecast.ds,
            y=forecast['yhat_upper'],
            name='Upper_prediction',
            line=dict( color='orange',width=2, dash='dot')
        ),
            go.Scatter(
            x=forecast.ds,
            y=forecast['yhat_lower'],
            name='Lower_prediction',
            line=dict( width=2, dash='dot')
        ),
        
    ]
    plot_layout = go.Layout(
            title='Forecast_Range_Graph',
            yaxis_title='Positive_Cases',
            xaxis_title='Month',
            plot_bgcolor="#f8f8f8"
        )
    fig = go.Figure(data=plot_data, layout=plot_layout)
    fig = fig.update_xaxes(rangeslider_visible=True)
    st.plotly_chart(fig)

   ####################  Prediction Char #######################################
    image = Image.open('/Users/admin/Documents/project/images/res_img.jpg')
    st.image(image,
            width = 300)
    st.header('Prediction Chart')
    result=pd.read_csv("/Users/admin/Documents/project/Prediction.csv")
    result = result.iloc[:,1:]
    st.dataframe(result)


    



if __name__ == "__main__":
    forecast=pd.read_csv("/Users/admin/Documents/project/prophet_data.csv")
    who=pd.read_csv("/Users/admin/Documents/project/who_data.csv")

    forecast, who = clean(forecast,who)
    plot(forecast, who)




 