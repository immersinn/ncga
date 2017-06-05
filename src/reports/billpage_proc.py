#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 08:31:41 2017

@author: immersinn
"""



def get_meta(soup):
    
    tds_2_find = ['Last Action:', 'Attributes:', ]
    ths_2_find = ['Sponsors:', 'Counties:', 'Statutes:', 'Keywords:']

    tds = soup.find_all('td')
    target_tds = [td for td in tds if td.text in tds_2_find]
    
    ths = soup.find_all('th')
    target_ths = [th for th in ths if th.text in ths_2_find]
    
    meta = []
    for tag in target_tds:
        label = tag.text.strip(':')
        content = tag.find_next('td', {'class' : 'tableText'}).text
        meta.append({'label' : label,
                     'content' : content})
    for tag in target_ths:
        label = tag.text.strip(':')
        content = tag.find_next('td', {'class' : 'tableText'})
        if label == 'Sponsors':
            values = content.find_all('a')
            sponsors = []
            for v in values:
                sponsors.append({'name' : v.text,
                                 'link' : v['href']})
            content = sponsors
        else:
            content = content.text
        meta.append({'label' : label,
                     'content' : content})
    
    return(meta)


def get_session_and_editions(soup):
    """
    "supposed to" extract editions info and such from the main bills page
    """
    # FIXME
    
    
    def get_edition_content(target_rows, header_values):

        edition_content = []

        for entry in target_rows:
            tmp = []
            cols = entry.find_all('td')
            for c,h in zip(cols, header_values):
                if h == 'Bill Text':
                    links = {'pdf' : '', 'html' : ''}
                    vals = c.find_all('a')
                    for v in vals:
                        t = v.text.strip()
                        link = v['href']
                        if t.lower() == 'html':
                            links['html'] = link
                        else:
                            edition = t
                            links['pdf'] = link
                    tmp.append({'Links' : links})
                elif h == 'Fiscal Note':
                    tmp.append({h : c.text.strip()})
            edition_content.append({edition : tmp})

        return(edition_content)


    content = []
    
    # Session Info
    session = soup.find('div', {'class' : 'titleSub'})
    content.append({'label' : 'Session',
                    'content' : session.text.strip()})
    
    # Bill Editions, Summary
    editions_table = session.next_sibling.find('table')
    entries = editions_table.find_all('tr')
    
    bill_summaries = entries[0]
    content.append({'label' : 'SummaryLink',
                    'content' : bill_summaries.find('a')['href']})
    
    header = entries[1]
    header_values = [th.text for th in header.find_all('th')]    
    edition_content = get_edition_content(entries[2:], header_values)
    content.append({'label' : 'EditionsInfo',
                    'content' : edition_content})
    
    return(content)


def pipe(bill_pages):
    
    bill_pages['meta'] = bill_pages.soup.apply(get_meta)
