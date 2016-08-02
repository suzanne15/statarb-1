# -*- coding: utf-8 -*-
"""
Created on Tue Aug 02 08:54:39 2016

@author: gdpan
"""
from inc import datadir, allMeta
from datetime import datetime
import matplotlib as mplt
import csv, os
from basis.io import loadComponent

def getDataFile(symbol):
    return datadir + '%s.csv' % symbol
    
def downloadData():    
    start = datetime(2000, 1,1)
    end = datetime.today()
    
    if not os.path.exists(datadir):
        os.makedirs(datadir)
    
    symbol_list = loadComponent(allMeta)
        
    for symbol in symbol_list:
        data = mplt.finance.quotes_historical_yahoo_ohlc(symbol, start, end)
        filename = getDataFile(symbol)
        with open(filename, "wb") as f:
            writer = csv.writer(f)
            writer.writerow(("epoch time", "open", "high", "low", "close", "volume"))
            writer.writerows(data)
            print("Finish %s" % symbol)
    
if __name__ == "__main__":
    downloadData()