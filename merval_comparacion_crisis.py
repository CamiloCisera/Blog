import pandas as pd
import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"]=[12,8]
plt.style.use('seaborn-white')
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["font.size"] = 12
plt.rcParams["axes.labelweight"] = "bold"

#El excel que se descarga esta en el github
merv = pd.read_excel("/Users/ciser/Desktop/Camilo/Exportados desde Python/merval_actualizado.xlsx",
                     index_col=0)

# 2 grandes crisis: "1" es 2001 y "2" la actual
fecha_max_1 = merv["Merval_dlr"].loc["1999-05-15":"2003-05-15"].idxmax()
fecha_min_1 = merv["Merval_dlr"].loc["1999-05-15":"2003-05-15"].idxmin()
fecha_max_2 = merv["Merval_dlr"].loc["2017-11-15":"2020-05-15"].idxmax()

#=====GRAFICO1=================================================================
plt.plot(merv["Merval_dlr"].loc["1999-01-05":"2007-05-15"], c="indigo")
plt.title("MERVAL EN U$S NOMINALES - CRISIS 2001 Y RECUPERACION", fontweight="bold")
plt.ylabel("U$S", fontsize=15, c="k")
plt.xlabel("AÑOS", fontsize=14, c="k")
plt.axvline(dt.date(2001,12,23), c="k", lw=0.95, ls="--", ymax=0.85)
plt.text(dt.date(2001,6,23),675, s="23/12/2001 "+"\n"+"  Default")
plt.axvline(dt.date(2003,9,22), c="k", lw=0.95, ls="--", ymax=0.5)
plt.text(dt.date(2002,5,15),415, s="   22/09/2003 "+"\n"+"1ra propuesta"+"\n"+" 75% de quita")
plt.axvline(dt.date(2004,6,1), c="k", lw=0.95, ls="--", ymax=0.7)
plt.text(dt.date(2002,6,23),550, s="      01/06/2004 "+"\n"+"  Mejoran propuesta")
plt.axvline(dt.date(2003,5,25), c="k", lw=0.95, ls="--", ymax=0.4)
plt.text(dt.date(2002,3,23),320, s="  25/05/2003 "+"\n"+"  Asume NK")

plt.axvspan(dt.date(2001,12,21),fecha_min_1,ymin=0.045, ymax=0.25,
            color="r", alpha=0.4)
plt.annotate("Pesificación forzada"+"\n"+"Retenciones a petroleras"+"\n"+"Devaluación",
             weight ='bold', xy=(dt.date(2001,12,21), 125), xytext=(dt.date(1999,1,6), 80),
             arrowprops=dict(arrowstyle="->", color="k"))
plt.annotate("03/12/2001"+"\n"+"Corralito",
             weight ='bold', xy=(dt.date(2001,12,3), 178), xytext=(dt.date(2000,1,6), 220),
             arrowprops=dict(arrowstyle="->", color="k"))

plt.axvline(dt.date(2005,3,3), c="k", lw=0.95, ls="--", ymax=0.85)
plt.text(dt.date(2003,12,23),665, s="        03/03/2005 "+"\n"+"  76% entra al canje"+"\n"+"     Quita del 65%")

#==============================================================================
#   PREPARACION DE DATOS PARA EL GRAFICO 2
#==============================================================================

crisis1 = merv.copy()
crisis2 = merv.copy()

crisis1 = crisis1.loc[fecha_max_1:"2002-12-12"]
crisis2 = crisis2.loc[fecha_max_2:"2020-05-29"]

crisis1["base1"] = crisis1["Merval_dlr"] / crisis1["Merval_dlr"].loc[fecha_max_1]
crisis2["base1"] = crisis2["Merval_dlr"] / crisis2["Merval_dlr"].loc[fecha_max_2]

crisis1_adj = crisis1.resample("D").mean()
crisis1_adj["base1"].plot()

crisis2_adj = crisis2.resample("D").mean()
crisis2_adj["base1"].plot()

crisis1_adj.reset_index(inplace=True)
crisis2_adj.reset_index(inplace=True)

crisis1_adj["base1"].fillna(method="backfill", inplace=True)
crisis2_adj["base1"].fillna(method="backfill", inplace=True)

#========GRAFICO2==============================================================
plt.title("Merval en U$S - Crisis 2001 y actual comparadas",
          fontweight="bold",
          fontsize=16)
