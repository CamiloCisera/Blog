import pandas as pd, numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import datetime as dt
plt.style.use('seaborn-white')
plt.rcParams['figure.figsize'] = [12,9]
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["font.size"] = 16
plt.rcParams["axes.labelweight"] = "bold"

#=============
# Equity USA
#=============
spx = yf.download('^GSPC', period='max')['Close']

tiempo = (spx.index[-1] - spx.index[0]).days/365
ret = spx[-1] / spx[0] -1
cagr = (1+ret)**(1/tiempo)-1
print('\n'+f'Retorno S&P 500 desde {spx.index[0].year} y sin dividendos es {round(cagr*100,1)}% anual')

spx2 = spx.to_frame().copy()
spx2 = spx2.resample("Y").last()
spx2["var"] = spx2["Close"].pct_change()
spx2.dropna(inplace=True)

plt.title("Variación anual del S&P 500 (%)", fontweight="bold")
plt.bar(spx2.index, spx2["var"]*100, width=200, color="darkblue")
plt.axhline(0, c="k")
plt.axhline(cagr*100, c="r", ls="--", lw=1.2, label='Retorno promedio 6%')
plt.fill_between(spx2.index, y1=(cagr-0.02)*100, y2=(cagr+0.02)*100, color='lime',
                 label="Retorno promedio +/- 2%", edgecolors='k')
plt.legend()
plt.show()

dentro = 0
doble_digit = 0
for i in range(len(spx2)):
    if spx2['var'][i] <= cagr+0.02 and spx2['var'][i] >= cagr-0.02:
        var = spx2['var'][i]
        print(f'retorno {spx2.index[i].year} fue de {round(var*100,2)}%')
        dentro += 1
    elif spx2['var'][i] <= -0.1 or spx2['var'][i] >= 0.1:
        var = spx2['var'][i]
        doble_digit += 1
        
print('\n'+f'En {len(spx2)} años, el S&P 500 rindió +/- 2% de su promedio {dentro} veces')
percent = doble_digit / len(spx2)
print('\n'+f'En {len(spx2)} años, el S&P 500 rindió dos dígios {doble_digit} veces. El {round(percent*100,2)}% del tiempo')

#=============
# Equity Arg
#=============

start = '2018-01-01'
end = dt.date.today()
ggal_local = yf.download("GGAL.BA", start, end)["Adj Close"]
ggal_adr = yf.download("GGAL", start, end)["Adj Close"]

ccl = (ggal_local*10/ggal_adr).to_frame()
ccl.dropna(inplace=True)
ccl.columns = ["CCL"]
#====

tickers = ["BPAT.BA", "LOMA.BA", "YPFD.BA", "CTIO.BA", "SUPV.BA",
           "BHIP.BA", "BYMA.BA", "CRES.BA", "COME.BA", "MIRG.BA",
           "EDN.BA", "PAMP.BA", "TXAR.BA", "TECO2.BA", "TGSU2.BA",
           "VALO.BA", "CEPU.BA", "ALUA.BA", "BMA.BA", "GGAL.BA",
           'TRAN.BA', 'IRSA.BA']

Stonks = yf.download(tickers, start, end)["Adj Close"]

#Crisis  
data = pd.DataFrame()
for ticker in tickers:
    data[ticker] = Stonks[ticker].div(ccl.CCL, axis=0).fillna(method='backfill')
    data[ticker+'1'] = data[ticker] / data[ticker].loc[data[ticker].idxmax()] *100

plt.title(f'{len(tickers)} acciones argetinas - de máximos 2018 a mínimos', fontweight='bold')
for ticker in tickers:
    plt.plot(data[ticker+'1'].loc[data[ticker].idxmax():data[ticker].idxmin()])
    plt.scatter(data[ticker].idxmin(), data[ticker+'1'].min())
plt.show()

returns = pd.DataFrame(index=tickers, columns=["retorno"])
for ticker in tickers:
    ret = data[ticker].loc['2020-01-01':].min() / data[ticker].loc[:'2018-12-31'].max() -1
    returns["retorno"].loc[ticker] = ret
    #print(f'{ticker} retorno semanal {round(ret*100,2)}% {ticker}')
returns.dropna(inplace=True)
print('\n'+'Retornos crisis reciente - desde máximos 2018 a mínimos')
for i in range(len(returns)):
    print(f'{(returns["retorno"]*100).sort_values(ascending=False).index[i]} {round((returns["retorno"]*100).sort_values(ascending=False)[i],1)}%')

# Recuperación (?)
data2 = pd.DataFrame()
for ticker in tickers:
    data2[ticker] = Stonks[ticker].div(ccl.CCL, axis=0).fillna(method='backfill')
    data2[ticker+'1'] = data2[ticker] / data2[ticker].loc[data2[ticker].idxmin()] *100

plt.title(f'{len(tickers)} acciones argetinas - ¿Recuperación? ', fontweight='bold')
for ticker in tickers:
    if data2[ticker].iloc[-1] / data2[ticker].min() -1 > 0.5:
        plt.plot(data2[ticker+'1'].loc[data2[ticker].idxmin():])
        plt.scatter(data2.index[-1], data2[ticker+'1'].iloc[-1])
        plt.scatter(data2[ticker].idxmin(), data2[ticker+'1'].min(), c='r', edgecolors='k')
        plt.text(data2.index[-1],data2[ticker+'1'].iloc[-1], ticker[:4])
        #plt.scatter(data2[ticker].loc[data2[ticker].idxmin():].idxmax(), data2[ticker+'1'].loc[data2[ticker].idxmin():].max())
plt.show()

returns = pd.DataFrame(index=tickers, columns=["retorno"])
for ticker in tickers:
    ret = data2[ticker].iloc[-1] / data2[ticker].min() -1
    returns["retorno"].loc[ticker] = ret
    print(f'{ticker} minimo de {round(data2[ticker].min(),2)} el {data2[ticker].idxmin()}')
returns.dropna(inplace=True)
print('\n'+'Retornos desde mínimos')
for i in range(len(returns)):
    print(f'{(returns["retorno"]*100).sort_values(ascending=False).index[i]} {round((returns["retorno"]*100).sort_values(ascending=False)[i],1)}%')
