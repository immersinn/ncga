#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 20:26:07 2017

@author: immersinn
"""


from collections import defaultdict

import pandas

import utils
import bill_proc_utils as bpu
import bill_sponsor_analysis_pipeline



def get_repr_bi(bill_info, repr_bills):
    sub_bi = bill_info.ix[repr_bills].copy()
    sub_bi['Title'] = sub_bi['TableInfo'].apply(lambda x: x['Short   Title'])
    sub_bi = sub_bi[['Session', 'Chamber', 'Bill', 'Title', 'Keywords', 'Sponsors']]
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
        


def get_repr_data(repr_id, bill_info, reprs_info, reprs_bills, bills_reprs):
    
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
    
    return({'Bills': sub_bi,
            'Cosponsors' : repr_cosp_df,
            'BillKeywords' : repr_bkws_df})



def build_all_pages():
    
    for session in ['2014']:
        reprs_info, bill_info, sponsor_info = bill_sponsor_analysis_pipeline.main(session)
        
        # These are our lookup tables
        reprs_bills = sponsor_info.groupby('SponsorID')
        bills_reprs = sponsor_info.groupby('BillID')
        
        for repr_id in list(reprs_info.index):
            repr_data = get_repr_data(repr_id,
                                      bill_info, reprs_info,
                                      reprs_bills, bills_reprs,)
            
            