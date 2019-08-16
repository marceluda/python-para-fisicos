---
title: Ejemplos para realizar ajustes de datos
description: Ejemplos para realizar ajustes de datos
layout: page
navbar: repo
mathjax: true
---




<div class="alert alert-danger" role="alert" >
  <strong>Aviso:</strong> La página está en construcción.
</div>

<div class="alert alert-info" role="alert" >
  <strong>Archivo:</strong> <a href="../repo_tutos_ajustes.py"> repo_tutos_ajustes.py </a>
</div>



Se presentan ejemplos de ajustes lineales, polinomiales y no lineales para uso general.

## Ejemplo de ajuste lineal simple

Este es el método más rápido para hacer un ajuste lineal

El modelo a usar es:

modelo_y = parametros[0] * modelo_x + parametros[1]


![grafico](../repo_tutos_ajustes_000.png "repo_tutos_ajustes_000.png")

<a data-toggle="collapse" href="#desplegable000" aria-expanded="false" aria-controls="desplegable000">ver código<span class="caret"></span></a>

<div id="desplegable000" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

```python
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

# plt.savefig('repo_tutos_ajustes_000.png')


```
</div>


## Ejemplo de ajuste lineal con errores

Acá se incluye la posibilidad de agregar un vector de errores de medicion para 
la coordenada Y y obtener tambien el error estandar de los parametros hallados

El modelo a usar es:

modelo_y = parametros[0] * modelo_x + parametros[1]


![grafico](../repo_tutos_ajustes_001.png "repo_tutos_ajustes_001.png")

<a data-toggle="collapse" href="#desplegable001" aria-expanded="false" aria-controls="desplegable001">ver código<span class="caret"></span></a>

<div id="desplegable001" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

```python
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

# plt.savefig('repo_tutos_ajustes_001.png')
```
</div>


