import exchange_calendars
import pandas as pd
import time

from tqdm import tqdm
from pykrx import stock
from typing import Optional

class MarketData:
    def __init__(self, start_date: str, end_date: str, market: str = "KOSPI"):
        self.start_date = start_date
        self.end_date = end_date
        self.market = market

    def get_ticker_list(self, date: Optional[str] = None):
        if date is None:
            date = self.end_date
        return stock.get_market_ticker_list(date, market=self.market)
    
    def get_business_days(self):
        code = "XKRX"
        return exchange_calendars.get_calendar(code, start=self.start_date, end=self.end_date).sessions.strftime("%Y-%m-%d").tolist()
    
    def load_data(self, ticker: str):
        if ticker == "all":
            business_day_list = self.get_business_days()
            res = pd.DataFrame()
            for business_day in tqdm(business_day_list):
                df = stock.get_market_ohlcv(business_day, market=self.market)
                df.reset_index(inplace=True)
                df["Date"] = business_day
                res = pd.concat([res, df])
                time.sleep(1)
        else:
            res = stock.get_market_ohlcv(self.start_date, self.end_date, ticker)
            res.reset_index(inplace=True)
        res = res.rename(columns={"티커": "Ticker", "날짜": "Date",
                                  "시가": "Open", "고가": "High",
                                  "저가": "Low", "종가": "Close",
                                  "거래량": "Volume",
                                  "거래대금": "Trading value", "등락률": "Change"})
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
        else:
            res = stock.get_market_fundamental(self.start_date, self.end_date, ticker)
            res["ticker"] = ticker
            res.reset_index(inplace=True)
            res = res.rename(columns={"날짜": "Date"})
        return res
    