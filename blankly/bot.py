import blankly
from blankly.indicators import rsi, macd, sma
from blankly.utils import trunc
# API SECRET KEY: eZUlyxbZ1AP+ZN92QJJ+MCwc325NUMxCc8CZHpVN/Fj8oX+yXgOCoDwv6BEegYUq9f/x6vaXV0ycxfOiJ+tPgg==
# passphrase: jkaz04251211
# API KEY: 4cedb7e759bc6cc696933be5375fdba4


def price_event(price, symbol, state: blankly.StrategyState):
    """ This function will give an updated price every 15 seconds from our definition below """
    state.variables['history'].append(price)
    rsi = blankly.indicators.rsi(state.variables['history'])
    if rsi[-1] < 30 and not state.variables['owns_position']:
        # Dollar cost average buy
        buy = trunc(state.interface.cash/price,8)
        state.interface.market_order(symbol, side='buy', size=buy)
        state.variables['owns_position'] = True
    elif rsi[-1] > 70 and state.variables['owns_position']:
        # Dollar cost average sell
        curr_value = state.interface.account[state.base_asset].available
        state.interface.market_order(symbol, side='sell', size=curr_value)
        state.variables['owns_position'] = False


def init(symbol, state: blankly.StrategyState):
    # Download price data to give context to the algo
    state.variables['open_history'] = state.interface.history(symbol, to=150, return_as='deque',
                                                         resolution=state.resolution)['open']
    state.variables['high_history'] = state.interface.history(symbol, to=150, return_as='deque',
                                                         resolution=state.resolution)['high']
    state.variables['low_history'] = state.interface.history(symbol, to=150, return_as='deque',
                                                         resolution=state.resolution)['low']                                                     
    state.variables['close_history'] = state.interface.history(symbol, to=150, return_as='deque',
                                                         resolution=state.resolution)['close']
    state.variables['volume_history'] = state.interface.history(symbol, to=150, return_as='deque',
                                                         resolution=state.resolution)['volume']
    
    state.variables['owns_position'] = False


if __name__ == "__main__":
    # Data preprocessing


    # Authenticate coinbase pro strategy
    exchange = blankly.CoinbasePro(portfolio_name="my cool portfolio")
    paper_trade = blankly.PaperTrade(exchange, initial_account_values={'USD': 10000})

    # Use our strategy helper on coinbase pro
    strategy = blankly.Strategy(paper_trade)

    # Run the price event function every time we check for a new price - by default that is 15 seconds
    strategy.add_price_event(price_event, symbol='BTC-USD', resolution='1d', init=init)

    # Start the strategy. This will begin each of the price event ticks
    # strategy.start()
    # Or backtest using this
    results = strategy.backtest(to='1y', initial_values={'USD': 10000})
    print(results)
