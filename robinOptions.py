from itertools import tee
from linecache import getline
from msvcrt import kbhit
import math
import robin_stocks
import robin_stocks.robinhood as r 
import sys
from robin_stocks.robinhood.helper import *
from robin_stocks.robinhood.urls import *
from dotenv import load_dotenv
from multipledispatch import dispatch
import os 
load_dotenv()
newline = "\n"
u = os.environ.get('rh_username')
p = os.environ.get('rh_password')

def start(email, pw):
    try:
        login = r.login(email, pw)
        print("Logged in!")
    except:
        print("Error while trying to login.")

start(u, p) # If authentication code is not cached, then a code will be prompted for the user to enter.

# Development methods/relevant documentation | https://robin-stocks.readthedocs.io/en/latest/robinhood.html
def get_key_list(dict):
    return dict.keys()

def get_rounded_amount(amount, digits=None):
    return round(float(amount), digits)

def get_open_stock_info(key=None): # Returns a list of stocks that are currently held. 
    return robin_stocks.robinhood.account.get_open_stock_positions(key) 
#   Valid dict_keys list: (['url', 'instrument', 'instrument_id', 'account', 'account_number', 'average_buy_price', 'pending_average_buy_price', 'quantity', 'intraday_average_buy_price', 'intraday_quantity', 'shares_available_for_exercise', 'shares_held_for_buys', 'shares_held_for_sells', 'shares_held_for_stock_grants', 'shares_held_for_options_collateral', 'shares_held_for_options_events', 'shares_pending_from_options_events', 'shares_available_for_closing_short_position', 'ipo_allocated_quantity', 'ipo_dsp_allocated_quantity', 'avg_cost_affected', 'avg_cost_affected_reason', 'is_primary_account', 'updated_at', 'created_at'])

def get_open_option_info(key=None):
    open_options = robin_stocks.robinhood.options.get_open_option_positions(key) #Returns a list of dictionaries of key/value pairs for each option. If info parameter is provided, a list of strings is returned where the strings are the value of the key that matches info.
#   Valid dict_keys list: (['account', 'average_price', 'chain_id', 'chain_symbol', 'id', 'option', 'type', 'pending_buy_quantity', 'pending_expired_quantity', 'pending_expiration_quantity', 'pending_exercise_quantity', 'pending_assignment_quantity', 'pending_sell_quantity', 'quantity', 'intraday_quantity', 'intraday_average_open_price', 'created_at', 'trade_value_multiplier', 'updated_at', 'url', 'option_id'])
    return open_options

@dispatch(str, str, str, str)
def get_option_instrument_data(ticker, expirationDate, strikePrice, optionType): #BY OPTION INFO; 4 parameters
    option_data = robin_stocks.robinhood.options.get_option_instrument_data(ticker, expirationDate, strikePrice, optionType)
#   Valid dict_keys list: (['chain_id', 'chain_symbol', 'created_at', 'expiration_date', 'id', 'issue_date', 'min_ticks', 'rhs_tradability', 'state', 'strike_price', 'tradability', 'type', 'updated_at', 'url', 'sellout_datetime', 'long_strategy_code', 'short_strategy_code'])
    return option_data

@dispatch(str, str, str, str, str)
def get_option_instrument_data(ticker, expirationDate, strikePrice, optionType, key): #BY OPTION INFO; 5 parameters
    option_data = robin_stocks.robinhood.options.get_option_instrument_data(ticker, expirationDate, strikePrice, optionType, key)
    return option_data

@dispatch(str, str)
def get_option_instrument_data(id, key=None): #BY ID; 2 parameters
    option_data = robin_stocks.robinhood.options.get_option_instrument_data_by_id(id, key) #Returns the option instrument information.
    return option_data 

def get_strike_price(id): #Returns strike price of option id passed in
    return get_option_instrument_data(id, "strike_price")

def get_greeks(id, greek="delta"): #Returns greek value for an option. Valid greek strings are: delta, gamma, theta, rho, vega.
    return robin_stocks.robinhood.options.get_option_market_data_by_id(id, greek)

def get_option_data(id, key=None): 
    return robin_stocks.robinhood.options.get_option_market_data_by_id(id, key)
#   Valid dict_keys list: (['adjusted_mark_price', 'adjusted_mark_price_round_down', 'ask_price', 'ask_size', 'bid_price', 'bid_size', 'break_even_price', 'high_price', 'instrument', 'instrument_id', 'last_trade_price', 'last_trade_size', 'low_price', 'mark_price', 'open_interest', 'previous_close_date', 'previous_close_price', 'updated_at', 'volume', 'symbol', 'occ_symbol', 'state', 'chance_of_profit_long', 'chance_of_profit_short', 'delta', 'gamma', 'implied_volatility', 'rho', 'theta', 'vega', 'high_fill_rate_buy_price', 'high_fill_rate_sell_price', 'low_fill_rate_buy_price', 'low_fill_rate_sell_price'])

def get_stock_holdings(with_dividends=False, ticker=None):
    if ticker == None:
        return robin_stocks.robinhood.account.build_holdings(with_dividends)
    return get_stock_holdings()[ticker]

