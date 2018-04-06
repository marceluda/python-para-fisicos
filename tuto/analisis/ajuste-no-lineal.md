---
title: Ajuste no lineal
description: Ajuste de datos a funciones arbitrarias
layout: page
mathjax: true
navbar: analisis
---

{% include page_navbar.html %}


$$
\definecolor{var}{RGB}{199,37,78}
$$


<div class="alert alert-danger" role="alert" >
  <strong>Aviso:</strong> La página está en construcción.
</div>

Los ejemplos de tratados aquí se pueden descargar de:

<center>
<a href="https://github.com/marceluda/python-para-fisicos/tree/master/tutoriales/analisis" class="btn btn-primary btn-lg" role="button">
GitHub python-para-fisicos/as
</a>
</center>

Vamos a ver ejemplos de ajuste no lineal con diferentes funciones del paquete
de `scipy.optimize`.

## Armamos una serie de datos

El código a continuación tiene los `import` necesarios para usar las funciones
de ajuste no lineal. Generamos dos tiras de datos que simularán ser el resultado
de mediciones o relevamientos: `x_datos` e `y_datos`.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit,least_squares

x_datos  = np.linspace(0, 10, 100)
y_exacto = np.exp(-(x_datos-2.8)**2/0.5**2)+np.exp(-(x_datos-4.8)**2/1.5**2)

# Para comparar después, Parámetros en orden de aparición:
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
![Datos fabricados](datos-originales.png "Datos fabricados"){:style="width: 80%;"}

## Ajuste de modelos

El objetivo de hacer un ajuste es encontrar los parámetros óptimos de un modelo
determinado que para que los valores que predice el modelo sean lo **"más parecidos
posible a los datos"**. Esto último es un criterio subjetivo que debe ser formalizado
para poder hallar el óptimo en términos matemáticos. La forma más usual de hacerlo
es por **cuadrados mínimos** (en inglés: *least squares*).

El procedimiento es el siguiente.
Contamos con dos vectores `x_datos` e `y_datos` con la información de nuestras
mediciones.

Definimos una función modelo que creemos que describe el fenómeno medido.
Esta función tiene como argumento de entrada los valores de `x` y como salida
una predicción para valores de `y`. A su vez, depende de parámetros. Por ejemplo:


$$
f_{a,b,c,d}(x) = e^{-\frac{(x-a)^2}{b^2}} + e^{-\frac{(x-c)^2}{d^2}}
$$

Luego, se define un criterio de optimización. En el caso de cuadrados mínimos
el criterio es **"minimizar la suma cuadrática de los residuos"**. Esto es:


$$
{\color{var}\texttt{residuos}} = f_{a,b,c,d}({\color{var}\texttt{x_datos}}) - {\color{var}\texttt{y_datos}}
$$

Se busca optimizar:

$$
\min_{a,b,c,d} \sum_i {\color{var}\texttt{residuos}}[i]^2
$$

Esto es cuadrados mínimos. Un algoritmo se encargará de ir porbando diferentes valores
para los parámetros, variándolos en la dirección en que los residuos se minimicen.

Al hallar el mínimo se encuentran los parámetros óptimos.

## Ajustamos un modelo usando `curve_fit`

  1. **Definimos un modelo**. Es una función, cuyo primer argumento son los valores
    del eje x y el resto de los argumentos son los parámetros a hallar.
  1. Luego definimos los **parámetros iniciales** desde donde arranca el proceso
    de optimización.
  1. **Ejecutamos `curve_fit`**
  1. Graficamos

```python
from scipy.optimize import curve_fit

def modelo(x, a, b, c, d):
    return np.exp(-(x-a)**2/b**2)+np.exp(-(x-c)**2/d**2)

# Parámetros iniciales con los que vamos a iniciar el proceso de fiteo
parametros_iniciales=[2, 1, 6, 1]

# Hacemos el ajuste con curve_fit
popt, pcov = curve_fit(modelo, x_datos, y_datos, p0=parametros_iniciales)

# curve_fit devuelve dos resultados. El primero (popt) son los
# parámetros óptimos hallados. El segundo (pcov) es la matriz de
# covarianza de los parámetros hallados.

x_modelo  = np.linspace(0, 10, 1000)

plt.figure()
plt.plot( x_datos,                 y_datos,  'o', label='datos')
plt.plot(x_modelo, modelo(x_modelo, *popt), 'r-', label='modelo ajustado')
plt.legend(loc='best')
plt.xlabel('x')
plt.ylabel('y')
plt.tight_layout()
```

