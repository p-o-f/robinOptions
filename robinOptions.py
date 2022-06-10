from itertools import tee
from linecache import getline
from math import gamma
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

# Development methods
def get_key_list(dict):
    return dict.keys()

def get_greeks(id, greek="delta"): # Valid greek strings are: delta, gamma, theta, rho, vega.
    ret = robin_stocks.robinhood.options.get_option_market_data_by_id(id, greek)
    return ret

def get_open_option_info(key=None):
    open_options = robin_stocks.robinhood.options.get_open_option_positions(key) #Returns a list of dictionaries of key/value pairs for each option. If info parameter is provided, a list of strings is returned where the strings are the value of the key that matches info.
#   Valid dict_keys list: (['account', 'average_price', 'chain_id', 'chain_symbol', 'id', 'option', 'type', 'pending_buy_quantity', 'pending_expired_quantity', 'pending_expiration_quantity', 'pending_exercise_quantity', 'pending_assignment_quantity', 'pending_sell_quantity', 'quantity', 'intraday_quantity', 'intraday_average_open_price', 'created_at', 'trade_value_multiplier', 'updated_at', 'url', 'option_id'])
    return open_options

def get_option_instrument_data(id, key=None): # DO STUFF HERE<__--------------------------------
    option_data = robin_stocks.robinhood.options.get_option_instrument_data_by_id(id, key) #Returns the option instrument information.
    return option_data # Valid dict_keys list: (['chain_id', 'chain_symbol', 'created_at', 'expiration_date', 'id', 'issue_date', 'min_ticks', 'rhs_tradability', 'state', 'strike_price', 'tradability', 'type', 'updated_at', 'url', 'sellout_datetime', 'long_strategy_code', 'short_strategy_code'])

def get_rounded_amount(amt):
    return round(float(amt))

# All of the following variables are lists.
general_option_info = get_open_option_info()
option_id = get_open_option_info("option_id")
short_or_long = get_open_option_info("type")
symbol = get_open_option_info("chain_symbol")
amount = list(map(get_rounded_amount, get_open_option_info("quantity")))

for o in range(len(general_option_info)):
    print(symbol[o] + " " + str(amount[o]) + " " + short_or_long[o])
    delta  = str(get_greeks(option_id[o], "delta") * amount[o])
    gamma = get_greeks(option_id[o], "gamma") * amount[o]
    theta = get_greeks(option_id[o], "theta") * amount[o]
    vega = get_greeks(option_id[o], "vega") * amount[o]
    print("Delta: " + delta)


   