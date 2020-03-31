#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TITULO: Ajuste de modelos a datos
# RESUMEN: Ejemplos de cómo optimizar parámetros de un modelo para ajustar a un conjunto de datos

"""
Ejemplos para realizar ajustes de datos
Se presentan ejemplos de ajustes lineales, polinomiales y no lineales para uso general.
"""

#%%  Ejemplo de ajuste lineal simple
"""
Este es el método más rápido para hacer un ajuste lineal

El modelo a usar es:

`modelo_y = parametros[0] * modelo_x + parametros[1]`

"""
from numpy import *
import matplotlib.pyplot as plt

# Fabricamos algunos datos de ejemplo #####################
random.seed(0)

datos_x = linspace(-5,5,14)
datos_y = 2 + datos_x * 0.4  + random.normal(size=len(datos_x))/5

###########################################################


# La función polyfit permite hacer un ajuste polinomial
# El tercer parámetro es el orden del polinomio a usar como modelos
# Si vamos a hacer un ajuste linea, usamos un 1

parametros  = polyfit(datos_x,datos_y,1)

# Generamos un vector para las coordenadas x del modelo obtenido
modelo_x    = linspace(-5,5)

# Y calculasmos las coordanas Y usando los parámetros ajustados
modelo_y    = polyval( parametros , modelo_x )


# En el vector parametros están guardados los parametrso optimos hallados
# ordenados desde el mayor orden hasta el menor
print('modelo_y = parametros[0] * modelo_x + parametros[1]')

for i,parametro in enumerate(parametros):
    print('parametro' , i , ': ' , parametro)

plt.figure(1)

# modelo_y = parametros[0] * modelo_x + parametros[1]
# parametro 0 :  0.380832335273259
# parametro 1 :  2.1408751646721713

# Graficamos datos_x , datos_y 
plt.plot( datos_x, datos_y, 'o' , label='datos')
plt.plot(modelo_x,modelo_y, '-' , label='modelo' , color='red')
plt.legend()
plt.grid(True)
plt.xlabel('Eje X')
plt.ylabel('Eje Y')

# plt.savefig('repositorio_ajustes_000.png')

#%%  Ejemplo de ajuste lineal con errores
"""
Acá se incluye la posibilidad de agregar un vector de errores de medicion para 
la coordenada Y y obtener tambien el error estandar de los parametros hallados

El modelo a usar es:

`modelo_y = parametros[0] * modelo_x + parametros[1]`

"""
from numpy import *
import matplotlib.pyplot as plt

# Fabricamos algunos datos de ejemplo #####################
random.seed(0)

datos_x = linspace(-5,5,14)
datos_y = 2 + datos_x * 0.4  + random.normal(size=len(datos_x))/5
error_y = array([1.1, 1.0, 1.2, 0.8, 1.1, 0.9, 0.8, 0.9, 0.9, 1.0, 0.8, 1.2, 1.1, 0.7])

###########################################################


# La función polyfit permite hacer un ajuste polinomial
# El tercer parámetro es el orden del polinomio a usar como modelos
# Si vamos a hacer un ajuste linea, usamos un 1

# El parametro cov=True le pide a la función que, además de entregar los parámetros
# óptimos, entregue tambien la matris de covarianza de los parámetros hallados

# El parámetro w (de weight en inglés) es el peso de cada dato. Para errores
# gaussianos debe ser inversamente proporcional al error estadar de cada medición

parametros , covarianza  = polyfit( datos_x, datos_y, 1, w=1/error_y , cov=True)

# Generamos coordenadas para el modelo obtenido
modelo_x    = linspace(-5,5)
modelo_y    = polyval( parametros , modelo_x )

# El error estandar de cada parámetro es la raiz de la varianza de cada parámetro.
# Las varianzas estan en la diagonal de la matris de covarianza
# diag() extrae en un vector esa diagonal, y sqrt() calcula la raiz cuadrada

errores_parametros = sqrt( diag( covarianza ) )

# En el vector parámetros están guardados los parámetros optimos hallados
# ordenados desde el mayor orden hasta el menor
print('modelo_y = parametros[0] * modelo_x + parametros[1]')

for i,parametro in enumerate(parametros):
    print('parametro' , i , ': ' , parametro , ' ± ' , errores_parametros[i] )

plt.figure(2)

# modelo_y = parametros[0] * modelo_x + parametros[1]
# parametro 0 :  0.3766687543504051  ±  0.015266006110067724
# parametro 1 :  2.1314827167907717  ±  0.046942080829030126

# Graficamos datos_x , datos_y 
plt.errorbar( datos_x, datos_y, yerr=error_y, fmt='o' , label='datos')
plt.plot(modelo_x,modelo_y, '-' , label='modelo' , color='red')
plt.legend()
plt.grid(True)
plt.xlabel('Eje X')
plt.ylabel('Eje Y')

# plt.savefig('repositorio_ajustes_001.png')


