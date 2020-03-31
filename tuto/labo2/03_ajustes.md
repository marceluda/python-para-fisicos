---
title: Ajustes no lineales
description: Ajuste de un modelos no lineal a los datos
layout: page
mathjax: true
navbar: labo2
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

<div class="alert alert-info" role="alert" >
  <strong>Actualización 2018-11-06:</strong> Cálculo del
  <a href="https://en.wikipedia.org/wiki/Coefficient_of_determination">Coeficiente de determinación</a> .
</div>

Un estimador de bondad de ajuste que se puede calcular para evaluar el modelo es el
[Coeficiente de determinación](https://en.wikipedia.org/wiki/Coefficient_of_determination)
$R^2$. Este valor coincide con el cuadrado del
[Coeficiente de correlación de Pearson](https://en.wikipedia.org/wiki/Pearson_correlation_coefficient) $r^2$
sólo cuando el modelo es lineal

```python
print('Coeficiente de determinacion R2')

# Suma de los cuadrados de los residuos
ss_res = np.sum( (y_datos - modelo(x_datos, *popt))**2  )

# Suma total de cuadrados
ss_tot = np.sum( (y_datos - np.mean(y_datos) )**2  )

R2     = 1 - (ss_res / ss_tot)

print('R2 = {:10.8f}'.format(R2) )

print('Nota 1: Solo en los ajustes lineales este valor coincide con el r2 de pearson.')

print('''Nota 2: Se puede pensar el coeficiente de determinación R2 como
        "el porcentaje de la varianza que se puede explicar a partir del modelo
        propuesto (con los parámetros hallados)". En ese sentido, 1-R2 representa
        la variaza que NO se explica a partir del modelo (que puede ser ruido o
        un indicio de que el modelo no es bueno).''')
```
<a data-toggle="collapse" href="#ajustar_con_incertezas" aria-expanded="false" aria-controls="ajustar_con_incertezas">Más opciones de ajuste con <span style="font-family: monospace;">curve_fit</span> <span class="caret"></span></a>

<div id="ajustar_con_incertezas" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

Una lista mas completa de parámetros para `curve_fit` es la siguientes:

```python
curve_fit(
      funcion_del_modelo,
      xdata,
      ydata,
      p0=parametros_iniciales,
      sigma=intervalos_de_incerteza,
      bounds=limites_de_los_parametros,
      method=metodo_de_fiteo,
      jac=funcion_que_calcula_el_jacobiano
    )
```
Ya sabesmos que `funcion_del_modelo` es una función que tiene como primer argumento
el vector de coordenadas `x` de los datos y como argumentos siguientes los valores
de los parámetros a ajustar:

```python
def funcion_del_modelo(x, a, b, c):
    return a * np.exp(-b * x) + c
```

`parametros_iniciales` es una lista o vector con los parámetros desde los que se parte
para realizar la optimización. Puede ser cualquiera de estas opciones:

```python
# orden de los parametros:  a , b , c
parametros_iniciales = [2, 1, 6]            # lista
parametros_iniciales = (2, 1, 6)            # tuple
parametros_iniciales = np.array([2, 1, 6])  # array
```

`xdata` e `ydata` son los vectores de coordenadas `x` e `y` de los datos.


`intervalos_de_incerteza` permite especificar los intervalos de incerteza en `y`.
Se puede definir de varias formas:

```python
# Si es un objeto de una dimensión, se lo interpreta como la desviación estandar del error
# en cada uno de los elementos del vector y de datos
intervalos_de_incerteza = np.array([0.3, 1.8, ... , 1.2, 0.5])  
```

`limites_de_los_parametros` es un tuple que especifica en el primer elemento
los límites inferiores de los parámetros, y en el segundo los límites superiores.
Por ejemplo:


```python
# Los parámetros en orden son a,b,c

# Especificamos que todos los parametros son como mínimo 0.
# Luego, a < 10 , b < 100 y c < +infinito
limites_de_los_parametros = ( 0 , [10,100,np.inf] )

# Tambien podemos especificar límites separados para cada parámetro
a * np.exp(-b * x) + c
#         0 < a < 10000
#         1 < b < 5
# -infinito < c < -10
limites_de_los_parametros = ( [0,1,-np.inf] , [10000,5,-10] )
```
`metodo_de_fiteo` es uno de estos tres:
`lm`, `trf`, `dogbox`.
Para más información [ver la documentacion](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html#scipy.optimize.least_squares).


</div>


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

Como nosotros mismo definimos la función que calcula el residuo, podemos incluir
más instrucciones para, por ejemplo, graficar paso a paso como el modelo se acerca
a los datos a medida que se optimizan los parámetros, o para guardar la lista
de parámetros que se fueron probando.

```python
from scipy.optimize import least_squares

def modelo(p,x):
    # p es un vector con los parámetros
    # x es el vector de datos x
    return np.exp(-(x-p[0])**2/p[1]**2)+np.exp(-(x-p[2])**2/p[3]**2)

param_list = []

def residuos(p, x, y):
    # p es un vector con los parámetros
    # x es el vector de datos x
    # y es el vector de datos y
    y_modelo = modelo(p, x)
    plt.clf()
    plt.plot(x,y,'o',x,y_modelo,'r-')
    plt.pause(0.05)
    param_list.append(p)
    return y_modelo - y

parametros_iniciales=[1, 2, 8, 3]  # Ajusta
res = least_squares(residuos, parametros_iniciales, args=(x_datos, y_datos), verbose=1)

# Estos son los parámetros hallados:
print('parámetros hallados')
print(res.x)

# Calculamos la matriz de covarianza "pcov"
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

# De la matriz de covarinza podemos obtener los valores de desviación estándar
# de los parametros hallados
pstd = np.sqrt(np.diag(pcov))

print('Parámetros hallados (con incertezas):')
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
A continuación se pueden ver los pasos que realiza el algoritmo de optimización.
A la izquierda están los datos y la predicción del modelo para un dado conjunto
de parámetros.
A la derecha, cada uno de los parámetros probados y su evolución. Las líneas celestes
son los "valores reales" de los parámetros con los que se fabricaron los datos
(el array `parametros_reales`).


![ajuste-least_squares](ajuste-least_squares.gif "Ajuste least_squares"){:style="width: 100%;"}



A menudo, la función a minimizar (la suma cuadrática de los residuos, en este caso) tiene mínimos locales
que no se corresponden con el conjunto óptimo de parámetros que buscamos. Es esencial elegir
bien los parámetros iniciales para que el algoritmo converja.

<a data-toggle="collapse" href="#ajuste_no_converge" aria-expanded="false" aria-controls="ajuste_no_converge">
Ejemplo de ajuste que no converge
<span class="caret"></span></a>

<div id="ajuste_no_converge" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">
El siguiente parte de los párametros iniciales:
```python
parametros_iniciales=[0, 3, 8, 3] # Ajusta mal
```

![ajuste-least_squares que no converge](ajuste-least_squares_mal_inicio.gif "Ajuste least_squares que no converge"){:style="width: 100%;"}

El siguiente parte de los parámetros iniciales:
```python
parametros_iniciales=[0, 3, 10, 3]  # No ajusta
```

![ajuste-least_squares que no converge](ajuste-least_squares_no_ajusta_2.gif "Ajuste least_squares que no converge"){:style="width: 100%;"}

</div>


{% include page_navbar.html up=1 %}
