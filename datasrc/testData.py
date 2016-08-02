# -*- coding: utf-8 -*-
"""
Created on Tue Aug 02 16:50:42 2016

@author: gdpan
"""

from inc import financeMeta
from datasrc import getDataFile
from basis.io import loadComponent, loadData
import matplotlib.pyplot as plt
from matplotlib.dates import num2date

symbol_list = loadComponent(financeMeta)
symData = dict()
plt.figure(figsize=(50, 30), dpi = 200)
for symbol in symbol_list:
    filename = getDataFile(symbol)
    symData[symbol] = loadData(filename)
    ts, clp = symData[symbol].getTimeAndReturn()
    ts = map(num2date, ts)
    plt.xticks(ts)
    plt.plot(ts, clp)
    print("Finish %s" % symbol)
    
plt.savefig("testDate.png")