import scipy.integrate as integrate
import numpy as np

# Informar ao usuário sobre a unidade de medida esperada
print("Por favor, insira o raio e a altura do cilindro em centímetros (cm).")

# Solicitar ao usuário para inserir o raio e a altura do cilindro
R = float(input("Digite o raio do cilindro: "))  # Raio em cm
h = float(input("Digite a altura do cilindro: "))  # Altura em cm

# Função a ser integrada
def integrand(r, theta, z):
    return r

# Executar a integração tripla
volume, error = integrate.tplquad(integrand,
                                  0, h,        # Limites para z
                                  lambda z: 0, lambda z: 2*np.pi,  # Limites para theta
                                  lambda z, theta: 0, lambda z, theta: R)  # Limites para r

# Formatar o volume para mostrar no máximo dois dígitos após a vírgula
volume_formatado = f"{volume:.2f}"

# Imprimir o volume calculado com formatação
print(f"Volume do cilindro com raio {R} cm e altura {h} cm é: {volume_formatado} cm³")