import scipy.integrate as integrate
import numpy as np

# Informar ao usuário sobre a unidade de medida esperada
print("Por favor, insira o raio e a altura do inseticida em centímetros (cm).")

try:
    h = float(input("Informe a altura do inseticida em centímetros: "))
    R = float(input("Informe o raio do inseticida em centímetros: "))
except ValueError:
    print("Erro: Por favor, insira valores numéricos para a altura e o raio do inseticida.")
    exit()

# Função a ser integrada
def integrand(r, theta, z):
    return r

# Executar a integração tripla
volume, error = integrate.tplquad(integrand, 
                                  0, h,        # Limites para z
                                  lambda z: 0, lambda z: 2*np.pi,  # Limites para theta
                                  lambda z, theta: 0, lambda z, theta: R)  # Limites para r

volume_litros = volume / 1000  # Convertendo para litros
volume_mililitros = volume_litros * 1000  # Convertendo para mililitros

# Imprimir o volume calculado com formatação
print(f'Volume do inseticida: {volume:.2f} cm³\nRaio: {R:.2f} cm\nAltura: {h:.2f} cm\nVolume: {volume_litros:.2f} L\nVolume: {volume_mililitros:.2f} mL')
