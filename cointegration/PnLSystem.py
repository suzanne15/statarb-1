# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 17:26:44 2016

@author: delvin
"""

from enum import Enum
from logger import infor

class TradeAction(Enum):
    Long = 1
    Short = 2
    Entry = 3
    Exit = 4

class TradeRecord:
    def __init__(self, timestamp, tradeaction, price, contractNum):
        self.ts = timestamp
        self.action = tradeaction
        self.price = price
        self.contractNum = contractNum
        
    def show(self):
        msg = "{ts} {action} {price} {cn}".format(
                ts = self.ts, action = self.action, price =self.price,
                cn = self.contractNum)
        infor(msg)
        

class TradeSheet:
    def __init__(self):
        self.trades = []
    
    def addTradeRecord(self, tr):
        self.trades.append(tr)
        
    def showAllTrades(self):
        if len(self.trades) == 0:
            infor("No trade in tradebook")
            return
        for tr in self.trades:
            tr.show()

    def computePnL(self, price):
        if len(self.trades) == 0:
            return 0
        pnl = 0
        for tr in self.trades:
            if self.action == TradeAction.Long:
                pnl = pnl - tr.price * tr.contractNum
            if self.action == TradeAction.Short:
                pnl = pnl + tr.price * tr.contractNum
        return pnl
    
    def getNetPosition(self):
        return self.getLongPosition() + self.getShortPosition()
        
    def getLongPosition(self):
        if len(self.trades) == 0:
            return 0
        pos = 0
        for t in self.trades:
            if t.action == TradeAction.Long:
                pos = pos + t.contractNum
        return pos
        
    def getShortPosition(self):
        if len(self.trades) == 0:
            return 0
        pos = 0
        for t in self.trades:
            if t.action == TradeAction.Short:
                pos = pos - t.contractNum
        return pos
        
class TradeBook:
    def __init__(self, symbol):
        self.book = dict()
        self.symbol = symbol

    def addTradeSheet(self, d, tradesheet):            
        self.book[d] = tradesheet

    def getTradeSheet(self, d):
        if d not in self.book.keys():
            self.book[d] = TradeSheet()
            
        return self.book[d]

    def computeNetProfit(self, since, till):
        pass

    def computeSharpeRatio(self, since, till):
        pass

class tradeManager:
    def __init__(self, symbolList):
        self.tbs = dict()
        self.symbols = symbolList
        for s in self.symbols:
            self.tbs[s] = TradeBook(s)
    
    # each symbol has a trade book        
    def getTradeBook(self, symbol):        
        return self.tbs[symbol]

    def addTradeRecord(self, symbol, date, ts, action, price, contractNum):      
        tr = TradeRecord(ts, action, price, contractNum)
        self.getTradeBook(symbol).getTradeSheet(date).addTradeRecord(tr)

    def getNetPosition(self, symbol, date):
        np = self.getTradeBook(symbol).getTradeSheet(date).getNetPosition()
        return np        
        
    def getPnL(self, symbol, date):
        return self.getTradeBook(symbol).getTradeSheet(date).computePnL()
        
    def showTradeBook(self, symbol, date):
        self.getTradeBook(symbol).getTradeSheet(date).showAllTrades()

        
class pairTradeManager(tradeManager):
    def __init__(self, symbol1, symbol2, contractNum1, contractNum2):
        tradeManager.__init__(self, (symbol1, symbol2))
        self.contractNum1 = contractNum1
        self.contractNum2 = contractNum2
        
    def addPairTradeRecord(self, date, ts, action, price1, price2, pairNum):
        if action == TradeAction.Long:
            tradeManager.addTradeRecord(self, self.symbols[0], date, ts, TradeAction.Long, price1, self.contractNum1 * pairNum)
            tradeManager.addTradeRecord(self, self.symbols[1], date, ts, TradeAction.Short, price2, self.contractNum2 * pairNum)
            infor("Long symbol1 " + str(self.contractNum1 * pairNum) + " short symbol2 " + str(self.contractNum2 * pairNum))

        if action == TradeAction.Short:
            tradeManager.addTradeRecord(self, self.symbols[0], date, ts, TradeAction.Short, price1, self.contractNum1 * pairNum)
            tradeManager.addTradeRecord(self, self.symbols[1], date, ts, TradeAction.Long, price2, self.contractNum2 * pairNum)
            infor("Short symbol1 " + str(self.contractNum1 * pairNum) + " long symbol2 " + str(self.contractNum2 * pairNum))
 
       
    def getNetPosition(self, date):
        pos1 = tradeManager.getNetPosition(self, self.symbols[0], date)
        pos2 = tradeManager.getNetPosition(self, self.symbols[1], date)
        
        if pos1 == 0 and pos2 == 0:
            return 0
        
        return float(pos1) / float(self.contractNum1)
            
    def getPnL(self, date):
        pnl1 = tradeManager.getPnL(self, tradeManager.symbols[0], date)
        pnl2 = tradeManager.getPnL(self, tradeManager.symbols[1], date)
        return pnl1 + pnl2
        
    def showTradeBook(self, date):
        infor("Show trade book on " + str(date))
        tradeManager.showTradeBook(self, self.symbols[0], date)
        tradeManager.showTradeBook(self, self.symbols[1], date)
            