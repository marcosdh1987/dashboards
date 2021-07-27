from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, View
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from numpy.core.numeric import flatnonzero

from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
from plotly.subplots import make_subplots

from datetime import datetime, timedelta

from django.contrib.staticfiles.storage import staticfiles_storage

#variables and parameters for views

starttime = datetime.now()
#starttime = pd.to_datetime('2021-07-12 06:00:00')

#import for SQL connections
import pyodbc
from sqlalchemy import create_engine

#azure DB connection
"""
server = 'daqsamsrv01.database.windows.net'        
database = 'daqdb01'
username = 'marcos'
password = 'Asdf*123'   
driver= '{ODBC Driver 17 for SQL Server}'
"""
#postgresql connection
# Postgres username, password, and database name
POSTGRES_ADDRESS = '192.168.0.7'   #or 192.168.0.7 , melectronica.ddns.net
POSTGRES_PORT = '5432'
POSTGRES_USERNAME = 'marcosdb' 
POSTGRES_PASSWORD = '32922161' 
POSTGRES_DBNAME = 'mydb' 
# A long string that contains the necessary Postgres login information
postgres_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'
.format(username=POSTGRES_USERNAME,
password=POSTGRES_PASSWORD,
ipaddress=POSTGRES_ADDRESS,
port=POSTGRES_PORT,
dbname=POSTGRES_DBNAME))



#the default view
class HomeView(View):
    
    def get(self, *args, **kwargs):
 
        context = {             
                    }                                                             

        return render(self.request, 'home.html', context)



