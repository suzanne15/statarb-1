# -*- coding: utf-8 -*-
"""
Created on Tue Aug 02 16:43:58 2016

@author: gdpan
"""
import sys
sys.path.append("../")
import os, csv
from basis.bar import Bar, BarSeries

def cleanFile(inputfile, outfile):
    def cleanRow(row):
        listNew = []
        for elem in row:
            if len(elem) > 0:
                listNew.append(elem)
        return listNew
        
    with open(inputfile, "rb") as inf:
        with open(outfile, "wb") as outf:
            reader = csv.reader(inf)
            writer = csv.writer(outf)
            for row in reader:
                row = cleanRow(row)
                writer.writerow(row)
        
def loadComponent(hsicomp):
    tickers = []
    if os.path.exists(hsicomp):
        with open(hsicomp, "rb") as inf:
            reader = csv.reader(inf)
            for row in reader:
                tickers.append(row[0])    
    return tickers
    
def loadData(fileName):
    bs = BarSeries()
    with open(fileName, "rb") as inf:
        reader = csv.reader(inf)
        rowId = 0
        for row in reader:
            if rowId > 1:
                bs.addBar(Bar(row))
            rowId = rowId + 1
    return bs