#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 20:56:42 2017

@author: immersinn
"""

import os
import unittest

from bs4 import BeautifulSoup as bs
from ncga import extract_dailyfeed_content


THIS_DIR = os.path.dirname(os.path.abspath(__file__))



class TestProcessDailyfeed(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        file_names = {'S' : 'senate_dailyfeed_01.html',
                      'H' : 'house_dailyfeed_01.html'}
        cls.pages = {}
        for chamber in file_names:
            with open(os.path.join(THIS_DIR,
                                   'test_data/dailyfeed_html',
                                   file_names[chamber]),
                     'rb') as f:
                cls.pages[chamber] = f.read()
        cls.soups = {chamber : bs(cls.pages[chamber],
                                  'html.parser') \
                     for chamber in cls.pages}
    
    def test_build_url(self):
        """Test function for building the ``dailyfeed`` URLs
        """        
        
        senate_url = "http://www.ncleg.net/gascripts/lastaction/todaysfiledaction.pl?Biennium=2015&ActionChamber=S&DateReport=06%2F01%2F2016"
        house_url = "http://www.ncleg.net/gascripts/lastaction/todaysaction.pl?Biennium=2015E3&ActionChamber=H&DateReport=12%2F14%2F2016"
        
        info = {'H' : {'bien' : '2015E3',
                       'year' : 2016,
                       'mo' : 12,
                       'day' : 14,
                       'filed' : False,
                       'url' : house_url},
    
                'S' : {'bien' : 2015,
                       'year' : 2016,
                       'mo' : 6,
                       'day' : 1,
                       'filed' : True,
                       'url' : senate_url}
                }
                
        for chamber in info:
            d = info[chamber]
            test_url = extract_dailyfeed_content.build_query_url_from_date(biennium=d['bien'],
                                                                           da=d['day'],
                                                                           yr=d['year'],
                                                                           mo=d['mo'],
                                                                           chamber=chamber,
                                                                           filed=d['filed'])
            self.assertEqual(d['url'], test_url)
            
    def test_get_content_table(self):
        true_data = {'H' : {'n_rows' : 139,
                            'h_text' : 'BillShort TitleActionDateAction\xa0Text',
                            'r_text' : '\nH59\n\nRevenue Laws Technical Changes.\n\nH\n06/21/2017\nSigned by Gov. 6/21/2017\n'},
                     'S' : {'n_rows' : 123,
                            'h_text' : 'BillShort TitleActionDateAction\xa0Text',
                            'r_text' : '\nH21\n\nDriver Instruction/Law Enforcement Stops.\n\nS\n06/21/2017\nWithdrawn From Cal\n'}
                     }
        for chamber in self.soups:
            header, rows = extract_dailyfeed_content.get_content_table(self.soups[chamber])
            self.assertEqual(true_data[chamber]['h_text'], header.text)
            self.assertEqual(true_data[chamber]['n_rows'], len(rows))
            self.assertEqual(true_data[chamber]['r_text'], rows[0].text)
            
            
    def test_process_content_table(self):
        true_data = {'H' : {0 : {'Bill' : 'H59',
                                 'ActionChamber' : 'H',
                                 'Title' : 'Revenue Laws Technical Changes.',
                                 'Date' : '06/21/2017',
                                 'ActionText' : 'Signed by Gov. 6/21/2017'},
                            -1 : {'Bill' : 'S681',
                                  'ActionChamber' : 'H',
                                  'Title' : 'Honor Ralph Hunt, Sr., Former Member.',
                                  'Date' : '06/21/2017',
                                  'ActionText' : 'Ordered Enrolled'}
                              }
                    }
        with open(os.path.join(THIS_DIR,
                               'test_data/dailyfeed_html/house_tablerows.txt'), 
                    'r') as f:
            rows = bs(f.read(), 'html.parser').find_all('tr')
                    
        df = extract_dailyfeed_content.process_content_table(rows)
        for i in [0, -1]:
            self.assertDictEqual(true_data['H'][i],
                                 df.loc[df.index[i],:].to_dict())
            
    def test_content_from_full_page(self):
        true_data = {'H' : {0 : {'Bill' : 'H59',
                                 'ActionChamber' : 'H',
                                 'Title' : 'Revenue Laws Technical Changes.',
                                 'Date' : '06/21/2017',
                                 'ActionText' : 'Signed by Gov. 6/21/2017',
                                 'Session' : '2017',
                                 'Link' : 'http://www.ncleg.net/gascripts/BillLookUp/BillLookUp.pl?Session=2017&BillID=H59'},
                            -1 : {'Bill' : 'S681',
                                  'ActionChamber' : 'H',
                                  'Title' : 'Honor Ralph Hunt, Sr., Former Member.',
                                  'Date' : '06/21/2017',
                                  'ActionText' : 'Ordered Enrolled',
                                  'Session' : '2017',
                                  'Link' : 'http://www.ncleg.net/gascripts/BillLookUp/BillLookUp.pl?Session=2017&BillID=S681'},
                              }
                    }
                            
        df = extract_dailyfeed_content.content_from_full_page(self.pages['H'], '2017')
        for i in [0, -1]:
            self.assertDictEqual(true_data['H'][i],
                                 df.loc[df.index[i],:].to_dict())