#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 13:34:31 2017

@author: immersinn
"""

import utils
import textacy_pipelines


def main():
    corpus_name = "CORPUS_bills_filed_pipe01"
    data = utils.load_filed_bill_data()
    corpus = textacy_pipelines.pipe01(data, n_threads=7, batch_size=300)
    utils.save_corpus(corpus_name, corpus)
    
    
if __name__=="__main__":
    main()