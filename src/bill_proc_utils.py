#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 17:30:11 2017

@author: immersinn
"""

import re


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
    