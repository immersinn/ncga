#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 16:13:14 2017

@author: immersinn
"""

import os
from time import sleep
import datetime
import logging


import pandas

import utils
import mysql_utils
import process_dailyupdates_pages


def process_day(date, sleep_time):
    
    yr = date.year
    mo = date.month
    da = date.day
    
    for c in ['H', 'S']:
        try:
            logging.info("Retrieving data for Day " + \
                         datetime.datetime.strftime(date, '%Y-%m-%d') + \
                         " Chamber: " + c)
            data = process_dailyupdates_pages.get_DailyUpdateForDateChamber(yr, mo, da, c)
            data = data[data.Action=='Filed']
            logging.info("{} new filed billes retrieved".format(data.shape[0]))
            out = mysql_utils.dump_filed_bills(data)
            if out == 'Fail':
                logging.warning("Failed to add to DB.")
            
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except BaseException as err:
            err_type = str(type(err))
            err_msg = str(err.args)
            logging.error("Day " + datetime.datetime.strftime(date, '%Y-%m-%d') + \
                          ": " + err_type + ': ' + err_msg)
        finally:
            sleep(sleep_time)


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