import datetime
import logging

import pandas as pd
import yfinance as yf
from pandas.tseries.offsets import BDay
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
SOURCES = ['yahoo', 'morningstar']
def get_ranged_data(ticker, start, end=None, useQuandl=True):
    if not end:
        end = datetime.date.today()
    logging.info(f"Fetching data for {ticker}")
    df = yf.download(ticker, start=start, end=end)
    return df
def get_data(ticker, useQuandl=True):
    logging.info(f"Fetching data for {ticker}")
    df = yf.download(ticker, period="max")
    return df
def get_treasury_rate(ticker=None):
    return 0.05
def get_spx_prices(start_date=None):
    if not start_date:
        start_date = datetime.datetime(2017, 1, 1)
    df = pd.DataFrame()
    df = get_data('^GSPC')
    if df.empty:
        logging.error("Unable to get SNP 500 Index from Web. Please check connection")
        raise IOError("Unable to get Treasury Rate from Web")
    return df
if __name__ == '__main__':
    # df = get_data('AAPL', datetime.datetime(2017, 1, 1), useQuandl=True)
    # df = get_data('SPX', datetime.datetime(2017, 1, 1), useQuandl=False)
    df = get_data('WMT', useQuandl=True)
    print(df.head())
    print(df.tail())
    # rate = get_treasury_rate()
    # print type(rate), rate