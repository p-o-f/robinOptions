from itertools import tee
from linecache import getline
from msvcrt import kbhit
import robin_stocks
import robin_stocks.robinhood as r 
import sys
from robin_stocks.robinhood.helper import *
from robin_stocks.robinhood.urls import *
from dotenv import load_dotenv
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

def get_rounded_amount(amt):
    return round(float(amt))

def get_open_stock_info(ticker=None, key=None): # Returns a list of stocks that are currently held. <---- FIX THEN ADD IMPLEMENTATION OF THIS METHOD
    return robin_stocks.robinhood.account.get_open_stock_positions(key)

def get_greeks(id, greek="delta"): #Returns greek value for an option. Valid greek strings are: delta, gamma, theta, rho, vega.
    return robin_stocks.robinhood.options.get_option_market_data_by_id(id, greek)

def get_open_option_info(key=None):
    open_options = robin_stocks.robinhood.options.get_open_option_positions(key) #Returns a list of dictionaries of key/value pairs for each option. If info parameter is provided, a list of strings is returned where the strings are the value of the key that matches info.
#   Valid dict_keys list: (['account', 'average_price', 'chain_id', 'chain_symbol', 'id', 'option', 'type', 'pending_buy_quantity', 'pending_expired_quantity', 'pending_expiration_quantity', 'pending_exercise_quantity', 'pending_assignment_quantity', 'pending_sell_quantity', 'quantity', 'intraday_quantity', 'intraday_average_open_price', 'created_at', 'trade_value_multiplier', 'updated_at', 'url', 'option_id'])
    return open_options

def get_option_instrument_data(id, key=None): # DO STUFF HERE<__--------------------------------
    option_data = robin_stocks.robinhood.options.get_option_instrument_data_by_id(id, key) #Returns the option instrument information.
    return option_data # Valid dict_keys list: (['chain_id', 'chain_symbol', 'created_at', 'expiration_date', 'id', 'issue_date', 'min_ticks', 'rhs_tradability', 'state', 'strike_price', 'tradability', 'type', 'updated_at', 'url', 'sellout_datetime', 'long_strategy_code', 'short_strategy_code'])

def get_strike_price(id): #Returns strike price of option id passed in
    return get_option_instrument_data(id, "strike_price")

# def account_put_or_call(id)  make function to reverse greeks based on if call or put

# All of the following variables are lists.
general_option_info = get_open_option_info()
option_id = get_open_option_info("option_id")
short_or_long = get_open_option_info("type")
symbol = get_open_option_info("chain_symbol")
amount = list(map(get_rounded_amount, get_open_option_info("quantity")))

"""for o in range(len(general_option_info)):
    print(symbol[o] + " " + str(amount[o]) + " " + short_or_long[o])
    delta  = str(get_greeks(option_id[o], "delta") * amount[o])
    gamma = get_greeks(option_id[o], "gamma") * amount[o]
    theta = get_greeks(option_id[o], "theta") * amount[o]
    vega = get_greeks(option_id[o], "vega") * amount[o]
    print("Delta: " + delta)"""

#print(get_option_instrument_data(option_id[0], "strike_price"))

def get_net_delta(ticker=None): # Get portfolio net delta or net delta for a given ticker. NEED TO FIX TO ACCOUNT FOR DELTA REVERSE IF SHORT + SHARES.
    net_delta = 0 
    if ticker == (None):
        for o in range(len(general_option_info)):
            delta = get_greeks(option_id[o], "delta") * amount[o] #delta list in string form
            delta = sum(list(map(float, delta))) * 100 #conversion to float and summed to account for quantity, multiplied by 100 to account for options multiplier
            net_delta += delta
    else:
        for o in range(len(symbol)):
            if symbol[o] == ticker:
                delta = get_greeks(option_id[o], "delta") * amount[o] #delta list in string form
                delta = sum(list(map(float, delta))) * 100 #conversion to float and summed to account for quantity, multiplied by 100 to account for options multiplier
                net_delta += delta
    return net_delta

print(get_net_delta("AMD"))
