import pandas as pd, numpy as np
import yfinance as yf
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt

#Caracteristicas para los graficos
plt.style.use('seaborn-white')
plt.rcParams['figure.figsize'] = [12,9]
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["font.size"] = 16
plt.rcParams["axes.labelweight"] = "bold"

#======IMPORTACIÓN DE DATOS====================================================

tickers = ["GLD", "SHY", "SPY", "AGG", "TLT", "QQQ"]
start= dt.date.today()-dt.timedelta(5840)
end= dt.date.today()
cartera = yf.download(tickers, start, end)["Adj Close"]
cartera.dropna(inplace=True)

#============CORRELACIONES=====================================================
sns.heatmap(cartera.pct_change().corr(), cmap='coolwarm',
            annot=True, linewidths=.5)

#===========MÉTRICAS DE RENDIMIENTO============================================
yields = cartera.pct_change()

años = (cartera.index[-1] - cartera.index[0]).days/365
print(f'los años de análisis son {round(años,1)} y van desde {cartera.index[0]} hasta {cartera.index[-1]}')
risk_free = 0.0214

for ticker in tickers:
    yields2 = yields.copy()
    yields2["acum_ret"] = (1+yields2[ticker]).cumprod()-1
    print("\n"+ticker)
    print("retorno total ", round(yields2["acum_ret"][-1]*100,2), "%")
    retorno = ((1+yields2["acum_ret"][-1])**(1/años))-1
    print(f"Rerono anual (CAGR) {round(retorno*100,2)} %")
    
    volatilidad = yields2[ticker].std() * np.sqrt(252)
    print(f"Volatilidad anual {round(volatilidad*100,2)} %")
    
    sharpe = (retorno-risk_free)/volatilidad
    print(f'Sharpe ratio {round(sharpe,2)}')
    
    cartera2 = cartera.copy()
    cartera2["maximo"] = cartera2[ticker].cummax()
    cartera2["perdida"] = (cartera2[ticker] / cartera2["maximo"]) -1
    max_dd = cartera2["perdida"].min()
    print(f'Pérdida máxima {round(max_dd*100,2)} %')
    
#=======REBALANCEO=============================================================
proporciones = [0.25, 0.25, 0.25, 0, 0.25, 0] # Podés probar cambiar combinaciones
# GLD - SHY - SPY - AGG - TLT - QQQ
# Si la suma de proporciones es <1 el resto se considera cash

capital_inicial = 10000
capital = capital_inicial
comision = 0.01
acciones = []
fecha = []
GLD = cartera["GLD"][0]
SHY = cartera["SHY"][0]
SPY = cartera["SPY"][0]
AGG = cartera["AGG"][0]
TLT = cartera["TLT"][0]
QQQ = cartera["QQQ"][0]
acciones2 = [proporciones[0]*capital/GLD,
             proporciones[1]*capital/SHY,
             proporciones[2]*capital/SPY,
             proporciones[3]*capital/AGG,
             proporciones[4]*capital/TLT,
             proporciones[5]*capital/QQQ]
acciones.append(acciones2)
fecha.append(cartera.index[0])

#==============================================================================
año = cartera.index[0].year
for i in range(len(cartera)):
    if año != cartera.index[i].year:
        gld_var = cartera["GLD"][i]/ GLD -1
        shy_var = cartera["SHY"][i]/ SHY -1
        spy_var = cartera["SPY"][i]/ SPY -1
        agg_var = cartera["AGG"][i]/ AGG -1
        tlt_var = cartera["TLT"][i]/ TLT -1
        QQQ_var = cartera["QQQ"][i]/ QQQ -1
        resultado_anual = (proporciones[0]*gld_var + proporciones[1]*shy_var +
                           proporciones[2]*spy_var + proporciones[3]*agg_var +
                           proporciones[4]*tlt_var + proporciones[5]*QQQ_var)
        capital = capital*(1+resultado_anual)
        print("Fecha ", cartera.index[i])
        print(f'El capital invertido es de U$S {round(capital,2)}')
        GLD = cartera["GLD"][i]
        SHY = cartera["SHY"][i]
        SPY = cartera["SPY"][i]
        AGG = cartera["AGG"][i]
        TLT = cartera["TLT"][i]
        QQQ = cartera["QQQ"][i]    
        acciones2 = [proporciones[0]*capital/GLD,
                     proporciones[1]*capital/SHY,
                     proporciones[2]*capital/SPY,
                     proporciones[3]*capital/AGG,
                     proporciones[4]*capital/TLT,
                     proporciones[5]*capital/QQQ]
        acciones.append(acciones2)
        fecha.append(cartera.index[i])
        print(acciones2)
    año = cartera.index[i].year
