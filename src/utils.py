#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 13:39:01 2017

@author: immersinn
"""

import os
import pickle

import pandas
from textacy.corpus import Corpus


def get_main_dir():
    fd = os.path.split(os.path.realpath(os.path.split(__file__)[0]))[0]
    return(fd)


def get_data_dir(which='project'):
    
    if which=='Dropbox':
        fd = get_main_dir()
        fd = os.path.realpath(os.path.split(os.path.split(fd)[0])[0])
        data_dir = os.path.join(fd, 'Dropbox/Analytics/NCGA/data')
    elif which=='project':
        fd = get_main_dir()
        data_dir = os.path.join(fd, "data")
        
    return(data_dir)


def load_filed_bill_data(data_dir=''):
    if not data_dir:
        data_dir = get_data_dir(which="project")
        data_dir = os.path.join(data_dir, 'raw')
        
    # Load
    with open(os.path.join(data_dir, "bill_texts_filed_content.pkl"), 'rb') as f1:
        btfc = pickle.load(f1)
    
    with open(os.path.join(data_dir, "bill_page_keywords.pkl"), 'rb') as f1:
        keywords = pickle.load(f1)
        
    # Merge
    btfc = btfc.set_index(["session", "house", "bill"])
    keywords = keywords.set_index(["session", "house", "bill"])
    btfc = btfc.join(keywords, how="left")
    btfc = pandas.DataFrame(btfc.to_records())
    
    return(btfc)


def save_corpus(name, corpus, data_sub_dir="processed", compression='gzip'):
    data_dir = get_data_dir(which='project')
    path = os.path.join(data_dir, data_sub_dir, name)
    os.mkdir(path)
    corpus.save(path=path, name=name, compression=compression)
    
    
def load_corpus(name, data_sub_dir="processed", compression='gzip'):
    data_dir = get_data_dir(which='project')
    path = os.path.join(data_dir, data_sub_dir, name)
    return(Corpus.load(path=path, name=name, compression=compression))