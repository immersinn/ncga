#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 18:50:08 2017

@author: immersinn
"""

import os
import unittest

from bs4 import BeautifulSoup as bs
from ncga import extract_billpage_content
from targets import TARGET_BILLPAGE_LINKS,TARGET_BILLPAGE_METAS

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

          
class TestExtractBillpageContent(unittest.TestCase):
    
    def setUp(self):
        """Load the necessary data for the tests"""
        file_names = ['bill_0', 'bill_1']
        pages = []
        for fn in file_names:
            with open(os.path.join(THIS_DIR, "test_data/billpage_html", fn + '.txt'),
                      'rb') as f:
                pages.append(f.read())
        self.soups = [bs(page, 'html.parser') for page in pages]
    
    def test_extract_links(self):
        """Test if links to Bill Texts are properly extracted"""
        links = [extract_billpage_content.extract_links(soup) for \
                 soup in self.soups]
        self.assertEqual(links, TARGET_BILLPAGE_LINKS)
        
    def test_extract_meta(self):
        """Test if metadata from Bill Pages are properly extracted"""
        metas = [extract_billpage_content.extract_meta(soup) for \
                 soup in self.soups]
        self.assertEqual(metas, TARGET_BILLPAGE_METAS)