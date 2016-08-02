# -*- coding: utf-8 -*-
"""
Cointegration Analysis

Created on Mon Jun 13 18:57:04 2016

@author: delvin
"""

import csv, collections
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std

filename = "C:\Users\delvin\Desktop\data\HHI_HSI_second.csv";

def loadData(filename):
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

def getDate(ts):
    date, time = ts.split(" ")
    return float(date), float(time)    
    
def processDailyData(secData):
    dailyData = dict()
    
    for key in secData.keys():
        d, t = getDate(key)
        if d not in dailyData.keys():
            dailyData[d] = dict()            
        dailyData[d][t] = secData[key]
        
    for d in dailyData.keys():
        dailyData[d] = collections.OrderedDict(sorted(dailyData[d].items()))
    
    dailyData = collections.OrderedDict(sorted(dailyData.items()))
    return dailyData
        
def checkDailyData(dailyData):
    for d in dailyData.keys():
        intraDay = dailyData[d]
        for t in intraDay.keys():
            print(d, t, intraDay[t])


def findMostClosePair(ratio, maxVal):
    ratioTable = dict()
    for i in range(1, maxVal+1):
        for j in range(1, maxVal+1):
            ratioTable[float(j)/float(i)] = [i, j]
    
    head = 0;
    tail = 0;
    keylist = sorted(ratioTable.keys())
    for i in range(0, len(keylist)-2):
        if keylist[i] <= ratio and ratio <= keylist[i+1]:
            head = keylist[i]
            tail = keylist[i+1]
            break
    if head == ratio:
        return ratioTable[head]

    if tail == ratio:
        return ratioTable[tail]
        
    return ratioTable[head] if sum(ratioTable[head]) < sum(ratioTable[tail]) else ratioTable[tail]
               

secData, data1, data2 = loadData(filename)
dailyData = processDailyData(secData)
# checkDailyData(dailyData)

#np.log is ln function
ldata1 = np.array(np.log(data1)).reshape(-1, 1) 
ldata2 = np.array(np.log(data2)).reshape(-1, 1)
ldata2_arg = np.column_stack((ldata2,np.ones(len(data2))))


# linear regression
model = sm.OLS(ldata1, ldata2_arg) # data1 is y, data2 is x
results = model.fit()
print(results.summary())
ratio = results.params[0]
Instr1, Instr2 = findMostClosePair(ratio, 5)
Instr1 = 2
Instr2 = 1
print("Use the following ratio")
print(Instr1, Instr2)

# adfuller test
#x = Instr1*ldata1 - Instr2*ldata2
#adfstat  = adfuller(x.ravel())
#print adfstat

timeVec = []
spreadVec = []

count = 0
figureCount = 0
spread = [] 
for d in dailyData.keys():
    intradata = dailyData[d]   
        
  
    for k in intradata.keys():
        spread.append(np.log(intradata[k][0]) * Instr1 - np.log(intradata[k][1] * Instr2))
    
    if count % 1 == 0 and count <> 0:
        plt.figure(figureCount)
        figureCount = figureCount + 1
        plt.title(d)               
        plt.plot(spread)
        spread = [] 

    count = count + 1 
    for k in intradata.keys():
        timeVec.append(d * 1000000 + k)
        spreadVec.append(np.log(intradata[k][0]) * Instr1 - np.log(intradata[k][1]) * Instr2)


plt.title("Long Term")
plt.plot(spreadVec)
