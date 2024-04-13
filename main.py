import string
import json
from datamodel import Listing, Observation, Order, OrderDepth, ProsperityEncoder, Symbol, Trade, TradingState
from typing import Any
import math

AMETHYSTS = "AMETHYSTS"
STARFRUIT = "STARFRUIT"

class Trader:
    
    def getPositionLimit(self, product):
        position_limits = {AMETHYSTS: 20, STARFRUIT: 20}
        return position_limits[product]

    def getDefaultPrice(self, product):
        default_prices = {AMETHYSTS: 10000, STARFRUIT: 5000}
        return default_prices[product]

    def getPosition(self, product, state: TradingState):
        return state.position.get(product, 0)

    def amethystsStrat(self, state: TradingState):
        amethystsPosition = self.getPosition(AMETHYSTS, state)

        orders = []

        howManyBuyAmethysts = self.getPositionLimit(AMETHYSTS) - amethystsPosition
        howManySellAmethysts = -(self.getPositionLimit(AMETHYSTS) + amethystsPosition)

        maxDeviation = 3.8


        for buyPrice, buyVolume in state.order_depths[AMETHYSTS].buy_orders.items():
            if buyPrice > self.getDefaultPrice(AMETHYSTS):

                dev = buyPrice - self.getDefaultPrice(AMETHYSTS)
                scalar = dev / maxDeviation

                amount = int(math.ceil(scalar * howManySellAmethysts))

                print(f"BUY -> PRICE: {buyPrice} -> AMOUNT: {buyVolume} -> MY VOLUME {amount}")

                newOrder = Order(AMETHYSTS, buyPrice, amount)
                orders.append(newOrder)


        for sellPrice, sellVolume in state.order_depths[AMETHYSTS].sell_orders.items():
            if sellPrice < self.getDefaultPrice(AMETHYSTS):

                dev = self.getDefaultPrice(AMETHYSTS) - sellPrice
                scalar = dev / maxDeviation

                amount = int(math.ceil(scalar * howManyBuyAmethysts))

                print(f"SELL -> PRICE: {buyPrice} -> AMOUNT: {buyVolume} -> MY VOLUME {amount}")

                newOrder = Order(AMETHYSTS, buyPrice, amount)
                orders.append(newOrder)

        return orders

    def run(self, state: TradingState):

        # Orders to be placed on exchange matching engine
        result = {}
        
        # logger.print(state)

        result[AMETHYSTS] = self.amethystsStrat(state)

        traderData = "SAMPLE"
        conversions = 1
        return result, conversions, traderData