plt.plot(crisis1_adj["base1"], label="Crisis 2001", c="black",
         lw=1.3)
plt.plot(crisis2_adj["base1"], label="Crisis actual", c="g",
         lw=1.3)
plt.ylabel("MÁXIMO PRE-CRISIS = 1", c="black")
plt.xlabel("DÍAS DESDE EL MÁXIMO", c="black")
plt.legend()
plt.show()

#==============================================================================
#   PREPARACION DE DATOS PARA EL GRAFICO 3
#==============================================================================
#Crisis subprime de 2008
fecha_max_08 = merv.Merval_dlr.loc["2008-01-05":"2010-01-05"].idxmax()
fecha_min_08 = merv.Merval_dlr.loc["2008-01-05":"2010-01-05"].idxmin()
max_precrisis_08 = merv.Merval_dlr.loc["2008-01-05":"2010-01-05"].max()
min_crisis_08 = merv.Merval_dlr.loc["2008-01-05":"2010-01-05"].min()

crisis_2008 = merv.copy()
crisis_2008 = crisis_2008.loc[fecha_max_08:fecha_min_08 ] #"2010-10-13"
crisis_2008["base1"] = crisis_2008["Merval_dlr"] / crisis_2008["Merval_dlr"].loc[fecha_max_08]

crisis2008_adj = crisis_2008.resample("D").mean()
crisis2008_adj.reset_index(inplace=True)
crisis2008_adj["base1"].fillna(method="backfill", inplace=True)

#Crisis Eurozona fines 2010 - ppios 2011
fecha_max_11 = merv.Merval_dlr.loc["2010-01-01":"2014-01-01"].idxmax()
fecha_min_11 = merv.Merval_dlr.loc["2010-01-01":"2014-01-01"].idxmin()
max_precrisis_11 = merv.Merval_dlr.loc["2010-01-01":"2014-01-01"].max()
min_crisis_11 = merv.Merval_dlr.loc["2010-01-01":"2014-01-01"].min()

crisis_2011 = merv.copy()
crisis_2011 = crisis_2011.loc[fecha_max_11:fecha_min_11] #"2015-03-18"
crisis_2011["base1"] = crisis_2011["Merval_dlr"] / crisis_2011["Merval_dlr"].loc[fecha_max_11]

crisis2011_adj = crisis_2011.resample("D").mean()
crisis2011_adj.reset_index(inplace=True)
crisis2011_adj["base1"].fillna(method="backfill", inplace=True)

#========GRAFICO3==============================================================
plt.title("Merval en U$S - Crisis comparadas",
          fontweight="bold",
          fontsize=18)
plt.plot(crisis1_adj["base1"], label="Crisis 2001", c="black",
         lw=1.3)
plt.plot(crisis2008_adj["base1"], label="Crisis 2008", c="r",
         lw=1.3)
plt.plot(crisis2011_adj["base1"], label="Crisis 2011", c="b",
         lw=1.3)
plt.plot(crisis2_adj["base1"], label="Crisis actual", c="g",
         lw=1.3)
plt.ylabel("MÁXIMO PRE-CRISIS = 1", c="black")
plt.xlabel("DÍAS DESDE EL MÁXIMO", c="black")
plt.legend()
plt.show()

#========GRAFICO4==============================================================

plt.title("MERVAL EN U$S - CRISIS ACTUAL", fontweight="bold", fontsize=16)
plt.ylabel("U$S", fontsize=15, c="k")
plt.xlabel("AÑOS", fontsize=14, c="k")
plt.plot(merv.Merval_dlr.loc["2018-01-05":], c="indigo")
plt.annotate("CIERRE PRE-PASO",
             weight ='bold', xy=(dt.date(2019,8,9), 970), xytext=(dt.date(2019,7,6), 1100),
             arrowprops=dict(arrowstyle="->", color="k"))
plt.annotate("CIERRE POST-PASO"+"\n"+"DÓLAR +20% A $ 55",
             weight ='bold', xy=(dt.date(2019,8,12), 499), xytext=(dt.date(2019,2,6), 320),
             arrowprops=dict(arrowstyle="->", color="k"))
