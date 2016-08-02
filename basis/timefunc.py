# -*- coding: utf-8 -*-
"""
Created on Tue Aug 02 20:51:00 2016

@author: gdpan
"""
import time

def epochDate2Date(epoch):
    return time.strftime("%Y-%m-%d", time.localtime(epoch))