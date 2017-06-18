#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 11:44:24 2017

@author: immersinn
"""

import socks
from sockshandler import SocksiPyHandler
from urllib import request
import requests


    
def configure_tor_opener():
    
    opener = request.build_opener(SocksiPyHandler(socks.SOCKS5,
                                                  "127.0.0.1",
                                                  9050))
    return(opener)


def get_page(url, tor=True):
    
    if tor:
        status_test = lambda x: x < 300
        
        opener = configure_tor_opener()
        response = opener.open(url)
        status = status_test(response.status)
        
        if status:
            page = response.read()
        else:
            page = ''
    else:
        response = requests.get(url)
        status = response.status_code == requests.codes.ok
        
        if status:
            page = response.text
        else:
            page = ''
            
    return(page, status)
        
    