# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 16:48:02 2016

@author: delvin
"""

from ds import loadDailyData
from PnLSystem import tradeManager, TradeAction

class Strategy:
    def __init__(self):
        self.dataReady = False
    
    def loadData(self, fileName):
        self.dailyData = loadDailyData(fileName)       
        self.dataReady = True
    
    def setParameter(self, symbol):
        self.symbol = symbol
        self.tm = tradeManager(symbol)
    
    def buy(self, date, time, price, contractNum):
        self.tm.addTradeRecord(date, time, TradeAction.Long, price, contractNum)
    
    def sell(self, date, time, price, contractNum):
        self.tm.addTradeRecord(date, time, TradeAction.Short, price, contractNum)
    
    def getPnL(self):
        pass
    
    def getTradeRecord(self):
        pass
    
    def run(self):
        pass
    
    def getNetPosition(self, date):
        return self.tm.getNetPosition(self.symbol, date)
    

if __name__ == "__main__":
    strat = Strategy()
    filename = "C:\Users\delvin\Desktop\data\HHI_HSI_second_small.csv";
    strat.loadData(filename)