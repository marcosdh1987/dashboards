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

        ds = pd.read_csv(r'D:\OneDrive\OneDrive - WFT\Compartido\Well_Datasets\La_Calera_Pluspetrol\Post_Process\Analytics_files\df\ds_grouped.csv',low_memory=False)
        ds2 = pd.read_csv(r'D:\OneDrive\OneDrive - WFT\Compartido\Well_Datasets\La_Calera_Pluspetrol\Post_Process\Analytics_files\df\fsf_prod.csv')
        ds3 = pd.read_csv(r'D:\OneDrive\OneDrive - WFT\Compartido\Well_Datasets\La_Calera_Pluspetrol\Post_Process\Analytics_files\df\fsf_prod_post_table.csv')
        by = 'WELL Name'
        # List of graph objects for figure.
        # Each object will contain on series of data.
        graphs = []

        # Adding linear plot of y1 vs. x.
        df = px.data.iris()
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

        ds = pd.read_csv(r'\\192.168.0.7\3tdata\data_lake\shell_pad11\compared_data_full.csv',low_memory=False)

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
                            hoverinfo='text+name',
                            line_shape='spline'))

        fig.update_traces(hoverinfo='text+name', mode='lines+markers')
        fig.update_layout(title="Gas Flow Rates", legend=dict(y=0.5, traceorder='reversed', font_size=16))

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=ds['Time_x'], y=ds['Oil Flow m3/d'], name="Separator",
                            line_shape='linear'))
        fig2.add_trace(go.Scatter(x=ds['Time_x'], y=ds['QoStd[m3/d]'], name="Foresite Flow",
                            hoverinfo='text+name',
                            line_shape='spline'))

        fig2.update_traces(hoverinfo='text+name', mode='lines+markers')
        fig2.update_layout(title="Oil Flow Rates",legend=dict(y=0.5, traceorder='reversed', font_size=16))
        
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=ds['Time_x'], y=ds['Water Flow Ratem3/d'], name="Separator",
                            line_shape='linear'))
        fig3.add_trace(go.Scatter(x=ds['Time_x'], y=ds['QwStd[m3/d]'], name="Foresite Flow",
                            hoverinfo='text+name',
                            line_shape='spline'))

        fig3.update_traces(hoverinfo='text+name', mode='lines+markers')
        fig3.update_layout(title="Water Flow Rates",legend=dict(y=0.5, traceorder='reversed', font_size=16))
        



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

        import pandas as pd
        from sqlalchemy import create_engine
        # Postgres username, password, and database name
        POSTGRES_ADDRESS = '192.168.0.7' ## INSERT YOUR DB ADDRESS IF IT'S NOT ON PANOPLY
        POSTGRES_PORT = '5432'
        POSTGRES_USERNAME = 'marcosdb' ## CHANGE THIS TO YOUR PANOPLY/POSTGRES USERNAME
        POSTGRES_PASSWORD = '32922161' ## CHANGE THIS TO YOUR PANOPLY/POSTGRES PASSWORD
        POSTGRES_DBNAME = 'mydb' ## CHANGE THIS TO YOUR DATABASE NAME
        # A long string that contains the necessary Postgres login information
        postgres_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'.format(username=POSTGRES_USERNAME,
        password=POSTGRES_PASSWORD,
        ipaddress=POSTGRES_ADDRESS,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DBNAME))
        # Create the connection
        cnx = create_engine(postgres_str)

        df = pd.read_sql_query('''SELECT * FROM modbus_data''', con=cnx)

        d1 = pd.pivot_table(df,values=['value'],
                        index=['created_on'],
                        columns=['description'], aggfunc='first')


        flat = pd.DataFrame(d1.to_records())
        flat.columns = [hdr.replace("('value', '", "").replace("')", "") \
                            for hdr in flat.columns]
       
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=flat['created_on'], y=flat['Qg – Standard Conditions'], name="FSF",
                            line_shape='linear'))

        fig.update_traces(hoverinfo='text+name', mode='lines+markers')
        fig.update_layout(title="Gas Flow Rates", legend=dict(y=0.5, traceorder='reversed', font_size=16))

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=flat['created_on'], y=flat['Qo – Standard Conditions'], name="FSF",
                            line_shape='linear'))

        fig2.update_traces(hoverinfo='text+name', mode='lines+markers')
        fig2.update_layout(title="Oil Flow Rates",legend=dict(y=0.5, traceorder='reversed', font_size=16))
        
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=flat['created_on'], y=flat['Qw – Standard Conditions'], name="FSF",
                            line_shape='linear'))

        fig3.update_traces(hoverinfo='text+name', mode='lines+markers')
        fig3.update_layout(title="Water Flow Rates",legend=dict(y=0.5, traceorder='reversed', font_size=16))


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