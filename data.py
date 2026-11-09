import yfinance as yf
import pandas as pd
import math

def get_stock_data(ticker: str, period: str = '6mo') -> pd.DataFrame:
    stock = yf.Ticker(ticker)
    df = stock.history(period = period)
    if df.empty:
        raise ValueError(f"No data for ticker '{ticker}'")
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
            "52w_low": info.get("fiftyTwoWeekLow", None),
            "currency": info.get("currency", "")
            }

def search_ticker(query: str, max_results: int = 8) -> list[dict]:
    try:
        quotes = yf.Search(query, max_results=max_results).quotes
    except Exception:
        return []

    options = []
    for q in quotes:
        if q.get("quoteType") not in ("EQUITY", "ETF"):   # skip futures, currencies etc.
            continue
        name = q.get("longname") or q.get("shortname") or q["symbol"]
        label = f"{name} ({q['symbol']}, {q.get('exchange', '')})"
        options.append({"label": label, "value": q["symbol"]})
    return options


def compute_metrics(df):
    
    n = len(df) - 1
    prices = df["Close"]
    return {
        "ann_return": annualized_return(df, prices, n),
        "ann_volatility": annualized_volatility(df, prices, n),
        "max_drawdown": max_drawdown(df, prices, n),
    }
    

def annualized_return(df, prices, n):
    return (prices.iloc[-1] / prices.iloc[0]) ** (252 / n) - 1

def annualized_volatility(df, prices, n):
    returns = [prices.iloc[r] / prices.iloc[r - 1] - 1 for r in range(1, len(prices))]
    r_avg = sum(returns)/n
    r_std = math.sqrt(sum((r - r_avg) ** 2 for r in returns) / (n - 1))
    return r_std * math.sqrt(252)

def max_drawdown(df, prices, n):
    max_p = prices.iloc[0]
    mdd = 0
    for p in prices:
        if p >= max_p:
            max_p = p
        mdd = min(mdd, p / max_p - 1)
    return mdd
        
