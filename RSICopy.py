import datetime as dt
import pandas as pd
import yfinance as yf

stock_list = ['SPY', 'EFA', 'IWD', 'IWF', 'IJH', 'IWM', 'EWJ']


def get_stock_prices(company_name):
    start = dt.datetime(2003, 1, 1)
    end = dt.datetime(2022, 12, 31)
    stock_price = yf.download(company_name, start, end)['Adj Close']
    stock_price_df = pd.DataFrame(stock_price.div(stock_price.iat[0]))
    stock_price_df.columns = [company_name]
    return stock_price_df


def rsi_strategy(data, start, end, rsi_value):
    df = pd.DataFrame()
    data_list = list(data)

    for datum in data_list:
        df[datum] = data.iloc[:, 0]
        print(df[datum])
        print(df[datum].shift(0))
        rolled = df[datum].rolling(90)
        print(rolled)
        print(rolled.mean())
        print(rolled.mean().shift(0))


if __name__ == '__main__':
    prices = get_stock_prices('GOOG')
    rsi_strategy(prices, 0, 0, 90)
