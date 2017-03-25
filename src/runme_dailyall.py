#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 15:30:23 2017

@author: immersinn

Single "runme" for all daily (M-F) tasks that need to be performed in a 
particular sequence.
"""

import runme_dailyupdate_bills
import runme_update_billpages


if __name__=="__main__":
    
    runme_dailyupdate_bills.main()
    runme_update_billpages.main()