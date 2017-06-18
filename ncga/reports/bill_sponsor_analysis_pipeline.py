#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 17:36:10 2017

@author: immersinn
"""

import pandas

import utils
import bill_proc_utils as bpu

    

def build_name_lookup_func(reprs_df):
    
    last_names = [bpu.get_last_name(n) for n in reprs_df.Name]
    firstinits = [bpu.get_firstinit(n) for n in reprs_df.Name]
    name_info = pandas.DataFrame(data={'LN':last_names,
                                       'FILN':[f+'.'+l for l,f in zip(last_names, firstinits)],
                                       'Chamber':reprs_df.Chamber},
                                 index=reprs_df.index)
    
    ln_dict = {ln+'-'+c : ind for ln,c,ind in zip(name_info.LN,
                                                  name_info.Chamber,
                                                  name_info.index)}
    filn_dict = {filn+'-'+c : ind for filn,c,ind in zip(name_info.FILN,
                                                        name_info.Chamber,
                                                        name_info.index)}
    
    # Hand correct some issues
    ln_dict['Adcock-S'] = ln_dict['Adcock-H']
    ln_dict['Robinson-H'] = ln_dict['Robinson-S']
    
    def name_lookup(name, chamber):
        key = name + '-' + chamber
        try:
            return(filn_dict[key])
        except KeyError:
            try:
                return(ln_dict[key])
            except KeyError:
                return(-1)
            
    return(lambda n,c: name_lookup(n,c))


def post_proc_bi(bi):
    columns = ['session', 'house', 'bill', 'content', 'long_title', 'table_info', 'keywords']
    new_cols = ['Session', 'Chamber', 'Bill', 'Content', 'LongTitle', 'TableInfo', 'Keywords']
    bi = bi[columns]
    bi.columns = new_cols
    return(bi)


def main(session):

    # Load Representative and Bill data for session
    all_reps = utils.load_repr_data(session)
    all_reps['Label'] = all_reps.apply(lambda x: bpu.get_filn(x.Name) + " (" + x.Party + ")", axis=1)
    btfc = utils.load_filed_bill_data()
    btfc = post_proc_bi(btfc)
    nluf = build_name_lookup_func(all_reps)
       
    
    # Extract Sponsor Name info from Bill Metadata
    btfc['Sponsors'] = btfc['TableInfo'].apply(lambda x: bpu.extract_sponsors(x))
    sponsors_info = btfc.apply(lambda x: [{'BillID' : x.name,
                                           'Name' : s,
                                           'Chamber' : x['Chamber']} for s in x['Sponsors']], axis=1)
    sponsors_info = pandas.DataFrame([s for l in sponsors_info for s in l])
    sponsors_info['SponsorID'] = [nluf(sponsors_info['Name'][i], sponsors_info['Chamber'][i]) \
                                   for i in sponsors_info.index]
    
#    # Missing data stuff
#    missing = sponsors_info[sponsors_info.sponsor_ix==-1]
#    missing_names = set(missing.name)
    
    sponsors_info = sponsors_info[sponsors_info['SponsorID'] != -1]
    
    # Compute total counts per repr
    counts = pandas.DataFrame(sponsors_info.groupby('SponsorID').apply(len))
    counts.columns = ['BillCount']
    no_bills = set(all_reps.index).difference(set(counts.index))
    counts = pandas.concat((counts, 
                            pandas.DataFrame(data=[0 for _ in range(len(no_bills))],
                                             index=no_bills,
                                             columns=['BillCount'])))
    all_reps = all_reps.join(counts)
    all_reps.sort_values(by='BillCount', ascending=False, inplace=True)
    
    return(all_reps, btfc, sponsors_info)