#Main dashboard view, with overall information, based on analytics view
class dashboardView(View):
    
    def get(self, *args, **kwargs):
        
        cur = 'dashboard'                           # to change text active in the left nav bar
        cur1 = 'Overall'                            # to add information to the title 
        
        url = 'static/ds/compared_data_full.csv'    # to read files from static folder
        
        ds = pd.read_csv(url)

        gassep = ds['GasFlowRate'].mean().round(1)
        gasfsf = ds['QgStd[m3/d]'].mean().round(1)
        difg = (100*(gassep - gasfsf)/gassep).mean().round(2)
        oilsep = ds['OilFlowRate'].mean().round(1)
        oilfsf = ds['QoStd[m3/d]'].mean().round(1)
        difo = (100*(oilsep - oilfsf)/oilsep).mean().round(2)
        watersep = ds['WaterFlowRate'].mean().round(1)
        waterfsf = ds['QwStd[m3/d]'].mean().round(1)
        difw = (100*(watersep - waterfsf) / watersep).mean().round(2)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ds['Time_x'], y=ds['GasFlowRate'], name="Separator",
                            line_shape='linear'))
        fig.add_trace(go.Scatter(x=ds['Time_x'], y=ds['QgStd[m3/d]'], name="Foresite Flow",
                            line_shape='spline'))
        fig.update_layout(hovermode='x unified',title="Gas Flow Rates",margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=40, #top margin
        ))
        fig.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01)) #to use legend inside of plot
        fig.update_yaxes(title_text="<b>Flow Rate</b> (m3/d)")
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=ds['Time_x'], y=ds['OilFlowRate'], name="Separator",
                            line_shape='linear'))
        fig2.add_trace(go.Scatter(x=ds['Time_x'], y=ds['QoStd[m3/d]'], name="Foresite Flow",
                            line_shape='spline'))
        fig2.update_layout(hovermode='x unified',title="Oil Flow Rates",margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=40, #top margin
        ))
        fig2.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01)) #to use legend inside of plot
        fig2.update_yaxes(title_text="<b>Flow Rate</b> (m3/d)")
        
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=ds['Time_x'], y=ds['WaterFlowRate'], name="Separator",
                            line_shape='linear'))
        fig3.add_trace(go.Scatter(x=ds['Time_x'], y=ds['QwStd[m3/d]'], name="Foresite Flow",
                            line_shape='spline'))
        fig3.update_layout(hovermode='x unified',title="Water Flow Rates",margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=40, #top margin
        ))
        fig3.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01)) #to use legend inside of plot
        fig3.update_yaxes(title_text="<b>Flow Rate</b> (m3/d)")
        
        fig4 = go.Figure()
        fig4 = make_subplots(specs=[[{'secondary_y': True}]])
        fig4.add_trace(go.Scatter(x=ds['Time_x'], y=ds['WHP'], name="Well Head Pressure",
                            line_shape='linear'), secondary_y=False)
        fig4.add_trace(go.Scatter(x=ds['Time_x'], y=ds['WHT'], name="Well Head Temperature",
                            line_shape='spline'), secondary_y=True)
        fig4.update_layout(hovermode='x unified',title="Well Head Pressure & Temperature",margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=40, #top margin
        ))
        fig4.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01)) #to use legend inside of plot
        # Set y-axes titles
        fig4.update_yaxes(title_text="<b>Pressure</b> (Psig)", secondary_y=False)
        fig4.update_yaxes(title_text="<b>Temperature</b> (°C)", secondary_y=True)

        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(x=ds['Time_x'], y=ds['sp'], name="Separator Pressure",
                            line_shape='linear'))
        fig5.add_trace(go.Scatter(x=ds['Time_x'], y=(ds['Pressure[Bar]']*14.5038), name="ForeSite Flow Pressure",
                            line_shape='spline'))
        fig5.update_layout(hovermode='x unified',title="Meters Pressure",margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=40, #top margin
        ))
        fig5.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01)) #to use legend inside of plot
        fig5.update_yaxes(title_text="<b>Pressure</b> (Psig)")

        fig6 = go.Figure()
        fig6.add_trace(go.Scatter(x=ds['Time_x'], y=ds['gasT'], name="Separator Gas Temperature",
                            line_shape='linear'))
        fig6.add_trace(go.Scatter(x=ds['Time_x'], y=ds['Temperature[C]'], name="ForeSite Flow Temperature",
                            line_shape='spline'))
        fig6.update_layout(hovermode='x unified',title="Meters Temperature[C]",margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=40, #top margin
        ))
        fig6.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01)) #to use legend inside of plot
        fig6.update_yaxes(title_text="<b>Temperature</b> (°C)")


        # Setting layout of the figure.
        layout = {
            'title': 'Productions Flow rates comparison',
            'xaxis_title': 'X',
            'yaxis_title': 'Y',
        }

        # Getting HTML needed to render the plot.
        plot_div = plot({'data': fig, 'layout': layout}, 
                        output_type='div')
        plot_div2 = plot({'data': fig2, 'layout': layout}, 
                        output_type='div')
        plot_div3 = plot({'data': fig3, 'layout': layout}, 
                        output_type='div')
        plot_div4 = plot({'data': fig4, 'layout': layout}, 
                        output_type='div')
        plot_div5 = plot({'data': fig5, 'layout': layout}, 
                        output_type='div')
        plot_div6 = plot({'data': fig6, 'layout': layout}, 
                        output_type='div')
        
        context = {  'plot_div' : plot_div  , 'plot_div2': plot_div2,
                     'plot_div3': plot_div3 , 'plot_div4':plot_div4, 
                     'plot_div5':plot_div5, 'plot_div6':plot_div6, 
                     'cur':cur, 'cur1':cur1
                    ,'gassep':gassep , 'gasfsf':gasfsf , 'oilsep':oilsep , 'oilfsf':oilfsf, 'waterfsf':waterfsf, 'watersep':watersep, 
                    'difg':difg,'difw':difw,'difo':difo,
                    }                                                            

        return render(self.request, 'analytics.html', context)

