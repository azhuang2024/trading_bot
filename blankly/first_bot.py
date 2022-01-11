from blankly import CoinbasePro, Strategy, StrategyState, Interface
from models import OrderDecisionModel, OrderPricingModel

def init(symbol, state: StrategyState):
    # initialize this once and store it into state
    variables = state.variables
    variables['decision_model'] = OrderDecisionModel(symbol)
    variables['pricing_model'] = OrderPricingModel(symbol)
    variables['has_bought'] = False

def price_event(price, symbol, state: StrategyState):
    interface: Interface = state.interface
    variables = state.variables
    decision_model = variables['decision_model']
    pricing_model = variables['pricing_model']

    # make a decision to buy, sell, or hold
    decision = decision_model(symbol)

    if decision == 0:
        curr_value = interface.account[symbol].available * price
        # call pricing model to determine how much to buy
        size_to_buy = pricing_model(price, symbol, interface.cash, curr_value)
        interface.market_order(symbol, 'buy', size_to_buy)
    elif decision == 1:
        curr_value = interface.account[symbol].available * price
        size_to_sell = pricing_model(price, symbol, interface.cash, curr_value)
        interface.market_order(symbol, 'sell', size_to_sell)


coinbase = CoinbasePro()
s = Strategy(coinbase)
s.add_price_event(price_event, 'MSFT', resolution='1d', init=init)
# decision_model = OrderDecisionModel() <-- global state can also be accessed in price event functions 
# pricing_model = OrderPricingModel()
s.backtest(initial_values={'USD': 10000}, to='2y')