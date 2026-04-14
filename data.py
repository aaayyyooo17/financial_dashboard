import yfinance as yf
import pandas as pd

def get_stock_data(ticker: str, period: str = '6mo') -> pd.DataFrame:
    stock = yf.Ticker(ticker)
    df = stock.history(period = period)
    df.index = pd.to_datetime(df.index)
    
    return df 

def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    return {"name": info.get("longName", ticker),
            "price": info.get("currentPrice", None),
            "market_cap": info.get("marketCap", None),
            "pe_ratio": info.get("trailingPE", None),
            "52w_high": info.get("fiftyTwoWeekHigh", None),
            "52w_low": info.get("fiftyTwoWeekLow", None)
            }