#Today Analytics view, with the las 24hs of information, based on analytics view
class analyticsView(View):
    
    def get(self, *args, **kwargs):
        
        cur = 'analytics'                           # to change text active in the left nav bar
        cur1 = 'Last 24hs '                         # to add information to the title 
        
        url = 'static/ds/compared_data_full.csv'    # to read files from static folder 
        
        ds = pd.read_csv(url)

        ds['Time_hs'] = pd.to_datetime(ds['Time_hs'])

        mask = (ds['Time_hs'] > (starttime- timedelta(hours=24))) & (ds['Time_hs'] <= starttime)

        ds = ds.loc[mask]

        gassep = round(ds['GasFlowRate'].mean(),1)
        gasfsf = round(ds['QgStd[m3/d]'].mean(),1)
        difg = round((100*(gassep - gasfsf)/gassep).mean(),2)
        oilsep = round(ds['OilFlowRate'].mean(),1)
        oilfsf = round(ds['QoStd[m3/d]'].mean(),1)
        difo = round((100*(oilsep - oilfsf)/oilsep).mean(),2)
        watersep = round(ds['WaterFlowRate'].mean(),1)
        waterfsf = round(ds['QwStd[m3/d]'].mean(),1)
        difw = round((100*(watersep - waterfsf) / watersep).mean(),2)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ds['Time_x'], y=ds['GasFlowRate'], name="Separator",
                            line_shape='linear'))
        fig.add_trace(go.Scatter(x=ds['Time_x'], y=ds['QgStd[m3/d]'], name="Foresite Flow",
                            line_shape='spline'))
        fig.update_layout(hovermode='x unified',title="Gas Flow Rates",margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=40, #top margin
        ))
        fig.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01)) #to use legend inside of plot
        fig.update_yaxes(title_text="<b>Flow Rate</b> (m3/d)")
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=ds['Time_x'], y=ds['OilFlowRate'], name="Separator",
                            line_shape='linear'))
        fig2.add_trace(go.Scatter(x=ds['Time_x'], y=ds['QoStd[m3/d]'], name="Foresite Flow",
                            line_shape='spline'))
        fig2.update_layout(hovermode='x unified',title="Oil Flow Rates",margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=40, #top margin
        ))
        fig2.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01)) #to use legend inside of plot
        fig2.update_yaxes(title_text="<b>Flow Rate</b> (m3/d)")
        
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=ds['Time_x'], y=ds['WaterFlowRate'], name="Separator",
                            line_shape='linear'))
        fig3.add_trace(go.Scatter(x=ds['Time_x'], y=ds['QwStd[m3/d]'], name="Foresite Flow",
                            line_shape='spline'))
        fig3.update_layout(hovermode='x unified',title="Water Flow Rates",margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=40, #top margin
        ))
        fig3.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01)) #to use legend inside of plot
        fig3.update_yaxes(title_text="<b>Flow Rate</b> (m3/d)")
        
        fig4 = go.Figure()
        fig4 = make_subplots(specs=[[{'secondary_y': True}]])
        fig4.add_trace(go.Scatter(x=ds['Time_x'], y=ds['WHP'], name="Well Head Pressure",
                            line_shape='linear'), secondary_y=False)
        fig4.add_trace(go.Scatter(x=ds['Time_x'], y=ds['WHT'], name="Well Head Temperature",
                            line_shape='spline'), secondary_y=True)
        fig4.update_layout(hovermode='x unified',title="Well Head Pressure & Temperature",margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=40, #top margin
        ))
        fig4.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01)) #to use legend inside of plot
        # Set y-axes titles
        fig4.update_yaxes(title_text="<b>Pressure</b> (Psig)", secondary_y=False)
        fig4.update_yaxes(title_text="<b>Temperature</b> (°C)", secondary_y=True)

        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(x=ds['Time_x'], y=ds['sp'], name="Separator Pressure",
                            line_shape='linear'))
        fig5.add_trace(go.Scatter(x=ds['Time_x'], y=(ds['Pressure[Bar]']*14.5038), name="ForeSite Flow Pressure",
                            line_shape='spline'))
        fig5.update_layout(hovermode='x unified',title="Meters Pressure",margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=40, #top margin
        ))
        fig5.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01)) #to use legend inside of plot
        fig5.update_yaxes(title_text="<b>Pressure</b> (Psig)")

        fig6 = go.Figure()
        fig6.add_trace(go.Scatter(x=ds['Time_x'], y=ds['gasT'], name="Separator Gas Temperature",
                            line_shape='linear'))
        fig6.add_trace(go.Scatter(x=ds['Time_x'], y=ds['Temperature[C]'], name="ForeSite Flow Temperature",
                            line_shape='spline'))
        fig6.update_layout(hovermode='x unified',title="Meters Temperature[C]",margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=40, #top margin
        ))
        fig6.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01)) #to use legend inside of plot
        fig6.update_yaxes(title_text="<b>Temperature</b> (°C)")


        # Setting layout of the figure.
        layout = {
            'title': 'Productions Flow rates comparison',
            'xaxis_title': 'X',
            'yaxis_title': 'Y',
        }

        # Getting HTML needed to render the plot.
        plot_div = plot({'data': fig, 'layout': layout}, 
                        output_type='div')
        plot_div2 = plot({'data': fig2, 'layout': layout}, 
                        output_type='div')
        plot_div3 = plot({'data': fig3, 'layout': layout}, 
                        output_type='div')
        plot_div4 = plot({'data': fig4, 'layout': layout}, 
                        output_type='div')
        plot_div5 = plot({'data': fig5, 'layout': layout}, 
                        output_type='div')
        plot_div6 = plot({'data': fig6, 'layout': layout}, 
                        output_type='div')
        
        context = {  'plot_div' : plot_div  , 'plot_div2': plot_div2,
                     'plot_div3': plot_div3 , 'plot_div4':plot_div4, 
                     'plot_div5':plot_div5, 'plot_div6':plot_div6, 
                     'cur':cur, 'cur1':cur1
                    ,'gassep':gassep , 'gasfsf':gasfsf , 'oilsep':oilsep , 'oilfsf':oilfsf, 'waterfsf':waterfsf, 'watersep':watersep, 
                    'difg':difg,'difw':difw,'difo':difo,
                    }          
        return render(self.request, 'analytics.html', context)


