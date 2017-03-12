#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 17:30:11 2017

@author: immersinn
"""

from collections import defaultdict
import re

import pandas


#######################################
### General Helper Functions
#######################################


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

def build_repr_ballotpedia_link(full_name):
    url_base = "https://ballotpedia.org/"
    url = url_base + get_first_name(full_name) + "_" + get_last_name(full_name)
    return(url)

def build_district_ballotpedia_link(district_no, chamber):
    url_base = "https://ballotpedia.org/"
    chamber_base = {'H' : 'North_Carolina_House_of_Representatives_',
                    'S' : 'North_Carolina_State_Senate_'}
    url = url_base + chamber_base[chamber] + 'District_' + str(district_no)
    return(url)


def build_repr_internal_link(full_name):
    pass

def build_ahref_link(text, url):
    return('<a href="' + url + '">' + text + '</a>')


#######################################
### Keywords Helper Utils
#######################################


def count_keywords(keywords_iterator):
    keyword_counts = defaultdict(int)
    for kw in keywords_iterator:
        for w in kw:
            keyword_counts[w] += 1
    return(keyword_counts)


def build_ranking(df, col='Count'):
    ranking = range(1,df.shape[0]+1)
    return(ranking)


def build_keywords_df(bill_info, sub_index=[], cutoff=10, sort=True):
    
    if not sub_index:
        sub_index = [True for _ in range(bill_info.shape[0])]
    kw_counts = count_keywords(bill_info[sub_index]['Keywords'])
    
    kw_df = pandas.DataFrame(data = [{'Keyword' : k, 'Count' :c} \
                                     for k,c in kw_counts.items()])
    kw_df = kw_df[kw_df.Count > cutoff]
    if sort:
        kw_df.sort_values(by='Count', ascending=False, inplace=True)
        kw_df['Rank'] = build_ranking(kw_df)
        columns = ['Keyword', 'Count', 'Rank']
    else:
        columns = ['Keyword', 'Count']
    kw_df = kw_df[columns]
    return(kw_df)


def build_chamber_keywords_df(bill_info, chamber):
    sub_index = bill_info['Chamber']==chamber
    return(build_keywords_df(bill_info, sub_index))



#######################################
### Info from Bill Metadata
#######################################

sponsor_split = re.compile(r';|,| and')
known_modifiers = {'By Request', 'Primary   Sponsors', 'Primary Sponsor', 'Primary Sponsors'}


def extract_sponsors(table_info):
    
    def strip_modifiers(s):
        if s.endswith(')'):
            s = s.split('(')[0].strip()
        return(s)
    
    def parse_sponsor_string(sponsors_str, base_token):
    
        if sponsors_str[:(len(base_token) + 1)] == base_token + 's':
            nl = len(base_token) + 1
            sponsors_str = sponsors_str[nl:].strip()
            sponsors_toks = re.split(sponsor_split, sponsors_str)
            sponsors_toks = [s.strip() for s in sponsors_toks]
            sponsors_toks = [s for s in sponsors_toks if s]

        else:
            nl = len(base_token)
            sponsors_str = sponsors_str[nl:].strip()
            sponsors_toks = [sponsors_str]
            
        sponsors_toks = [strip_modifiers(s) for s in sponsors_toks]
        sponsors_toks = [s.replace(' ', '').strip() for s in sponsors_toks]
            
        return(sponsors_toks)
    
    def main(sponsors):
        sponsors = sponsors.strip('.')

        if sponsors[:14] =='Representative':
            base_token = 'Representative'
        elif sponsors[:7] =='Senator':
            base_token = 'Senator'
    
        if base_token:    
            sponsors = parse_sponsor_string(sponsors, base_token)
            
        return(sponsors)
            
    
    sponsors_raw = table_info['Sponsors']
    
    if sponsors_raw.strip()[:9] == 'Committee':
        sponsors = [sponsors_raw.strip()]
    elif sponsors_raw.find('/') > -1:
        sponsors_raw = sponsors_raw.split('/')
        sponsors = []
        for s in sponsors_raw:
            sponsors.extend(main(s))
    else:
        sponsors = main(sponsors_raw)
    
    return(sponsors)
    