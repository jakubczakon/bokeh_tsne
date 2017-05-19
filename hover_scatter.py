import glob,os

import pandas as pd

from bokeh.io import output_notebook
from bokeh.plotting import figure, show, ColumnDataSource
from bokeh.models import HoverTool

from ipywidgets import interact


def scatterplot(df, **kwargs):
    plot_width = kwargs.get('plot_width',300)
    plot_height = kwargs.get('plot_height',300)
    size = kwargs.get('size',10)
    
    hover = HoverTool(
        tooltips="""
        <div>
            <div>
                <img
                    src="@img_filepath" height="200" alt="@img_filepath" width="200"
                    style="float: left; margin: 0px 15px 15px 0px;"
                    border="2"
                ></img>
            </div>
            
        </div>
        """
    )

    p = figure(plot_width=plot_width, plot_height=plot_height, 
               toolbar_location = 'right',
               tools='pan,box_zoom,wheel_zoom,reset,resize')
    p.add_tools(hover)
    
    source = ColumnDataSource(df)
    circles = p.circle('x', 'y', size=size, source=source)

    output_notebook()
    show(p)