plt.axvline(dt.date(2018,6,7), c="k", lw=0.95, ls="--", ymax=0.7)
plt.text(dt.date(2018,5,5),1400, s="  07/06/2018 "+"\n"+"  CRÉDITO FMI")
plt.annotate("DÓLAR EN $ 25",
             weight ='bold', xy=(dt.date(2018,5,14), 1209), xytext=(dt.date(2017,12,6), 1000),
             arrowprops=dict(arrowstyle="->", color="k"))
plt.annotate("DÓLAR +10%"+"\n"+"EN DOS RUEDAS",
             weight ='bold', xy=(dt.date(2018,5,3), 1294), xytext=(dt.date(2017,12,3), 1350),
             arrowprops=dict(arrowstyle="->", color="k"))
plt.annotate("DÓLAR"+"\n"+" +$100",
             weight ='bold', xy=(dt.date(2020,4,13), 281), xytext=(dt.date(2020,3,29), 550),
             arrowprops=dict(arrowstyle="->", color="k"))
plt.axvline(dt.date(2019,12,10), c="k", lw=0.95, ls="--", ymax=0.35)
plt.text(dt.date(2019,11,5),765, s="ASUME AF")
plt.axvline(dt.date(2020,3,19), c="k", lw=0.95, ls="--", ymax=0.3)
plt.text(dt.date(2020,2,5),700, s="CUARENTENA")
plt.axvline(dt.date(2018,9,25), c="k", lw=0.95, ls="--", ymax=0.58)
plt.text(dt.date(2018,7,15),1200, s="SANDLERIS AL BCRA"+"\n"+"BANDAS CAMBIARIAS")
plt.annotate("RENUNCIA"+"\n"+" STURZENEGGER",
             weight ='bold', xy=(dt.date(2018,6,14), 1065), xytext=(dt.date(2017,12,14), 800),
             arrowprops=dict(arrowstyle="->", color="k"))
plt.annotate("  VENTAS DEL BCRA"+"\n"+" TENSIÓN CAPUTO-FMI",
             weight ='bold', xy=(dt.date(2018,7,14), 800), xytext=(dt.date(2017,11,20), 600),
             arrowprops=dict(arrowstyle="->", color="k"))
plt.annotate("DÓLAR +10% EN 3 DÍAS"+"\n"+" TASA LELIQ +70%",
             weight ='bold', xy=(dt.date(2019,4,26), 750), xytext=(dt.date(2019,1,20), 1400),
             arrowprops=dict(arrowstyle="->", color="k"))

#==============================================================================
#                   UPSIDE Y CAIDAS
#    El codigo que sigue es 99% de Juan Pablo Pisano @JohnGalt_is_www
#    tiene algunas modificaciones personales para fines puntuales
#==============================================================================
años = 10

adr = yf.download("GGAL", period = str(años)+"Y")["Adj Close"]
local = yf.download("GGAL.BA", period= str(años)+"Y")["Adj Close"]
ccl = (local*10/adr).to_frame()
ccl.columns = ["CCL"]

tickers = ["GGAL.BA", "BMA.BA", "BPAT.BA","CRES.BA", "IRSA.BA",
           "YPFD.BA", "CTIO.BA", "BHIP.BA", "EDN.BA", "PAMP.BA",
           "ALUA.BA", "TGSU2.BA", "MIRG.BA", "TRAN.BA"]

data = yf.download(tickers, period=str(años)+"Y")["Adj Close"]
dataCCL = data.div(ccl.CCL, axis=0)
dataCCL.dropna(inplace=True)

promedios = dataCCL.mean()
fechasMax_Macri = dataCCL.loc["2015-12-10":,:].idxmax()
preciosMax = dataCCL.loc["2015-12-10":,:].max()
fechasMin = dataCCL.loc["2015-12-10":,:].idxmin()
preciosHoy = dataCCL.tail(1).squeeze()
upside = ((promedios/preciosHoy-1)*100)
upside_a_max = ((preciosMax/preciosHoy-1)*100)
desdeMax = ((preciosHoy/preciosMax-1)*100)

tabla = pd.concat([fechasMax_Macri, fechasMin, preciosMax, preciosHoy, desdeMax, upside_a_max, upside], axis=1)
tabla.columns = ["Fecha px max", "Fecha px min", "Px max",
                 "Px actual", "Baja desde Max", "Suba potencial hasta max",
                 "Suba potencial hasta promedio"]

tabla = tabla.sort_values("Suba potencial hasta max", ascending=False).round(2)

print('\n', tabla)
