import pandas_datareader.data as pdr
import exchange_calendars
import yfinance as yf
import pandas as pd
import time

from tqdm import tqdm
from pykrx import stock
from typing import Optional

class MarketData:
    def __init__(self, start_date, end_date, market="KOSPI"):
        self.start_date = start_date
        self.end_date = end_date
        self.market = market

    def get_ticker_list(self):
        return stock.get_market_ticker_list(self.end_date, market=self.market)
    
    def get_business_days(self):
        code = "XKRX"
        return exchange_calendars.get_calendar(code, start=self.start_date, end=self.end_date).sessions.strftime("%Y-%m-%d").tolist()
    
    def load_data(self, ticker: str):
        if ticker == "all":
            ticker_list = self.get_ticker_list()
            res = pd.DataFrame()
            for ticker in tqdm(ticker_list):
                df = pdr.DataReader(ticker, 'naver', start=self.start_date, end=self.end_date)
                df["ticker"] = ticker
                res = pd.concat([res, df])
        else:
            res = pdr.DataReader(ticker, 'naver', start=self.start_date, end=self.end_date)
            res["ticker"] = ticker
        return res
    
    def load_fundamental_data(self, ticker: str):
        if ticker == "all":
            business_day_list = self.get_business_days()
            res = pd.DataFrame()
            for business_day in tqdm(business_day_list):
                df = stock.get_market_fundamental(business_day, market=self.market).reset_index()
                df["Date"] = business_day
                res = pd.concat([res, df])
                time.sleep(1)
            res = res.rename(columns={"티커": "ticker"})
            res = res.set_index("Date")
            res.index = pd.DatetimeIndex(res.index)
        else:
            res = stock.get_market_fundamental(self.start_date, self.end_date, ticker)
            res["ticker"] = ticker
            res.index.name = "Date"
        return res
    