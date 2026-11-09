# Stock Dashboard

Interactive dashboard for analyzing stocks: search by company name,
candlestick chart, trading volume and key risk/return metrics.

## Features
- Company search (name → ticker)
- Candlestick price chart and daily volume, periods from 1 month to 5 years
- Key figures: price, P/E, 52-week range
- Risk/return metrics computed from price data:
  - Annualized return (geometric): (P_end / P_start)^(252/n) − 1
  - Annualized volatility: std of daily returns × √252
  - Maximum drawdown: largest fall from a running peak

## Run locally
pip install -r requirements.txt
python app.py
Then open http://127.0.0.1:8050

## Limitations
- Annualizing short periods (1–3 months) exaggerates returns; interpret with care.
- Data comes from Yahoo Finance via yfinance (unofficial, may be delayed or rate-limited).

## Next steps
- Compare several tickers
- Benchmark against an index (e.g. S&P 500, DAX)

Built with AI assistance; metric calculations implemented and verified by me
