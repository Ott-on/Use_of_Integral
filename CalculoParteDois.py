import numpy as np
import pandas
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from prophet import Prophet

def eh_numero(texto):
        while True:
            number = input(texto)
            if number.isdigit():
                return int(number)
            else:
                print("Isso não é um número válido!\n")

def vericacao_datas(ano_inicio, ano_final):
    global ey_end, ey_start
    if(ano_inicio > ano_final):               
      ey_start = ano_final
      ey_end = ano_inicio

ey_start = 2000#max(2010, eh_numero("Defina o ano de início: "))
ew_start = 1#min(1, (eh_numero("Defina a semana de início: ")))
ey_end = 2024#max(2010, eh_numero("Defina o ano de término: "))
ew_end = 1#min(1, (eh_numero("Defina a semana de término: ")))

vericacao_datas(ey_start, ey_end)

if ew_start > 1:
    ew_start = ew_start - 1
else:
    ew_start = 53
    ey_start = ey_start - 1
    
def obter_dados(*arg):
    if len(arg) > 0:
        disease = arg[0]
    else:
        disease = "dengue"

    url = "https://info.dengue.mat.br/api/alertcity"
    geocode = 2611606
    format = "csv"

    params =(
    "&disease="
    + f"{disease}"
    + "&geocode="
    + f"{geocode}"
    + "&disease="
    + f"{disease}"
    + "&format="
    + f"{format}"
    + "&ew_start="
    + f"{ew_start}"
    + "&ew_end="
    + f"{ew_end}"
    + "&ey_start="
    + f"{ey_start}"
    + "&ey_end="
    + f"{ey_end}"
    )

    url_resp = "?".join([url, params])

    return pandas.read_csv(url_resp)

# Criar e ajustar o modelo Prophet aos dados históricos
dados = obter_dados("Dengue")
modelo = Prophet()
dados.rename(columns={'data_iniSE': 'ds', 'casos_est': 'y'}, inplace=True)
modelo.fit(dados.iloc[:,[0, 2]])

# Fazer previsões futuras para os próximos 120 dias
futuro = modelo.make_future_dataframe(periods=120, freq='W')
previsao = modelo.predict(futuro)
print(previsao)

# Plotar os resultados da previsão
fig = modelo.plot(previsao)
plt.title('Previsão de casos futuros de dengue')
plt.xlabel('Data')
plt.ylabel('Número de casos')
plt.show()