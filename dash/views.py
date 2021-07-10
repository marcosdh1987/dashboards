from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, View
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from numpy.core.numeric import flatnonzero

from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import plotly.figure_factory as ff

from datetime import datetime, timedelta

from django.contrib.staticfiles.storage import staticfiles_storage

# Create your views here.
#def home_view(request):
    
#    return render(request, "admin.html", {})


class HomeView(View):
    
    def get(self, *args, **kwargs):
 
        context = {             
                    }                                                             

        return render(self.request, 'home.html', context)


class dashboardView(View):
    
    def get(self, *args, **kwargs):
        """ 
        View demonstrating how to display a graph object
        on a web page with Plotly. 
        """

        cur = 'dashboard'
        import pandas as pd
        # Get data for plots.
        url = 'static/ds/compared_data_full.csv'
        #ds = pd.read_csv(r'\\192.168.0.7\3tdata\data_lake\shell_pad11\compared_data_full.csv',low_memory=False)
        ds = pd.read_csv(url)

        gas = ds['GasFlowRate'].mean().round(1)
        oil = ds['OilFlowRate'].mean().round(1)
        water = ds['WaterFlowRate'].mean().round(1)


        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ds['Time_x'], y=ds['GasFlowRate'], name="Separator",
                            line_shape='linear'))
        fig.add_trace(go.Scatter(x=ds['Time_x'], y=ds['QgStd[m3/d]'], name="Foresite Flow",
                            line_shape='spline'))

        fig.update_layout(hovermode='x unified',title="Gas Flow Rates")
        

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=ds['Time_x'], y=ds['OilFlowRate'], name="Separator",
                            line_shape='linear'))
        fig2.add_trace(go.Scatter(x=ds['Time_x'], y=ds['QoStd[m3/d]'], name="Foresite Flow",
                            
                            line_shape='spline'))

        fig2.update_layout(hovermode='x unified',title="Oil Flow Rates")
        
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=ds['Time_x'], y=ds['WaterFlowRate'], name="Separator",
                            line_shape='linear'))
        fig3.add_trace(go.Scatter(x=ds['Time_x'], y=ds['QwStd[m3/d]'], name="Foresite Flow",
                            
                            line_shape='spline'))

        fig3.update_layout(hovermode='x unified',title="Water Flow Rates")



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

        context = {  'plot_div' : plot_div  , 'plot_div2': plot_div2
                    ,'plot_div3': plot_div3 
                    ,'gas':gas , 'oil':oil , 'water':water , 'cur':cur,                               
                    }                                                             

        return render(self.request, 'dashboard.html', context)

#Today Analytics
class analyticsView(View):
    
    def get(self, *args, **kwargs):
        """ 
        View demonstrating how to display a graph object
        on a web page with Plotly. 
        """
        cur = 'analytics'
        import pandas as pd
        # Get data for plots.
        #url = staticfiles_storage.path('ds/compared_data_full.csv')
        url = 'static/ds/compared_data_full.csv'
        #ds = pd.read_csv(r'\\192.168.0.7\3tdata\data_lake\shell_pad11\compared_data_full.csv',low_memory=False)
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

        fig.update_layout(hovermode='x unified',title="Gas Flow Rates")
        

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=ds['Time_x'], y=ds['OilFlowRate'], name="Separator",
                            line_shape='linear'))
        fig2.add_trace(go.Scatter(x=ds['Time_x'], y=ds['QoStd[m3/d]'], name="Foresite Flow",
                            
                            line_shape='spline'))

        fig2.update_layout(hovermode='x unified',title="Oil Flow Rates")
        
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=ds['Time_x'], y=ds['WaterFlowRate'], name="Separator",
                            line_shape='linear'))
        fig3.add_trace(go.Scatter(x=ds['Time_x'], y=ds['QwStd[m3/d]'], name="Foresite Flow",
                            
                            line_shape='spline'))

        fig3.update_layout(hovermode='x unified',title="Water Flow Rates")
        



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
        """plot_div4 = plot({'data': fig4, 'layout': layout}, 
                        output_type='div')
        plot_div5 = plot({'data': fig5, 'layout': layout}, 
                        output_type='div')
        plot_div6 = plot({'data': fig6, 'layout': layout}, 
                        output_type='div')
"""
        context = {  'plot_div' : plot_div  , 'plot_div2': plot_div2,
                     'plot_div3': plot_div3 , 'cur':cur
                    ,'gassep':gassep , 'gasfsf':gasfsf , 'oilsep':oilsep , 'oilfsf':oilfsf, 'waterfsf':waterfsf, 'watersep':watersep, 
                    'difg':difg,'difw':difw,'difo':difo,
                    }                                                             

        return render(self.request, 'analytics.html', context)



