# -*- coding: utf-8 -*-
"""
Created on Tue Aug 02 08:54:39 2016

@author: gdpan
"""
from datetime import datetime
import pandas as pd, requests
import pandas_datareader.data as web
import matplotlib as mplt

def get_intraday_data(symbol, interval_seconds=301, num_days=10):
    # Specify URL string based on function inputs.
    url_string = 'http://www.google.com/finance/getprices?q={0}'.format(symbol.upper())
    url_string += "&i={0}&p={1}d&f=d,o,h,l,c,v".format(interval_seconds,num_days)

    # Request the text, and split by each line
    r = requests.get(url_string).text.split()

    # Split each line by a comma, starting at the 8th line
    r = [line.split(',') for line in r[7:]]

    # Save data in Pandas DataFrame
    df = pd.DataFrame(r, columns=['Datetime','Close','High','Low','Open','Volume'])

    # Convert UNIX to Datetime format
    df['Datetime'] = df['Datetime'].apply(lambda x: datetime.fromtimestamp(int(x[1:])))

    return df


start = datetime(2000, 1,1)
end = datetime.today()

symbol_list = ['2388.HK']


'''
for symbol in symbol_list:
    aapl_from_google = web.DataReader("%s" % symbol, 'google', start, end)
    aapl_from_google.to_csv("%s_from_google.csv" % symbol)
    
    aapl_from_yahoo = web.DataReader("%s" % symbol, 'yahoo', start, end)
    aapl_from_yahoo.to_csv("%s_from_yahoo.csv" % symbol)
'''
    
for symbol in symbol_list:
    data = mplt.finance.quotes_historical_yahoo_ohlc(symbol, start, end)
    print data