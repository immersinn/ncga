#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 16:13:14 2017

@author: immersinn
"""

import os
import logging

import pandas

import utils
from runme_dailyupdate_bills import process_day


def main(sleep_time=1):
    
    fd = utils.get_main_dir()
    logpath = os.path.join(fd, 'main_bills_init.log')
    logging.basicConfig(filename=logpath,
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    
    start_date = '1/11/2017'
    end_date = '3/23/2017'
    
    dates = list(pandas.date_range(start=start_date, end=end_date))
    
    for i,d in enumerate(dates):
        i += 1
        if i == 1 or i % 10 == 0:
            print('At day {}'.format(d))
        process_day(d, sleep_time)
        
        
if __name__=="__main__":
    main()