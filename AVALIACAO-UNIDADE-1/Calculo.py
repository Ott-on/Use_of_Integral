import numpy as np
import pandas

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def eh_numero(texto):
  while True:
    number = input(texto)
    if number.isdigit():
      return int(number)
    else:
      print("Isso não é um número válido!\n")

def vericacao_datas(ano_inicio, ano_final):
  global ey_end, ey_start
  if ano_inicio > ano_final:
    ey_start = ano_final
    ey_end = ano_inicio

ey_start = max(2010, eh_numero("Defina o ano de início: "))
ew_start = max(1, (eh_numero("Defina a semana de início: ")))
ey_end = max(2010, eh_numero("Defina o ano de término: "))
ew_end = max(1, (eh_numero("Defina a semana de término: ")))

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

  params = (
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

# Dados data 2023 semana inicial 1 e semana final 14 ano final 2024
# data_iniSE      SE  casos_est  casos_est_min  casos_est_max  ...  casprov_est  casprov_est_min  casprov_est_max  casconf  notif_accum_year
# 0    2024-06-02  202423      385.0            182            865  ...          NaN              NaN              NaN      NaN            179137
# 1    2024-05-26  202422      374.5            249            622  ...          NaN              NaN              NaN      NaN            179137
# 2    2024-05-19  202421      358.5            265            537  ...          NaN              NaN              NaN      NaN            179137
# 3    2024-05-12  202420      366.0            292            495  ...          NaN              NaN              NaN      NaN            179137
# 4    2024-05-05  202419      335.0            288            410  ...          NaN              NaN              NaN      NaN            179137

x = np.array([i for i in range(len(dados['SE'].values))])  # intervalo de semanas
if len(x) >= 2:
  y = np.array([dados['casos_est'].values][0][::-1])  # valores do fim de cada semana

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
  plt.gcf().autofmt_xdate()  # auto formatação
  largura = plt.gcf().get_size_inches()[0]  # obtem a largura do gráfico
  plt.gca().xaxis.set_major_locator(
    mdates.DayLocator(interval=max(1, int(len(datas) / largura * 0.8)))
  )  # cria um intervalo entre as datas de acordo com a largura do gráfico
  plt.title("Cálculo no Estudo de Doenças")

  # exibindo o gráfico
  plt.show()
else:
  print("Não foi possivel construir o gráfico!")


def calcular_integral_dupla(f, a, b, c, d, nx, ny):
  dx = (b - a) / nx
  dy = (d - c) / ny
  integral = 0

  for i in range(nx):
    for j in range(ny):
      x = a + i * dx
      y = c + j * dy
      integral += f(x, y) * dx * dy

  return integral


def f(x, y):
  return x ** 2 + y ** 2


a = 0
b = 1
c = 0
d = 1
nx = 100
ny = 100

double_integral = calcular_integral_dupla(f, a, b, c, d, nx, ny)
print("O valor da integral dupla é:", double_integral)
