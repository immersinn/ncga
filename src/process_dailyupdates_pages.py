#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 14:04:47 2017

@author: immersinn
"""


from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer
import pandas

import urlreqs_utils


def build_query_url_from_date(biennium, yr, mo, da, chamber):
    
    url_base = "http://www.ncleg.net/gascripts/lastaction/todaysfiledaction.pl?"
    query_base = "Biennium={0}&ActionChamber={1}&DateReport={2}"
    
    def mdstr(md):
        mdstr = str(md)
        if md < 10:
            mdstr = '0' + mdstr
        return(mdstr)
    
    def ds_from_comps(yr, mo, da):
        ds = mo + "%2F" + da + "%2F" + yr
        return(ds)
    
    yr = str(yr)
    mo = mdstr(mo)
    da = mdstr(da)
    ds = ds_from_comps(yr, mo, da)
    
    query = query_base.format(biennium, chamber, ds)
    return(url_base + query)


def extract_datarows_m01(soup):
    """
    "Dead-Reckon" table and extract rows accordingly
    """
    content_table_filter = SoupStrainer("table",
                                    {'border':0, 'cellpadding':2,})
    table = soup.find(content_table_filter)
    if table:
        rows = table.find_all('tr', {'class':""})
        header = rows[0]
        rows = rows[1:]
    else:
        header = []
        rows = []
    
    return(header, rows)


def extract_datarows_m02(soup):
    """
    Pull all of the target columns and rebuild into sets of rows;
    Convert easch back to a single bs4 tag object
    """
    column_filter = SoupStrainer("td", {"class":"tableText"})
    columns = soup.find_all(column_filter)
    rows = []
    
    if columns:
        for i in range(0,len(columns), 5):
            rows.append(bs("<tr class="">\n" + \
                           '\n'.join([str(c) for c in columns[i:(i+5)]]) +\
                           "\n<\tr>",
                          'html.parser'))
        
    return(rows)


def process_tag_rows(rows):
    
    
    # Columns are known:
    cols = ['Bill', 'Short Title', 'Action', 'Date', 'Action Text']
    col_order = ['Bill', 'Action', 'Date', 'Short Title', 'Link', 'Action Text']
    col_names_new = ['Bill', 'Chamber', 'Date', 'Title', 'Link', 'Action']
    
    
    data = []
    for row in rows:
        d = {}
        for col,entry in zip(cols, row.find_all('td')):
            d[col] = entry.text
           # if col in link_cols:
            if col == 'Bill':
                link = entry.find('a')['href']
                d['Link'] = link
        data.append(d)
        
    data = pandas.DataFrame(data)
    data = data[col_order]
    data.columns = col_names_new
    
    return(data)


def create_empty_fills_df():
    df = pandas.DataFrame(data=[],
                          columns=['Bill', 'Chamber', 'Date', 
                                   'Title', 'Link', 'Action', 'Session'])
    return(df)


def content_from_page(html, biennium):
    
    soup = bs(html, 'html.parser')
    header, rows = extract_datarows_m01(soup)
    if rows:
        data = process_tag_rows(rows)
        data['Session'] = biennium
    else:
        data = create_empty_fills_df()
    return(data)


def get_DailyUpdateForDateChamber(yr, mo, da, chamber, session_type='reg'):
    """
    Retireves the data for the daily update page corresponding to a particular
    date, chamber combo
    """
    if session_type=='reg':
        biennium = str(yr)
    else:
        pass
    
    url = build_query_url_from_date(biennium, yr, mo, da, chamber)
    html, status = urlreqs_utils.get_page(url, tor=True)
    
    if status:
        data = content_from_page(html, biennium)
    else:
        data = pandas.DataFrame()
    return(data)