# Foresite flow production information, based on data_dash 
class fsfdataView(View):
    
    def get(self, *args, **kwargs):
        
        cur = 'fsfdata'                             # to change text active in the left nav bar
        cur1 = 'ForeSite Flow '                     # to add information to the title 
        
        url4 = 'static/ds/compared_data_full.csv'   # to read files from static folder 

        ds4 = pd.read_csv(url4)

        ds4['Time_hs'] = pd.to_datetime(ds4['Time_hs'])

        mask = (ds4['Time_hs'] > (starttime- timedelta(hours=24))) & (ds4['Time_hs'] <= starttime)

        ds24 = ds4.loc[mask]

        gas = round(ds24['QgStd[m3/d]'].astype(float).mean(),1)
        oil = round(ds24['QoStd[m3/d]'].astype(float).mean(),1)
        water = round(ds24['QwStd[m3/d]'].astype(float).mean(),1)
        whp = round(ds24['WHP'].astype(float).mean(),1)
        wht = round(ds24['WHT'].astype(float).mean(),1)
        sp = round(ds24['Pressure[Bar]'].astype(float).mean()*14.5038,1)
        st = round(ds24['Temperature[C]'].astype(float).mean(),1)
        ot = round(ds24['Temperature[C]'].astype(float).mean(),1)
        wc = round(ds24['WWC[%]'].astype(float).mean(),1)
        gor = round((gas / oil),1)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ds24['Time_hs'], y=ds24['QgStd[m3/d]'].astype(float), name="Gas Flow Rate", text='m3/d',
                            line_shape='linear',
                            line=dict(color='darkgray', width=4)))

        fig.update_traces(hoverinfo='name+y+text', mode='markers+lines')
        fig.update_layout(title="Gas Flow Rate",margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=40, #top margin
        ))
        fig.update_yaxes(title_text="<b>Flow Rate</b> (m3/d)")

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=ds24['Time_hs'], y=ds24['QoStd[m3/d]'].astype(float), name="Oil Flow Rate", text='m3/d',
                            line_shape='linear',
                            line=dict(color='darkgreen', width=4)))

        fig2.update_traces(hoverinfo='name+y+text', mode='markers+lines')
        fig2.update_layout(title="Oil Flow Rate",margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=40, #top margin
        ))
        fig2.update_yaxes(title_text="<b>Flow Rate</b> (m3/d)")

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=ds24['Time_hs'], y=ds24['QwStd[m3/d]'].astype(float), name="Water Flow Rate", text='m3/d',
                            line_shape='linear',
                            line=dict(color='lightskyblue', width=4)))

        fig3.update_traces(hoverinfo='name+y+text', mode='markers+lines')
        fig3.update_layout(title="Water Flow Rate",margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=40, #top margin
        ))
        fig3.update_yaxes(title_text="<b>Flow Rate</b> (m3/d)")


        fig4 = go.Figure()
        fig4 = make_subplots(specs=[[{'secondary_y': True}]])
        fig4.add_trace(go.Scatter(x=ds24['Time_hs'], y=round(ds24['Pressure[Bar]'].astype(float)*14.5038,2), name="Flow Line Pressure",
                            line_shape='linear'), secondary_y=False)
        fig4.add_trace(go.Scatter(x=ds24['Time_hs'], y=round(ds24['Temperature[C]'].astype(float),2), name="Flow Line Temperature",
                            line_shape='spline'), secondary_y=True)
        fig4.update_layout(hovermode='x unified',title="Meter Pressure & Temperature",margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=40, #top margin
        ))
        fig4.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01)) #to use legend inside of plot
        # Set y-axes titles
        fig4.update_yaxes(title_text="<b>Pressure</b> (Psig)", secondary_y=False)
        fig4.update_yaxes(title_text="<b>Temperature</b> (°C)", secondary_y=True)

        # Setting layout of the figure.
        layout = {
            'title': 'Productions Flow rates',
            'xaxis_title': 'X',
            'yaxis_title': 'Y',
        }

        # Getting HTML needed to render the plot.
        plot_div = plot({'data': fig, 'layout': layout}, 
                        output_type='div')
        plot_div2 = plot({'data': fig2, 'layout': layout}, 
                        output_type='div')
        plot_div3 = plot({'data': fig3, 'layout': layout}, 
                        output_type='div')
        plot_div4 = plot({'data': fig4, 'layout': layout}, 
                        output_type='div')                


        context = {  'plot_div' : plot_div  , 'plot_div2': plot_div2
                    ,'plot_div3': plot_div3 ,'plot_div4': plot_div4 ,
                     'cur1':cur1
                    ,'cur':cur,'gas':gas , 'oil':oil , 'water':water
                    ,'whp':whp, 'wht':wht , 'wc':wc , 'gor':gor 
                    ,'sp':sp , 'st':st , 'ot':ot                             
                    }                                                            

        return render(self.request, 'data_dash.html', context)

