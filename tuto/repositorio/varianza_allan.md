---
title: Varianza de Allan con allantools
description: Varianza de Allan con allantools
layout: page
navbar: repo
mathjax: true
---

<div class="alert alert-info" role="alert" >
  <strong>Archivo:</strong> <a href="../repositorio_04_varianza_allan.py"> repositorio_04_varianza_allan.py </a>
</div>

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

