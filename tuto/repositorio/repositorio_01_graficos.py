#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TITULO: Gráficos (básico)
# RESUMEN: Ejemplos para graficar datos de forma rápida

"""
Se presentan a continuación ejemplos de graficación de datos
incluyendo las opciones más habituales.
"""

#%%  Ejemplo de graficos varios
"""
Acá se muestra un ejemplo rápido para generar gráficos
"""
from numpy import *
import matplotlib.pyplot as plt

# Fabricamos algunos datos de ejemplo #####################
random.seed(0)

x0 = linspace(0,10,1000)
y0 = ( 2+sin(x0*5) ) * ( 1 + x0**2 )

x1 = arange(10)
y1 = 100 - x1 * 15.5 + random.normal(size=10)*8
e1 = 20+random.normal(size=10).round(1)

x2 = arange(10)
y2 = exp(x2)/8000*200 +20
###########################################################

# Creamos la figura 1
plt.figure(1)

# Graficamos x0 , y0 con el formato por defecto (una línea)
plt.plot(x0,y0)

# Graficamos x1, y1 considerando errores +-e1
plt.errorbar(x1,y1,yerr=e1)

# Graficamos x2 , y2 con bolitas
plt.plot(x2,y2,'o')

# plt.savefig('repositorio_graficos_000.png')


#%%  Ejemplo de OPCIONES rapidas de graficos
"""
Acá se muestra un ejemplo rápido para generar gráficos con OPCIONES de formato
"""
from numpy import *
import matplotlib.pyplot as plt

# Fabricamos algunos datos de ejemplo #####################
random.seed(0)

x0 = linspace(0,10,1000)
y0 = ( 2+sin(x0*5) ) * ( 1 + x0**2 )

x1 = arange(10)
y1 = 100 - x1 * 15.5 + random.normal(size=10)*8
e1 = 20+random.normal(size=10).round(1)

x2 = arange(10)
y2 = exp(x2)/8000*200 +20
###########################################################

# Creamos la figura 2
plt.figure(2)

# Graficamos x0 , y0 con el formato por defecto (una línea)
plt.plot(x0,y0, '-' ,  label='datos 1' , color='blue' )

# Graficamos x1, y1 considerando errores +-e1
plt.errorbar(x1,y1,yerr=e1 , fmt='o',  label='datos 2' , color='C1')

# Graficamos x2 , y2 con bolitas
plt.plot(x2,y2,'.-',  label='datos 3' , color='red' , alpha=0.5)

# Graficar las leyendas de los datos (los textos de los parametros 'label')
plt.legend()

# Agregamos una grilla de referencia
plt.grid(True)

# Etiquetas para los Ejes
plt.xlabel('Eje X')
plt.ylabel('Eje Y')

# Título
plt.title('Título')

# plt.savefig('repositorio_graficos_001.png')


#%%  Ejemplo de multiples gráficos en uno
"""
Acá se muestra un ejemplo de subplots
"""
from numpy import *
import matplotlib.pyplot as plt

# Fabricamos algunos datos de ejemplo #####################
random.seed(0)

x0 = linspace(0,10,1000)
y0 = ( 2+sin(x0*5) ) * ( 1 + x0**2 )

x1 = arange(10)
y1 = 100 - x1 * 15.5 + random.normal(size=10)*8
e1 = 20+random.normal(size=10).round(1)

x2 = arange(10)
y2 = exp(x2)/8000*200 +20
###########################################################

# Creamos la figura 3
plt.figure(3)

# plt.subplot tiene la siguiente sintaxys:
# plt.subplot( numero_de_filas , numero_de_columnas , indice_del_grafico_actual )

plt.subplot(3,1,1)
plt.plot(x0,y0 )
plt.title('Titulo del primer grafico')
plt.ylabel('Datos 1 [V]')
plt.xlabel('Eje X1')
plt.ylim(-50,200)  # Ejemplo de como especificar los límites del eje Y
plt.xticks( [0,1,2,3,4,5,6,7,8,9,10] )  # Especificar lines de la grilla en X


plt.subplot(3,1,2)
plt.errorbar(x1,y1,yerr=e1 , fmt='o')
plt.ylabel('Datos 2 [V]')
plt.xlabel('Eje X2')
plt.xticks( [0,3,6, 9] , ['cero', 'tres' , 'seis', 'nueve'] )  # Especificar lines de la grilla en X


plt.subplot(3,1,3)
plt.plot(x2,y2,'.-')
plt.ylabel('Datos 3 [V]')
plt.xlabel('Eje X3')
plt.grid(True)
plt.xlim(5.5,9.5)  # Ejemplo de como especificar los límites del eje X

# Etiquetas para los Ejes

plt.tight_layout()

# plt.savefig('repositorio_graficos_002.png')


#%%  Ejemplo de multiples gráficos con semilog
"""
Acá se muestra un ejemplo de subplots con distintas
optciones de escalas logarítmicas
"""
from numpy import *
import matplotlib.pyplot as plt

# Fabricamos algunos datos de ejemplo #####################
random.seed(0)

x0 = linspace(0,1e5,30000)
y0 = ( 1+1e-4+sin(x0/50 * exp(-x0/10000) ) ) * exp(-x0/10000) 
y1 = 2*exp(-x0/10000) 


plt.figure(8)

plt.subplot(2,2,1)
plt.plot(x0,y0)
plt.plot(x0,y1)
plt.grid(True)
plt.grid(which='minor', alpha=0.2)
plt.title('Escala lineal')

plt.subplot(2,2,2)
plt.plot(x0,y0)
plt.plot(x0,y1)
plt.semilogx()
plt.grid(True)
plt.grid(which='minor', alpha=0.2)
plt.title('semilog X')


plt.subplot(2,2,3)
plt.plot(x0,y0)
plt.plot(x0,y1)
plt.semilogy()
plt.grid(True)
plt.grid(which='minor', alpha=0.2)
plt.title('semilog Y')


plt.subplot(2,2,4)
plt.plot(x0,y0)
plt.plot(x0,y1)
plt.semilogx()
plt.semilogy()
plt.grid(True)
plt.grid(which='minor', alpha=0.2)
plt.title('log X y log Y')

plt.tight_layout()

# plt.savefig('repositorio_graficos_003.png')

