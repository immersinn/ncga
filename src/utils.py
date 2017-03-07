#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 13:39:01 2017

@author: immersinn
"""

import os
import pickle

import numpy
import pandas
from textacy.corpus import Corpus


senator_data_session_key = {"2017" : "North Carolina General Assembly - N.C. Senators (2017-2018 Session) Raw.csv",
                            }

rep_data_session_key = {"2017" : "North Carolina General Assembly - N.C. House of Representatives Members (2017-2018 Session) Raw.csv",
                        }


election_data_key = {'senate' : {
                                 '2016' : '2016 North Carolina Senate general election candidates.txt',
                                 '2014' : '2014 North Carolina Senate election info raw.txt',
                                 },
                     'house' : {
                                '2016' : '2016 North Carolina House general election candidates.txt',
                                '2014' : '2014 North Carolina House election info raw.txt',
                                }
                     }


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


def load_senator_data(session="2017"):
    fn = senator_data_session_key[session]
    fn = os.path.join('raw', fn)
    dd = get_data_dir()
    with open(os.path.join(dd, fn), 'rb') as f:
        return(pandas.read_csv(f))
    
    
def load_rep_data(session="2017"):
    fn = rep_data_session_key[session]
    fn = os.path.join('raw', fn)
    dd = get_data_dir()
    with open(os.path.join(dd, fn), 'rb') as f:
        return(pandas.read_csv(f))
    
    
def parse_election_data_cur(raw_text, chamber, session):

    def parse_entry(entry, col, district):
        if entry:
            if entry.strip().lower() == 'no candidate':
                data = {}
            else:

                if col == 'Democratic Party Democrat':
                    party = 'D'
                elif col == 'Republican Party Republican':
                    party = 'R'
                elif col == 'Other':
                    party = entry.strip().split()[-1][1:-1]

                if entry.find(':') > -1:
                    name, oth = entry.split(': ')
                    name = name.strip()
                    oth = oth.strip()
                    if oth.endswith('Approved'):
                        won = True
                        oth = oth[:-9]
                    else:
                        won = False
                    oth = oth.split(' ')
                    votes = oth[0].strip()

                    if len(oth) > 1:
                        if col == 'Other':
                            incombant = False
                        elif oth[1].strip() == '(I)':
                            incombant = True
                        else:
                            incombant = False
                    else:
                        incombant = False

                else:
                    votes = 'NA'
                    won = True
                    name = entry.strip()[:-(len('(I)') + len('Approved') + 2)]
                    incombant = True
                    
#                last = name.split()[-1]
#                fi = name[0]

                data = {'Name' : name,
  #                      'LastName' : last,
  #                      'FILN' : fi + '.' + last,
                        'Party' : party,
                        'Won' : won,
                        'Incombant' : incombant,
                        'Votes' : votes,
                        'District' : district,
                        'Session' : session,
                        'Chamber' : chamber,}

        else:
            data = {}

        return(data)


    def parse_line(line, cols):
        district = line[0]
        data = [parse_entry(e,col,district) for e,col in zip(line[1:], cols[1:])]
        return(data)


    def parse_data(lines, cols):
        data = []
        for line in lines:
            data.extend(parse_line(line, cols))

        return(data)
    
    
    header = raw_text[0].decode('utf').strip().split('\t')

    transform_line = lambda line: line.decode('utf').strip('\n').split('\t')
    contents = [transform_line(line) for line in raw_text[1:]]
    df = pandas.DataFrame(data=[e for e in parse_data(contents, header) if e])
    
    return(df)


def parse_election_data_2014(raw_text, chamber):
    """
    
    """
    
    def parse_sections(raw):
    
        if type(raw[0]) == bytes:
            raw = [l.decode('utf') for l in raw]
        
        start_district = lambda x: x[:8] == 'District'
        starts = numpy.where([start_district(l) for l in raw])[0]
        sections = [raw[starts[i] : starts[i+1]] for i in range(len(starts)-1)]
        sections.append(raw[starts[-1]:])
        
        data = []
        for section in sections:
            data.extend(parse_section(section))
            
        df = pandas.DataFrame(data)
        
        return(df)
        
    
    def parse_section(section):
        """
    
        Pattern:
    
        Demo pre
            cand 1
            cand 2
            ...
        Rep pre
            cand 1
            cand 2
            ...
        Lib / Oth cands
            cand 1
            ...
        General Election Cands
            cand 1
            cand 2
            ...
    
        """
        
        def extract_party(item):
            if item[:10] == 'Democratic':
                party = 'D'
                i = 16
            elif item[:10] == 'Republican':
                party = 'R'
                i = 16
            elif item[:11] == 'Independent':
                party = 'I'
                i = 11
            elif item[:11] == 'Libertarian':
                party = 'L'
                i = 17
            else:
                party = ''
                i = 0
                
            item = item[i:].strip()
            return(party, item)
        
        
        def extract_won(item):
            phrase = 'Green check mark transparent.png'
            if item[-1*len(phrase):] == phrase:
                won = True
                item = item[:(len(item)-len(phrase))].strip()
            else:
                won = False
            return(won, item)
        
        
        def extract_gen_cand_info(sub_sect):
            """
            Order: D, R, (L)"""
            cand_info = []
            for item in sub_sect[1:]:
                item = item.strip()
                if item[:5] != 'Note:':
                    party, item = extract_party(item)
                    won, item = extract_won(item)
                    item = item.split(':')
                    name = item[0].strip()
                    if len(item) == 2:
                        votes = item[1].strip()
                    else:
                        votes = 'NA'
                    entry = {'Name' : name,
                             'Party' : party,
                             'Won' : won,
                             'Votes': votes,
                             'Incombant' : 'NA',
                             'Session' : '2014',
                             'Chamber' : chamber,}
                    cand_info.append(entry)
            return(cand_info)
    
    
        district = section[0].strip()[9:].strip()
        
        loc_gen_start = lambda x: x.lower().find('general election candidates:') > -1
        for i,item in enumerate(section[1:]):
            if loc_gen_start(item):
                s = i+1
                break
        if s:
            gen_cands_info = extract_gen_cand_info(section[s:])
            for entry in gen_cands_info:
                entry['District'] = district
        
        return(gen_cands_info)
    
    
    # Run the main function
    return(parse_sections(raw_text))

    
    
def load_election_data(chamber, session="2016"):
    """
    sen2016 = load_election_data('senate', '2016')
    sen2016.shape == (88, 8)
    sen2016.ix[0].to_dict == {'Chamber': 'S',
                              'District': '1',
                              'Incombant': False,
                              'Name': 'Brownie Futrell',
                              'Party': 'D',
                              'Session': '2016',
                              'Votes': '36,759',
                              'Won': False}
    
    hou2016 = load_election_data('house', '2016')
    hou2016.shape == (189, 8)
    hou2016.ix[0].to_dioct == {'Chamber': 'H',
                               'District': '1',
                               'Incombant': False,
                               'Name': 'Sam Davis',
                               'Party': 'D',
                               'Session': '2016',
                               'Votes': '12,240',
                               'Won': False}
    
    sen2014 = load_election_data('senate', '2014')
    sen2014.shape == (82, 8)
    sen2014.ix[0].to_dict == {'Chamber': 'S',
                              'District': '1',
                              'Incombant': 'NA',
                              'Name': 'Stan White',
                              'Party': 'D',
                              'Session': '2014',
                              'Votes': '27,957',
                              'Won': False}
    
    hou2014 = load_election_data('house', '2014')
    hou2014.shape == (182, 8)
    hou2014.ix[0].to_dict() == {'Chamber': 'H',
                                'District': '1',
                                'Incombant': 'NA',
                                'Name': 'Garry Meiggs',
                                'Party': 'D',
                                'Session': '2014',
                                'Votes': '10,082',
                                'Won': False}
    
    """
    order = ['District', 'Session', 'Chamber', 'Name', 'Party', 'Incombant', 'Won', 'Votes']
    clu = {'senate' : 'S', 'house' : 'H'}
    if int(session) >= 2016:
        with open(os.path.join(get_data_dir(), 
                               os.path.join('raw', 
                                            election_data_key[chamber][session])),
                  'rb') as f:
            df = parse_election_data_cur(f.readlines(), 
                                         chamber=clu[chamber],
                                         session=session)
    elif int(session) == 2014:
        with open(os.path.join(get_data_dir(), 
                               os.path.join('raw', 
                                            election_data_key[chamber][session])),
                  'rb') as f:
            df = parse_election_data_2014(f.readlines(), clu[chamber])
            
    df = df[order]
    return(df)
    


def save_corpus(name, corpus, data_sub_dir="processed", compression='gzip'):
    data_dir = get_data_dir(which='project')
    path = os.path.join(data_dir, data_sub_dir, name)
    os.mkdir(path)
    corpus.save(path=path, name=name, compression=compression)
    
    
def load_corpus(name, data_sub_dir="processed", compression='gzip'):
    data_dir = get_data_dir(which='project')
    path = os.path.join(data_dir, data_sub_dir, name)
    return(Corpus.load(path=path, name=name, compression=compression))