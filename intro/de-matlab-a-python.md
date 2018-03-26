---
title: De Matlab a Python
description: Para que usamos python en física
layout: page
mathjax: true
---

<div class="alert alert-danger" role="alert" >
  <strong>Aviso:</strong> La página está en construcción y aún tiene muchas carencias
</div>

[MATLAB](https://es.wikipedia.org/wiki/MATLAB) es software para reliazar cálculo numérico
que utiliza el lenguaje interpretado "M". Es un software privativo y costoso, pero muy popular en el ámbito
científico y de ingeniería. Es por eso que muchas personas buscan reemplazarlo con algo
"similar" o "amigable". Existen otros interpretadores de lenguaje M que son libres, gratuitos
y multiplataforma, como [Octave](https://es.wikipedia.org/wiki/GNU_Octave) o
[Scilab](https://es.wikipedia.org/wiki/Scilab).

Otra opción es reemplazarlo por Python. Existen librerías para cálculo numérico y graficación
que emulan muchas de las funciones más utilizadas de MATLAB (y hasta usan los mismos nombres
para facilitar la migración!). Vamos a volcar algo de información útil para lograr migrar
de MATLAB a Python.

## Instalar un entorno de trabajo
A direfencia de MATLAB, Python es un lenguaje de programación multipropósito. No tiene una interfase
pensada específicamente para procesar datos, hacer cálculo numérico, etc. Y las funciónes específicas
vienen en paquetes que "hay que instalar". Pero para hacerla más fácil y rápida, hay instaladores que nos
resuelven en pocos clics todo lo que necesitamos tener para reemplazar el MATLAB.

**Más simple y rápido**, hay que **instalar el [Anaconda Python](https://www.anaconda.com/download/#download)**.
Hay instaladores para Windows, Linux y MAC. La mayoría de las computadoras modernas aceptan la verisón **64 bits (x86)**.
Es preferible la version de **Python 3** (3.6 actualmente).

Una vez instalado vamos a usar la **[Interfaz Gráfica Spyder](https://github.com/spyder-ide/spyder)**, que se ve así:

![spyder_ejemplo]({{ site.baseurl }}/img/spyder_ejemplo.png "spyder_ejemplo")

Similitudes con la interfase de MATLAB:
  - Tiene varios paneles, incluyendo un **editor**, una **consola** donde se ejecutan los comandos y un **inspector de objetos**.
  - Los gráficos se pueden ver directamente en ventanas manipulables (con zoom y controles afines)
  - Algunos "atajos" son idénticos:
    - **`F5` para ejecutar un archivo completo**
    - **`F9` para ejecutar la selección**
  - Se puede **dividir el código en bloques**, que inician con `#%% [titulo del bloque]` y que se ejecutan con
    `CTRL+Enter`.
  - La consola de comando es interactiva (gracias a [IPython](https://es.wikipedia.org/wiki/IPython)). Por ejemplo,
    se pueden auto-completar comandos con la tecla `TAB` o imprimir la ayuda de un comando con `comando?`

## Consideraciones rápidas sobre el lenguaje Python

Para realizar cálculo numérico, graficar, hacer estadística, etc, Python utiliza un conjunto de librerías
que deben ser llamadas antes de usarlas. Aquí se incluyen las que reemplazan las funciones que usamos
en MATLAB.

**Librerías útiles:**
  - **[Numpy](http://www.numpy.org/)** para hacer cálculo numérico.
  - **[Matplotlib](http://matplotlib.org/)** para hacer gráficos
  - **[SciPy](http://www.scipy.org/)**
    para tareas varias, como optimizacion, FFT, procesamiento de imágenes, etc.
  - **PyLab** es una colección de funciones que permite llamar varias de las funciones
    de Numpy, Matplotlib y SciPy en unsa sola librería.

**La forma rápida y simple de tener todas estas funciones es ejecutar el siguiente comando:**

```python
from pylab import *
```
<div class="alert alert-info" role="alert" >
  <strong>Aviso:</strong> esta forma de importar comandos es la más simple, pero es desaconsejada.
  Leer bien acá abajo el detalle de porqué.
</div>

Con esa importación vamos a disponer directamente de comandos como `ones`, `diag`, `eye`, `plot` y
varios idénticos de MATLAB. Sola hay que escribirlos.

La forma más mecánica de importar librerías sería la siguiente:

```python
import numpy as np
import matplotlib.pyplot as plt
```
En este caso, las funciones importadas hay que llamarlas anteponiendo el "alias" de la
librería de donde vienen: `np.diag`, `np.eye`, `plt.plot`.

<a data-toggle="collapse" href="#importar_librerias" aria-expanded="false" aria-controls="importar_librerias">¿Por que es importante la forma de importar librerías? <span class="caret"></span></a>

<div id="importar_librerias" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

**Por que usar la importación canónica?**

Hay nombres de funciones que se repiten en diferentes librebrías. Por ejemplo,
si tenemos dos librerías con la función plot, una la de `matplotlib.pyplot` y otra (que inventamos acá)
llamada `graficos`.

Si uno importa de esta manera:
```python
import matplotlib.pyplot as plt
import graficos as gra
```
Luego puede llamar cada funcion de plot de forma diferente:
```python
plt.plot(variable_A, color='blue')
gra.plot(otra_variable)
```

En cambio haciendo:
```python
from  matplotlib.pyplot import *
```

Llamamos a `matplotlib.pyplot.plot` simplemente como:

```python
plot(variable_A, color='blue')
```

Pero, si queremos usar ambas librerías:
```python
from  matplotlib.pyplot import *
from  graficos import *
```

Solo la última llamada responderá a la función  `plot` y la anterior será inaccesible.

Entonces .. **¿que es mejor?**.
  - **Lo mejor es llamar funciones con Alias, como `np` y `plt`.
  - **Lo más simple y parecido a MATLAB es imporatar todo scipy con `from pylab import *`

</div>
