# -*- coding: utf-8 -*-
"""
Created on Tue Aug 02 18:28:14 2016

@author: gdpan
"""

class Bar:
    def __init__(self, datastr):     
        self.ts = float(datastr[0]) # epoch time
        self.open = float(datastr[1])
        self.high = float(datastr[2])
        self.low = float(datastr[3])
        self.close = float(datastr[4])
        self.vol = float(datastr[5])
        
    def show(self):
        pass
    
    def getTimeStamp(self):
        return self.ts
        
class BarSeries:
    def __init__(self):
        self.bars = dict()
        
    def addBar(self, Bar):
        self.bars[Bar.getTimeStamp()] = Bar
        
    def getTimeAndClose(self):
        ts = []
        cl = []
        for t in sorted(self.bars.keys()):
            ts.append(t)
            cl.append(self.bars[t].close)
        return ts, cl
        
    def getTimeAndReturn(self):
        ts, cl = self.getTimeAndClose()
        clp = [ x / cl[0] * 100 for x in cl]
        return ts, clp