#==============================================================================

cantidades = pd.DataFrame(acciones, index=fecha,
                          columns=["n_gld","n_shy", "n_spy",
                                   "n_agg", "n_tlt", "n_QQQ"])

#CALCULO DE COMISIONES
for i in range(len(cantidades)):
    if i == 0:
        precio_gld = cartera.loc[cantidades.index[i]]["GLD"]
        precio_shy = cartera.loc[cantidades.index[i]]["SHY"]
        precio_spy = cartera.loc[cantidades.index[i]]["SPY"]
        precio_agg = cartera.loc[cantidades.index[i]]["AGG"]
        precio_tlt = cartera.loc[cantidades.index[i]]["TLT"]
        precio_QQQ = cartera.loc[cantidades.index[i]]["QQQ"]
        comision_gld = cantidades["n_gld"][i]*precio_gld*comision
        comision_shy = cantidades["n_shy"][i]*precio_shy*comision
        comision_spy = cantidades["n_spy"][i]*precio_spy*comision
        comision_agg = cantidades["n_agg"][i]*precio_agg*comision
        comision_tlt = cantidades["n_tlt"][i]*precio_tlt*comision
        comision_QQQ = cantidades["n_QQQ"][i]*precio_QQQ*comision
        comisiones = [comision_gld + comision_shy + comision_spy +
                      comision_agg + comision_tlt + comision_QQQ]
    elif i != 0:
        precio_gld = cartera.loc[cantidades.index[i]]["GLD"]
        precio_shy = cartera.loc[cantidades.index[i]]["SHY"]
        precio_spy = cartera.loc[cantidades.index[i]]["SPY"]
        precio_agg = cartera.loc[cantidades.index[i]]["AGG"]
        precio_tlt = cartera.loc[cantidades.index[i]]["TLT"]
        precio_QQQ = cartera.loc[cantidades.index[i]]["QQQ"]
        comision_gld = abs(cantidades["n_gld"][i]-cantidades["n_gld"][i-1])*precio_gld*comision
        comision_shy = abs(cantidades["n_shy"][i]-cantidades["n_shy"][i-1])*precio_shy*comision
        comision_spy = abs(cantidades["n_spy"][i]-cantidades["n_spy"][i-1])*precio_spy*comision       
        comision_agg = abs(cantidades["n_agg"][i]-cantidades["n_agg"][i-1])*precio_agg*comision
        comision_tlt = abs(cantidades["n_tlt"][i]-cantidades["n_tlt"][i-1])*precio_tlt*comision
        comision_QQQ = abs(cantidades["n_QQQ"][i]-cantidades["n_QQQ"][i-1])*precio_QQQ*comision       
        comisiones.append(comision_gld + comision_shy + comision_spy +
                          comision_agg + comision_tlt + comision_QQQ)

comisiones_df = pd.DataFrame(comisiones, index=fecha,
                             columns=["comisiones"])
comisiones_df["comisiones_acumuladas"] = comisiones_df["comisiones"].cumsum()
comisiones_df = comisiones_df.drop(["comisiones"], axis=1)
# Supone que las comisiones se pagan en efectivo, sin vender activos.
#==============================================================================
cartera_casi_final = pd.merge(left=cartera, right=cantidades, how="outer",
                         left_on="Date", right_on=cantidades.index)

cartera_total = pd.merge(left=cartera_casi_final, right=comisiones_df, how="outer",
                         left_on="Date", right_on=comisiones_df.index)

cartera_total.set_index("Date", inplace=True)
cartera_total.fillna(method="ffill", inplace=True)

cash = (1-(proporciones[0]+proporciones[1]+proporciones[2]+
           proporciones[3]+proporciones[4]+proporciones[5]))*capital_inicial
cartera_total["total"] = (cash + cartera_total["GLD"]*cartera_total["n_gld"] +
                          cartera_total["SHY"]*cartera_total["n_shy"] +
                          cartera_total["SPY"]*cartera_total["n_spy"] +
                          cartera_total["AGG"]*cartera_total["n_agg"] +
                          cartera_total["TLT"]*cartera_total["n_tlt"] +
                          cartera_total["QQQ"]*cartera_total["n_QQQ"] -
                          cartera_total["comisiones_acumuladas"])
