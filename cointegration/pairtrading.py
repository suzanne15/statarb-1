# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 17:45:06 2016

@author: delvin
"""
from strategy import Strategy
from enum import Enum
import collections
import numpy as np
from PnLSystem import pairTradeManager, TradeAction
from logger import debugger

class PriceType(Enum):
        raw = 1
        log = 2
        ln = 3

class PairTrading(Strategy):
    def __init__(self):
        Strategy.__init__(self)
        self.isDayOpen = False
        self.mean = 0
        
    
    def setParameter(self, symbolList, Instr1ContractNum, Instr2ContractNum, level, pricetype,\
                    marketopen=91500, marketclose=161000):
        self.symbolList = symbolList        
        self.marketopen = marketopen
        self.marketclose = marketclose
        self.I1Num = Instr1ContractNum
        self.I2Num = Instr2ContractNum
        self.level = level
        self.pricetype = pricetype
        self.tm = pairTradeManager(symbolList[0], symbolList[1], self.I1Num, self.I2Num)
     
    def getNetPosition(self, date):
        return self.tm.getNetPosition(date)
    
    def loadData(self, filename):
        Strategy.loadData(self, filename)
        self.spread = collections.OrderedDict()        
        for d in self.dailyData.keys():
            data = self.dailyData[d]

            if self.pricetype == PriceType.raw:
                spread = {t : data[t][0] * self.I1Num -data[t][1]*self.I2Num for t in data.keys()}
                self.spread[d] = collections.OrderedDict(sorted(spread.items()))
                
            if self.pricetype == PriceType.ln:
                spread = {t : np.log(data[t][0])*self.I1Num - np.log(data[t][1])*self.I2Num for t in data.keys()}
                self.spread[d] = collections.OrderedDict(sorted(spread.items()))
                
    def sell(self, date, time, price1, price2, pairNum):
        self.tm.addPairTradeRecord(date, time, TradeAction.Short, price1, price2, pairNum)
        msg = "{date} {time} {action} {p1} {p2} {NO}".format(
                date = date, time = time, action = TradeAction.Short, 
                p1 = price1, p2 = price2, NO = pairNum)
        debugger(msg)
        
    def buy(self, date, time, price1, price2, pairNum):
         self.tm.addPairTradeRecord(date, time, TradeAction.Long, price1, price2, pairNum)
         msg = "{date} {time} {action} {p1} {p2} {NO}".format(
                date = date, time = time, action = TradeAction.Long, 
                p1 = price1, p2 = price2, NO = pairNum)
         debugger(msg)
                
    def _marketOpenAction(self, ts, spread, price1, price2):
        pass
        
    def _intraMarketActions(self, ts, spread, price1, price2):
        pass

    def _marketCloseAction(self, ts, spread, price1, price2):
        pass

    def run(self):
        for d in self.dailyData.keys():            
            priceData = self.dailyData[d]
            spreadData = self.spread[d]                     
            self.isDayOpen = True
            self.today = d
            for t in sorted(priceData.keys()):
                if self.marketopen <= t and t < self.marketclose:
                    if self.isDayOpen:
                        self.isDayOpen = False
                        self._marketOpenAction(t, spreadData[t], priceData[t][0], priceData[t][1])
                    else:
                        self._intraMarketActions(t, spreadData[t], priceData[t][0], priceData[t][1])
                if t >= self.marketclose:
                    self._marketCloseAction(t, spreadData[t], priceData[t][0], priceData[t][1])
                    break
                    

if __name__ == "__main__":
    strat = PairTrading()
    strat.setParameter(("HHI", "HSI"), 2, 1, 0.005, PriceType.ln)
    filename = "C:\Users\delvin\Desktop\data\HHI_HSI_second_small.csv";
    strat.loadData(filename)
    strat.run()