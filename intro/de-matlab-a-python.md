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

### ¿Que tan parecido se ve el código?

Ejemplo comparativo (extraído de [aquí](http://stsievert.com/blog/2015/09/01/matlab-to-python/)):

```python
# PYTHON                        | % MATLAB
from pylab import *             | clc; clear all; close all
                                |
# matrix multiplication         | % matrix multiplication
A = rand(3, 3)                  | A = rand(3, 3);
A[0:2, 1] = 4                   | A(1:2, 2) = 4;
I = A @ inv(A)                  | I = A * inv(A);
I = A.dot(inv(A))               |
                                |
# vector manipulations          | % vector manipulations
t = linspace(0, 4, num=1e3)     | t = linspace(0, 4, 1e3);
y1 = cos(t/2) * exp(-t)         | y1 = cos(t/2) .* exp(-t);
y2 = cos(t/2) * exp(-5*t)       | y2 = cos(t/2) .* exp(-5*t);
                                |
# plotting                      | % plotting
figure()                        | figure; hold on
plot(t, y1, label='Slow decay') | plot(t, y1)
plot(t, y2, label='Fast decay') | plot(t, y2)
legend(loc='best')              | legend('Slow decay', 'Fast decay')
show()                          |
```

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

La forma más canónica de importar librerías sería la siguiente:

```python
import numpy as np
import matplotlib.pyplot as plt
```
En este caso, las funciones importadas hay que llamarlas anteponiendo el "alias" de la
librería de donde vienen: `np.diag`, `np.eye`, `plt.plot`.

<a data-toggle="collapse" href="#importar_librerias" aria-expanded="false" aria-controls="importar_librerias">¿Por que usar la importación canónica? <span class="caret"></span></a>

<div id="importar_librerias" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

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

## Recursos para empezar a programar YA MISMO (y otros)

Si estás apurado/a por empezar, seguramente querés una lista de comandos de MATLAB
y su traducción a Python, como las que está acá.

<center>
<a href="http://mathesaurus.sourceforge.net/matlab-numpy.html" class="btn btn-primary btn-lg" role="button">
Equivalencias Matlab-Python
</a>
</center>

La mayoría de esos ejemplos asumen que importaste las librerías usando `from pylab import *`.

Si queremos profundizar, pasando la urgencia, acá hay una serie de recursos útiles:

  - **Equivalencias entre comandos de Matlab y de Python - Numpy:**
    - En HTML: [mathesaurus](http://mathesaurus.sourceforge.net/matlab-numpy.html)
    - En PDF: [matlab-python-xref.pdf](http://mathesaurus.sourceforge.net/matlab-python-xref.pdf)
  - **Tutorial (muy completo) de herramientas de python para el ámbito científico:**
    - En inglés: [www.scipy-lectures.org](http://www.scipy-lectures.org/)
    - En español (parcialmente traducido): [scipy-lecture-notes-ES](https://claudiovz.github.io/scipy-lecture-notes-ES/)
    - Fundamentalmente los capítulos de [NumPy](https://claudiovz.github.io/scipy-lecture-notes-ES/intro/numpy/index.html)
      y [Matplolib](https://claudiovz.github.io/scipy-lecture-notes-ES/intro/matplotlib/matplotlib.html)
      ([1.3](https://claudiovz.github.io/scipy-lecture-notes-ES/intro/numpy/index.html) y
      [1.4](https://claudiovz.github.io/scipy-lecture-notes-ES/intro/matplotlib/matplotlib.html))
      serán de especial interés.
    - Es una guía pormenorizada.
  - **Consejos oficiales de SciPy para migrar a Python (en inglés):**
    - [NumPy_for_Matlab_Users](http://scipy.github.io/old-wiki/pages/NumPy_for_Matlab_Users.html)
  - **Referencia del lenguaje Python** (para programadores, no tanto para ciencia/ingeniería):
    - El WikiBook es de gran utilidad (inglés): [Python_Programming](https://en.wikibooks.org/wiki/Python_Programming)
    - Si nunca programaste, podés arrancar por acá:
      [Non-Programmer's_Tutorial_for_Python_3](https://en.wikibooks.org/wiki/Non-Programmer%27s_Tutorial_for_Python_3)
    - En español, este blog es una referencia útil:
      [python-para-impacientes](http://python-para-impacientes.blogspot.com.ar/p/indice.html)
  - **Gráficos**
    - [Ejemplos introductorios a Matplotlib](http://webs.ucm.es/info/aocg/python/modulos_cientificos/matplotlib/index.html)
    - [Galería de emplos oficial de Matplotlib](https://matplotlib.org/gallery.html)
      - Hacer clic en cada imagen para ver el código de ejemplo que la genera

## Ayudas y confusiones más frecuentes al empezar

Comandos útile de IPython:
  - `%reset` borra toda la memoria de la sesion actual (como el `clear all` de MATLAB)


  - <a data-toggle="collapse" href="#ayudas_slices" aria-expanded="false" aria-controls="ayudas_slices">Diferencias entre slices (python) y ":" (MATLAB)  <span class="caret"></span></a>

<div id="ayudas_slices" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

En MATLAB la expresión `1:3:10` es en sí mismo un array que comienza en uno y va en pasos de a 3 hasta 10. Es equivalente
a un vector `[1, 4, 7, 10]`. O la expresión `3:6` es equivalente a `[3,4,5,6]`.

Además, si uno tiene un vector cualqueira y quiere obtener los elementos de las posiciones 3, 4, 5 y 6, puede hacer:

```matlab
vec = [1 4 7 3 5 8 4 3 8 9 5 3 4 6 2]
vec(3:6)
```
> ```ans =

     7     3     5     8```

</div>

  - <a data-toggle="collapse" href="#ayudas_copy" aria-expanded="false" aria-controls="ayudas_copy">Cómo copiar un array en Python <span class="caret"></span></a>

<div id="ayudas_copy" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">
Completar
</div>

- <a data-toggle="collapse" href="#ayudas_copy" aria-expanded="false" aria-controls="ayudas_copy">Cómo acceder a instrumentos VISA del laboratorio <span class="caret"></span></a>

<div id="ayudas_copy" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">
Por ahora vamos a referenciar el GitHub de Hernán Grecco, que tiene ejemplos aramados para varios instrumentos:

[hgrecco/labosdf](https://github.com/hgrecco/labosdf/tree/master/software/python/instrumentos)

</div>
