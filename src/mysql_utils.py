#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 15:18:32 2017

@author: immersinn
"""

import os
import logging

import pandas
import mysql.connector
from mysql.connector.cursor import MySQLCursor
from mysql.connector.errors import IntegrityError, ProgrammingError

import utils


DB = "ncga"
TABLES = ['camp_doc_lu']
TABLE = TABLES[0]


########################################
## General Helper functions
########################################


def ids2ints(id_series):
    return([int(i) for i in list(id_series)])


def getCnx():
    u,p = utils.get_creds('MySQL')
    cnx = mysql.connector.connect(user=u, password=p, database=DB)
    return(cnx)


def getCur(cnx):
    return(MySQLCursor(cnx))


def dfDocsFromCursor(cursor):
    return(pandas.DataFrame(data = cursor.fetchall(),
                            columns = cursor.column_names))
    

def dictDocFromCursor(cursor):
    return({k : f for f, k in zip(cursor.next(),
                                  cursor.column_names)})
    

class curWith:
    
    def __init__(self, query_text, args_tuple=()):
        self.qt = query_text
        self.at = args_tuple
    
    def __enter__(self):
        self.cnx = getCnx()
        self.cur = getCur(self.cnx)
        if self.at:
            self.cur.execute(self.qt, self.at)
        else:
            self.cur.execute(self.qt)
        return(self.cur)
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.cnx.close()
        
        
class curWithReuse:
    
    def __init__(self,):
        pass
    
    def __enter__(self,):
        self.cnx = getCnx()
        self.cur = getCur(self.cnx)
        return(self.cur)
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.cnx.close()
        
class curInsert:
    
    def __init__(self,):
        pass
    
    def __enter__(self,):
        self.cnx = getCnx()
        self.cur = getCur(self.cnx)
        return(self.cur)
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.cnx.commit()
        self.cnx.close()
        

def df_tuplerow2dict(tuple_row, cols):
    return({col : entry for col, entry in zip(cols, tuple_row)})


def convert_date(date):
    """'YYYY-MM-DD'"""
    if date.strip():
        parts = date.split('/')
        return(parts[2] + '-' + parts[0] + '-' + parts[1])
    else:
        return(None)
        
    
########################################
## Insert Functions
########################################


def dump_campdoc_entries(df):
    
    add_entry = ("INSERT INTO " + TABLE + " "
                 "(committee, report_year, report_type, amend, rec_date, start_date, end_date, image_link, data_link) "
                 "VALUES (%(committee)s, %(report_year)s, %(report_type)s, "
                 "%(amend)s, %(rec_date)s, %(start_date)s, %(end_date)s, "
                 "%(image_link)s, %(data_link)s)")
    
    trconv = lambda tr: df_tuplerow2dict(tr, df.columns)
    
    try:
        with curInsert() as cursor:
            for i,rt in enumerate(df.itertuples()):
                if i == 1 or i % 1000 == 0:
                    print('At entry {}'.format(i))
                cursor.execute(add_entry, trconv(list(rt)[1:]))
        return('Pass')
    except KeyboardInterrupt:
        raise(KeyboardInterrupt)
    except BaseException as err:
        err_type = str(type(err))
        err_msg = str(err.args)
        logging.error(err_type + ': ' + err_msg)
        return('Fail')
        

def dump_filed_bills(bills_df):
    
    cols_keep = ['Bill', 'SQLDate', 'Title', 'Link', 'Session']
    cols_lookup = {'Bill' : 'bill_id',
                   'Session' : 'session',
                   'SQLDate' : 'date_filed',
                   'Title' : 'title',
                   'Link' : 'link',
                   }
    
    bills_df['SQLDate'] = bills_df['Date'].apply(convert_date)
    bills_df = bills_df[cols_keep]
    bills_df.columns = [cols_lookup[c] for c in bills_df.columns]
    
    add_entry = ("INSERT INTO bills "
                 "(bill_id, session, date_filed, title, link)"
                 "VALUES (%(bill_id)s, %(session)s, %(date_filed)s, %(title)s, %(link)s)"
                )
    
    trconv = lambda tr: df_tuplerow2dict(tr, bills_df.columns)
    
    try:
        with curInsert() as cursor:
            for i,rt in enumerate(bills_df.itertuples()):
                i += 1
#                if i == 1 or i % 1000 == 0:
#                    print('At entry {}'.format(i))
                cursor.execute(add_entry, trconv(list(rt)[1:]))
        return('Pass')
    except KeyboardInterrupt:
        raise(KeyboardInterrupt)
    except BaseException as err:
        err_type = str(type(err))
        err_msg = str(err.args)
        logging.error(err_type + ': ' + err_msg)
        return('Fail')