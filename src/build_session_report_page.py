#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 20:03:14 2017

@author: immersinn
"""

import os

import utils
import bill_proc_utils as bpu
import bill_sponsor_analysis_pipeline
import plotly_utils


def build_chamber_summary_table(reprs_info, chamber, sort_by='LN'):
    peeps = reprs_info[reprs_info.Chamber == chamber].copy()
    
    if sort_by=='LN':
        peeps['LN'] = peeps.Name.apply(bpu.get_last_name)
    
    peeps.sort_values(by=sort_by, inplace=True)
    
    data_matrix = [['Name', 'District', 'Party', 'Bills Sponsored']]

    for n,d,p,b in zip(peeps.apply(lambda x: bpu.build_ahref_link(x.Name, x.PersonURL), axis=1),
                       peeps.apply(lambda x: bpu.build_ahref_link(x.District, x.DistrictURL), axis=1),
                       peeps.Party,
                       peeps.BillCount):
        data_matrix.append([n,d,p,b])
    
    table_url = plotly_utils.plotly_table_from_df(chamber + '_rep_table',
                                                  data_matrix)
    
    return(table_url)


def build_chamber_keywords_table(bill_info, chamber, cutoff=10):
    
    table_url = plotly_utils.plotly_table_from_df(chamber + '_keyword_table',
                                                  bpu.build_chamber_keywords_df(bill_info, chamber),
                                                  )
    return(table_url)


def main():
    
    session = '2014'
    
    main_repo_dir = utils.get_main_dir()
    
    reprs_info, bill_info, sponsor_info = bill_sponsor_analysis_pipeline.main(session)
    
    total_bills = bill_info.shape[0]
    sen_bills = sum(bill_info['Chamber'] == 'S')
    hou_bills = sum(bill_info['Chamber'] == 'H')
    
    # Build the main bar plot URL
    sponsor_summary_url = plotly_utils.build_sponsor_summary_plot_url("NC GA Bill Sponsorship Counts 2015-2016",
                                                                      reprs_info)
    
    reprs_info['PersonURL'] = reprs_info.apply(lambda x: bpu.build_repr_link(x['Name'],
                                                                             x.name,
                                                                             session),
                                               axis=1)
    reprs_info['DistrictURL'] = reprs_info.apply(lambda x: bpu.build_district_ballotpedia_link(x.District, x.Chamber),
                                             axis=1)
    reprs_info['District'] = reprs_info.District.apply(lambda x: 'District ' + str(x))
    
    
    # Build the House & Senate Summary Tables
    house_table_url = build_chamber_summary_table(reprs_info, 'H')
    senate_table_url = build_chamber_summary_table(reprs_info, 'S')
    
    
    # Chamber summary tables
    house_kwtable_url = build_chamber_keywords_table(bill_info, 'H')
    senate_kwtable_url = build_chamber_keywords_table(bill_info, 'S')
    
    
    html_string = '''
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{ margin:0 100; background:whitesmoke; }</style>
    </head>
    <body>
        <h1>NCGA: Summary Info for Bills Filed During 2015 - 2016 Session</h1>

        <!-- *** Section 1 *** --->
        <h2>Section 1: General Summary Info</h2>
            <h4>Total Bills Filed: ''' + str(total_bills) + '''</h4>
            <h4>Senate Bills Filed: ''' + str(sen_bills) + '''</h4>
            <h4>House Bills Filed: ''' + str(hou_bills) + '''</h4>

        
        <!-- *** Section 2 *** --->
        <h2>Section 2: Breakdown by Representative</h2>

            <iframe width="1500" height="800" frameborder="0" seamless="seamless" scrolling="no"\
    src="''' + sponsor_summary_url + '''"></iframe>
    
    
        <table width="100%">
                <tr>
                    <td width="48%"><h3>House of Representatives Summary</h3></td>
                    <td width="48%"><h3>Senate Summary</h3></td>
                </tr>
            </table>
        
        <iframe style="padding:40px" width="48%" height="480" frameborder="0" seamless="seamless" scrolling="yes" align="left"\
    src="''' + house_table_url + '''"></iframe>
    
        <iframe style="padding:40px" width="48%" height="480" frameborder="0" seamless="seamless" scrolling="yes" align="right"\
    src="''' + senate_table_url + '''"></iframe>
    
    
        <!-- *** Section 3 *** --->
        <h2>Section 3: Bill Topics Overview</h2>
        
            <p>Table with keyword info, other topic info goes here</p>
            
            <table width="100%">
                <tr>
                    <td width="48%"><h3>House of Representatives</h3></td>
                    <td width="48%"><h3>Senate</h3></td>
                </tr>
            </table>
        
        <iframe style="padding:40px" width="48%" height="480" frameborder="0" seamless="seamless" scrolling="yes" align="left"\
    src="''' + house_kwtable_url + '''"></iframe>
    
        <iframe style="padding:40px" width="48%" height="480" frameborder="0" seamless="seamless" scrolling="yes" align="right"\
    src="''' + senate_kwtable_url + '''"></iframe>

    
    </body>
</html>'''
    
    with open(os.path.join(main_repo_dir,'reports/dashboards/NCGABillsSummary.html'),'w') as f:
        f.write(html_string)
        
        
if __name__=="__main__":
    main()