#Current Report
class fsfdataView(View):
    
    def get(self, *args, **kwargs):
        """ 
        View demonstrating how to display a graph object
        on a web page with Plotly. 
        """
        cur = 'fsfdata'
        import pandas as pd
        # Get data for plots.
        url = 'static/ds/ds_grouped.csv'
        url2 = 'static/ds/fsf_prod.csv'
        url3 = 'static/ds/fsf_prod_post_table.csv'
        url4 = 'static/ds/compared_data_full.csv'
        
        #ds = pd.read_csv(r'D:\OneDrive\OneDrive - WFT\Compartido\Well_Datasets\La_Calera_Pluspetrol\Post_Process\Analytics_files\df\ds_grouped.csv',low_memory=False)
        #ds2 = pd.read_csv(r'D:\OneDrive\OneDrive - WFT\Compartido\Well_Datasets\La_Calera_Pluspetrol\Post_Process\Analytics_files\df\fsf_prod.csv')
        #ds3 = pd.read_csv(r'D:\OneDrive\OneDrive - WFT\Compartido\Well_Datasets\La_Calera_Pluspetrol\Post_Process\Analytics_files\df\fsf_prod_post_table.csv')

        ds = pd.read_csv(url)
        ds2 = pd.read_csv(url2)
        ds3 = pd.read_csv(url3)
        ds4 = pd.read_csv(url4)

        ds4['Time_hs'] = pd.to_datetime(ds4['Time_hs'])

        mask = (ds4['Time_hs'] > (datetime.now()- timedelta(hours=5))) & (ds4['Time_hs'] <= datetime.now())

        ds24 = ds4.loc[mask]

        gas = ds24['QgStd[m3/d]'].astype(float).mean().round(1)
        oil = ds24['QoStd[m3/d]'].astype(float).mean().round(1)
        water = ds24['QwStd[m3/d]'].astype(float).mean().round(1)
        whp = ds24['WHP'].astype(float).mean().round(1)
        wht = ds24['WHT'].astype(float).mean().round(1)
        sp = ds24['Pressure[Bar]'].astype(float).mean().round(1) * 14.5038
        st = ds24['Temperature[C]'].astype(float).mean().round(1)
        ot = ds24['Temperature[C]'].astype(float).mean().round(1)
        wc = ds24['WWC[%]'].astype(float).mean().round(1)
        gor = gas / oil
        

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ds4['Time_hs'], y=ds4['QgStd[m3/d]'].astype(float), name="Gas Flow Rate", text='m3/d',
                            line_shape='linear',
                            line=dict(color='darkgray', width=4)))

        fig.update_traces(hoverinfo='name+y+text', mode='markers+lines')
        fig.update_layout(title="Gas Flow Rate")


        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=ds4['Time_hs'], y=ds4['QoStd[m3/d]'].astype(float), name="Oil Flow Rate", text='m3/d',
                            line_shape='linear',
                            line=dict(color='darkgreen', width=4)))

        fig2.update_traces(hoverinfo='name+y+text', mode='markers+lines')
        fig2.update_layout(title="Oil Flow Rate")


        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=ds4['Time_hs'], y=ds4['QwStd[m3/d]'].astype(float), name="Water Flow Rate", text='m3/d',
                            line_shape='linear',
                            line=dict(color='lightskyblue', width=4)))

        fig3.update_traces(hoverinfo='name+y+text', mode='markers+lines')
        fig3.update_layout(title="Water Flow Rate")



        fig4 = px.box(ds2, x='pad', color='Meter', y="Oil Flow Sm3/d")
        fig5 = px.box(ds2, x='pad', color='Meter', y="Water Flow Rate m3/d")

        fig6 = ff.create_table(ds3, index=False,height_constant=25)


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
        plot_div5 = plot({'data': fig5, 'layout': layout}, 
                        output_type='div')
        plot_div6 = plot({'data': fig6, 'layout': layout}, 
                        output_type='div')

        context = {  'plot_div' : plot_div  , 'plot_div2': plot_div2
                    ,'plot_div3': plot_div3 , 'plot_div4': plot_div4
                    ,'plot_div5': plot_div5 , 'plot_div6': plot_div6
                    ,'cur':cur,'gas':gas , 'oil':oil , 'water':water
                    ,'whp':whp, 'wht':wht , 'wc':wc , 'gor':gor 
                    ,'sp':sp , 'st':st , 'ot':ot                             
                    }                                                            

        return render(self.request, 'data_dash.html', context)





