---
title: Ajuste no lineal
description: Ajuste de datos a funciones arbitrarias
layout: page
mathjax: true
navbar: analisis
---


{% include page_navbar.html %}

<div class="alert alert-danger" role="alert" >
  <strong>Aviso:</strong> La página está en construcción.
</div>

Los ejemplos de tratados aquí se pueden descargar de:
https://github.com/marceluda/python-para-fisicos/tree/master/tutoriales/analisis

Vamos a ver ejemplos de ajuste no lineal con diferentes funciones del paquete
de `scipy.optimize`.

## Armamos una serie de datos

El código a continuación tiene los `import` necesarios para usar las funciones
de ajuste no lineal. Generamos dos tiras de datos que simularán ser el resultado
de mediciones o relevamientos.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit,least_squares

x_datos  = np.linspace(0, 10, 100)
y_exacto = np.exp(-(x_datos-2.8)**2/0.5**2)+np.exp(-(x_datos-4.8)**2/1.5**2)

# Pare comparar después, Parámetros en orden de aparición:
parametros_reales = [2.8, 0.5, 4.8, 1.5]

# agregamos ruido
np.random.seed(1729)
y_ruido = 0.05 * np.random.normal(size=x_datos.size)
y_datos = y_exacto + y_ruido


# Graficamos

plt.figure()
plt.plot(x_datos,  y_datos, 'o', label='datos medidos')
plt.plot(x_datos, y_exacto, '-', label='curva exacta')
plt.legend(loc='best')
plt.xlabel('x')
plt.ylabel('y')
plt.tight_layout()
```
![Datos fabricados](datos-originales.png "Datos fabricados")



{% include page_navbar.html up=1 %}
