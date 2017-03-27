#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 18:06:19 2017

@author: immersinn
"""

import os

#import plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly import figure_factory as FF
import plotly.graph_objs as pogo
from plotly.graph_objs import Marker, Line, Data

import utils


def urlmod(url, trim_url, url2localhost):
    
    if trim_url:
        url = url[7:]
    if url2localhost:
        url = url[7:]
#        url = utils.dirpath2localhost(url)
        url = utils.dirpath2gitpages(url)
        
    return(url)


def plotly_table_from_df(name, data, 
                         cols=[], 
                         directory='images', 
                         trim_url=False,
                         url2localhost=True):
    
#    if not cols:
#        cols = df.columns
#    df = df[cols]
    
    if directory=='images':
        img_dir = utils.get_report_image_dir()
        
    table = FF.create_table(data)
    table_url = plot(table, 
                     filename=os.path.join(img_dir, name) + '.html',
                     auto_open=False,)
    
    table_url = urlmod(table_url, trim_url, url2localhost)
        
    return(table_url)


def build_sponsor_summary_plot_url(name, reprs_info,
                                   directory='images',
                                   trim_url=False,
                                   url2localhost=True):
    
    if directory=='images':
        img_dir = utils.get_report_image_dir()
    
    color_dict = {'R' : 'red', 'D' : 'blue'}

    trace0 = pogo.Bar(
        x=list(reprs_info['Label']),
        y=list(reprs_info['BillCount']),
        text=list(reprs_info['Label']),
        marker=dict(
            color=[color_dict[p] for p in reprs_info['Party']],
            ),
    )
    
    data = [trace0]
    layout = pogo.Layout(
        title='NC GA Bill Sponsorship Counts, 2015-2016',
    )

    fig = pogo.Figure(data=data, layout=layout)
    
    sponsor_summary_url = plot(fig, 
                               filename=os.path.join(img_dir, name) + '.html',
                               auto_open=False,)
    
    sponsor_summary_url = urlmod(sponsor_summary_url, trim_url, url2localhost)
    
    return(sponsor_summary_url)