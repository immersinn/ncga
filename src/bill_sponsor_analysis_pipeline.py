#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 17:36:10 2017

@author: immersinn
"""

import pandas

import utils
import bill_proc_utils


name_suffix_list = ['Jr', 'Sr', 'II', 'III', 'IV']
    
def get_last_name(full_name):
    name_parts = [p.strip() for p in full_name.split()]
    name_parts = [p for p in name_parts if p]
    
    last = ''
    if name_parts[-1].strip('.') not in name_suffix_list:
        last = name_parts[-1]
    else:
        last = name_parts[-2].strip(',')
    return(last)


def get_first_name(full_name):
    return(full_name.split()[0])


def get_firstinit(full_name):
    return(full_name[0])


def get_filn(full_name):
    l = get_last_name(full_name)
    f = get_firstinit(full_name)
    return(f+'.'+l)
    

def build_name_lookup_func(reprs_df):
    
    last_names = [get_last_name(n) for n in reprs_df.Name]
    firstinits = [get_firstinit(n) for n in reprs_df.Name]
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



def main(session):

    # Load Representative and Bill data for session
    all_reps = utils.load_repr_data(session)
    all_reps['Label'] = all_reps.apply(lambda x: get_filn(x.Name) + " (" + x.Party + ")", axis=1)
    btfc = utils.load_filed_bill_data()
    nluf = build_name_lookup_func(all_reps)
       
    
    # Extract Sponsor Name info from Bill Metadata
    btfc['sponsors'] = btfc.table_info.apply(lambda x: bill_proc_utils.extract_sponsors(x))
    sponsors_info = btfc.apply(lambda x: [{'bill_ix' : x.name,
                                           'name' : s,
                                           'chamber' : x.house} for s in x.sponsors], axis=1)
    sponsors_info = pandas.DataFrame([s for l in sponsors_info for s in l])
    sponsors_info['sponsor_ix'] = [nluf(sponsors_info.name[i], sponsors_info.chamber[i]) \
                                   for i in sponsors_info.index]
    
#    # Missing data stuff
#    missing = sponsors_info[sponsors_info.sponsor_ix==-1]
#    missing_names = set(missing.name)
    
    sponsors_info = sponsors_info[sponsors_info.sponsor_ix != -1]
    
    # Compute total counts per repr
    counts = pandas.DataFrame(sponsors_info.groupby('sponsor_ix').apply(len))
    counts.columns = ['BillCount']
    no_bills = set(all_reps.index).difference(set(counts.index))
    counts = pandas.concat((counts, 
                            pandas.DataFrame(data=[0 for _ in range(len(no_bills))],
                                             index=no_bills,
                                             columns=['BillCount'])))
    all_reps = all_reps.join(counts)
    all_reps.sort_values(by='BillCount', ascending=False, inplace=True)
    
    return(all_reps, btfc, sponsors_info)

