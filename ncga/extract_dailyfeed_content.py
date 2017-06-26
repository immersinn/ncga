#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 14:04:47 2017

@author: immersinn
"""

import regex as re
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer
import pandas

from ncga import urlreqs_utils


def build_query_url_from_date(biennium, yr, mo, da, chamber, filed=True):
    
    if filed is True:
        url_base = "http://www.ncleg.net/gascripts/lastaction/todaysfiledaction.pl?"
    else:
        url_base = "http://www.ncleg.net/gascripts/lastaction/todaysaction.pl?"
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


def get_content_table(soup):
    """
    Find the ``table`` element that has the daily feed and return
    """
    def tot_act_match(ele):
        return ele.name=='div' and \
               re.compile(r"^Total Bill Actions:").search(ele.get_text()) != None
               
    def check_header(header):
        labels = [th.text for th in header.find_all('th')]
        return labels == ['Bill', 'Short Title', 'Action', 'Date', 'Action\xa0Text']
    
    empty_soup = bs('', 'html.parser')
    
    div = soup.body.find(tot_act_match)
    if div:
        n_rows = int(div.text.split(':')[-1].strip())
        table = div.find_next_sibling(name='table')
        if table:
            header = table.find('tr')
            if check_header(header):
                rows = table.find_all('tr', {'class':""})[1:]
                if len(rows) == n_rows:
                    return header, rows
                else:
                    return empty_soup, empty_soup
            else:
                return empty_soup, empty_soup
        else:
            return empty_soup, empty_soup
    else:
        return empty_soup, empty_soup

            
def process_content_table(rows):
    """
    Process the bs4 table rows to extract and format content
    """
    # Columns are known:
    cols = ['Bill', 'Short Title', 'Action', 'Date', 'Action Text']
    col_order = ['Bill', 'Action', 'Date', 'Short Title', 'Action Text']
    col_names_new = ['Bill', 'ActionChamber', 'Date', 'Title', 'ActionText']
    prev_ent_cols = ['Bill', 'Short Title']
    
    
    data = []
    prev_entry = {}
    for row in rows:
        d = {}
        for col, entry in zip(cols, row.find_all('td')):
            d[col] = entry.text.strip()
            
        if d['Bill'].strip():
            prev_entry = {pec : d[pec] for pec in prev_ent_cols}
        else:
            for pec in prev_ent_cols:
                d[pec] = prev_entry[pec]
                
        data.append(d)
        
    data = pandas.DataFrame(data)
    data = data[col_order]
    data.columns = col_names_new
    
    return(data)


def process_filed_content_table(rows):
    """
    Process the bs4 table rows to extract and format content
    """
    # Columns are known:
    cols = ['Bill', 'Short Title', 'Action', 'Date', 'Action Text']
    col_order = ['Bill', 'Action', 'Date', 'Short Title', 'Link', 'Action Text']
    col_names_new = ['Bill', 'ActionChamber', 'Date', 'Title', 'Link', 'ActionText']
    
    
    data = []
    for row in rows:
        d = {}
        for col,entry in zip(cols, row.find_all('td')):
            d[col] = entry.text
            if col == 'Bill':
                link = entry.find('a')['href']
                d['Link'] = link
        data.append(d)
        
    data = pandas.DataFrame(data)
    data = data[col_order]
    data.columns = col_names_new
    
    return(data)


def create_empty_df():
    df = pandas.DataFrame(data=[],
                          columns=['Bill', 'ActionChamber', 'Date', 
                                   'Title', 'Link', 'ActionText',
                                   'Session'])
    return(df)


#def create_empty_filed_df():
#    df = pandas.DataFrame(data=[],
#                          columns=['Bill', 'Chamber', 'Date', 
#                                   'Title', 'Link', 'Action',
#                                   'Session'])
#    return(df)


def create_billpage_link(bill_id, session):
    return "http://www.ncleg.net/gascripts/BillLookUp/BillLookUp.pl?Session=" +\
           str(session) + \
           "&BillID=" + bill_id


def content_from_full_page(html, biennium):
    
    soup = bs(html, 'html.parser')
    header, rows = get_content_table(soup)
    if rows:
        data = process_content_table(rows)
        data['Session'] = biennium
        data['Link'] = data.Bill.apply(lambda x: create_billpage_link(x, biennium))
    else:
        data = create_empty_df()
    return(data)


def content_from_filed_page(html, biennium):
    
    soup = bs(html, 'html.parser')
    header, rows = get_content_table(soup)
    if rows:
        data = process_filed_content_table(rows)
        data['Session'] = biennium
    else:
        data = create_empty_df()
    return(data)


def content_from_page(html, biennium, filed):
    if filed is True:
        return content_from_filed_page(html, biennium)
    else:
        return content_from_full_page(html, biennium)


def get_DailyUpdateForDateChamber(yr, mo, da, chamber, 
                                  session_type='reg', filed=True):
    """
    Retireves the data for the daily update page corresponding to a particular
    date, chamber combo
    """
    if session_type=='reg':
        biennium = str(yr)
    else:
        pass
    
    url = build_query_url_from_date(biennium, yr, mo, da, chamber, filed=filed)
    html, status = urlreqs_utils.get_page(url, tor=False)
    
    if status:
        data = content_from_page(html, biennium, filed)
    else:
        data = pandas.DataFrame()
    return(data)
