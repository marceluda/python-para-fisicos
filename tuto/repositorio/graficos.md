---
title: Gráficos (básico)
description: Gráficos (básico)
layout: page
navbar: repo
mathjax: true
---

<div class="alert alert-info" role="alert" >
  <strong>Archivo:</strong> <a href="../repositorio_01_graficos.py"> repositorio_01_graficos.py </a>
</div>
Se presentan a continuación ejemplos de gráficos de datos
incluyendo las opciones más habituales.

Para más información (en inglés) se puede consultar este completo tutorial:


<center>
<p> <a href="https://github.com/rougier/matplotlib-tutorial" class="btn btn-primary btn-lg" role="button">
matplotlib-tutorial
</a> </p>
</center>
## Ejemplo de graficos varios

Acá se muestra un ejemplo rápido para generar gráficos

![grafico](repositorio_graficos_000.png "repositorio_graficos_000.png")

<a data-toggle="collapse" href="#desplegable000" aria-expanded="false" aria-controls="desplegable000">ver código<span class="caret"></span></a>

<div id="desplegable000" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

```python

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
```
</div>


## Ejemplo de OPCIONES rapidas de graficos

Acá se muestra un ejemplo rápido para generar gráficos con OPCIONES de formato

![grafico](repositorio_graficos_001.png "repositorio_graficos_001.png")

<a data-toggle="collapse" href="#desplegable001" aria-expanded="false" aria-controls="desplegable001">ver código<span class="caret"></span></a>

<div id="desplegable001" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

```python

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
plt.errorbar(x1,y1,yerr=e1 , fmt='o',  label='datos 2' , color='C1', capsize=3)

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
```
</div>


## Ejemplo de multiples gráficos en uno

Acá se muestra un ejemplo de subplots

![grafico](repositorio_graficos_002.png "repositorio_graficos_002.png")

<a data-toggle="collapse" href="#desplegable002" aria-expanded="false" aria-controls="desplegable002">ver código<span class="caret"></span></a>

<div id="desplegable002" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

```python

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
```
</div>


## Ejemplo de multiples gráficos con semilog

Acá se muestra un ejemplo de subplots con distintas
optciones de escalas logarítmicas

![grafico](repositorio_graficos_003.png "repositorio_graficos_003.png")

<a data-toggle="collapse" href="#desplegable003" aria-expanded="false" aria-controls="desplegable003">ver código<span class="caret"></span></a>

<div id="desplegable003" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

```python

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
```
</div>


## Ejemplo de histogramas

Acá se muestran ejemplos de gráficos de histogramas

![grafico](repositorio_graficos_004.png "repositorio_graficos_004.png")

<a data-toggle="collapse" href="#desplegable004" aria-expanded="false" aria-controls="desplegable004">ver código<span class="caret"></span></a>

<div id="desplegable004" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

```python

from numpy import *
import matplotlib.pyplot as plt

# Fabricamos algunos datos de ejemplo #####################
random.seed(0)

# Creamos un vector de datos simulados:
#   Una distribución normal centrada en 10, con desviación estándar de 2.5
#   y tamaño muestral de 300
datos1 = random.normal(loc=10,scale=2.5, size=400)

# Creo otro vector de datos para comparación
datos2 = random.normal(loc=10,scale=5, size=400)

plt.figure(9)

plt.subplot(2,2,1)
plt.hist( datos1 )
plt.xlabel('valores')
plt.ylabel('apariciones')
plt.title('10 bines')

plt.subplot(2,2,2)
# ancho de bin óptimo: 
#    https://en.wikipedia.org/wiki/Freedman%E2%80%93Diaconis_rule
iqr = diff(percentile(datos1, [25 ,75]))[0]
ancho_de_bin = 2*iqr/(len(datos1)**(1/3))
n_bines = round( (datos1.max()-datos1.min())/ancho_de_bin  )
plt.hist( datos1 , density=True, bins=n_bines)
plt.xlabel('valores')
plt.ylabel('frecuencia')
plt.title(f'{n_bines} bines')


plt.subplot(2,2,3)
rango = linspace(-5,24,21)
plt.hist( datos1 , density=True, bins=rango, alpha=0.7)
plt.hist( datos2 , density=True, bins=rango, alpha=0.7)
plt.xlabel('valores')
plt.ylabel('frecuencia')
plt.title('Dos histogramas')

plt.subplot(2,2,4)
plt.hist( datos1 , density=True, cumulative=True, histtype='step', lw=3)
plt.hist( datos2 , density=True, cumulative=True, histtype='step', lw=3)
plt.xlabel('valores')
plt.ylabel('Acumulado [%]')
plt.title('Acumulado')
plt.grid()

plt.tight_layout()

# plt.savefig('repositorio_graficos_004.png')
```
</div>

