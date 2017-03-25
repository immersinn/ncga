#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 09:53:45 2017

@author: immersinn
"""

import os
import time
import logging

import utils
import urlreqs_utils
import mysql_utils
import mongo_utils


bill_link_root = 'http://www.ncleg.net'
base_update = 'UPDATE bills SET page_scraped=1 WHERE id={}'


def pull_and_insert(entry):
    
    id_ = entry.id
    link = entry.link
    
    try:
        # Pull page
        html, status = urlreqs_utils.get_page(bill_link_root + link)
        
        if status:            
            # Dump page & Update mysql
            with mongo_utils.collWithBP() as coll:
                mr = coll.insert_one({'bill_id' : int(id_),
                                      'html' : html})
            with mysql_utils.curInsert() as con:
                con.execute(base_update.format(id_))
                
        else:
            logging.warning("Page for Bill {} not successfully retreived".format(id_))
            
    except KeyboardInterrupt:
        raise KeyboardInterrupt
        
    except BaseException as err:
        err_type = str(type(err))
        err_msg = str(err.args)
        logging.error("Bill {}".format(id_) + \
                      ": " + err_type + ': ' + err_msg)
    finally:
        time.sleep(1)    


def main():
    
    # Config logging
    fd = utils.get_main_dir()
    logpath = os.path.join(fd, 'main_billspages_update.log')
    logging.basicConfig(filename=logpath,
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    
    
    logging.info("Starting Bill Pages Update")
    
    
    # Get the bills whose pages have not been scraped from the mysqldb
    with mysql_utils.curWith('SELECT * FROM bills WHERE page_scraped=0') as cur:
        bills = mysql_utils.dfDocsFromCursor(cur)
        
    
    logging.info("{} bills to pull pages".format(bills.shape[0]) )
        
    # For each bill retrieved, pull page, dup, and update mysql
    _ = bills.apply(pull_and_insert, axis=1)
    
    
    logging.info("Update complete")
    
    
if __name__=="__main__":
    main()