#%%  Ejemplo de ajuste Polinomial con información estadística
"""
Ejemplo de un ajuste cuadrático (que puede ser polinomio de cualquier orden)
y de cómo extraer a información estadística del ajuste más relevante
  - Error Estandar
  - Interalos de confianza
  - r Coeficiente de Pearson
  - Rsq Coeficiente de determinación

"""
from numpy import *
import matplotlib.pyplot as plt

from scipy.stats.distributions import  t,chi2


# Fabricamos algunos datos de ejemplo #####################
random.seed(0)

datos_x = linspace(0,12,20)
datos_y = 0.25*datos_x**2  - 0.5 * datos_x + 4.2 + random.normal(size=len(datos_x))*2

###########################################################

grado_del_polinomio = 2

# Cantidad de parámetros
P = grado_del_polinomio + 1

# Número de datos
N = len(datos_x)

# Grados de libertas (Degrees Of Freedom)
dof = N-P-1

parametros , covarianza  = polyfit( datos_x, datos_y, grado_del_polinomio, cov=True)

# Cauculamos coordenadas del modelo
modelo_x    = linspace(0,12)
modelo_y    = polyval( parametros , modelo_x )

# Predicción del modelo para los datos_x medidos
prediccion_modelo = polyval(parametros,datos_x)

# Calculos de cantidades estadísticas relevantes
COV       = covarianza                                # Matriz de Covarianza
SE        = sqrt(diag( COV  ))                        # Standar Error / Error estandar de los parámetros
residuos  = datos_y - prediccion_modelo               # diferencia enrte el modelo y los datos

SSE       = sum(( residuos )**2 )                     # Resitual Sum of Squares
SST       = sum(( datos_y - mean(datos_y))**2)        # Total Sum of Squares

# http://en.wikipedia.org/wiki/Coefficient_of_determination
# Expresa el porcentaje de la varianza que logra explicar el modelos propuesto
Rsq       =  1 - SSE/SST                               # Coeficiente de determinación
Rsq_adj   = 1-(1-Rsq) * (N-1)/(N-P-1)                  # Coeficiente de determinación Ajustado   

# https://en.wikipedia.org/wiki/Pearson_correlation_coefficient#In_least_squares_regression_analysis
# Expresa la correlación que hay entre los datos y la predicción del modelo
r_pearson = corrcoef( datos_y ,  prediccion_modelo )[0,1]

# Reduced chi squared
# https://en.wikipedia.org/wiki/Reduced_chi-squared_statistic
chi2_red  = sum( residuos**2 )/(N-P)

# Chi squared test
chi2_test = sum( residuos**2 / abs(prediccion_modelo) )
# p-value del ajuste
p_val  = chi2(dof).cdf( chi2_test )


alpha=0.05

sT = t.ppf(1.0 - alpha/2.0, N - P ) # student T multiplier
CI = sT * SE

print('R-squared    ',Rsq)
print('R-sq_adjusted',Rsq_adj)
print('chi2_test    ',chi2_test)
print('r-pearson    ',r_pearson)
print('p-value      ',p_val)
print('')
print('Error Estandard (SE):')
for i in range(P):
    print('parametro[{:3d}]: '.format(i) , parametros[i], ' ± ' , SE[i])
print('')
print('Intervalo de confianza al '+str((1-alpha)*100)+'%:')
for i in range(P):
    print('parametro[{:3d}]: '.format(i) , parametros[i], ' ± ' , CI[i])


# R-squared     0.9709054284131089
# R-sq_adjusted 0.9654501962405668
# chi2_test     5.459402288696202
# r-pearson     0.9853453345975252
# p-value       0.00704534668870643
#
# Error Estandard (SE):
# parametro[  0]:  0.2592152018458697  ±  0.03181201602868888
# parametro[  1]:  -0.8001200646799337  ±  0.39545643406102493
# parametro[  2]:  6.685419630405925  ±  1.023804331399124
#
# Intervalo de confianza al 95.0%:
# parametro[  0]:  0.2592152018458697  ±  0.06711748697960664
# parametro[  1]:  -0.8001200646799337  ±  0.8343401449363104
# parametro[  2]:  6.685419630405925  ±  2.160038327038956


plt.subplot(2,1,1)
plt.plot( datos_x,  datos_y, 'o',              label='datos')
plt.plot(modelo_x, modelo_y, '-', color='red', label='modelo')

plt.legend()
plt.grid(True,linestyle='--',color='lightgray')
plt.xlabel('Eje X')
plt.ylabel('Eje Y')
plt.title('Ajuste polinomio de grado '+ str(grado_del_polinomio))

plt.subplot(2,1,2)
plt.plot( datos_x,  zeros(N),  '-', color='red', linewidth=2 )
plt.plot( datos_x,  residuos, '.-',              label='residuos')

#plt.legend()
plt.grid(True,linestyle='--',color='lightgray')
plt.xlabel('Eje X')
plt.ylabel('residuos')

plt.tight_layout()



# plt.savefig('repositorio_ajustes_002.png')
# plt.savefig('repositorio_ajustes_002_lineal.png')



