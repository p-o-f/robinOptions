from ast import Continue
from configparser import NoOptionError
from itertools import tee
from linecache import getline
from msvcrt import kbhit
import math
from operator import truediv
import robin_stocks
import robin_stocks.robinhood as r 
import sys
from robin_stocks.robinhood.helper import *
from robin_stocks.robinhood.urls import *
from dotenv import load_dotenv
import os 
load_dotenv()

u = os.environ.get('rh_username')
p = os.environ.get('rh_password')

def start(email, pw):
    try:
        login = r.login(email, pw)
        print("Logged in!")
    except:
        print("Error while trying to login.")

start(u, p) # If authentication code is not cached yet, then a code will be prompted for the user to enter.

# Developmental methods/relevant documentation | https://robin-stocks.readthedocs.io/en/latest/robinhood.html
def get_key_list(dict): # Returns keys, helps use the API.
    return dict.keys()

def get_rounded_amount(amount, digits=None): 
    return round(float(amount), digits)

def get_open_stock_info(key=None): # Returns a list of stocks that are currently held. 
    return robin_stocks.robinhood.account.get_open_stock_positions(key) 
#   Valid dict_keys list: (['url', 'instrument', 'instrument_id', 'account', 'account_number', 'average_buy_price', 'pending_average_buy_price', 'quantity', 'intraday_average_buy_price', 'intraday_quantity', 'shares_available_for_exercise', 'shares_held_for_buys', 'shares_held_for_sells', 'shares_held_for_stock_grants', 'shares_held_for_options_collateral', 'shares_held_for_options_events', 'shares_pending_from_options_events', 'shares_available_for_closing_short_position', 'ipo_allocated_quantity', 'ipo_dsp_allocated_quantity', 'avg_cost_affected', 'avg_cost_affected_reason', 'is_primary_account', 'updated_at', 'created_at'])

def get_open_option_info(key=None): # Returns a list of dictionaries of key/value pairs for each option. If info parameter is provided, a list of strings is returned where the strings are the value of the key that matches info.
    open_options = robin_stocks.robinhood.options.get_open_option_positions(key)
    return open_options
#   Valid dict_keys list: (['account', 'average_price', 'chain_id', 'chain_symbol', 'id', 'option', 'type', 'pending_buy_quantity', 'pending_expired_quantity', 'pending_expiration_quantity', 'pending_exercise_quantity', 'pending_assignment_quantity', 'pending_sell_quantity', 'quantity', 'intraday_quantity', 'intraday_average_open_price', 'created_at', 'trade_value_multiplier', 'updated_at', 'url', 'option_id'])

def get_option_id(ticker, expirationDate, strikePrice, optionType, key="id"): # Given option metrics, returns its corresponding ID.
    option_data = robin_stocks.robinhood.options.get_option_instrument_data(ticker, expirationDate, strikePrice, optionType, key)
    return option_data
#    Valid dict_keys list: (['chain_id', 'chain_symbol', 'created_at', 'expiration_date', 'id', 'issue_date', 'min_ticks', 'rhs_tradability', 'state', 'strike_price', 'tradability', 'type', 'updated_at', 'url', 'sellout_datetime', 'long_strategy_code', 'short_strategy_code'])

def get_greeks(id, greek="delta"): # Returns greek value for an option. Valid greek strings are: delta, gamma, theta, rho, vega.
    return robin_stocks.robinhood.options.get_option_market_data_by_id(id, greek)

def get_option_data(id, key=None): # Returns metrics for an option, like the price the contract is trading at.
    return robin_stocks.robinhood.options.get_option_market_data_by_id(id, key)
#   Valid dict_keys list: (['adjusted_mark_price', 'adjusted_mark_price_round_down', 'ask_price', 'ask_size', 'bid_price', 'bid_size', 'break_even_price', 'high_price', 'instrument', 'instrument_id', 'last_trade_price', 'last_trade_size', 'low_price', 'mark_price', 'open_interest', 'previous_close_date', 'previous_close_price', 'updated_at', 'volume', 'symbol', 'occ_symbol', 'state', 'chance_of_profit_long', 'chance_of_profit_short', 'delta', 'gamma', 'implied_volatility', 'rho', 'theta', 'vega', 'high_fill_rate_buy_price', 'high_fill_rate_sell_price', 'low_fill_rate_buy_price', 'low_fill_rate_sell_price'])

