'''
(c) This code is inspired and a spin off of Georgia tech Course Compputational investing. This source code is released under the New BSD license.  Please see
http://wiki.quantsoftware.org/index.php?title=QSTK_License
for license details.

@author:  Madhav

@summary: This code alculates optimizes a portfolio based on annual Sharpe Ration of the Portfolio, assuming that stocks are buy and hold for one complete year.

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


def folio_sym(dt_start,dt_end,ls_symbol,ls_allocation):
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

    # Normalizing the prices to start at 1 and see relative returns
    na_normalized_price = na_price / na_price[0, :]
    #Get the respective returns of the individual stocks based on their allocations.
    na_price_folio = na_normalized_price[:] * ls_allocation
    # Copy the normalized prices to a new ndarry to find returns.
    na_rets = na_price_folio.copy()
    # Calculate the daily total based on allocations of the stocks
    sum_daily_ret_each_day = na_rets.sum(axis=1)
    #copy of sum_daily_ret_each_day
    cc = sum_daily_ret_each_day.copy()
    rows = cc.shape[0] -1
    # calculate the daily return of the portfolio 
    tsu.returnize0(sum_daily_ret_each_day)
    # calculate the average return of Portfolio
    f_average_daily_return = np.mean(sum_daily_ret_each_day)
    # calculate the Risk(Volatility)  of the portfolio
    f_std_of_daily_return = np.std(sum_daily_ret_each_day)
    # calculate the Sharpe Ratio of the portfolio ( assuming buying and hold for a year)
    f_sharpe_ratio = np.sqrt(252) * ( f_average_daily_return/f_std_of_daily_return)


    print "******" +"\n"
    print "Allocation:" + str(ls_allocation)
    print "Sharpe Ratio: " + str(f_sharpe_ratio)
    return f_sharpe_ratio

def main():
    # initialize of f_max_sharpe_ratio, ls_best_portfolio
    f_max_sharpe_ratio = 0
    ls_best_portfolio = []
    ls_allocations = []
    # list of symbols
    ls_symbol = ["BRCM", "TXN","AMD", "ADI"]
    # duration of buy and hold
    dt_start = dt.datetime(2010, 1, 1)
    dt_end = dt.datetime(2010, 12, 31)
    # Set of permitted combination of allocation of the stocks in Portfolio
    ls_legal_allocations = np.arange(0,1.1,0.1) 
    for a in ls_legal_allocations:
        for b in ls_legal_allocations:
            for c in ls_legal_allocations:
                for d in ls_legal_allocations:
                    if((a + b + c + d) == 1.0):
                        ls_allocations = [a, b, c, d]
                        #Call to calculate Sharpe Ratio
                        f_final_sharpe = folio_sym(dt_start,dt_end,ls_symbol,ls_allocations)
                        # find best sharpe ratio and portfolio
                        if(f_final_sharpe > f_max_sharpe_ratio):
                            f_max_sharpe_ratio = f_final_sharpe
                            ls_best_portfolio = [a, b, c, d]
                    else:
                        continue                    
    # Output optimized postfolio with its sharpe ratio
    print "************************************" +  "\n"  + "Optimized Portfolio:" + "\n"
    print "max sharpe_ratio:" + str(f_max_sharpe_ratio) + "with portfolio" + str(ls_best_portfolio)
if __name__ == "__main__":
    main()
