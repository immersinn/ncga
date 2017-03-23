#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 20:26:07 2017

@author: immersinn
"""

import os
from collections import defaultdict

import pandas

import utils
import bill_proc_utils as bpu
import bill_sponsor_analysis_pipeline
import plotly_utils



def get_repr_bi(bill_info, repr_bills):
    
    def get_title(entry):
        try:
            st = entry['TableInfo']['ShortTitle']
        except KeyError:
            st = entry['LongTitle'][:50] + '...'
        return(st)
            
    sub_bi = bill_info.ix[repr_bills].copy()
    sub_bi['Title'] = sub_bi.apply(get_title, axis=1)
    return(sub_bi)


def get_bill_cosponsors(bill_id, repr_id,
                        bills_reprs):
    cosponsors = list(bills_reprs.get_group(bill_id)['SponsorID'])
    cosponsors.remove(repr_id)
    return(cosponsors)
        

def get_all_cosponsors(bill_ids, repr_id,
                       bills_reprs):
    repr_cosponsors = [get_bill_cosponsors(bid, repr_id, bills_reprs) for bid in bill_ids]
    total = len(repr_cosponsors)
    repr_cosponsors = [co for co in repr_cosponsors if co]
    only_sponsor = total - len(repr_cosponsors)
    
    cosponsors = defaultdict(int)
    for cos in repr_cosponsors:
        for co in cos:
            cosponsors[co] += 1
    cosponsors = dict(cosponsors)
    cosponsors[repr_id] = only_sponsor

    return(cosponsors)


def build_cos_df(bill_ids, repr_id,
                 reprs_info,
                 reprs_bills, bills_reprs):
    repr_cosp_data = get_all_cosponsors(list(reprs_bills.get_group(repr_id)['BillID']),
                                        repr_id,
                                        bills_reprs)
    repr_cosp_df = pandas.DataFrame(data = [{'ID' : k, 'Count' : v} \
                                             for k,v in repr_cosp_data.items()])
    repr_cosp_df['Name'] = repr_cosp_df.ID.apply(lambda x: reprs_info.ix[x]['Name'])
    repr_cosp_df.sort_values(by='Count', ascending=False, inplace=True)
    repr_cosp_df = repr_cosp_df[['ID', 'Name', 'Count']]
    return(repr_cosp_df)


def get_repr_data(repr_id, bill_info, reprs_info, reprs_bills, bills_reprs,
                  bill_cols = ['Session', 'Chamber', 'Bill', 'Title']):
    
    # List of Bill IDs for Repr
    repr_bills = list(reprs_bills.get_group(repr_id)['BillID'])
    
    # Subset of Bills for Repr
    sub_bi = get_repr_bi(bill_info, repr_bills)
    
    # Co-Sponsor data
    repr_cosp_df = build_cos_df(repr_bills, repr_id,
                                reprs_info,
                                reprs_bills, bills_reprs)
    
    # Keyword Data
    if len(repr_bills) > 40:
        co = 5
    elif len(repr_bills) > 20:
        co = 3
    else:
        co = 0
    repr_bkws_df = bpu.build_keywords_df(sub_bi, cutoff=co)
    
    sub_bi = sub_bi[bill_cols]
    
    return({'Bills': sub_bi,
            'Cosponsors' : repr_cosp_df,
            'BillKeywords' : repr_bkws_df})
    
    
def build_test_html(repr_name, table_url_dict, n_bills):
    
    bill_table_url = table_url_dict['bills']
    keyword_table_url = table_url_dict['keywords']
    cosponsor_table_url = table_url_dict['cosponsors']
    
    html_string = '''
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{ margin:0 100; background:whitesmoke; }</style>
    </head>
    <body>
        <h1>NCGA: Summary Info for Representative ''' + str(repr_name) + '''</h1>
        
            <h3>Sponsored Bills (''' + str(n_bills) + ''' total)</h3>
            
            <iframe style="padding:40px" width="90%" height="480" frameborder="0" seamless="seamless" scrolling="yes" \
    src="''' + bill_table_url + '''"></iframe>
        
        
            <table width="100%">
                <tr>
                    <td width="48%"><h3>Bill Keywords</h3></td>
                    <td width="48%"><h3>Co-Sponsors</h3></td>
                </tr>
            </table>
        
        <iframe style="padding:40px" width="48%" height="480" frameborder="0" seamless="seamless" scrolling="yes" align="left"\
    src="''' + keyword_table_url + '''"></iframe>
    
        <iframe style="padding:40px" width="48%" height="480" frameborder="0" seamless="seamless" scrolling="yes" align="right"\
    src="''' + cosponsor_table_url + '''"></iframe>
    
    </body>
</html>'''

    return(html_string)



def build_session_page(repr_links, session):
        
    def build_ahref_link(text, url):
        return('<a href="' + url + '">' + str(text) + '</a>')
    
    hrefs = [build_ahref_link(n, l) for n,l in repr_links]
    hrefs_string = '\n\n'.join(hrefs)
    hrefs_df = pandas.DataFrame(data = [{'HREF' : h} for h in hrefs])
    table_url = plotly_utils.plotly_table_from_df('test_href_table', hrefs_df)
    
    html_string = '''
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{ margin:0 100; background:whitesmoke; }</style>
    </head>
    <body>
        <h1>NCGA: Session Overview Page for Session ''' + str(session) + '''</h1>
        
            <h2>Representative Pages</h2>
            
            ''' + hrefs_string + '''
            
        <iframe style="padding:40px" width="48%" height="480" frameborder="0" seamless="seamless" scrolling="yes" align="left"\
    src="''' + table_url + '''"></iframe>
    
    </body>
</html>'''    

    return(html_string)


def build_all_pages(build_session_page=False):
    
    page_link_list = []
    
    for session in ['2014']:
        # Get data for session
        reprs_info, bill_info, sponsor_info = bill_sponsor_analysis_pipeline.main(session)
        
        # These are our lookup tables
        reprs_bills = sponsor_info.groupby('SponsorID')
        bills_reprs = sponsor_info.groupby('BillID')
        
        for repr_id in list(reprs_info.index):
            repr_data = get_repr_data(repr_id,
                                      bill_info, reprs_info,
                                      reprs_bills, bills_reprs)
            
            # Build tables, get URLs
            bill_url = plotly_utils.plotly_table_from_df(str(repr_id) + '_billtable',
                                                       repr_data['Bills'])
            kw_url = plotly_utils.plotly_table_from_df(str(repr_id) + '_kwtable',
                                                       repr_data['BillKeywords'])
            cos_url = plotly_utils.plotly_table_from_df(str(repr_id) + '_costable',
                                                       repr_data['Cosponsors'])
            
            # Build HTML with Table URLs, Repr info
            html = build_test_html(repr_id, {'bills' : bill_url,
                                             'keywords' : kw_url,
                                             'cosponsors' : cos_url,
                                             },
                                   repr_data['Bills'].shape[0])
            
            link_apd = bpu.build_repr_link('', repr_id, session)

            with open(utils.build_fullpath_file_from_page(link_apd), 'w') as f:
                f.write(html)
                
            page_link_list.append((repr_id, 
                                   utils.build_fullpath_link_from_page(link_apd)))

        
        if build_session_page:
            session_page_html = build_session_page(page_link_list, session)
            link_apd = 'sessionPage_' + str(session) + '.html'
            
            with open(utils.build_fullpath_file_from_page(link_apd), 'w') as f:
                    f.write(session_page_html)

            
if __name__=="__main__":
    build_all_pages(build_session_page=False)
            