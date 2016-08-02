# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 10:03:48 2016

@author: delvin
"""

from pairtrading import PairTrading, PriceType
import math

class PairTrading_Method1(PairTrading):
    def __init__(self):
        PairTrading.__init__(self)
        
    def _marketOpenAction(self, ts, spread, price1, price2):
        PairTrading._marketOpenAction(self, ts, spread, price1, price2)
        self.mean = spread
        
    def _intraMarketActions(self, ts, spread, price1, price2):
        PairTrading._intraMarketActions(self, ts, spread, price1, price2)
    
        # entry
        targetPos = self.getTargetPosition(spread)
        if targetPos > 0 and self.getNetPosition(self.today) < targetPos:
            print("long Target Pos ", targetPos,  "Hold Pos", self.getNetPosition(self.today))
            self.buy(self.today, ts, price1, price2, targetPos - self.getNetPosition(self.today))            
            self.tm.showTradeBook(self.today)
            input("Wait")
            
        if targetPos < 0 and self.getNetPosition(self.today) > targetPos:
            print("short Target Pos ", targetPos,  "Hold Pos", self.getNetPosition(self.today))
            self.sell(self.today, ts, price1, price2, self.getNetPosition(self.today) - targetPos)            
            self.tm.showTradeBook(self.today)
            input("Wait")
            
        # exit
        if targetPos > 0 and self.getNetPosition(self.today) > targetPos+1:
            self.sell(self.today, ts, price1, price2, self.getNetPosition(self.today)-targetPos-1)
 
            #self.tm.showTradeBook(self.today)
            
        if targetPos < 0 and self.getNetPosition(self.today) < targetPos-1:
            self.buy(self.today, ts, price1, price2,  targetPos-1-self.getNetPosition(self.today))

            #self.tm.showTradeBook(self.today)
    
    def getTargetPosition(self, spread):
        levelNum = float(spread - self.mean) / float(self.level)
        if levelNum > 0:
            levelNum = math.floor(levelNum)
        if levelNum < 0:
            levelNum = math.ceil(levelNum)
        return -levelNum

if __name__ == "__main__":
    strat = PairTrading_Method1()
    strat.setParameter(("HHI", "HSI"), 2, 1, 0.005, PriceType.ln)
    filename = "C:\Users\gdpan\Desktop\cointegration\HHI_HSI_second_small.csv";
    strat.loadData(filename)
    strat.run()