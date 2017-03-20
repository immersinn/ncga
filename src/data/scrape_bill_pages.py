#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 09:24:08 2017

@author: immersinn
"""

import time
import pickle
from urllib.request import urlopen

from bs4 import BeautifulSoup as bs


bill_root = "http://www.ncleg.net/gascripts/BillLookUp/BillLookUp.pl?"
session_head = "Session="
bill_head = "BillID="


def buildBillURL(session, bill_id):
    return(bill_root + session_head + session + "&" + bill_head + bill_id)


def isEmptyPage(page):
    soup = bs(page, 'html.parser')
    return(soup.find('div', {"id":"title"}).text.lower().find("not found") > -1)


def main():
    
    sess = ['2015E4', '2015E3', '2015E2', '2015E1', '2015']    
    pages = []
    for ses in sess:
        print('Session ' + ses)
        for house_flag in ["H", "S"]:
            print('  House ' + house_flag)
            stop = False
            counter = 1
            repeat_flag = False
            while not stop:
                if counter == 1 or counter % 100 == 0:
                    print('\tBill ' + str(counter))
                time.sleep(0.75)
                bill_id = house_flag + str(counter)
                url = buildBillURL(session=ses, bill_id=bill_id)
                with urlopen(url) as page:
                    if page.status < 300:
                        page = page.read()
                        if not isEmptyPage(page):
                            pages.append({'session' : ses, 'house' : house_flag, 'page' : page, 'bill' : counter})
                            counter += 1
                        else:
                            stop = True
                        repeat_flag = False
                    else:
                        if repeat_flag == True:
                            stop = True
                        else:
                            repeat_flag = True
             ## DO NOT COMMENT  FOR TESTING
             #   if counter >= 1:
             #       stop = True
            print('  Total bills in {} session {}: {}'.format(house_flag, ses, counter-1))
                    
    #
    print('\nTotal pages scrapped: {}'.format(len(pages)))
                    
    # Pickle the data
    print('\nPickling data...')
    with open('data/test_pages.pkl', 'wb') as f1:
        pickle.dump(pages, f1)
        
    print('\nAll done!')
    print('\n')