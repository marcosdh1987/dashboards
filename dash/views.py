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
        import pandas as pd
        # Get data for plots.
        url = staticfiles_storage.path('ds/ds_grouped.csv')
        url2 = staticfiles_storage.path('ds/fsf_prod.csv')
        url3 = staticfiles_storage.path('ds/fsf_prod_post_table.csv')

        #ds = pd.read_csv(r'D:\OneDrive\OneDrive - WFT\Compartido\Well_Datasets\La_Calera_Pluspetrol\Post_Process\Analytics_files\df\ds_grouped.csv',low_memory=False)
        #ds2 = pd.read_csv(r'D:\OneDrive\OneDrive - WFT\Compartido\Well_Datasets\La_Calera_Pluspetrol\Post_Process\Analytics_files\df\fsf_prod.csv')
        #ds3 = pd.read_csv(r'D:\OneDrive\OneDrive - WFT\Compartido\Well_Datasets\La_Calera_Pluspetrol\Post_Process\Analytics_files\df\fsf_prod_post_table.csv')

        ds = pd.read_csv(url)
        ds2 = pd.read_csv(url2)
        ds3 = pd.read_csv(url3)

        by = 'WELL Name'
        
        gas = ds['Gas Rate Sm3/d'].mean()
        

        fig = px.scatter(ds, x=by, y="GOR", color='Meter', size='Gas Rate Sm3/d',title="Gas Oil Rate Comparison")
        fig2 = px.scatter(ds, x=by, y="GWR", color='Meter', size='Gas Rate Sm3/d',title="Gas Water Rate Comparison")
        #fig2 = go.Box(y=ds["GOR"], x=ds[by], boxpoints=False)
        fig3 = px.box(ds2, x='pad', color='Meter', y="Gas Rate Sm3/d")

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
                    ,'gas':gas                                
                    }                                                             

        return render(self.request, 'dashboard.html', context)


class comparisonView(View):
    
    def get(self, *args, **kwargs):
        """ 
        View demonstrating how to display a graph object
        on a web page with Plotly. 
        """
        import pandas as pd
        # Get data for plots.
        url = staticfiles_storage.path('ds/compared_data_full.csv')
        #ds = pd.read_csv(r'\\192.168.0.7\3tdata\data_lake\shell_pad11\compared_data_full.csv',low_memory=False)
        ds = pd.read_csv(url)

        by = 'WELL Name'
        # List of graph objects for figure.
        # Each object will contain on series of data.
        graphs = []


        x = np.array([1, 2, 3, 4, 5])
        y = np.array([1, 3, 2, 3, 1])

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ds['Time_x'], y=ds['Gas Rate m3/d'], name="Separator",
                            line_shape='linear'))
        fig.add_trace(go.Scatter(x=ds['Time_x'], y=ds['QgStd[m3/d]'], name="Foresite Flow",
                            line_shape='spline'))

        fig.update_layout(hovermode='x unified',title="Gas Flow Rates")

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=ds['Time_x'], y=ds['Oil Flow m3/d'], name="Separator",
                            line_shape='linear'))
        fig2.add_trace(go.Scatter(x=ds['Time_x'], y=ds['QoStd[m3/d]'], name="Foresite Flow",
                            
                            line_shape='spline'))

        fig2.update_layout(hovermode='x unified',title="Oil Flow Rates")
        
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=ds['Time_x'], y=ds['Water Flow Ratem3/d'], name="Separator",
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
                     'plot_div3': plot_div3
                                              
                    }                                                             

        return render(self.request, 'dashboard.html', context)

class realtimeView(View):
    
    def get(self, *args, **kwargs):
        """ 
        View demonstrating how to display a graph object
        on a web page with Plotly. 
        """
        import pandas as pd
        # Get data for plots.
        import pyodbc
        
        server = 'daqsamsrv01.database.windows.net'
        database = 'daqdb01'
        username = 'marcos'
        password = 'Asdf*123'   
        driver= '{ODBC Driver 17 for SQL Server}'


        cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()
        # Insert Dataframe into SQL Server:

        query = "SELECT * FROM modbus_data"

        ds = pd.read_sql(query,cnxn)

        cnxn.commit()
        cursor.close()


        d1 = pd.pivot_table(ds,values=['value'],index=['created_on'],columns=['Description'], aggfunc='first')


        flat = pd.DataFrame(d1.to_records())
        flat.columns = [hdr.replace("('value', '", "").replace("')", "") \
                            for hdr in flat.columns]

        #mask = (flat['created_on'] > '2021-06-06 18:00:00') & (flat['created_on'] <= '2021-06-08 22:00:00')                    
        
        mask = (flat['created_on'] > (datetime.now()- timedelta(hours=5))) & (flat['created_on'] <= datetime.now())

        flat = flat.loc[mask]
       
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=flat['created_on'], y=flat['Qg – Standard Conditions'], name="Gas Flow Rate", text='m3/d',
                            line_shape='linear',
                            line=dict(color='darkgray', width=4)))

        fig.update_traces(hoverinfo='name+y+text', mode='markers+lines')
        fig.update_layout(title="Gas Flow Rate")

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=flat['created_on'], y=flat['Qo – Standard Conditions'], name="Oil Flow Rate", text='m3/d',
                            line_shape='linear',
                            line=dict(color='darkgreen', width=4)))

        fig2.update_traces(hoverinfo='name+y+text', mode='markers+lines')
        fig2.update_layout(title="Oil Flow Rate")
        
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=flat['created_on'], y=flat['Qw – Standard Conditions'], name="Water Flow Rate", text='m3/d',
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
                    ,'plot_div3': plot_div3                             
                    }                                                             

        return render(self.request, 'realtimechart.html', context)