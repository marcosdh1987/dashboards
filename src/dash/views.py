from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, View
from django.shortcuts import redirect
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

        context = {'plot_div': plot_div, 'plot_div2': plot_div2
                                ,'plot_div3': plot_div3 , 'plot_div4': plot_div4
                                , 'plot_div5': plot_div5, 'plot_div6': plot_div6                            
                    }                                                             

        return render(self.request, 'home.html', context)