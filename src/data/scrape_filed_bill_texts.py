#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 20:47:11 2017

@author: immersinn
"""

import time
from urllib.request import urlopen
from urllib.error import HTTPError
import pickle


def main():
    
    bill_links_file = "data/bill_links_all.pkl"
    bill_texts_file = "data/bill_texts_filed.pkl"
    root = "http://www.ncleg.net/"
    
    with open(bill_links_file, 'rb') as f1:
        bill_links = pickle.load(f1)
    bill_links_filed = bill_links[bill_links.label==b'Filed']
    
    
    bill_texts = []
    missed = []
    
    print("Scraping bill 'Filed' texts...")
    
    for i,bill in enumerate(bill_links_filed.itertuples()):
        
        if i % 100 == 0:
            print('Retrieveing text for Bill {}-{}-{}...'.format(bill.session,
                                                                 bill.house, bill.bill))
        
        url = root + bill.html
        stop = False
        repeat_flag = False
        while not stop:
            try:
                with urlopen(url) as page:
                    if page.status < 300:
                        page = page.read()
                        bill_texts.append({'session' : bill.session, 
                                           'house' : bill.house, 
                                           'bill' : bill.bill,
                                           'text' : page})
                        stop = True
                        repeat_flag = False
                    else:
                        if repeat_flag == True:
                            stop = True
                        else:
                            repeat_flag = True
            except HTTPError:
                if repeat_flag == True:
                    stop = True
                    missed.append({'session' : bill.session, 
                                   'house' : bill.house,
                                   'bill' : bill.bill})
                else:
                    repeat_flag = True
                            
        # Pause
        time.sleep(1)
    
    #
    print('\nTotal pages scrapped: {}'.format(len(bill_texts)))
    print('\nTotal pages skipped: {}'.format(len(missed)))
                    
    # Pickle the data
    print('\nPickling data...')
    with open(bill_texts_file, 'wb') as f1:
        pickle.dump(bill_texts, f1)
    
    with open('data/missed_filed.pkl', 'wb') as f1:
        pickle.dump(missed, f1)
    
        
    print('\nAll done!')
    print('\n')