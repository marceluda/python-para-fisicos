#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TITULO: Cargar y guardar datos
# RESUMEN: Ejemplos leer/importar datos desde varios formatos y guardar/exportar a varios formatos


"""
En este archivo se muestran ejemplos prácticos para leer datos desde 
diferentes formatos de archivos y para guardarlos en diferentes formatos.
"""

#%%  Carga de datos a mano
"""
Cargar datos a mano
"""

from numpy import *
import matplotlib.pyplot as plt

datos_x1  = arange(0,100,5)
datos_y1  = [-2.02, -0.16, 1.76, 0.28, 0.37, 1.83, 2.92, 2.11,
              3.06,  2.36, 0.57, 5.16, 4.64, 4.4 , 7.44, 4.48, 
              5.22,  6.2,  5.7, 6.64]


datos_x2 = linspace(15,80,10)
datos_y2 = array([0.7, 1.06, 0.35, 0.1, 1.6, 2.73, 1.22, 1.16, 3.58, 2.52] )

plt.figure()
plt.plot(datos_x1, datos_y1, 'o-')
plt.plot(datos_x2, datos_y2, '.-')
plt.xlabel('Eje X')
plt.ylabel('Eje Y')

#%%  Carga de datos desde CSV
"""
Cargar datos desde un archivo CSV u otro archivo de texto plano
"""
from numpy import *
import matplotlib.pyplot as plt

# Cargamos los datos completos en una matris
DATOS_todos = genfromtxt('decaimiento.csv', delimiter=',' )

# El parámetro 'delimiter' nos dice cual es el separador entre columnas
# Si el separador entre columnas es un espacio va ' ' y si es un TAB va '\t'

# Extraemos cada columna por separado en un vector
datos_columna0 = DATOS_todos[:,0]
datos_columna1 = DATOS_todos[:,1]
datos_columna2 = DATOS_todos[:,2]


# graficamos
plt.figure()
plt.errorbar( datos_columna0 , datos_columna1 , yerr=datos_columna2   )
plt.xlabel('Eje X')
plt.ylabel('Eje Y')



#%%  Carga de datos desde un excel
"""
Cargar datos desde un archivo tipo excel
"""
from numpy import *
import matplotlib.pyplot as plt
import pandas as pd  # solo lo vamos a usar para leer EXCEL

datos = pd.read_excel('dolar.xlsx', sheetname=0)

# Veamos cuales son las columnas:
print(datos.columns.tolist())


fecha = datos['Fecha']
dolar = datos['Dolar']

plt.plot( fecha , dolar )
plt.xlabel('fecha')
plt.ylabel('dolar [$]')
plt.grid(True)

#%% Carga de datos desde un archivo .mat de matlab
"""
Cargar datos desde un archivo .mat de MATLAB
"""
from numpy import *
import matplotlib.pyplot as plt
from scipy.io import loadmat

# Importamos los datos del archivo
datos = loadmat('archivo_matlab.mat')

# Veamos qué variables fueron guardadas en el archivo:
for nombre_variable in datos.keys():
    print(nombre_variable)

tt  = datos['tt']
ch2 = datos['ch2']
ch3 = datos['ch3']



plt.plot( tt , ch2 , label='canal 1')
plt.plot( tt , ch3 , label='canal 2' )

plt.xlabel('tiempo [s]')
plt.ylabel('canales osciloscopio [V]')
plt.legend()
plt.grid(True)


#%% Carga de datos desde un archivo NPZ (de NumPy)
"""
Cargar datos desde un archivo NPZ
"""

from numpy import *
import matplotlib.pyplot as plt

# Generamos datos de prueba

datos=load('datos_de_ejemplo.npz', allow_pickle=True)


for item in datos.keys():
    print(item)

xx = datos['xx']
yy = datos['yy']


plt.plot(xx,yy)
plt.xlabel('xx')
plt.ylabel('yy')
plt.grid(True)


#%% Guardar datos en un archivo NPZ (de NumPy)
"""
Guardar datos en un archivo NPZ (de NumPy)
"""
from numpy import *
import matplotlib.pyplot as plt

# Generamos datos de prueba
xx = linspace(0,10,1000)
yy = ( 1+sin(xx*5) ) * ( 1 + xx**2 )

# plt.plot(xx,yy)

# los guardamos
savez('datos_de_ejemplo.npz' , xx=xx , yy=yy )


#%% Guardar datos en un archivo CSV
"""
Guardar datos en un archivo CSV
"""
from numpy import *
import matplotlib.pyplot as plt

# Generamos datos de prueba
xx = linspace(0,10,1000)
yy = ( 1+sin(xx*5) ) * ( 1 + xx**2 )

# plt.plot(xx,yy)

# los guardamos

savetxt('datos_de_ejemplo.csv', array([xx,yy]).T , delimiter="," , header='xx,yy')

# La expresión: array([ ACA VAN LOS VECTORES SEPARADOS POR COMAS  ]).T
# Es necesaria para que los datos se exporten como columnas

savetxt('datos_de_ejemplo2.csv', array([xx,yy]).T , delimiter="\t" , header='xx yy', fmt='%5f')

# En esta segunda version, la separación son TABs y el formato numérico es mas corto


#%% Guardar datos en un archivo .mat de MATLAB
"""
Guardar datos en un archivo .mat de MATLAB
"""
from numpy import *
import matplotlib.pyplot as plt
from scipy.io import savemat


# Generamos datos de prueba
xx = linspace(0,10,1000)
yy = ( 1+sin(xx*5) ) * ( 1 + xx**2 )

# plt.plot(xx,yy)

# los guardamos
savemat('datos_de_ejemplo.mat' , { 'xx': xx , 'yy': yy }  )

# Los datos son guardados a partir de un diccionario
#  - los keys del diccionario van a ser los nombres de las variables en el archivo .mat
#  - los contenidos, los vectores correspondientes a cada variable