#================PASO A BASE 1 PARA GRAFICAR==================================
pfolio = cartera_total.copy()
pfolio["base_1"] = pfolio["total"] / pfolio["total"].iloc[0]
pfolio["GLD_1"] = pfolio["GLD"] / pfolio["GLD"].iloc[0]
pfolio["SHY_1"] = pfolio["SHY"] / pfolio["SHY"].iloc[0]
pfolio["SPY_1"] = pfolio["SPY"] / pfolio["SPY"].iloc[0]
pfolio["AGG_1"] = pfolio["AGG"] / pfolio["AGG"].iloc[0]
pfolio["TLT_1"] = pfolio["TLT"] / pfolio["TLT"].iloc[0]
pfolio["QQQ_1"] = pfolio["QQQ"] / pfolio["QQQ"].iloc[0]

#===============GRAFICO========================================================

plt.plot(pfolio["base_1"], label="MIX", c="b")
plt.scatter(pfolio.index[-1], pfolio["base_1"][-1], c="b")
plt.plot(pfolio["SPY_1"], lw=0.7, label="S&P 500", c="g")
plt.scatter(pfolio.index[-1], pfolio["SPY_1"][-1], c="g")
plt.plot(pfolio["SHY_1"], lw=0.7, label="Bonos cortos", c="r")
plt.scatter(pfolio.index[-1], pfolio["SHY_1"][-1], c="r")
plt.plot(pfolio["GLD_1"], lw=0.7, label="Oro", c="y")
plt.scatter(pfolio.index[-1], pfolio["GLD_1"][-1], c="y")
plt.plot(pfolio["AGG_1"], lw=0.7, label="Bonos corporativos", c="c")
plt.scatter(pfolio.index[-1], pfolio["AGG_1"][-1], c="c")
plt.plot(pfolio["TLT_1"], lw=0.7, label="Bonos largos", c="k")
plt.scatter(pfolio.index[-1], pfolio["TLT_1"][-1], c="k")
plt.plot(pfolio["QQQ_1"], lw=0.7, label="Nasdaq", c="salmon")
plt.scatter(pfolio.index[-1], pfolio["QQQ_1"][-1], c="salmon")
plt.legend()

#===========MÉTRICAS DE RENDIMIENTO PARA COMBINACIÓN===========================
yields = pfolio["total"].pct_change()
vol_anual = yields.std() * np.sqrt(252)

accum = pfolio["total"][-1] / pfolio["total"][0] -1
años = (cartera.index[-1] - cartera.index[0]).days/365
cagr = ((1+accum)**(1/años))-1

risk_free = 0.0214 
sharpe = (cagr - risk_free)/vol_anual

calc_caidas = pfolio.copy()
calc_caidas["max_acumulado"] = calc_caidas["total"].cummax()
calc_caidas["desde_max"] = (calc_caidas["total"] / calc_caidas["max_acumulado"] -1)*100
perdida_maxima = calc_caidas["desde_max"].min()

print("\n"+"Tu cartera está compuesta por:")
print(f"{proporciones[0]*100}% GLD, {proporciones[1]*100}% SHY, {proporciones[2]*100}% SPY")
print(f"{proporciones[3]*100}% AGG, {proporciones[4]*100}% TLT, {proporciones[5]*100}% QQQ")
print("\n"+"Métricas de tu combinación:"+"\n"+f"CAGR = {round(cagr*100,2)}%")
print(f"Retorno total = {round(accum*100,2)}%")
print(f"""Volatilidad = {round(vol_anual*100,2)}%
Sharpe = {round(sharpe,2)}
Pérdida máxima = {round(perdida_maxima,2)}%""")

# GRAFICO HISTORICO DE BAJAS
plt.title("Caídas desde maximos (%)")
plt.plot(calc_caidas["desde_max"], c="r")
plt.fill_between(calc_caidas.index, calc_caidas["desde_max"], 0,
                 color="red")


#Grafico portfolio y bajas
fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True, figsize=(12,8))
ax1.set(title="Rendimiento de U$S 1 invertido en la cartera permanente")
ax1.plot(pfolio["base_1"], label="MIX", c="k")
ax1.grid(True)

ax2.set(title="Bajas desde máximos (%)")
ax2.plot(calc_caidas["desde_max"], c="k")
ax2.fill_between(calc_caidas.index, calc_caidas["desde_max"], 0,
                 color="k")

# FIN!





