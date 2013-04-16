'''
(c) This code is inspired and a spin off of Georgia tech Course Compputational investing. This source code is released under the New BSD license.  Please see
http://wiki.quantsoftware.org/index.php?title=QSTK_License
for license details.

@author:  Madhav

@summary: This code calculates Annual Sharpe Ration of the Portfolio assuming that stocks are buy and hold for one complete year
'''

# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
print "Pandas Version", pd.__version__


def folio_sim(dt_start,dt_end,ls_symbol,ls_allocation):
    

    # List of symbols
    ls_symbols = ls_symbol
    # Start and End date of the charts
    dt_start = dt_start
    dt_end = dt_end
    ls_allocation = ls_allocation
    # We need closing prices so the timestamp should be hours=16.
    dt_timeofday = dt.timedelta(hours=16)

    # Get a list of trading days between the start and the end.
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    # Creating an object of the dataaccess class with Yahoo as the source.
    c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)
    
    # Keys to be read from the data, it is good to read everything in one go.
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    # Reading the data, now d_data is a dictionary with the keys above.
    # Timestamps and symbols are the ones that were specified before.
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    # Getting the numpy ndarray of close prices.
    na_price = d_data['close'].values
    print na_price
    # Normalizing the prices to start at 1 and see relative returns
    na_normalized_price = na_price / na_price[0, :]
    # Get the respective returns of the individual stocks based on their allocations
    na_price_folio = na_normalized_price[:] * ls_allocation
    # Copy the normalized prices to a new ndarry to find returns.
    na_rets = na_price_folio.copy()
    #calculate the daily total based on allocations of the stocks
    sum_daily_ret_each_day = na_rets.sum(axis=1)
    #copy of sum_daily_ret_each_day
    cc = sum_daily_ret_each_day.copy()
    rows = cc.shape[0] -1 
    # calculate the daily return of the portfolio
    tsu.returnize0(sum_daily_ret_each_day)
    #calculate the average return 
    f_average_daily_return = np.mean(sum_daily_ret_each_day)
    #calculate the Risk(Volatility)  of the portfolio
    f_std_of_daily_return = np.std(sum_daily_ret_each_day)
    #calculate the Sharpe Ratio of the portfolio
    f_sharpe_ratio = np.sqrt(252) * ( f_average_daily_return/f_std_of_daily_return)
    #cum_daily_ret=np.cumprod(1 + na_rets, axis=0,dtype=float)
    #na_portrets = np.sum(sum_daily_ret_each_day)
    na_port_total = np.cumprod(sum_daily_ret_each_day + 1)
    na_component_total =np.cumprod(na_normalized_price + 1, axis=0)
    # calculate cumulative return
    f_cum_daily_ret = cc[rows]

    # Print the Formatted Output
    print "****************"
    print "start date:" + str(dt_start)
    print "end date:" + str(dt_end)
    print "symbols: " + str(ls_symbol)
    print "Allocation:" + str(ls_allocation)
    print "Sharpe Ratio: " + str(f_sharpe_ratio)
    print "Volatility of  daily return: " + str(f_std_of_daily_return)
    print "average daily return: " + str(f_average_daily_return)
    print "Cumulative Return: " + str(f_cum_daily_ret)
    print "****************"
    return f_sharpe_ratio

def main():
    #List of Portfolio symbols to be analyzed
    ls_symbol = ["SPY", "GOOG","GLD", "AAPL"]
    #Duration of holding the stocks in portfolio
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2011, 1, 1)
    #Respective allocation of the stocks in Portfolio
    ls_allocation = [0.3, 0.2, 0.3,0.2 ]
    #Respective allocation of the stocks in Portfolio
    legal_allocations = np.arange(0,1.1,0.1) 
    #Call to calculate Sharpe Ratio
    final_sharpe = folio_sim(dt_start,dt_end,ls_symbol,ls_allocation)
    print "Calculated Portfolio Sharpe Ratio:" + str(final_sharpe)

if __name__ == "__main__":
    main()