def get_stock_holdings(with_dividends=False, ticker=None): # Returns number of shares for either the entire portfolio or a given ticker.
    if ticker == None:
        return robin_stocks.robinhood.account.build_holdings(with_dividends)
    return get_stock_holdings()[ticker]

def get_quotes(ticker, key="last_trade_price"): # Takes any number of stock tickers and returns information pertaining to its price.
    return robin_stocks.robinhood.stocks.get_quotes(ticker, key)
#   Valid dict_keys list: (['ask_price', 'ask_size', 'bid_price', 'bid_size', 'last_trade_price', 'last_extended_hours_trade_price', 'previous_close', 'adjusted_previous_close', 'previous_close_date', 'symbol', 'trading_halted', 'has_traded', 'last_trade_price_source', 'updated_at', 'instrument', 'instrument_id', 'state'])

def get_stock_price(ticker, priceType=None, includeExtendedHours = True): # Price Type is optional and is either "bid" or "ask", this will set includeExtendedHours to false automatically if passed in.
    try: 
        ret = robin_stocks.robinhood.stocks.get_latest_price(ticker, priceType, includeExtendedHours)[0]
        return float(ret)
    except: # This will run if there is no bid or ask for the stock at the moment and return the last traded price.
        ret = get_quotes("ticker")[0]
        return float(ret)

# All of the following variables are lists used in the functions below.
general_option_info = get_open_option_info()
option_id = get_open_option_info("option_id")
short_or_long = get_open_option_info("type")
symbol = get_open_option_info("chain_symbol")
amount = list(map(get_rounded_amount, get_open_option_info("quantity")))

# The main methods for adding functionality to Robinhood.
def get_net_delta(ticker=None): # Get portfolio net delta or net delta for a given ticker. 
    net_delta = 0
    if (ticker is None):
        for o in range(len(general_option_info)):
            delta = get_greeks(option_id[o], "delta") * amount[o] # Delta list in string form
            if (None in delta): # On opex day, this accounts for options no longer existing
                delta[0] = 0
            delta = sum(list(map(float, delta))) # Conversion to float and summed to account for quantity
            net_delta = net_delta+delta if (short_or_long[o] == "long") else net_delta-delta # Reverses delta ONLY IF short; eg short put is accounted for as positive delta
        share_delta = get_open_stock_info("quantity") # List of share quantities to add into the net delta
        share_delta = sum(list(map(float, share_delta))) # Convert list of strings to floats
        net_delta += (share_delta * 0.01) # 0.01 is here because there is x100 multiplication at the end
    else:
        for o in range(len(symbol)):
            if symbol[o] == ticker:
                delta = get_greeks(option_id[o], "delta") * amount[o] # Delta list in string form
                if (None in delta): # On opex day, this accounts for options no longer existing
                    delta[0] = 0
                delta = sum(list(map(float, delta))) # Conversion to float and summed to account for quantity
                net_delta = net_delta+delta if (short_or_long[o] == "long") else net_delta-delta # Reverses delta ONLY IF short; eg short put is accounted for as positive delta
        share_delta = float(get_stock_holdings(False, ticker)["quantity"])
        net_delta += (share_delta * 0.01) # 0.01 is here because there is x100 multiplication at the end
    return get_rounded_amount((net_delta * 100), 5) # Accounts for options 100x multiplier

def get_net_greek(greek="delta", ticker=None): # Get net gamma, theta, rho, or vega for a given ticker. The logic is similar to the net delta function, but is its own function because shares affect portfolio net delta but do not affect the other major greeks.
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

def price_approximation(ticker, deltaSP, deltaVol = 0): # Uses second degree and first degree Taylor series (centered at deltaSP and deltaVol respectively) to approximate pricing change of the entire portfolio given a change in stock price/implied volatility; deltaSP = ∂s (change in share price, or X - Xo); deltaVol = change in implied vol. as a percentage (for example 5 = 5% increase in IV).
    d = get_net_delta(ticker) # ∂f/∂s
    g = get_net_greek("gamma",ticker) # ∂²f/∂s²
    v = get_net_greek("vega", ticker) # ∂f/∂σ
    approx = (d * deltaSP) + (0.5 * g * (deltaSP ** 2)) # Second degree series for delta/gamma.
    approx += (v * deltaVol) # First degree series for volatility.
    return approx # This will be inaccurate because it is a trunucated series - IE no omega greek used to make the first series third degree.