![ajuste curve_fit](ajuste-con-curve_fit.png "Ajuste con curve_fit"){:style="width: 80%;"}

Imprimimos los parámetros hallados:
```python
print(popt)
# [ 2.82275337  0.51624571  4.8432543   1.48437521]
# De la matris de covarinza podemos obtener los valores de desviacion estandar
# de los parametros hallados
pstd = np.sqrt(np.diag(pcov))

nombres_de_param=['a','b','c','d']
print('Parámetros hallados:')
for i,param in enumerate(popt):
    print('{:s} = {:5.3f} ± {:5.3f}'.format( nombres_de_param[i] , param , pstd[i]/2) )
#
# Parámetros hallados:
#
# a = 2.823 ± 0.006
# b = 0.516 ± 0.009
# c = 4.843 ± 0.011
# d = 1.484 ± 0.014
```

## Ajustamos un modelo usando `least_squares`: mayor control del proceso
Para tener un control más riguroso del proceso de optimización se puede utilizar
la función de `least_squares`.

  1. Definimos un modelo. Es una función, cuyo primer argumento son los valores
    del eje x y el resto de los argumentos son los parámetros a hallar.
  1. Definimos una **función para los residuos**. Esta función será la optimizada, y
    deberá llamar constantemente a la función del modelo. `curve_fit` basicamente
    utiliza `least_squares` para optimizar la funcion de residuos `residuos = modelo(x_datos) - y_datos`.
  1. Luego definimos los parámetros iniciales desde donde arranca el proceso
    de optimización.
  1. Ejecutamos `curve_fit`
  1. Graficamos

```python

from scipy.optimize import least_squares

def modelo(p,x):
    # p es un vector con los parámetros
    # x es el vector de datos x
    return np.exp(-(x-p[0])**2/p[1]**2)+np.exp(-(x-p[2])**2/p[3]**2)

def residuos(p, x, y):
    # p es un vector con los parámetros
    # x es el vector de datos x
    # y es el vector de datos y
    y_modelo = modelo(p, x)
    plt.clf()
    plt.plot(x,y,'o',x,y_modelo,'r-')
    plt.pause(0.05)
    return y_modelo - y



parametros_iniciales=[2, 1, 6, 1]
res = least_squares(residuos, parametros_iniciales, args=(x_datos, y_datos), verbose=1)


# Estos son los parámetros hallados
res.x


# Calculamos la matris de covarianza
# https://stackoverflow.com/questions/40187517/getting-covariance-matrix-of-fitted-parameters-from-scipy-optimize-least-squares

def calcular_cov(res,y_datos):
    U, S, V = np.linalg.svd(res.jac, full_matrices=False)
    threshold = np.finfo(float).eps * max(res.jac.shape) * S[0]
    S = S[S > threshold]
    V = V[:S.size]
    pcov = np.dot(V.T / S**2, V)

    s_sq = 2 * res.cost / (y_datos.size - res.x.size)
    pcov = pcov * s_sq
    return pcov


pcov = calcular_cov(res,y_datos)

# De la matris de covarinza podemos obtener los valores de desviacion estandar
# de los parametrso hallados
pstd = np.sqrt(np.diag(pcov))

print('Parámetros hallados:')
for i,param in enumerate(res.x):
    print('parametro[{:d}]: {:5.3f} ± {:5.3f}'.format(i,param,pstd[i]/2))


y_modelo = modelo(res.x, x_datos)

plt.figure()
plt.plot(x_datos, y_datos ,  'o', markersize=4, label='datos')
plt.plot(x_datos, y_modelo, 'r-',               label='modelo fiteado')
plt.xlabel("x")
plt.ylabel("y")
plt.legend(loc='best')
plt.tight_layout()

```

{% include page_navbar.html up=1 %}