# Separator flow production information, based on data_dash 
class sepdataView(View):
    
    def get(self, *args, **kwargs):
        
        cur = 'sepdata'                             # to change text active in the left nav bar
        cur1 = 'Separator '                         # to add information to the title 
    
        url4 = 'static/ds/compared_data_full.csv'
        
        ds4 = pd.read_csv(url4)

        ds4['Time_hs'] = pd.to_datetime(ds4['Time_hs'])

        mask = (ds4['Time_hs'] > (starttime- timedelta(hours=24))) & (ds4['Time_hs'] <= starttime)

        ds24 = ds4.loc[mask]

        gas = round(ds24['GasFlowRate'].astype(float).mean(),1)
        oil = round(ds24['OilFlowRate'].astype(float).mean(),1)
        water = round(ds24['WaterFlowRate'].astype(float).mean(),1)
        whp = round(ds24['WHP'].astype(float).mean(),1)
        wht = round(ds24['WHT'].astype(float).mean(),1)
        sp = round(ds24['sp'].astype(float).mean(),1)
        st = round(ds24['gasT'].astype(float).mean(),1)
        ot = round(ds24['OilTemp'].astype(float).mean(),1)
        wc = round(ds24['WCFlow'].astype(float).mean(),1)
        gor = round((gas / oil),1)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ds24['Time_hs'], y=ds24['GasFlowRate'].astype(float), name="Gas Flow Rate", text='m3/d',
                            line_shape='linear',
                            line=dict(color='darkgray', width=4)))

        fig.update_traces(hoverinfo='name+y+text', mode='markers+lines')
        fig.update_layout(title="Gas Flow Rate",margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=40, #top margin
        ))
        fig.update_yaxes(title_text="<b>Flow Rate</b> (m3/d)")

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=ds24['Time_hs'], y=ds24['OilFlowRate'].astype(float), name="Oil Flow Rate", text='m3/d',
                            line_shape='linear',
                            line=dict(color='darkgreen', width=4)))

        fig2.update_traces(hoverinfo='name+y+text', mode='markers+lines')
        fig2.update_layout(title="Oil Flow Rate",margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=40, #top margin
        ))
        fig2.update_yaxes(title_text="<b>Flow Rate</b> (m3/d)")

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=ds24['Time_hs'], y=ds24['WaterFlowRate'].astype(float), name="Water Flow Rate", text='m3/d',
                            line_shape='linear',
                            line=dict(color='lightskyblue', width=4)))

        fig3.update_traces(hoverinfo='name+y+text', mode='markers+lines')
        fig3.update_layout(title="Water Flow Rate",margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=40, #top margin
        ))
        fig3.update_yaxes(title_text="<b>Flow Rate</b> (m3/d)")

        fig4 = go.Figure()
        fig4 = make_subplots(specs=[[{'secondary_y': True}]])
        fig4.add_trace(go.Scatter(x=ds24['Time_hs'], y=round(ds24['sp'].astype(float),2), name="Separator Gas Pressure",
                            line_shape='linear'), secondary_y=False)
        fig4.add_trace(go.Scatter(x=ds24['Time_hs'], y=round(ds24['gasT'].astype(float),2), name="Separator Gas Temperature",
                            line_shape='spline'), secondary_y=True)
        fig4.update_layout(hovermode='x unified',title="Separator Pressure & Temperature",margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=40, #top margin
        ))
        fig4.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01)) #to use legend inside of plot
        # Set y-axes titles
        fig4.update_yaxes(title_text="<b>Pressure</b> (Psig)", secondary_y=False)
        fig4.update_yaxes(title_text="<b>Temperature</b> (°C)", secondary_y=True)

        # Setting layout of the figure.
        layout = {
            'title': 'Productions Flow rates',
            'xaxis_title': 'X',
            'yaxis_title': 'Y',
        }

        # Getting HTML needed to render the plot.
        plot_div = plot({'data': fig, 'layout': layout}, 
                        output_type='div')
        plot_div2 = plot({'data': fig2, 'layout': layout}, 
                        output_type='div')
        plot_div3 = plot({'data': fig3, 'layout': layout}, 
                        output_type='div')
        plot_div4 = plot({'data': fig4, 'layout': layout}, 
                        output_type='div')                

        context = {  'plot_div' : plot_div  , 'plot_div2': plot_div2
                    ,'plot_div3': plot_div3 , 'plot_div4': plot_div4,
                    'cur1':cur1
                    ,'cur':cur,'gas':gas , 'oil':oil , 'water':water
                    ,'whp':whp, 'wht':wht , 'wc':wc , 'gor':gor 
                    ,'sp':sp , 'st':st , 'ot':ot                             
                    }                                                               

        return render(self.request, 'data_dash.html', context)

