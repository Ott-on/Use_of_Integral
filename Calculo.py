import numpy as np
import pandas
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import prophet

#import mplcursors

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

dados = obter_dados()
dado_auxiliar1 = obter_dados("chikungunya")

x = np.array([i for i in range(len(dados['SE'].values))]) # intervalo de semanas
if len(x) >= 2:
  y = np.array([dados['casos_est'].values][0][::-1]) # valores do fim de cada semana

  # Calcular a integral usando a regra do trapézio
  integral = np.trapz(y, x)

  print("O valor da integral é:", int(integral))
else:
  print("Nao foi possivel obter a integral!")

# adicionando os dados no gráfico
datas = dados['data_iniSE'].values[::-1]
if len(datas) >= 2:
  plt.plot(datas, y, label="dengue", color="red")
  plt.plot([dado_auxiliar1['casos_est'].values][0][::-1], label="chikungunya", color="green")

  # ajustando as legendas do gráfico
  plt.legend()
  plt.xlabel("Período")
  plt.ylabel("Casos")
  plt.gcf().autofmt_xdate() # auto formatação
  largura = plt.gcf().get_size_inches()[0] # obtem a largura do gráfico
  plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=max(1, int(len(datas) / largura * 0.8)))) # cria um intervalo entre as datas de acordo com a largura do gráfico
  plt.title('Cálculo no Estudo de Doenças')

  # exibindo o gráfico
  plt.show()
else:
  print("Não foi possivel construir o gráfico!")

# Criar e ajustar o modelo Prophet aos dados históricos
modelo = prophet.Prophet()
dados.rename(columns={'data_iniSE': 'ds', 'casos_est': 'y'}, inplace=True)
modelo.fit(dados.iloc[:,[0, 2]])

# Fazer previsões futuras para os próximos 365 dias
futuro = modelo.make_future_dataframe(periods=120, freq='W')
previsao = modelo.predict(futuro)
print(previsao)

# Plotar os resultados da previsão
fig = modelo.plot(previsao)
plt.title('Previsão de casos futuros de dengue')
plt.xlabel('Data')
plt.ylabel('Número de casos')
plt.show()

  