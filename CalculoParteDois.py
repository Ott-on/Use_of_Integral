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

ey_start = max(2010, eh_numero("Defina o ano de início: "))
ew_start = min(1, (eh_numero("Defina a semana de início: ")))
ey_end = max(2010, eh_numero("Defina o ano de término: "))
ew_end = min(1, (eh_numero("Defina a semana de término: ")))

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
x = np.array([i for i in range(len(dados['SE'].values))]) # intervalo de semanas
if len(x) >= 2:
  y = np.array([dados['casos_est'].values][0][::-1]) # valores do fim de cada semana

  # Calcular a integral usando a regra do trapézio
  integral = np.trapz(y, x)
else:
  print("Nao foi possivel obter a integral!")
modelo = Prophet()
dados.rename(columns={'data_iniSE': 'ds', 'casos_est': 'y'}, inplace=True)
modelo.fit(dados.iloc[:,[0, 2]])

# Fazer previsões futuras para os próximos 120 dias
futuro = modelo.make_future_dataframe(periods=120, freq='W')
previsao = modelo.predict(futuro)
print(previsao)

# Calcular a integral usando a regra do trapézio para os dados de previsão
y_previsao = previsao['yhat'].values
x_previsao = np.array([i for i in range(len(y_previsao))])
integral_previsao = np.trapz(y_previsao, x_previsao)


# Plotar os resultados da previsão
fig = modelo.plot(previsao)
plt.title('Previsão de casos futuros de dengue')
plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=0.5, wspace=0.5)
plt.gcf().set_size_inches(12, 15)
plt.xlabel('Data')
plt.ylabel('Número de casos')
plt.show()

# Mostrar valor da integral
print(f"O valor da integral da previsão é: {int(integral_previsao)}")

print(f"O quanto aumentou: {int(integral_previsao - integral)}")