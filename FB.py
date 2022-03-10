import pandas as pd
import datetime as dt
import yfinance as yf
import requests
import matplotlib.pyplot as plt
plt.style.use('seaborn-white')
plt.rcParams['figure.figsize'] = [12,7]
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["font.size"] = 15

# obtener apikey gratuita en https://fmpcloud.io/ (lleva 1 minuto)
apikey = 'acá_va_tu_APIkey_como_string'

ticker = 'FB'

def getProfile(symbol):
    url = 'https://fmpcloud.io/api/v3/profile/'+symbol
    p = {'apikey' : apikey}
    r = requests.get(url, params = p)
    js = r.json()
    df = pd.DataFrame(js)
    return df.T

# get balance sheet, income statement or cashflow statement
def getFundamental(symbol, what, period):
    p = {'apikey' : apikey, 'period' : period}
    if what == 'balance_sheet':
        url = 'https://fmpcloud.io/api/v3/balance-sheet-statement/'+symbol
    elif what == 'income_st':
        url = 'https://fmpcloud.io/api/v3/income-statement/'+symbol
    elif what == 'cash_flow':
        url = 'https://fmpcloud.io/api/v3/cash-flow-statement/'+symbol       
        
    r = requests.get(url, params = p)
    js = r.json()
    df = pd.DataFrame(js)
    return df[::-1]

fb = yf.download(ticker, period='max')['Adj Close'].to_frame()
fb['max'] = fb['Adj Close'].cummax()
fb['dd'] = (fb['Adj Close'] / fb['max'] -1) *100
print(fb.sort_values('dd', ascending=True)[0:5])

#==============================================================================
profile = getProfile(ticker)
mkt_cap = profile.loc['mktCap'][0]
name = profile.loc['companyName'][0]

bs = getFundamental(symbol=ticker, what='balance_sheet', period='annual')
inc = getFundamental(symbol=ticker, what='income_st', period='annual')
cf = getFundamental(symbol=ticker, what='cash_flow', period='annual')

url = f'https://fmpcloud.io/api/v3/enterprise-values/{ticker}?limit=40&apikey={apikey}'
r = requests.get(url)
js = r.json()
df = pd.DataFrame(js)[::-1]
df.set_index(pd.to_datetime(df['date']), inplace=True)
df.drop(['symbol', 'date'], axis=1, inplace=True)
df['cashAndShortTermInvestments'] = list(bs['cashAndShortTermInvestments']/1000000000)
df['netIncome'] = list(cf['netIncome']/1000000000)
df['operatingCashFlow'] = list(cf['operatingCashFlow']/1000000000)
df['capitalExpenditure'] = list(cf['capitalExpenditure']/1000000000)
df['freeCashFlow'] = list(cf['freeCashFlow']/1000000000)
df['revenue'] = list(inc['revenue']/1000000000)
df['R&D'] = list(inc['researchAndDevelopmentExpenses']/1000000000)
df['ebitda'] = list(inc['ebitda']/1000000000)

#==============================================================================
fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True, figsize=(12,8))
ax1.set(title=f'{name}', ylabel='USD')
ax1.plot(fb['Adj Close'], c="k")
ax1.set_facecolor('lightgray')
ax1.legend(['Price'])

ax2.set(title="Max drawdown (%)")
ax2.plot(fb['dd'], c="r")
ax2.fill_between(fb.index, fb['dd'], 0,
                 color="r")
ax2.set_facecolor('lightgray')
ax2.axhline(fb.dd[-100:].min(), c='k', lw=0.9, ls='--')
ax2.text(dt.date(2020,3,10), fb.dd[-100:].min()*0.95, f'Recent = {round(fb.dd[-100:].min(),1)}%')
plt.show()
#==============================================================================
#Estimates
years = 3
rev_growth = 0.1
target_margin = 0.42

date, revenue = [], []
for i in range(1,years+1):
    date.append(df.index[-1]+dt.timedelta(365*i))
    revenue.append(df.revenue[-1]*(1+rev_growth)**i)

proj = pd.DataFrame(revenue, index=date, columns=['revenue'])
proj['ebitda'] = proj['revenue']*target_margin

#==============================================================================
# graph
fig, ax = plt.subplots(figsize=(12,6))
ax.set_title(f'{name}', fontweight='bold')
revs = ax.bar([i.year for i in df.index], df['revenue'], label='Revenue', align='center',
              width=0.45, color='sienna', edgecolor='k')
ebitda = ax.bar([i.year for i in df.index], df['ebitda'], label='EBITDA', align='edge',
                width=0.45, color='darksalmon', edgecolor='k')
ax.set_ylabel('USD Bn')

ax2 = ax.twinx()
margin = ax2.plot([i.year for i in df.index], df['ebitda']/df['revenue']*100, ls='--', 
                  c='k', lw=1.5, label='EBITDA margin')
ax2.set_ylim(25,75)
ax2.set_ylabel('% EBITDA margin')

revs_proj = ax.bar([i.year for i in proj.index], proj['revenue'], align='center',
                   width=0.45, color='sienna',alpha=0.9, edgecolor='k', ls='-', lw=1.2)
ebitda_proj = ax.bar([i.year for i in proj.index], proj['ebitda'], align='edge',
                   width=0.45, color='darksalmon',alpha=0.9, edgecolor='k', ls='-', lw=1.2)
margin_proj = ax2.plot([i.year for i in proj.index], proj['ebitda']/proj['revenue']*100, ls='--',
                       c='k', lw=1.5)

lines_1, labels_1 = ax.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax.legend(lines_1 + lines_2, labels_1 + labels_2, loc=0)

plt.show()

#==============================================================================
fig, ax = plt.subplots(figsize=(12,6))
ax.set_title(f'{name}', fontweight='bold')
ax.set_facecolor('lightgray')
revs = ax.bar([i.year for i in df.index], df['revenue'], label='Revenue', align='center',
              width=0.45, color='w', edgecolor='k')

rd = ax.bar([i.year for i in df.index], df['R&D'], label='Research & Development', align='center',
              bottom=df['freeCashFlow'], width=0.45, color='lightsalmon', edgecolor='k')

fcf = ax.bar([i.year for i in df.index], df['freeCashFlow'], label='Free Cash Flow', align='center',
              width=0.45, color='yellowgreen', edgecolor='k') 
ax.set_ylabel('USD Bn')

ax2 = ax.twinx()
fcf_revs = ax2.plot([i.year for i in df.index], df['freeCashFlow']/df['revenue']*100, ls='--', 
                  c='k', lw=1.5, label='FCF to Revenue')

ax2.set_ylim(15,60)
ax2.set_ylabel('FCF to Revenue (%)')

lines_1, labels_1 = ax.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax.legend(lines_1 + lines_2, labels_1 + labels_2, loc=0)

plt.show()
#END!
