#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 14:31:57 2017

@author: immersinn
"""


from pymongo import MongoClient

    
class collWith:
    
    def __init__(self, db_name, coll_name):
        self.db_name = db_name
        self.coll_name = coll_name
    
    def __enter__(self,):
        self.client = MongoClient()
        self.db = self.client[self.db_name]
        self.coll = self.db[self.coll_name]
        return(self.coll)
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()        
    
    def query(self, conditions, fields=None):
        return(self.coll.find(conditions, fields))
    
    
class collWithBP(collWith):
    
    def __init__(self,):
        self.db_name = 'ncga'
        self.coll_name = 'bill_pages'