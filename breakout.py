import numpy as np
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import copy
import time

def ATR(DF, n):
    "function to calculate True Range and Average True Range"
    df = DF.copy()
    df['H-L'] = abs(df['High'] - df['Low'])
    df['H-PC'] = abs(df['High'] - df['Close'].shift(1))
    df['L-PC'] = abs(df['Low'] - df['Close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1, skipna=False)
    df['ATR'] = df['TR'].rolling(n).mean()
    df2 = df.drop(['H-L', 'H-PC', 'L-PC'], axis=1)
    return df2['ATR']

def CAGR(DF):
    "function to calculate the Cumulative Annual Growth Rate of a trading strategy"
    df = DF.copy()
    df["cum_return"] = (1 + df["ret"]).cumprod()
    n = len(df) / (252 * 78)
    if df["cum_return"].tolist():
        CAGR = (df["cum_return"].tolist()[-1]) ** (1 / n) - 1
    else:
        CAGR = 0  # Handle empty list case
    return CAGR

def volatility(DF):
    "function to calculate annualized volatility of a trading strategy"
    df = DF.copy()
    vol = df["ret"].std() * np.sqrt(252 * 78)
    return vol

def sharpe(DF, rf):
    "function to calculate sharpe ratio; rf is the risk-free rate"
    df = DF.copy()
    sr = (CAGR(df) - rf) / volatility(df)
    return sr

def max_dd(DF):
    "function to calculate max drawdown"
    df = DF.copy()
    df["cum_return"] = (1 + df["ret"]).cumprod()
    df["cum_roll_max"] = df["cum_return"].cummax()
    df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
    df["drawdown_pct"] = df["drawdown"] / df["cum_roll_max"]
    max_dd = df["drawdown_pct"].max()
    return max_dd

tickers = ["MSFT", "AAPL", "FB", "AMZN", "INTC", "CSCO", "VZ", "IBM", "TSLA", "AMD"]
api_key = "9ZV6KOZAVGJGLNAC"
ts = TimeSeries(key=api_key, output_format='pandas')

ohlc_intraday = {}
api_call_count = 0
start_time = time.time()

for ticker in tickers:
    try:
        data, _ = ts.get_intraday(symbol=ticker, interval='5min', outputsize='full')
        data.columns = ["Open", "High", "Low", "Close", "Volume"]
        data = data.iloc[::-1]
        data = data.between_time("09:35", "16:00")
        ohlc_intraday[ticker] = data
        api_call_count += 1
        time.sleep(12)  # Pause between API calls to avoid rate limiting
    except ValueError as e:
        print(f"Error fetching data for {ticker}: {e}")
        continue

    # Pause after every 5 API calls to respect rate limits
    if api_call_count == 5:
        api_call_count = 0
        elapsed_time = time.time() - start_time
        if elapsed_time < 60:
            time.sleep(60 - elapsed_time)
        start_time = time.time()

tickers = ohlc_intraday.keys()

ohlc_dict = copy.deepcopy(ohlc_intraday)
tickers_signal = {}
tickers_ret = {}
for ticker in tickers:
    print("calculating ATR and rolling max price for ", ticker)
    ohlc_dict[ticker]["ATR"] = ATR(ohlc_dict[ticker], 20)
    ohlc_dict[ticker]["rolling_max_cp"] = ohlc_dict[ticker]["High"].rolling(20).max()
    ohlc_dict[ticker]["rolling_min_cp"] = ohlc_dict[ticker]["Low"].rolling(20).min()
    ohlc_dict[ticker]["rolling_max_vol"] = ohlc_dict[ticker]["Volume"].rolling(20).min()
    ohlc_dict[ticker].dropna(inplace=True)
    tickers_signal[ticker] = ""
    tickers_ret[ticker] = []

for ticker in tickers:
    print("calculating returns for ", ticker)
    for i in range(1, len(ohlc_dict[ticker])):
        if tickers_signal[ticker] == "":
            if ohlc_dict[ticker]["High"][i] >= ohlc_dict[ticker]["rolling_max_cp"][i] and \
               ohlc_dict[ticker]["Volume"][i] > 1.5 * ohlc_dict[ticker]["rolling_max_vol"][i - 1]:
                tickers_signal[ticker] = "Buy"
            elif ohlc_dict[ticker]["Low"][i] <= ohlc_dict[ticker]["rolling_min_cp"][i] and \
                 ohlc_dict[ticker]["Volume"][i] > 1.5 * ohlc_dict[ticker]["rolling_max_vol"][i - 1]:
                tickers_signal[ticker] = "Sell"

        elif tickers_signal[ticker] == "Buy":
            if ohlc_dict[ticker]["Low"][i] < ohlc_dict[ticker]["Close"][i - 1] - ohlc_dict[ticker]["ATR"][i - 1]:
                tickers_signal[ticker] = ""
                tickers_ret[ticker].append(((ohlc_dict[ticker]["Close"][i - 1] - ohlc_dict[ticker]["ATR"][i - 1]) / ohlc_dict[ticker]["Close"][i - 1]) - 1)
            elif ohlc_dict[ticker]["Low"][i] <= ohlc_dict[ticker]["rolling_min_cp"][i] and \
                 ohlc_dict[ticker]["Volume"][i] > 1.5 * ohlc_dict[ticker]["rolling_max_vol"][i - 1]:
                tickers_signal[ticker] = "Sell"
                tickers_ret[ticker].append((ohlc_dict[ticker]["Close"][i] / ohlc_dict[ticker]["Close"][i - 1]) - 1)
            else:
                tickers_ret[ticker].append((ohlc_dict[ticker]["Close"][i] / ohlc_dict[ticker]["Close"][i - 1]) - 1)

        elif tickers_signal[ticker] == "Sell":
            if ohlc_dict[ticker]["High"][i] > ohlc_dict[ticker]["Close"][i - 1] + ohlc_dict[ticker]["ATR"][i - 1]:
                tickers_signal[ticker] = ""
                tickers_ret[ticker].append(((ohlc_dict[ticker]["Close"][i - 1] + ohlc_dict[ticker]["ATR"][i - 1]) / ohlc_dict[ticker]["Close"][i - 1]) - 1)
            elif ohlc_dict[ticker]["High"][i] >= ohlc_dict[ticker]["rolling_max_cp"][i] and \
                 ohlc_dict[ticker]["Volume"][i] > 1.5 * ohlc_dict[ticker]["rolling_max_vol"][i - 1]:
                tickers_signal[ticker] = "Buy"
                tickers_ret[ticker].append((ohlc_dict[ticker]["Close"][i - 1] / ohlc_dict[ticker]["Close"][i]) - 1)
            else:
                tickers_ret[ticker].append((ohlc_dict[ticker]["Close"][i - 1] / ohlc_dict[ticker]["Close"][i]) - 1)

    ohlc_dict[ticker]["ret"] = tickers_ret[ticker]

# Calculating overall strategy's KPIs
strategy_df = pd.DataFrame()
for ticker in tickers:
    strategy_df[ticker] = ohlc_dict[ticker]["ret"]
strategy_df["ret"] = strategy_df.mean(axis=1)
CAGR(strategy_df)
sharpe(strategy_df, 0.025)
max_dd(strategy_df)

# Visualization of strategy return
(1 + strategy_df["ret"]).cumprod().plot()

# Calculating individual stock's KPIs
cagr = {}
sharpe_ratios = {}
max_drawdown = {}
for ticker in tickers:
    print("calculating KPIs for ", ticker)
    cagr[ticker] = CAGR(ohlc_dict[ticker])
    sharpe_ratios[ticker] = sharpe(ohlc_dict[ticker], 0.025)
    max_drawdown[ticker] = max_dd(ohlc_dict[ticker])

KPI_df = pd.DataFrame([cagr, sharpe_ratios, max_drawdown], index=["Return", "Sharpe Ratio", "Max Drawdown"])
KPI_df.T




