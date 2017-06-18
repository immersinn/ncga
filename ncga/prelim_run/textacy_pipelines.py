#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 13:50:27 2017

@author: immersinn
"""

import spacy
import textacy

import utils


def process_metadata(data, meta_keys):
    
    if meta_keys:
        numeric_columns = data._get_numeric_data().columns.tolist()
        for mk in meta_keys:
            if mk in numeric_columns:
                data[mk] = data.apply(lambda x: str(x[mk]), axis=1)
        metas = [data.ix[data.index[i]][meta_keys].to_dict() \
                 for i in data.index]
    else:
        metas = []
        
    return(metas)



def pipe01(data, 
           content_key='content', meta_keys=["session", "house", "bill", "keywords"],
           n_threads=8, batch_size=800):
    
    # Define textacy doc preprocessing
    textacy_preprocessor = lambda text: textacy.preprocess.preprocess_text(text,
                                                                       no_contractions=True,
                                                                       no_numbers=True,
                                                                       no_emails=True,
                                                                       no_currency_symbols=True,
                                                                       lowercase=True)
    # Define nlp pipeline
    nlp = spacy.load("en", add_vectors=False)
    nlp.pipeline = [nlp.tagger, nlp.parser]
    
    # Get Texts and Metadatas
    ## Parallelize this step!
    texts = [textacy_preprocessor(con) for con in list(data[content_key])]
    metas = process_metadata(data, meta_keys)
        
    # Deinfe & Populate the corpus
    corpus = textacy.Corpus(lang=nlp)
    corpus.add_texts(texts=texts, metadatas=metas,
                     n_threads=n_threads, batch_size=batch_size)
    
    # Return the data
    return(corpus)


def make_pipe01_dataset(name = "CORPUS_bills_filed_pipe01"):
    data = utils.load_filed_bill_data()
    corpus = pipe01(data, n_threads=8, batch_size=800)
    utils.save_corpus(name, corpus)
    
    
if __name__=="__main__":
    make_pipe01_dataset()