#SQL connections
import pyodbc
from sqlalchemy import create_engine

#azure connection
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


class realtimeView(View):
    
    def get(self, *args, **kwargs):
        
        import pandas as pd
        
        cur = 'realtime'

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

        mask = (flat['created_on'] > (datetime.now()- timedelta(hours=5))) & (flat['created_on'] <= datetime.now())

        flat = flat.loc[mask]

        mask1 = (flat['created_on'] > (datetime.now()- timedelta(hours=1))) & (flat['created_on'] <= datetime.now())

        flat2 = flat.loc[mask1]

        gas = flat2['Qg – Standard Conditions'].astype(float).mean().round(1)
        oil = flat2['Qo – Standard Conditions'].astype(float).mean().round(1)
        water = flat2['Qw – Standard Conditions'].astype(float).mean().round(1)
        lpress = flat2['MVT Static Pressure'].astype(float).mean().round(1)
        ltemp = flat2['MVT Temperature'].astype(float).mean().round(1)

       
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=flat['created_on'], y=flat['Qg – Standard Conditions'].astype(float), name="Gas Flow Rate", text='m3/d',
                            line_shape='linear',
                            line=dict(color='darkgray', width=4)))

        fig.update_traces(hoverinfo='name+y+text', mode='markers+lines')
        fig.update_layout(title="Gas Flow Rate")
        

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=flat['created_on'], y=flat['Qo – Standard Conditions'].astype(float), name="Oil Flow Rate", text='m3/d',
                            line_shape='linear',
                            line=dict(color='darkgreen', width=4)))

        fig2.update_traces(hoverinfo='name+y+text', mode='markers+lines')
        fig2.update_layout(title="Oil Flow Rate")
        
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=flat['created_on'], y=flat['Qw – Standard Conditions'].astype(float), name="Water Flow Rate", text='m3/d',
                            line_shape='linear',
                            line=dict(color='lightskyblue', width=4)))

        fig3.update_traces(hoverinfo='name+y+text', mode='markers+lines')
        fig3.update_layout(title="Water Flow Rate")


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

        context = {  'plot_div' : plot_div  , 'plot_div2': plot_div2
                    ,'plot_div3': plot_div3 , 'cur':cur,  'gas':gas , 'oil':oil , 'water':water , 'lpress':lpress , 'ltemp':ltemp ,                          
                    }                                                             

        return render(self.request, 'realtimechart.html', context)