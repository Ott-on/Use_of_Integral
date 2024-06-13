import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import scipy

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

def obter_dados(region, disease="dengue"):
    url = "https://info.dengue.mat.br/api/alertcity"
    geocode = region
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

    return pd.read_csv(url_resp)

# Geocodes para, Jaboatão e Recife
regions = [2607901, 2611606]
region_names = ["Jaboatão dos Guararapes", "Recife"]
dados_regions = {region: obter_dados(region) for region in regions}

# Extraindo semanas e casos para cada região
weeks = np.array([i for i in range(len(next(iter(dados_regions.values()))['SE'].values))])

if len(weeks) >= 2:
    cases_per_region = {}
    for region in regions:
        dados = dados_regions[region]
        cases_per_region[region] = np.array(dados['casos_est'].values[::-1])

    # calculo da diferença de casos a partir da integral
    integral_diferenca = abs(np.trapz(cases_per_region[2607901], weeks) - np.trapz(cases_per_region[2611606], weeks))

    print("O valor da integral dupla é:", int(integral_diferenca))

    # Plotando os dados com preenchimento de área
    plt.figure(figsize=(10, 6))
    for i, region in enumerate(regions):
        dates = pd.to_datetime(dados_regions[region]['data_iniSE'].values[::-1])
        cases = cases_per_region[region]
        plt.plot(dates, cases, label=region_names[i])
        plt.fill_between(dates, cases, alpha=0.3)

    plt.legend()
    plt.xlabel("Período")
    plt.ylabel("Casos")
    plt.gcf().autofmt_xdate()
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.title("Cálculo de Casos em Diferentes Regiões")
    plt.show()
else:
    print("Não foi possível obter a integral!")