# Realtime data view, data from sql information
class realtimeView(View):
    
    def get(self, *args, **kwargs):
        
        cur = 'realtime'                            # to change text active in the left nav bar
        starttime = datetime.now()

        #azure connection
        """
        cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()
        # Insert Dataframe into SQL Server:

        query = "SELECT * FROM modbus_data"

        ds = pd.read_sql(query,cnxn)

        cnxn.commit()
        cursor.close()
        """

        #postgresql connection
        cnx = create_engine(postgres_str)

        df = pd.read_sql_query('''SELECT * FROM modbus_data WHERE "created_on" BETWEEN NOW() - INTERVAL '6 HOURS' AND NOW()''', con=cnx)

        #convert data
        d1 = pd.pivot_table(df,values=['value'],
                index=['created_on'],
                columns=['description'], aggfunc='first')

        flat = pd.DataFrame(d1.to_records())
        flat.columns = [hdr.replace("('value', '", "").replace("')", "") \
                            for hdr in flat.columns]

        mask = (flat['created_on'] > (starttime- timedelta(hours=6))) & (flat['created_on'] <= starttime)
        flat2 = flat.copy()

        flat = flat.loc[mask]

        mask1 = (flat2['created_on'] > (starttime- timedelta(hours=4))) & (flat2['created_on'] <= starttime)

        flat2 = flat2.loc[mask1]

        gas = round(flat2['Qg – Standard Conditions'].astype(float).mean(),1)
        oil = round(flat2['Qo – Standard Conditions'].astype(float).mean(),1)
        water = round(flat2['Qw – Standard Conditions'].astype(float).mean(),1)
        lpress = round(flat2['MVT Static Pressure'].astype(float).mean()*14.5038,1)
        ltemp = round(flat2['MVT Temperature'].astype(float).mean(),1)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=flat['created_on'], y=flat['Qg – Standard Conditions'].astype(float), name="Gas Flow Rate", text='m3/d',
                            line_shape='linear',
                            line=dict(color='darkgray', width=4)))

        fig.update_traces(hoverinfo='name+y+text', mode='markers+lines')
        fig.update_layout(title="Gas Flow Rate",margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=40, #top margin
        ))
        fig.update_yaxes(title_text="<b>Flow Rate</b> (m3/d)")
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=flat['created_on'], y=flat['Qo – Standard Conditions'].astype(float), name="Oil Flow Rate", text='m3/d',
                            line_shape='linear',
                            line=dict(color='darkgreen', width=4)))

        fig2.update_traces(hoverinfo='name+y+text', mode='markers+lines')
        fig2.update_layout(title="Oil Flow Rate",margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=40, #top margin
        ))
        fig2.update_yaxes(title_text="<b>Flow Rate</b> (m3/d)")
        
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=flat['created_on'], y=flat['Qw – Standard Conditions'].astype(float), name="Water Flow Rate", text='m3/d',
                            line_shape='linear',
                            line=dict(color='lightskyblue', width=4)))

        fig3.update_traces(hoverinfo='name+y+text', mode='markers+lines')
        fig3.update_layout(title="Water Flow Rate",margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=40, #top margin
        ))
        fig3.update_yaxes(title_text="<b>Flow Rate</b> (m3/d)")

        fig4 = go.Figure()
        fig4 = make_subplots(specs=[[{'secondary_y': True}]])
        fig4.add_trace(go.Scatter(x=flat['created_on'], y=round(flat['MVT Static Pressure'].astype(float)*14.5038,2), name="Flow Line Pressure",
                            line_shape='linear'), secondary_y=False)
        fig4.add_trace(go.Scatter(x=flat['created_on'], y=round(flat['MVT Temperature'].astype(float),2), name="Flow Line Temperature",
                            line_shape='spline'), secondary_y=True)
        fig4.update_layout(hovermode='x unified',title="Separator Pressure & Temperature",margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=40, #top margin
        ))
        fig4.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01)) #to use legend inside of plot
        # Set y-axes titles
        fig4.update_yaxes(title_text="<b>Pressure</b> (Psig)", secondary_y=False)
        fig4.update_yaxes(title_text="<b>Temperature</b> (°C)", secondary_y=True)

        # Setting layout of the figure.
        layout = {
            'title': 'Productions Flow rates',
            'xaxis_title': 'X',
            'yaxis_title': 'Y',
        }

        # Getting HTML needed to render the plot.
        plot_div = plot({'data': fig, 'layout': layout}, 
                        output_type='div')
        plot_div2 = plot({'data': fig2, 'layout': layout}, 
                        output_type='div')
        plot_div3 = plot({'data': fig3, 'layout': layout}, 
                        output_type='div')
        plot_div4 = plot({'data': fig4, 'layout': layout}, 
                        output_type='div')

        context = {  'plot_div' : plot_div  , 'plot_div2': plot_div2
                    ,'plot_div3': plot_div3 , 'plot_div4': plot_div4 ,
                    
                    'cur':cur,  'gas':gas , 'oil':oil , 'water':water , 'lpress':lpress , 'ltemp':ltemp ,                          
                    }                                                             

        return render(self.request, 'realtimechart.html', context)