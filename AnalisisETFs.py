"""
Creado en enero 2021

@autor: Camilo Cisera
"""
import pandas as pd, numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
plt.style.use('seaborn-white')
plt.rcParams['figure.figsize'] = [12,9]
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["font.size"] = 16
plt.rcParams["axes.labelweight"] = "bold"

#=================
#   Funciones
#=================
def max_dd (dataframe, ticker):
    df = dataframe.copy()
    df["max"] = df[ticker].cummax()
    df["baja"] = df[ticker] / df["max"] -1
    print(f'{ticker} baja max {round(df["baja"].min()*100,2)}%')
    return(df["baja"].min())
    
def volatilidad (dataframe, ticker):
    df = dataframe.copy()
    yields = df[ticker].pct_change().to_frame()
    vol = yields[ticker].std() * np.sqrt(252)
    print(f'La volatilidad de {ticker} es {round(vol*100,2)}%')
    return(vol)

def CAGR (dataframe, ticker):
    df = dataframe.copy()
    retorno = df[ticker].iloc[-1] / df[ticker].iloc[0] -1
    tiempo = (df.index[-1] - df.index[0]).days
    tiempo2 = tiempo/365
    cagr = ((1+retorno)**(1/tiempo2))-1
    print(f'Retorno total de {ticker} en {round(tiempo2,1)} años es {round(retorno*100,2)}%')
    print(f'Retorno de {ticker} desde {df.index[0].year} es de {round(cagr*100,2)}% anual')
    return(cagr)

#==========================================================

tickers = ["SPY", "QQQ", "VTI", "IWM", "DIA"] 
# También se puede probar con estos tickers ["^GSPC", "^NDX", "^DJI", "^RUT"]

stocks = yf.download(tickers, period="max")["Adj Close"]
stocks.dropna(inplace=True)

base1 = pd.DataFrame()
for ticker in tickers:
    base1[ticker+"1"] = stocks[ticker] / stocks[ticker].iloc[0]
    
for ticker in base1.keys():
    plt.plot(base1[ticker])
    plt.scatter(base1.index[-1], base1[ticker].iloc[-1], edgecolors="k")
    plt.text(base1.index[-1], base1[ticker].iloc[-1], ticker)
plt.grid(True)

for ticker in base1.keys():
    CAGR(base1, ticker)
    max_dd(base1, ticker)
    volatilidad(base1, ticker)
    print() 