def get_stock_price(ticker, priceType=None, includeExtendedHours = True): #Price Type is either "bid" or "ask"
    ret = robin_stocks.robinhood.stocks.get_latest_price(ticker, priceType, includeExtendedHours)[0]
    return float(ret)


# All of the following variables are lists.
general_option_info = get_open_option_info()
option_id = get_open_option_info("option_id")
short_or_long = get_open_option_info("type")
symbol = get_open_option_info("chain_symbol")
amount = list(map(get_rounded_amount, get_open_option_info("quantity")))

general_stock_info = get_open_stock_info()
stock_id = get_open_stock_info("instrument_id")

def get_net_delta(ticker=None): # Get portfolio net delta or net delta for a given ticker. 
    net_delta = 0
    if (ticker is None):
        for o in range(len(general_option_info)):
            delta = get_greeks(option_id[o], "delta") * amount[o] #delta list in string form
            if (None in delta): #on opex day, this accounts for options no longer existing
                delta[0] = 0
            delta = sum(list(map(float, delta))) #conversion to float and summed to account for quantity
            net_delta = net_delta+delta if (short_or_long[o] == "long") else net_delta-delta #reverses delta ONLY IF short; eg short put is accounted for as positive delta
        share_delta = get_open_stock_info("quantity") #list of share quantities to add into the net delta
        share_delta = sum(list(map(float, share_delta))) #convert list of strings to floats
        net_delta += (share_delta * 0.01) #0.01 is here because there is x100 multiplication at the end
    else:
        for o in range(len(symbol)):
            if symbol[o] == ticker:
                delta = get_greeks(option_id[o], "delta") * amount[o] #delta list in string form
                if (None in delta): #on opex day, this accounts for options no longer existing
                    delta[0] = 0
                delta = sum(list(map(float, delta))) #conversion to float and summed to account for quantity
                net_delta = net_delta+delta if (short_or_long[o] == "long") else net_delta-delta #reverses delta ONLY IF short; eg short put is accounted for as positive delta
        share_delta = float(get_stock_holdings(False, ticker)["quantity"])
        net_delta += (share_delta * 0.01) #0.01 is here because there is x100 multiplication at the end
    return get_rounded_amount((net_delta * 100), 5) # accounts for options 100x multiplier

def get_net_greek(greek="delta", ticker=None): #Get net gamma, theta, rho, or vega for a given ticker. Behaves somewhat differently to net delta function, but logic is mostly the same.
    if (greek == "delta" or ticker is None):
        return (get_net_delta())
    net_greek = 0
    for o in range(len(general_option_info)):
        current_greek = get_greeks(option_id[o], greek) * amount[o]
        if (None in current_greek):
            current_greek[0] = 0
        current_greek = sum(list(map(float, current_greek)))
        net_greek = net_greek+current_greek if (short_or_long[o] == "long") else net_greek-current_greek 
    return get_rounded_amount((net_greek * 100), 5)


def price_approximation(ticker, deltaSP, deltaVol = 0): #Uses second degree AND first degree taylor series centered at deltaSP to approximate option pricing change; deltaSP = ∂s (change in share price, or X - Xo); deltaVol = change in implied vol as a percentage (for example 5 = 5% increase in IV)
    d = get_net_delta(ticker) # ∂f/∂s, first partial derivative with respect to a change in share price (deltaSP)
    g = get_net_greek("gamma",ticker) # ∂²f/∂s², second partial derivative with respect to a change in share price (deltaSP)
    v = get_net_greek("vega", ticker) # ∂f/∂σ, first partial derivative with respect to a change in volatility (deltaVol)
    approx = (d * deltaSP) + (0.5 * g * (deltaSP ** 2)) #second degree series for delta/gamma
    approx+= (v * deltaVol) #first degree series for volatility
    return approx #will be inaccurate because it is a trunucated series, IE no omega greek used to make the first series third degree.
    
#print(get_net_delta("AMD"))
#print(price_approximation("AMD", (110-90), 2))

def get_leverage_factor(ticker, expiry, strike, type): # Expiry format is YYYY-MM-DD like 2022-07-29; type is "call" or "put"
    id = get_option_instrument_data(ticker, expiry, strike, type, "id") # This is done by ID because the API for getting option instrument market data off of options parameters returns a list rather than dictionary (inconvenient)
    delta = 100 * float(get_greeks(id)[0]) # Returns option ID of passed in option parameters, then returns delta of that option
    option_price = 100 * float(get_option_data(id, "ask_price")[0]) # Get option price by id; uses ask price because this is the most likely to be filled rather than the bid or mid prices
    stock_price =  get_stock_price(ticker)
    multiplier = (stock_price * delta)/option_price # Leverage factor 
    return get_rounded_amount(multiplier, 3) # Rounded leverage factor

def get_news():
    return 0

def get_most_liquid():
    return 0

def get_future_ttm_pe(ticker): #TODO get adjusted TTM pe upon next earnings report for a stock
    return ticker

print(get_stock_price("AMD"))
print(get_leverage_factor("AMD", "2022-07-29", "85", "call"))