#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 09:34:50 2017

@author: immersinn
"""

import os
from time import sleep
import datetime
import logging


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
    """
    To be once run Mon - Fri. 
    Grab data from the previous day and add to the db.
    The Monday run grabs data from the previous Friday.
    """
    
    # Config logging
    fd = utils.get_main_dir()
    logpath = os.path.join(fd, 'main_bills_dailyupdate.log')
    logging.basicConfig(filename=logpath,
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    
    # Get porevious day
    today = datetime.date.today()
    if today.weekday() == 1:
        day = datetime.timedelta(days=3)
    else:
        day = datetime.timedelta(days=1)
    date = today - day
    
    print("Processing day {}".format(date))
    process_day(date, sleep_time)
    
    
if __name__=="__main__":
    main()