def get_leverage_factor(ticker, expiry, strike, type="call"): # Returns the leverage factor of an option; if it's 13.43 for example, the option provides 13.43x leverage versus buying plain shares of stock. Expiry format is YYYY-MM-DD like 2022-07-29; type is "call" or "put".
    id = get_option_id(ticker, expiry, strike, type) # This is done via option ID because the API for getting option instrument market data based solely off of options parameters mistankenly returns a list rather than dictionary.
    delta = 100 * float(get_greeks(id)[0]) # Returns option ID of passed in option parameters, then returns delta of that option.
    option_price = 100 * float(get_option_data(id, "ask_price")[0]) # Get option price by id; uses ask price because this is the most likely to be filled rather than the bid or mid prices.
    stock_price =  get_stock_price(ticker)
    multiplier = (stock_price * delta)/option_price # Calculation of the leverage factor.
    return get_rounded_amount(multiplier, 3) 

def get_eps(ticker, key="eps", quarters=4, estimate = False): # Get cumulative EPS of a ticker for a specified number of quarters; If estimate is set to true, the analyst estimated earnings for the upcoming quarter will be accounted for in the # of quarters. 
    eps_list = (robin_stocks.robinhood.stocks.get_earnings(symbol[0], key))
    eps_list.reverse()
    eps = 0
    counter = 0
    if (estimate == False):
        for e in range(len(eps_list)):
            current = eps_list[e] # Current dictionary, contains actual/estimated eps (descending order by recent quarter).
            act = current.get("actual")
            if (act is None):
                Continue
            else:
                eps += float(act)
                counter = counter + 1
            if (counter == quarters):
                break
        return eps
    else:
        next_qrter_est = 0;
        for e in range(len(eps_list)):
            current = eps_list[e]
            if (current.get("estimate") is None):
                continue
            else:
                next_qrter_est = float(current.get("estimate"))
                break
        realized_eps = get_eps(ticker, "eps", quarters-1, False)
        next_qrter_est += realized_eps
        return next_qrter_est

def get_pe_ratio(ticker, ttm = True): # For a given ticker, return the new expected trailing 12 months P/E ratio after the company reports its next earnings based off of expected EPS. This gives a middleground of the P/E between TTM and forward.
    sp = get_stock_price(ticker)
    if (ttm == True):
        eps = get_eps(ticker)
        return get_rounded_amount(sp/eps, 2)
    else:
        eps = get_eps(ticker, "eps", 4, True)
        return get_rounded_amount(sp/eps, 2)



# Some examples of what you could use this for - $AMD is used as an example ticker because I have a varied position of shares and many options in their stock. #
TTM_PE = get_pe_ratio("AMD")
Intermediate_PE = get_pe_ratio("AMD", False)
Net_Delta = get_net_delta("AMD")
Current_Share_Price = get_stock_price("AMD")
Leverage_On_2024_Call = get_leverage_factor("AMD", "2024-01-19", "100")
Bullish_Price_Approximation = price_approximation("AMD", (150 - Current_Share_Price), 2.5) # Assuming here that AMD rises to $150 from the current share price and implied volatility of your options overall increases by 2.5%

print("The price of AMD shares is currently: $" + str(Current_Share_Price))
print("The current (12 months trailing) PE ratio is: " + str(TTM_PE))
print("If analyst estimates are met or relatively close to actual earnings for AMD next quarter, then the new trailing PE ratio becomes: " + str(Intermediate_PE))
print("Your current net delta position in AMD is: " + str(Net_Delta))
print("You own some LEAPS options for AMD. Your leverage on the January 19th, 2024 call option is: " + str(Leverage_On_2024_Call) + "x per contract")
print("If AMD rises to 150 dollars per share, your portfolio will appreciate by approximately: $" + str(Bullish_Price_Approximation))