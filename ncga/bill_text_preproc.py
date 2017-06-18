#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 20:08:40 2017

@author: immersinn

MESSY AND INCOMPLETE
"""

import os
import pickle

import pandas
from bs4 import BeautifulSoup as bs


import utils


def cleanRawText(text):
    """
    vtype text: str
    
    rtype text: str / utf8
    """
    text = text.encode('ascii', 'replace')
    text = text.replace(b'?', b'')
    text = text.replace(b'\r\n', b'\n')
    text = text.replace(b'\n', b' ')
    text = text.strip()
    text = text.decode('utf8')
    return(text)


def extractRawText(body):
    """
    vtype body: bs4.element.Tag
    
    rtype raw_text: str
    """
    paras = body.find_all('p')
    texts = [p.text for p in paras]
    texts = [t.strip() for t in texts]
    raw_text = '\n\n'.join(texts)
    raw_text = cleanRawText(raw_text)
    return(raw_text)


def extractLongTitle(body):
    try:
        return(cleanRawText(body.find('p', {'class':'aLongTitle'}).text))
    except AttributeError:
        return("")


def extractTableContent(body):
    info = {}
    contents = [tr for tr in body.find('table').find_all('tr') if tr.find('p')]
    for row in contents:
        attr = cleanRawText(row.find('p').text)
        value = cleanRawText(row.find_all('td')[-1].text)
        if attr.lower().startswith('short'):
            d = attr.split(': ')
            attr = d[0]
            value = d[1].strip() + ' ' + value
        attr = attr.strip().strip(':')
        attr = ''.join(attr.split())
        info[attr] = value
    return(info)


def extract_metadata(soup):
    
    meta_table = extractTableContent(soup)
    meta_table['LongTitle'] = extractLongTitle(soup)
    return(meta_table)


def pipe(bill_texts_df):
    """
    soup = bs(text, 'html.parser')
    raw_text = extractRawText(soup)
    clean_text = cleanRawText(raw_text)
    metadata = extract_metadata(soup)
    """
    
    
    bill_texts_df['soup'] = \
            bill_texts_df['html'].apply(lambda x: bs(x, 'html.parser'))
    bill_texts_df['content'] = \
            bill_texts_df['soup'].apply(lambda x: extractRawText(x.body))
    bill_texts_df['long_title'] = \
            bill_texts_df['soup'].apply(lambda x: extractLongTitle(x.body))
    bill_texts_df['table_info'] = \
            bill_texts_df['soup'].apply(lambda x: extractTableContent(x.body))
            
    return None

        
if __name__=="__main__":
    
    input_file = "bill_texts_filed.pkl"
    output_file = 'bill_texts_filed_content.pkl'
    data_dir = utils.get_data_dir()
    
    with open(os.path.join(data_dir, 'raw', input_file), 'rb') as f1:
        bill_texts_filed = pandas.DataFrame(pickle.load(f1))
        
    pipe(bill_texts_filed)
    
    bill_texts_filed_content = bill_texts_filed[['session', 'house', 'bill',
                                                 'content', 
                                                 'long_title', 'table_info']]
    
    with open(os.path.join(data_dir, 'interim', output_file), 'wb') as f1:
        pickle.dump(bill_texts_filed_content, f1)