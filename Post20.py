import pandas as pd
import datetime as dt
import yfinance as yf
import numpy as np

import matplotlib.pyplot as plt
plt.style.use('seaborn-white')
plt.rcParams['figure.figsize'] = [12,6]
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["font.size"] = 15

tickers = ["IWN", "IWO"]
etfs = yf.download(tickers, period="max")["Adj Close"]
etfs.dropna(inplace=True)

etfs["value1"] = etfs["IWN"] / etfs["IWN"].iloc[0] 
etfs["growth1"] = etfs["IWO"] / etfs["IWO"].iloc[0] 

plt.title("Value vs Growth (2000-2020)", fontweight="bold",
          c="k", fontsize=22)
plt.plot(etfs["value1"], c="b", label="iShares Russell 2000 Value (IWN)")
plt.plot(etfs["growth1"], c="r", label="iShares Russell 2000 Growth (IWO)")
plt.legend()
plt.show()

#etfs["ratio"] = etfs.iloc[:,0] / etfs.iloc[:,1]

anuales = etfs.copy()
anuales = anuales.resample("Y").last()
yields = anuales.pct_change().dropna()

#Grafico
labels = yields.index.year
x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots()
vong = ax.bar(x- width/2, yields["IWO"], width, label="Growth (IWO)", color="r")
vonv = ax.bar(x+ width/2, yields["IWN"], width, label="Value (IWN)", color="b")
ax.axhline(0, color="k")
ax.set_ylabel("Variación")
ax.set_title("Growth vs Value - Variaciones anuales",
             fontweight="bold", c="k", fontsize=25)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

fig.tight_layout()
plt.show()
