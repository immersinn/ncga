#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 09:03:14 2017

@author: immersinn


Process Data from the NCDOE website (https://www.ncsbe.gov/Campaign-Finance)

Data from XXX website with all "Document Type" boxes selected.  
Could probably issue a query and get a response, but easier to just 
do manual query, save individuals pages, and process the resuitling HTML,
which convienetly contains the data.


"
Yea all donation info is publicly available at the NCDOE website 
(https://www.ncsbe.gov/Campaign-Finance)

Usually, candidates file quarterly, but the dates for NC don't always line up
 with the federal dates (just a heads up). 

Two weeks before an election and then 48 hours before there are also special
 reports....to prevent people from taking large chunks of cash wihtout 
 disclosure at the end. Also I think anything above 1000 in the last week 
 has to be reported immediately. But that is all posted on the website. 

The key thing you'll need to do is sort the PAC's and individual 
contributions....sometimes more easily done than not. Also, some of the 
campaigns don't submit electronic forms that integrate with their donation 
software so these are photocopied pages that are turned into a PDF, 
possibly making it difficult to scrape. 

Look to OpenSecrets.com as a model. Also look at this site
 (http://www.carolinatransparency.com/)
"
"""

import os

from bs4 import BeautifulSoup as bs
import pandas

import utils
import mysql_utils


data_cols = ['Committee Name', 
             'Report Year', 'Report Type',
             'Amend',
             'Received Date', 'Start Date', 'End Date',
             'Image', 'Data',
             ]

col_mapping = {'Committee Name' : 'committee', 
               'Report Year' : 'report_year',
               'Report Type' : 'report_type',
               'Amend' : 'amend',
               'Received Date' : 'rec_date',
               'Start Date' : 'start_date',
               'End Date' : 'end_date',
               'Image' : 'image_link',
               'Data' : 'data_link',
               }


donation_docs = {'2014' : 'NC Campaign Document Search By Type-2014.html',
				 '2015' : 'NC Campaign Document Search By Type-2015.html',
				 '2016' : 'NC Campaign Document Search By Type-2016.html',
				}



def load_campdoc_html(year):

	try:
		fn = donation_docs[year]
		data_dir = utils.get_data_dir(which='Dropbox')
		with open(os.path.join(data_dir, 'PACDocs', fn), 'r') as f:
			html = f.read()
		return(html)

	except KeyError:
		err_msg = "Invalid Report Year specified.  Select on of: " + \
                  '; '.join(donation_docs.keys())
		raise KeyError(err_msg)
        
        
def extract_main_table_from_html(html):
    """
    Only 1 big table in each of the docs, so extyract this using bs4 and return
    """
    soup = bs(html, 'html.parser')
    table = soup.find('table')
    return(table)


def postproc_table_df(df):
    
    def yn2bool(y_or_n):
        if y_or_n == 'Y':
            return('1')
        elif y_or_n == 'N':
            return('0')
        else:
            return(None)
        
    def convert_date(date):
        """'YYYY-MM-DD'"""
        if date.strip():
            parts = date.split('/')
            return(parts[2] + '-' + parts[0] + '-' + parts[1])
        else:
            return(None)
        
    def clean_rep_type(rt):
        if not rt.strip():
            return(None)
        else:
            return(rt)
    
    df = df[data_cols]
    df['Report Type'] = df['Report Type'].apply(clean_rep_type)
    df['Amend'] = df['Amend'].apply(yn2bool)
    df['Received Date'] = df['Received Date'].apply(convert_date)
    df['Start Date'] = df['Start Date'].apply(convert_date)
    df['End Date'] = df['End Date'].apply(convert_date)
    
    df.columns = [col_mapping[c] for c in df.columns]
    
    return(df)


def process_main_table(table, limit=-1):
    
    def process_row(row):
        data = {}
        for cn, col in zip(col_names, row.find_all('td')):
            a = col.find('a')
            if a:
                if col.text.strip():
                    try:
                        data[cn] = a['href']
                    except KeyError:
                        data[cn] = 'MISSING DATA'  # Should never get here
                else:
                    data[cn] = ''
            else:
                data[cn] = col.text.strip()
        return(data)

    rows = table.find_all('tr')
    col_names = [h.text for h in rows[0].find_all('td')]
    
    if limit==-1:
        limit = len(rows)-1

    data = [process_row(row) for row in rows[1:limit]]
    df = pandas.DataFrame(data)
    df = postproc_table_df(df)
    
    return(df)


def lae_nccd(year):
    """
    'Load & Extract' data from a given year for donation data
    """
    html = load_campdoc_html(year)
    table = extract_main_table_from_html(html)
    data = process_main_table(table)
    return(data)


def dump_df_to_sql(df):
    out = {'status' : 'Fail'}
    status = mysql_utils.dump_campdoc_entries(df)
    out['status'] = status
    return(out)


def load_all():
    
    dfs = [lae_nccd(year) for year in ['2014', '2015', '2016']]
    df = pandas.concat(dfs)
    df.index = range(df.shape[0])
    return(df)


def dump_all():
    for year in ['2014', '2015', '2016']:
        print('Loading data for year {}'.format(year))
        df = lae_nccd(year)
        print('Dumping df to MySQL...')
        out = dump_df_to_sql(df)
        print(out['status'])
        
        
if __name__=="__main__":
    dump_all()
    