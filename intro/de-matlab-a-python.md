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
  - Recetas ya armadas (en ingles):
    - [scipy-cookbook.readthedocs.io](http://scipy-cookbook.readthedocs.io/)
  - **Consejos oficiales de SciPy para migrar a Python (en inglés):**
    - [NumPy_for_Matlab_Users](http://scipy.github.io/old-wiki/pages/NumPy_for_Matlab_Users.html)
    - El [sitio de SciPy](https://www.scipy.org/) en general tiene mucha información útil.
  - **Referencia del lenguaje Python** (para programadores, no tanto para ciencia/ingeniería):
    - El WikiBook es de gran utilidad (inglés): [Python_Programming](https://en.wikibooks.org/wiki/Python_Programming)
    - Si nunca programaste, podés arrancar por acá:
      [Non-Programmer's_Tutorial_for_Python_3](https://en.wikibooks.org/wiki/Non-Programmer%27s_Tutorial_for_Python_3)
    - En español, este blog es una referencia útil:
      [python-para-impacientes](http://python-para-impacientes.blogspot.com.ar/p/indice.html)
  - **Gráficos**
    - [Ejemplos introductorios a Matplotlib](http://webs.ucm.es/info/aocg/python/modulos_cientificos/matplotlib/index.html)
    - [Ejemplos más frecuentes de Matplotlib](https://matplotlib.org/users/screenshots.html)
      - Incluyen código para generar cáda imagen
    - [Galería completa de ejemplos de Matplotlib](https://matplotlib.org/gallery.html)
      - Hacer clic en cada imagen para ver el código de ejemplo que la genera

## Ayudas y confusiones más frecuentes al empezar

Comandos útiles de IPython:
  - `%reset` borra toda la memoria de la sesion actual (como el `clear all` de MATLAB)

  - `del nombre_de_variable` elimina la variable `nombre_de_variable`

  - <a data-toggle="collapse" href="#ayudas_slices" aria-expanded="false" aria-controls="ayudas_slices">Diferencias entre slices (python) y ":" (MATLAB)  <span class="caret"></span></a>

<div id="ayudas_slices" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

En MATLAB la expresión `1:3:10` es en sí mismo un array que comienza en uno y va en pasos de a 3 hasta 10. Es equivalente
a un vector `[1, 4, 7, 10]`. O la expresión `3:6` es equivalente a `[3,4,5,6]`.

Además, si uno tiene un vector cualqueira y quiere obtener los elementos de las posiciones 3, 4, 5 y 6, puede hacer:

```matlab
vec = [1 4 7 3 5 8 4 3 8 9 5 3 4 6 2]
vec(3:6)
```
```matlab
ans =

     7     3     5     8
```

Esto se ve similar a una expresión de NumPy para ver elementos de un array:

```python
vec = np.array([1,4,7,3,5,8,4,3,8,9,5,3,4,6,2])
vec[3:6]
```
```python
array([3, 5, 8])
```
... pero es en escencia MUY diferente:

  - En python, la expresión `3:6` es un [slice](http://librosweb.es/foro/pregunta/250/como-entender-bien-la-notacion-slice-de-python/). No es un array y
  no se lo puede multiplicar ni sumar a otro objeto.
  - En MATLAB los elementos empiezan a contar desde `1`, mientras que en Python se cuentan desde `0`.
  - Para obtener un vetor equivalente al de MATLAB `1:10` en Python se debe usar: `arange(1,11)`.

</div>

  - <a data-toggle="collapse" href="#ayudas_copy" aria-expanded="false" aria-controls="ayudas_copy">Cómo copiar un array en Python <span class="caret"></span></a>

<div id="ayudas_copy" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

En MATLAB, la expresión `a = b ;` genera un vector/matriz `a` con todos sus elementos idénticos a los elementos de `b`.

En Python, la expresión `a = b` (para un array) genera un objeto `a` que hace referencia al objeto `b`. Por ende,
se se modifica `a` también se modifica `b`.

Ejemplo de comportamiento en MATLAB:
```matlab
vec = [1 4 7 3 5 8 4 3 8 9 5 3 4 6 2] ;
a = vec(3:6) ;
disp(a)
%      7     3     5     8

disp(a(2))
%      3

a(2)=10 ;

disp(a)
%      7    10     5     8

disp(vec)
%     1     4     7     3     5     8     4     3     8     9     5     3     4     6     2

```

Ejemplo de comportamiento en Python:

```python
vec = np.array([1,4,7,3,5,8,4,3,8,9,5,3,4,6,2])

print( vec )
# [1 4 7 3 5 8 4 3 8 9 5 3 4 6 2]

print( a )
# [3 5 8]

print( a[1] )
# 5

a[1] = 10
print( a )
# [ 3 10  8]

print( vec )
# [ 1  4  7  3 10  8  4  3  8  9  5  3  4  6  2]

b = a.copy()

print(b)
# [ 3 10  8]

b[0] = 10
print(b)
# [10 10  8]

print(a)
# [ 3 10  8]
```

Para generar la "copia" de los elementos de `a` se usa  `a.copy()`

</div>

- <a data-toggle="collapse" href="#ayudas_visa" aria-expanded="false" aria-controls="ayudas_visa">Cómo acceder a instrumentos VISA del laboratorio <span class="caret"></span></a>

<div id="ayudas_visa" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">
Por ahora vamos a referenciar el GitHub de Hernán Grecco, que tiene ejemplos aramados para varios instrumentos:

[hgrecco/labosdf](https://github.com/hgrecco/labosdf/tree/master/software/python/instrumentos)

</div>

- <a data-toggle="collapse" href="#ayuda_ventanas_graficas" aria-expanded="false" aria-controls="ayuda_ventanas_graficas">Cómo habilitar los gráficos en ventanas independientes en Spyder<span class="caret"></span></a>

<div id="ayuda_ventanas_graficas" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

En muchos casos el comportamiento por defecto del IDE Spyder es mostrar los gráficos
en la propia consola de IPython. Eso resulta muy bonito para una presentación, pero
es incómodo para el análisis de datos.

Solo algunos ejemplos de la utilidad de tener los gráficos en ventanas independientes:

  - El comportamiento se asemeja al de MATLAB: Se pueden usar figuras independientes
    para cada gráfico y referenciarlas posteriormente para hacer modificaciones, sin
    perder de vistas las otras que se hayan graficado.
  - Permite hacer zoom, mover los ejes o guardar como archivo de imagen con sólo
    usar el mouse y los íconos de la ventana.
  - Se pueden usar comandosde interactividad, como por ejemplo el `plt.ginput()`
    que te permite obtener las coordenadas de un punto del gráfico haciendo clic
    con el mouse

Para habilitar los gráficos en ventanas independientes hay que hacer lo siguiente:
  1. Ir al menú **Herramientas** &rarr; **Preferencias**
  2. Seleccionar la sección de **Terminal de IPython**
  3. Seleccionar la solapa **Gráficas**
  4. En el recuadro **Salida gráfica**, seleccionar del menú desplegable
     la opción **Automático**
  5. **Aceptar** los cambios. Es posible que, para que el cambia surta efecto,
     haya que **cerrar y reabrir el Spyder**.

![spyder_pref]({{ site.baseurl }}/img/spyder_preferencias_iphython.png "spyder pref")

</div>

- <a data-toggle="collapse" href="#ayuda_guardar_numpy" aria-expanded="false" aria-controls="ayuda_guardar_numpy">Cómo guardar datos en el formato de NumPy<span class="caret"></span></a>

<div id="ayuda_guardar_numpy" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

### Guardar datos
En MATLAB basta con ejecutar `save nombre_de_archivo.mat` y se guardarán todas las variables que existen en el entorno de trabajo
en un archivo binario de formato privativo llamado `nombre_de_archivo.mat`. En Python
se debe decir explícitamente qué variables se quiere guardar. Paraello se usa el comado
de NumPy `np.savez()`, cuya [documentación está aquí](https://docs.scipy.org/doc/numpy/reference/generated/numpy.savez.html).

**Syntaxis del comando:**
Si quiero guardar las variables `varX`, `varY` y `texto_mio` en el archivo
`datos.npy` puedo escribir:

```python
np.savez('datos.npz', varX=varX, varY=varY, texto_mio=texto_mio)
```
El primer argumento es el nombre del archivo en formato de texto.
Luego, cada argumento que sige es una variable a guardar. Se lee así:
`varX=varX` significa "con el nombre `varX` (lo que está antes del igual)
guardá el objeto llamando `varX` (lo que está después del igual)"

Recordar que, si no se especifica la ruta completa, el archivo será creado en la carpeta de trabajo actual (que se puede averiguar ejecutando el comando `pwd`).

### Recuperar datos
En MATLAB los datos se recuperan ejecutando `load nombre_de_archivo.mat`. Cada variable es
cargada a la memoria con su nombre original. Si antes de ejecutar `load` ya existían
variables con esos nombres, son reemplazadas y se pierden los valores no guardados.

En Python, NumPy lee los archivos `.npz` con la instrucción `np.load` y los carga
en un objeto nuevo con nombre.
Por ejemplo, si se trata de recuperar el archivo guardado en el ejemplo anterior:

```python
datos = np.load('datos.npz')
```

El objeto `datos` será un [diccionario](https://claudiovz.github.io/scipy-lecture-notes-ES/intro/language/basic_types.html#diccionarios),
donde cada clave corresponde a una de las variables guardadas.

### Ejemplo completo

Guardamos los datos:
```python
varX = np.array([10,20,30,70,90,-1])

varY = -3.1415926535897

texto_mio = 'Este texto es una descripción que me recuerda para qué son los valores varX y varY que guardé.'

# Instrucción para guaradar datos en formato NumPy
np.savez('datos.npz', varX=varX, varY=varY, texto_mio=texto_mio)

```

Luego los recuperamos en el objeto `datos`:

```python
datos = np.load('datos.npz')

datos
# Out[2]: <numpy.lib.npyio.NpzFile at 0x7f71fa8f25f8>

# El método keys() del diccionario nos permite saber los nombres con que se guardaron las variables

datos.keys()
# Out[3]: ['varX', 'varY', 'texto_mio']

datos['varX']
# Out[4]: array([10, 20, 30, 70, 90, -1])

datos['varY']
# Out[5]: array(-3.1415926535897)

datos['texto_mio']
# Out[6]:
# array('Este texto es una descripción que me recuerda para qué son los valores varX y varY que guardé.',
#       dtype='<U94')
```

Notar que todos los objetos fueron guardados con el formato `array()` de NumPy, por mas que sean vectores, números
o texto. Si queremos que las variables vuelvan a tener los nombres originales solo hay que asignarlas a esos nombres.
Para los casos en los que no se desea que el formato final sea `array()` se utiliza el método `.tolist()`:

```python
varX      = datos['varX']
varY      = datos['varY'].tolist()
texto_mio = datos['texto_mio'].tolist()

varX
# Out[8]: array([10, 20, 30, 70, 90, -1])

varY
# Out[9]: -3.1415926535897

texto_mio
# Out[10]: 'Este texto es una descripción que me recuerda para qué son los valores varX y varY que guardé.'
```

</div>

- <a data-toggle="collapse" href="#ayuda_exportar_a_matlab" aria-expanded="false" aria-controls="ayuda_exportar_a_matlab">Cómo guardar datos en formato MATLAB (.mat)<span class="caret"></span></a>

<div id="ayuda_exportar_a_matlab" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

Para exportar datos a formato `.mat` se usa la función
[savemat()](https://docs.scipy.org/doc/scipy-0.19.0/reference/generated/scipy.io.savemat.html) de la librería `scipy.io`.
Esta función permite exportar a formato MATLAB un objeto
 [diccionario](https://claudiovz.github.io/scipy-lecture-notes-ES/intro/language/basic_types.html#diccionarios),
por lo que, si se queire guardar múltimples variables, habrá que
especificarlas dentro de un diccionario.

```python
from scipy.io import savemat

varX = np.array([10,20,30,70,90,-1])

varY = -3.1415926535897

texto_mio = 'Este texto es una descripción que me recuerda para qué son los valores varX y varY que guardé.'

savemat('datos.mat', mdict={'varX': varX, 'varY': varY, 'texto_mio': texto_mio})
```

Luego en matlab, al ejecutar el comando

```matlab
load datos.mat
```
se crearan las variables `varX`, `varY` y `texto_mio`.

</div>
