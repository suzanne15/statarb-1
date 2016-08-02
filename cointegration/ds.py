# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 17:05:02 2016

@author: delvin
"""

import csv, collections

def _loadData(filename):
    secData = dict()    
    data1 = []
    data2 = []
    
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            secData[row[0]] = float(row[1]), float(row[2])
            data1.append(float(row[1]))
            data2.append(float(row[2]))            
            
    return secData, data1, data2

def _getDate(ts):
    date, time = ts.split(" ")
    return float(date), float(time)    
    
def _processDailyData(secData):
    dailyData = dict()
    
    for key in secData.keys():
        d, t = _getDate(key)
        if d not in dailyData.keys():
            dailyData[d] = dict()            
        dailyData[d][t] = secData[key]
        
    for d in dailyData.keys():
        dailyData[d] = collections.OrderedDict(sorted(dailyData[d].items()))
    
    dailyData = collections.OrderedDict(sorted(dailyData.items()))
    return dailyData
        
def _checkDailyData(dailyData):
    for d in dailyData.keys():
        intraDay = dailyData[d]
        for t in intraDay.keys():
            print(d, t, intraDay[t])
            

def loadDailyData(filename):    
    secData, data1, data2 = _loadData(filename)
    dailyData = _processDailyData(secData)
    #_checkDailyData(dailyData)
    return dailyData