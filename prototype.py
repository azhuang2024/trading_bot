import os
import sys
import pandas as pd
import numpy as np
import csv
import time
import blankly

class Bot:


    def __init__(self):
        self.nextOperationBuy = True
        self.balance = 0
        self.time = 0
        self.DIP_THRESHOLD = -2.25
        self.UPWARD_TREND_THRESHOLD = 1.5
        self.PROFIT_THRESHOLD = 1.25
        self.STOP_LOSS_THRESHOLD = -2.00
        self.lastOpPrice = 100.00
        self.prices = pd.read_csv('prices.csv', sep=',')
        print(self.prices)

    # DO: GET request to exchange API for our account's balances
    # RETURN: Balances
    def getBalance(self):
        return self.balance

    # DO: GET request to exchange API for current prices of the asset
    # RETURN: Market Price
    def getMarketPrice(self):
        return self.prices['Price'][self.time]

    # DO: 1. Calculate the amount to sell (based on some threshold you get)
    #       e.g. 50 % total balance
    #     2. Send POST requeest to exchange API to do a SELL operation
    # RETURN: Price at operation execution
    def placeSellOrder(self):
        market_price = self.getMarketPrice()
        self.balance += market_price
        return market_price
    
    # DO: 1. Calculate the amount to buy (based on some threshold)
    #     2. Send a POST request to exchange API to do a BUY operation
    # RETURN: Price at operation execution
    def placeBuyOrder(self):
        market_price = self.getMarketPrice()
        self.balance -= market_price
        return market_price

    def attemptToMakeTrade(self):
        currentPrice = self.getMarketPrice()
        percentageDiff = (currentPrice - self.lastOpPrice)/self.lastOpPrice*100
        if self.nextOperationBuy:
            self.tryToBuy(percentageDiff)
        else:
            self.tryToSell(percentageDiff)
        
    def tryToBuy(self, percentageDiff):
        if percentageDiff >= self.UPWARD_TREND_THRESHOLD or percentageDiff <= self.DIP_THRESHOLD:
            self.lastOpPrice = self.placeBuyOrder()
            self.nextOperationBuy = False
            print("\tBought at: ", self.lastOpPrice)

    def tryToSell(self, percentageDiff):
        if percentageDiff >= self.PROFIT_THRESHOLD or percentageDiff <= self.STOP_LOSS_THRESHOLD:
            self.lastOpPrice = self.placeSellOrder()
            self.nextOperationBuy = True
            print("\tSold at: ", self.lastOpPrice)
            print("\tBalance: ", self.balance)

    def startBot(self):
        for i in range(16):
            print("Timestamp: ", self.time)
            self.attemptToMakeTrade()
            # time.sleep(3)
            self.time += 1
        if self.nextOperationBuy == False:
            self.balance += self.prices['Price'][self.time-1]
        print("Final Balance: ", self.balance)
        

def main():
    trading_bot = Bot()
    trading_bot.startBot()


if __name__ == "__main__":
    main()

