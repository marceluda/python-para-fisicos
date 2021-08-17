#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estructuras de programación básicas y alguans referencias para 
empezar a programar pronto

Basado en:
https://marceluda.github.io/python-para-fisicos/tuto/labo2/01_intro_python/
"""


import time

from matplotlib import pyplot as plt
import numpy as np


print(__doc__)



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Guardar datos en un archivo NPZ (de NumPy)
"""
Guardar datos en un archivo NPZ (de NumPy)
"""

# Generamos datos de prueba
xx = np.linspace(0,10,1000)
yy = ( 1+np.sin(xx*5) ) * ( 1 + xx**2 )

# plt.plot(xx,yy)

# los guardamos
np.savez('datos_de_ejemplo.npz' , xx=xx , yy=yy )


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Carga de datos desde un archivo NPZ (de NumPy)
"""
Cargar datos desde un archivo NPZ
"""

datos=np.load('datos_de_ejemplo.npz', allow_pickle=True)

# items que hay en el archivo abierto
print('contenido del archivo')
for item in datos.keys():
    print(f'{item}: {type(datos[item])} de largo {len(datos[item])}')

xx = datos['xx']
yy = datos['yy']


plt.plot(xx,yy)
plt.xlabel('xx')
plt.ylabel('yy')
plt.grid(True)





#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Guardar datos en un archivo CSV
"""
Guardar datos en un archivo CSV
"""

# Generamos datos de prueba
xx = np.linspace(0,10,1000)
yy = ( 1+np.sin(xx*5) ) * ( 1 + xx**2 )


# los guardamos

np.savetxt('datos_de_ejemplo.csv', np.array([xx,yy]).T , delimiter="," , header='xx,yy')

# La expresión: array([ ACA VAN LOS VECTORES SEPARADOS POR COMAS  ]).T
# Es necesaria para que los datos se exporten como columnas

np.savetxt('datos_de_ejemplo2.csv', np.array([xx,yy]).T , delimiter="\t" , header='xx yy', fmt='%5f')

# En esta segunda version, la separación son TABs y el formato numérico es mas corto



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Carga de datos desde CSV
"""
Cargar datos desde un archivo CSV u otro archivo de texto plano
"""

# Cargamos los datos completos en una matris
DATOS_todos = np.genfromtxt('datos_de_ejemplo.csv', delimiter=',' )

# Extraemos cada columna por separado en un vector
datos_columna0 = DATOS_todos[:,0]
datos_columna1 = DATOS_todos[:,1]

# graficamos
plt.figure()
plt.errorbar( datos_columna0 , datos_columna1   )
plt.xlabel('Eje X')
plt.ylabel('Eje Y')









#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Guardar datos en un archivo .mat de MATLAB
"""
Guardar datos en un archivo .mat de MATLAB
"""

from scipy.io import savemat


# Generamos datos de prueba
xx = np.linspace(0,10,1000)
yy = ( 1+np.sin(xx*5) ) * ( 1 + xx**2 )

# plt.plot(xx,yy)

# los guardamos
savemat('datos_de_ejemplo.mat' , { 'xx': xx , 'yy': yy }  )

# Los datos son guardados a partir de un diccionario
#  - los keys del diccionario van a ser los nombres de las variables en el archivo .mat
#  - los contenidos, los vectores correspondientes a cada variable


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Carga de datos desde un archivo .mat de matlab
"""
Cargar datos desde un archivo .mat de MATLAB
"""

from scipy.io import loadmat

# Importamos los datos del archivo
datos = loadmat('datos_de_ejemplo.mat')

# Veamos qué variables fueron guardadas en el archivo:
print('contenido del archivo:')
for item in datos.keys():
    print(f'{item}: {type(datos[item])} de largo {len(datos[item])}')

# Los datos estan en forma de matriz columna
print(f"datos['xx'].shape : {datos['xx'].shape}")

# Con flatten los pasamos a vector sinple (sin matriz)
tt  = datos['xx'].flatten()
yy  = datos['yy'].flatten()



plt.plot( tt , yy , label='canal 1')

plt.xlabel('tiempo [s]')
plt.ylabel('canales osciloscopio [V]')
plt.legend()
plt.grid(True)







#%%  Carga de datos desde un excel
"""
Cargar datos desde un archivo tipo excel
"""
from numpy import *
import matplotlib.pyplot as plt
import pandas as pd  # solo lo vamos a usar para leer EXCEL

datos = pd.read_excel('dolar.xlsx', sheet_name=0)

# Veamos cuales son las columnas:
print(datos.columns.tolist())


fecha = datos['Fecha']
dolar = datos['Dolar']

plt.plot( fecha , dolar )
plt.xlabel('fecha')
plt.ylabel('dolar [$]')
plt.grid(True)









