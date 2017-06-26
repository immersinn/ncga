#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 21:16:09 2017

@author: immersinn
"""

import regex as re


def billsummaryaref_matcher(tag):
    return tag.name =='a' and hasattr(tag, 'text') and tag.text == 'View Available Bill Summaries'

def extract_links(soup):
    """Extract Bill Text Links from Bill Page"""
    billtext_links = []
    target_a = soup.find_all(billsummaryaref_matcher)
    if len(target_a) == 1:
        target_a = target_a[0]
        content_table = target_a.parent.parent.parent
        for row in content_table.find_all('tr')[2:]:
            row_info = {}
            arefs = row.find_all('td')[0].find_all('a')
            for a in arefs:
                if a.text == 'HTML':
                    row_info['html'] = a['href']
                else:
                    
                    row_info['label'] = a.text.encode('utf8').replace(b'\xc2\xa0', b' ').decode('utf8')
                    row_info['pdf'] = a['href']
            billtext_links.append(row_info)
    return billtext_links

def extract_meta(soup):
    """Extract the(select) a bout the Bill Info Page"""
    chamber_re = re.compile(r"(?:(?<=Chamber=))(H|S)")
    userid_re = re.compile(r"(?:(?<=UserID=))([0-9]+)")
    
    meta = {}
    for kw in ["Sponsors","Counties", "Statutes", "Keywords"]:
        tr = soup.find('th', text=kw + ':').parent
        content = tr.find('td')
        if kw=='Sponsors':
            spons = content.find_all('a')
            spons_list = []
            for a in spons:
                hr = a['href']
                spons_list.append({'userid' : userid_re.findall(hr)[0],
                                   'chamber' : chamber_re.findall(hr)[0]})
            meta[kw] = spons_list
        elif kw in ['Counties', 'Keywords', 'Statutes']:
            meta[kw] = content.text.split(', ')
        else:
            meta[kw] = content.text
            
        if kw == 'Counties' and   \
           meta[kw][0].lower().strip() == 'no counties specifically cited':
                meta[kw] = None
        if kw == 'Statutes' and \
           meta[kw][0].lower().strip() == 'no affected general statutes':
                meta[kw] = None
            
    return meta