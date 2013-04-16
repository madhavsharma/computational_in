'''
(c) This code is for solving marketsimulation problem given in Georgia tech Course Compputational investing.
This source code is released under the New BSD license.  Please see
http://wiki.quantsoftware.org/index.php?title=QSTK_License
for license details.

Created on April, 2, 2013

@author: Madhav 

@summary:  MarketSimulator code for a order read from orders.csv 
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

# System Imports
import sys
from collections import defaultdict
import csv
from time import strptime
import math
def marketsim(argv):
    ''' Main Function'''

    #f_orders = open('f_orders.txt','w')
    # Reading the portfolio
    s_values_file = str(argv[0])
    s_index = str(argv[1])
    #f_values = open(s_value_file,'wb')
    #ls_values_data = []
    na_portfolio = np.loadtxt(s_values_file,dtype ='f4,f4,f4,f4', delimiter=",", comments="#", skiprows=0)
    na_orders = np.sort(na_portfolio,axis = 0)
    #na_portfolio_skeleton = np.empty((1,6))
    #print na_portfolio
    ls_date = []
    ls_symbols = [s_index]
    ls_port_ret = []
    for row in na_orders:
		# Get the date 
		ls_date.append((np.int_(row[0]),np.int_(row[1]),np.int_(row[2])))
		ls_port_ret.append(row[3])	
    #print na_portfolio_sorted
    dt_start = ls_date[0]
    dt_end = ls_date[-1]
    
    dt_start_date = dt.datetime(dt_start[0],dt_start[1],dt_start[2],16)
    dt_end_date = dt.datetime(dt_end[0],dt_end[1],dt_end[2],16)
    na_port_ret = np.array(ls_port_ret).reshape(len(ls_port_ret),1)
    #na_port_ret = np.cumprod(na_port_ret +1)
    #print dt_start_date,dt_end_date,ls_symbols
    #print na_port_ret
    dt_timeofday = dt.timedelta(hours=16)
    #dt_timeofday_date = dt.timedelta(hours=24)
    # Get a list of trading days between the start and the end.
    ldt_timestamps = du.getNYSEdays(dt_start_date, dt_end_date, dt_timeofday)
    #print str(ldt_timestamps)
    # Creating an object of the dataaccess class with Yahoo as the source.
    c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)
    
    # Keys to be read from the data, it is good to read everything in one go.
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    # Reading the data, now d_data is a dictionary with the keys above.
    # Timestamps and symbols are the ones that were specified before.
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)

    d_data = dict(zip(ls_keys, ldf_data))
    
    na_price = d_data['close'].values
    #na_price = np.hstack((na_price,na_port_ret))

    ##########Calculate specs for Index 
    na_normalized_price = na_price / na_price[0, :]
    # calculate the daily return of the index
    tsu.returnize0(na_normalized_price)
    #calculate the average return 
    f_average_daily_return_index = np.mean(na_normalized_price)
    #calculate the Risk(Volatility)  of the index
    f_std_of_daily_return_index = np.std(na_normalized_price)
    #calculate the Sharpe Ratio of the index
    f_sharpe_ratio_index  = np.sqrt(252) * ( f_average_daily_return_index/f_std_of_daily_return_index)
    
    ##########Calculate specs for Portfolio
    na_normalized_price_port = na_port_ret / na_port_ret[0, :]
    #na_normalized_price_port = np.cumprod(na_normalized_price_portm +1)
    
    # calculate the daily return of the portfolio
    tsu.returnize0(na_normalized_price_port)
    #calculate the average return 
    f_average_daily_return_port = np.mean(na_normalized_price_port)
    #calculate the Risk(Volatility)  of the portfolio
    f_std_of_daily_return_port = np.std(na_normalized_price_port)
    #calculate the Sharpe Ratio of the portfolio
    f_sharpe_ratio_port  = np.sqrt(252) * ( f_average_daily_return_port/f_std_of_daily_return_port)
    
    print 'The final value of the portfolio using the sample file is --',na_orders[-1]
    #print f_average_daily_return,f_std_of_daily_return,f_sharpe_ratio
    print 'Details of the Performance of the portfolio'
    
    print 'Data Range :',dt_start,' to ', dt_end
    
    print 'Sharpe Ration of Portfolio/Fund: ', f_sharpe_ratio_port
    print 'Sharpe Ration of %s :' % s_index , f_sharpe_ratio_index, '\n'
    
    print 'Total Return of Portfolio/Fund: ', na_orders[-1][3]/na_orders[0][3]
    print 'Total Return  of %s :' % s_index , na_price[-1][0]/na_price[0][0], '\n'

    print 'Std Dev of Portfolio/Fund: ', f_std_of_daily_return_port
    print 'Std Dev of %s :' % s_index , f_std_of_daily_return_index, '\n'
    
    print 'Average Daily Return Portfolio/Fund: ', f_average_daily_return_port
    print 'Average Daily Return of %s :' % s_index , f_average_daily_return_index, '\n'
    
    #print na_price
    na_plot = np.hstack((na_price,na_port_ret))
    #na_plot = na_price
    #na_plot = np.hstack((na_normalized_price,na_normalized_price_port))
    #print na_plot
    plt.clf()
    plt.plot(ldt_timestamps, na_plot)
    plt.legend(['$SPX','portfolio'])
    plt.ylabel('Close')
    plt.xlabel('Date')
    #low = min(na_price)
    #high = max(na_port_ret)
    #plt.ylim([math.ceil(low-0.5*(high-low)), math.ceil(high+0.5*(high-low))])
    #plt.ylim((1000,1000000))
    plt.savefig('HW33.pdf', format='pdf')
    #print len(ldt_timestamps),na_price.shape, na_port_ret.shape #na_port_ret.reshape(len(na_port_ret),1)
    #print ls_port_ret[0],ls_port_ret[1]
    '''ls_filtered_symb = list(set(ls_symbols))
    ls_filtered_sorted_symb = sorted(ls_filtered_symb,key = lambda x:x[0])
    dict_sorted_symb = {ls_filtered_sorted_symb[i]:i+1 for i in range(len(ls_filtered_sorted_symb))}
    dict_symb_holding = {i:0 for i in ls_filtered_sorted_symb}
    print dict_sorted_symb
    print ls_filtered_sorted_symb
    dict_action = {'Buy':-1,'Sell':1}
    #print 'symbol type' , type(ls_filtered_sorted_symb[0])
    s_symb = []
    for symb in range(len(ls_filtered_sorted_symb)):
		s_symb.append(ls_filtered_sorted_symb[symb])
    #print s_symb
    #print ls_quantity
    inputs = argv
    #print (inputs[0])
    # getting data 
    # We need closing prices so the timestamp should be hours=16.
    dt_timeofday = dt.timedelta(hours=16)
    #dt_timeofday_date = dt.timedelta(hours=24)
    # Get a list of trading days between the start and the end.
    ldt_timestamps = du.getNYSEdays(dt_start_date, dt_end_date, dt_timeofday)
    #print str(ldt_timestamps)
    # Creating an object of the dataaccess class with Yahoo as the source.
    c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)
    
    # Keys to be read from the data, it is good to read everything in one go.
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    # Reading the data, now d_data is a dictionary with the keys above.
    # Timestamps and symbols are the ones that were specified before.
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_filtered_sorted_symb, ls_keys)

    d_data = dict(zip(ls_keys, ldf_data))
    for row in na_orders:
        temp_date = dt.datetime(row[0],row[1],row[2],16)
        #print type(ls_filtered_sorted_symb[0])
        #print ((d_data['close'][s_symb]).ix[ldt_timestamps])
    # Getting the numpy ndarray of close prices.
    na_price = d_data['close'].values
    #f_close = d_data['close']
    #value = df_close[ls_filtered_sorted_symb].ix[ldt_timestamps]
    order_date = []
    for i in range(len(ls_date)):
		 order_date.append(dt.datetime(ls_date[i][0],ls_date[i][1],ls_date[i][2],16))
    #print order_date
    
    dicto = defaultdict(list)
    ls_index = []
    for ind,ele in enumerate(order_date):
		dicto[ele].append(ind)
    for ts in range(len(ldt_timestamps)):
        if ldt_timestamps[ts] in order_date:
            index = order_date.index(ldt_timestamps[ts])
            #index = np.where(order_date==ldt_timestamps[ts])

    #print (np.array(ldt_timestamps)).shape,(na_price.shape)
    np_timestamp = np.array(ldt_timestamps)
    np_ts = np_timestamp.reshape(len(ldt_timestamps),1)
    #print (np_timestamp.shape),(na_price.shape)
    
    ls_trade_done = []
    s_stock=""
    s_action=""
    f_number=""
    #print ls_filtered_sorted_symb
    #na_price_ts is array of date and price 
    na_price_ts = np.hstack((np_ts,na_price)) 
    #print type(order_date), type(ldt_timestamps)
    for i in range(len(na_price_ts)):
		if (na_price_ts[i][0]in dicto):
			#index = order_date.index(na_price_ts[i][0])
			#print na_orders[index]
			value = dicto[na_price_ts[i][0]]
			f_portfolio_value = 0.0
			#print "trade on ", na_price_ts[i][0],len(value),'current_holdings',dict_symb_holding,'total_fund',f_total_fund
			for trading_days in value:
				s_stock = na_orders[trading_days][3]
				s_action = na_orders[trading_days][4]
				f_number = int(na_orders[trading_days][5])
				#print (f_number)*(dict_action[s_action])
				#update cash first on trading
				f_traded_cash= ((dict_action[s_action])*((na_price_ts[i][dict_sorted_symb[s_stock]])*(f_number)))
				f_cash += f_traded_cash
				#update holdings
				dict_symb_holding[s_stock] += (-1*(dict_action[s_action])*(f_number))
				#calculate holdings value
				for stock in dict_symb_holding.keys():
					f_portfolio_value += ((na_price_ts[i][dict_sorted_symb[stock]])* (dict_symb_holding[stock]))
				print na_price_ts[i][0],s_action,s_stock,na_price_ts[i][dict_sorted_symb[s_stock]],dict_symb_holding[s_stock],'cash_val_of_trade',f_traded_cash,'cash_in_hand',f_cash,'portfolio_value',f_portfolio_value
				f_total_fund = f_cash + f_portfolio_value
				print 'total_fund',f_total_fund
				#print 'after_trade_holdings',dict_symb_holding,'total_fund',f_total_fund
			print "Trade over on ", na_price_ts[i][0],len(value),'current_holdings',dict_symb_holding,'total_fund',f_total_fund
			#f_values.writelines((str(na_price_ts[i][0]),str(f_total_fund)))
			#ls_values_data.append((na_price_ts[i][0].strftime('%Y,%m,%d'),f_total_fund))
		else:
			print 'no trade on this date holdings are ', dict_symb_holding
			f_portfolio_value=0
			for stock in dict_symb_holding.keys():
				#print 'price today', na_price_ts[i][dict_sorted_symb[s_stock]]
				f_portfolio_value += ((na_price_ts[i][dict_sorted_symb[stock]])* (dict_symb_holding[stock]))
				#print 'f_cash',f_cash,'f_portfolio',f_portfolio_value
				#f_total_fund = f_cash + f_portfolio_value
			print 'current_holdings_no_order_executed',dict_symb_holding,'cash_in_hand',f_cash,'Portfolio_value',f_portfolio_value,'total_fund',(f_cash + f_portfolio_value)
		f_total_fund = f_cash + f_portfolio_value
		print na_price_ts[i][0],f_total_fund
		ls_values_data.append((na_price_ts[i][0].strftime('%Y,%m,%d'),f_total_fund))
		print '***************************************************************************'
    data_length = len(ls_values_data)
    #print ls_values_data
    #print type(ls_values_data), len(ls_values_data)
    out = csv.writer(open(s_value_file,"w"), delimiter=',',quoting=csv.QUOTE_ALL)
    for i in range(len(ls_values_data)):
		ls_value_date = ls_values_data[i][0].split(',')
		i_year = ls_value_date[0]
		i_month = ls_value_date[1]
		i_day = ls_value_date[2]
		out.writerow((i_year,i_month,i_day,ls_values_data[i][1]))
    
    #f_values.close()
    '''

   
    
if __name__ == '__main__':
    marketsim(sys.argv[1:])
