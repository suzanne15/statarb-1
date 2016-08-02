# -*- coding: utf-8 -*-
"""
Created on Tue Aug 02 16:50:42 2016

@author: gdpan
"""

from inc import financeMeta
from datasrc import getDataFile
from basis.io import loadComponent, loadData
import matplotlib.pyplot as plt
from basis.timefunc import epochDate2Date

symbol_list = loadComponent(financeMeta)
symData = dict()
for symbol in symbol_list:
    filename = getDataFile(symbol)
    symData[symbol] = loadData(filename)
    ts, clp = symData[symbol].getTimeAndReturn()
    ts = map(epochDate2Date, ts)
    plt.plot(ts, clp)
    
