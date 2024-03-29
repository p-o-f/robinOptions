# Robin Options 
Extends the availability of information in Robinhood, specifically with options. Still in development, but not a priority. Made possible thanks to: 
https://robin-stocks.readthedocs.io/en/latest/intro.html#license

Use case:
- Robinhood provides a superficial and incomplete view of critical data relating to options contracts. As an example, it is inconvenient that you are unable to view the net delta position of your portfolio for a given stock ticker at a glance. This is a standard feature that comes with other brokerages like ThinkOrSwim, Fidelity, etc. Thus, this program aims to supplement availiability of options data in Robinhood with the help of the Robinhood API. 
- Since this is mainly for personal use, and is dependent on many API calls, speed and runtime are not critical priorities.

Features:
- Get net delta/gamma/theta/rho/vega for a given position. For instance, if you have 103 shares of $SPY and a varied option strategy involving short calls/puts in any order, retrieve the net greek metrics without having to calculate manually. 
- Price approximate your open options portfolio given changes in share price or implied volatility (similar to OptionsProfitCalculator, but only considers delta/gamma/vega). This is mainly useful for LEAPS options since their price adjustments are based mostly off of changes in delta, gamma, and vega.
- Retrieve a non-GAAP basis trailing P/E ratio instantly, as well as what the new P/E ratio will be in the intermediate time frame. For example, if $MSFT is reporting earnings soon, and analysts predict 3.45 earnings per share for this quarter, what will the new P/E ratio be after this report - assuming that estimates are met or are in the ballpark? Trailing P/E ratio is usually somewhat out of date on various platforms or sites, so that's why this portion was added.
- Other features will be added as needed - If I run into a useful task in trading, and I am finding myself manually doing it frequently, then I will try to automate it.

Account info:
- Stored safely on local host machine with a pickle file, cached on first run. Environmental variables are used for privacy.
