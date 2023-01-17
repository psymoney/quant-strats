from bokeh.plotting import show, output_file
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas_datareader.data as web
matplotlib.rc('font', family="Malgun Gothic", size=8, weight='bold')

주식리스트 = ['SPY', 'EFA', 'IWD', 'IWF', 'IJH', 'IWM', 'EWJ']
채권리스트 = ['IEF', 'TLT', 'LQD', 'IEF', 'TLT', 'LQD', 'IEF']
현금리스트 = ['SHY']
전체리스트 = 주식리스트


def 주가(stock, start):
    주가 = web.DataReader(name=stock, data_source='yahoo', start=start)['Adj Close']
    a = pd.DataFrame(주가.div(주가.iat[0]))
    a.columns = [stock]
    return a


def RSI전략(데이터, 매수기간, RSI값):
    a = pd.DataFrame()
    b = list(데이터)
    for i in b:
        a[i] = 데이터.iloc[:, 0]
        a[i + 'RSI'] = RSI(데이터, timeperiod=2, price=i)
        a[i + '매수시그널'] = np.where((a[i] > a[i].rolling(매수기간).mean().shift(0)) & (a[i+'RSI'].shift(0) < RSI값) &
                                  (a[i] < a[i].rolling(5).mean().shift(0)), 1, 0)
        a[i + '매도시그널'] = np.where(a[i] > a[i].rolling(5).mean().shift(1), 1, 0)
        a[i + '마켓포지션'] = np.where(a[i+'매수시그널'] == 1, 1, np.where(a[i + '매도시그널'] == 1, 0, np.nan))
        a[i + '최종포지션'] = a[i + '마켓포지션'].ffill()
        a[i + '수익'] = np.where(a[i + '최종포지션'].shift(1) == 1, a[i]/a[i].shift(1), 1).cumprod()
    return a[i+'수익']


def 다중RSI전략(데이터, 주기1, 주기2, 주기3, 주기4, 주기5, RSI값):
    a = pd.DataFrame()
    b = [주기1, 주기2, 주기3, 주기4, 주기5]
    for i in b:
        a[str(i)] = RSI전략(데이터, i, RSI값)

    return a.mean(axis=1)


def 전체데이터():
    a = pd.DataFrame()
    for i in 전체리스트:
        a = pd.concat([a, 주가(i, '2003-01-01')], axis=1)
    return a


a = pd.DataFrame()
for i in 전체리스트:
    a = pd.concat([a, 다중RSI전략(주가(i, '2003-01-01'), 90, 120, 150, 180, 200, 5)], axis=1)
a['mean'] = a.mean(axis=1)

전체데이터().mean(axis=1)
b = 전체데이터().mean(axis=1).to_frame()
b.columns = ['a']
chart = Line(다중RSI전략(b, 90, 120, 150, 180, 200, 20), ylabel='수익', xlabel='날짜')
show(chart)
