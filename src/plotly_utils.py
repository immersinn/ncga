#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 18:06:19 2017

@author: immersinn
"""

import os

import plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly import figure_factory as FF
import plotly.graph_objs as pogo
from plotly.graph_objs import Marker, Line, Data

import utils


def plotly_table_from_df(name, df, 
                         cols=[], 
                         directory='images', 
                         trim_url=True):
    
    if not cols:
        cols = df.columns
    df = df[cols]
    
    if directory=='images':
        img_dir = utils.get_report_image_dir()
        
    table = FF.create_table(df)
    table_url = plot(table, 
                     filename=os.path.join(img_dir, name) + '.html',
                     auto_open=False,)
    
    if trim_url:
        table_url = table_url[7:]
        
    return(table_url)