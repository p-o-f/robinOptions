# Robin Options
Greatly extends the availability of information in Robinhood, specifically with options. Still in development. Made possible thanks to: 
https://robin-stocks.readthedocs.io/en/latest/intro.html#license

Purpose:
- For one reason or another, you may be on the Robinhood brokerage and be unable (or reluctant) to switch to another brokerage with more sophisticated features, such as ThinkOrSwim. Robinhood provides a superficial and incomplete view of critical data relating to options contracts. Unlike ThinkOrSwim, for example, you may find it inconvenient that you are unable to view the net delta position of your portfolio for a given stock ticker at a glance. Thus, this simple program aims to supplement availiability of options data in Robinhood with the help of the Robinhood API.
- Since this is mainly for personal use, and is dependent on many API calls, speed and runtime are not critical priorities.

Features:
- Everything below is a work in progress. ? = considering developing this feature.
- Get net delta/gamma/theta/rho/vega for a given position. If you have 103 shares of SPY and a varied option strategy involving short calls/puts in any order, retrieve the net greek metrics without having  to calculate it manually. DONE
- Price approximate entire portfolio given a certain scenario (similar to optionsprofitcalculator). DONE
- Support for 2FA and non-2FA accounts.
- ? GUI to interact with the program seamlessly.
- Retrieve daily historical bid/ask prices for a given option.
- ? Historical volume for options (related to below - unsure if possible w/ RH API at the moment but this can still be implemented)
- ? Historical metrics for option prices for more insight into hypothetical situations (What if you sold a portion of XYZ on Y date and bought XYZ later? How would this have impacted your portfolio?)


Account info?
- Stored safely on local host machine with a pickle file, cached on first run.
