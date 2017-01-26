#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 21:37:07 2017

@author: immersinn
"""


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
    return(cleanRawText(body.find('p', {'class':'aLongTitle'}).text))
    

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
        info[attr] = value
    return(info)