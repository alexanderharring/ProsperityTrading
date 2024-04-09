from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string


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

        #basically how many can we buy and sell

        howManyBuyAmethysts = self.getPositionLimit(AMETHYSTS) - amethystsPosition
        howManySellAmethysts = -(self.getPositionLimit(AMETHYSTS) + amethystsPosition)

        buyOrder = Order(AMETHYSTS, self.getDefaultPrice(AMETHYSTS) - 1, howManyBuyAmethysts)
        sellOrder = Order(AMETHYSTS, self.getDefaultPrice(AMETHYSTS) + 1, howManySellAmethysts)

        orders.append(buyOrder)
        orders.append(sellOrder)

        return orders

    def run(self, state: TradingState):

        # Orders to be placed on exchange matching engine
        result = {}
        
        # logger.print(state)

        result[AMETHYSTS] = self.amethystsStrat(state)

        traderData = "SAMPLE" 
        conversions = 1
        # logger.flush(state, result, conversions, traderData)

        return result, conversions, traderData