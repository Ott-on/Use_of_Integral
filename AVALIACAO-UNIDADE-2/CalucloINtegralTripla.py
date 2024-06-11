import numpy as np
from mayavi import mlab

def cylinder_density(x, y, z, radius_cm, height_cm):
    radius_m = radius_cm / 100.0  # Convertendo o raio para metros
    height_m = height_cm / 100.0  # Convertendo a altura para metros
    if np.sqrt(x**2 + y**2) <= radius_m and 0 <= z <= height_m:
        return 1.0
    else:
        return 0.0

# Solicitar entrada do usuário para altura e raio do cilindro em centímetros
try:
    height_cm = float(input("Informe a altura do cilindro em centímetros: "))
    radius_cm = float(input("Informe o raio do cilindro em centímetros: "))
except ValueError:
    print("Erro: Por favor, insira valores numéricos para a altura e o raio do cilindro.")
    exit()

# Cálculo do volume do cilindro em centímetros cúbicos
volume_cm3 = np.pi * radius_cm**2 * height_cm

x_limits = (-5, 5)  # Limites em x
y_limits = (-5, 5)  # Limites em y
z_limits = (0, height_cm)   # Limites em z

nx, ny, nz = 50, 50, 50

try:
  x = np.linspace(x_limits[0], x_limits[1], nx)
  y = np.linspace(y_limits[0], y_limits[1], ny)
  z = np.linspace(z_limits[0], z_limits[1], nz)
  X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

  density = np.vectorize(cylinder_density)(X, Y, Z, radius_cm, height_cm)

  src = mlab.pipeline.scalar_field(X, Y, Z, density)
  contours = mlab.pipeline.iso_surface(src, contours=[0.5], color=(0.7, 0.7, 1))

  # Exibir os eixos em cores especificadas (vermelho, azul e amarelo)
  mlab.axes(xlabel='Eixo X (cm)', ylabel='Eixo Y (cm)', zlabel='Eixo Z (cm)', color=(1, 0, 0))  # Cor dos eixos: vermelho, azul, amarelo

  volume_litros = volume_cm3 / 1000  # Convertendo para litros
  volume_mililitros = volume_litros * 1000  # Convertendo para mililitros

  # Exibir texto com o volume, raio e altura do cilindro em centímetros
  mlab.text(0.1, 0.8, f'Volume do Cilindro: {volume_cm3:.2f} cm³\nRaio: {radius_cm:.2f} cm\nAltura: {height_cm:.2f} cm\nVolume: {volume_litros:.2f} L\nVolume: {volume_mililitros:.2f} mL', width=0.8, line_width=2, color=(1, 1, 0))

  mlab.show()
except Exception as e:
  print("\033[91mOcorrreu um erro ao tentar gerar a visualização 3D, verifique os valores informados!!\033[0m")
  exit()