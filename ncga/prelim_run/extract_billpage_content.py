#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 20:15:31 2017

@author: immersinn
"""
import pickle

from bs4 import BeautifulSoup as bs
import pandas


def extractBillLinks(soup, session, house, bill):
    """Extract complete list of links for Bill Texts (HTML & PDF Versions)
    """
    tables = soup.find_all("table")
    content_table = [t for t in tables if t.text.strip().startswith("View Available Bill Summaries")][-1]
    bill_text_links = []
    for row in content_table.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) > 1:
            try:
                label = cols[0].text.strip('[HTML]').strip().encode('utf8').replace(b'\xc2\xa0', b' ')
                links = cols[0].find_all('a')
                pdf_link = links[0]['href']
                html_link = links[1]['href']
                bill_text_links.append({'session' : session, 'house' : house, 'bill' : bill,
                                        'label' : label, 'pdf' : pdf_link, 'html' : html_link})
            except IndexError:
                pass
    return(bill_text_links)


def extractBillFiledLinks(soup):
    """Extract list of links for Filed Bill Texts (HTML & PDF Versions)
    """
    tables = soup.find_all("table")
    content_table = [t for t in tables if t.text.strip().startswith("View Available Bill Summaries")][-1]
    filed_links = {}
    for row in content_table.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) > 1:
            label = cols[0].text.strip('[HTML]').strip().encode('utf8').replace(b'\xc2\xa0', b' ')
            if label in [b'Filed']:
                links = cols[0].find_all('a')
                pdf_link = links[0]['href']
                html_link = links[1]['href']
                filed_links = {'label' : label, 'pdf' : pdf_link, 'html' : html_link}
                break
    return(filed_links)


def extractBillAdoptedLinks(soup):
    """Extract list of links for Adopted Bill Texts (HTML & PDF Versions)
    """
    tables = soup.find_all("table")
    content_table = [t for t in tables if t.text.strip().startswith("View Available Bill Summaries")][-1]
    adopted_links = {}
    for row in content_table.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) > 1:
            label = cols[0].text.strip('[HTML]').strip().encode('utf8').replace(b'\xc2\xa0', b' ')
            if label in [b'Adopted', b'Ratified']:
                links = cols[0].find_all('a')
                pdf_link = links[0]['href']
                html_link = links[1]['href']
                adopted_links = {'label' : label, 'pdf' : pdf_link, 'html' : html_link}
    return(adopted_links)


def extractKeywords(soup):
    ds = soup.find_all('tr')
    trs = [tr for tr in ds if len(tr.find_all('th')) > 0]
    ths = [tr for tr in trs if tr.find('th').text.lower().startswith('keyword')]
    keywords = [w.strip() for w in  ths[0].div.text.split(',')]
    return(keywords)


def main():
    source_file = "data/test_pages.pkl"
    bill_links_file = "data/bill_links_all.pkl"
    keywords_file = "data/bill_page_keywords.pkl"
    
    with open(source_file, 'rb') as f1:
        pages = pickle.load(f1)
    bill_info = pandas.DataFrame([{k : page[k] for k in ['session', 'house', 'bill']} for page in pages])
    
    soups = [bs(page['page'], 'html.parser') for page in pages]

#    titles = [soup.find('div', {"id":"title"}).text.strip() for soup in soups]
    
    # Bill Text Links
    bill_links = [extractBillLinks(soup, bi.session, bi.house, bi.bill) \
              for (bi, soup) in zip(bill_info.itertuples(), soups)]
    bill_links = [item for sublist in bill_links for item in sublist]
    bill_links = pandas.DataFrame(bill_links)
    bill_links = bill_links[['session', 'house', 'bill', 'label', 'html', 'pdf']]
    
    # Keywords
    keywords = [{'keywords' : extractKeywords(soup)} for soup in soups]
    keywords = pandas.DataFrame.join(bill_info, pandas.DataFrame(keywords))
    
    # Save Data
    with open(bill_links_file, 'wb') as f1:
        pickle.dump(bill_links, f1)
    with open(keywords_file, 'wb') as f1:
        pickle.dump(keywords, f1)