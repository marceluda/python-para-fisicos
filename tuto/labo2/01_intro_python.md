---
title: Introducción a Python
description: Programación y cálculo
layout: page
mathjax: true
navbar: labo2
---


{% include page_navbar.html %}

<div class="alert alert-danger" role="alert" >
  <strong>Aviso:</strong> La página está en construcción.
</div>




## Sistemas de cálculo numérico

Existen diversos programas de cálculo numérico, diseñados para facilitar la realización de cálculos complejos entre matrices y vectores de datos, así como facilitar diferentes métodos numéricos de análisis de datos. Estos programas suelen tener un modo de uso similar y comparten la misma sintaxis similar. Se los utiliza de forma análoga a un lenguaje de programación por “scripts”.
Algunos ejemplso de ellos son:

  - [MATLAB](https://www.mathworks.com/products/matlab.html) (privativo y pago) [**windows**,**linux**,**mac**]
  - [GNU/Octave](https://www.gnu.org/software/octave/) (Libre y gratuito) [**windows**,**linux**,**mac**]
  - [SciLab](https://www.scilab.org/) (Libre y gratuito) [**windows**,**linux**,**mac**]
  - [Maple](http://www.maplesoft.com/products/maple/) (privativo y pago) [**windows**]
  - [MathCAD](https://www.ptc.com/en/products/mathcad/) (privativo y pago) [**windows**]
  - [SAGE](http://www.sagemath.org/) (Libre y gratuito) [**Web**]
  - [Jupyter](http://jupyter.org/) (Libre y gratuito) [**Web**]
  - [Python+librerías](https://www.scipy.org) (Libre y gratuito) [**windows**,**linux**,**mac**]


En este instructivo se hará una introducción al uso de Python para reemplazar las herramientas de MATLAB/Octave de análisis y cálculo. Python es un lenguaje multiplataforma (windows, linux, mac, etc) y multipropósito (para cualquier tipo de progrmación) e interpretado (scripts). Para el uso específico que le vamos a dar, se vale de herramientas y librerías específucas.

  - Interfaz grafica [Spyder] (https://github.com/spyder-ide/spyder)
  - Línea de comandos [IPhython](https://ipython.org/)
  - Cálculo numérico con [NumPy](http://www.numpy.org/)
  - Gráficos con [Matplolib](https://matplotlib.org/)
  - Otras herramientas con [ScyPy ](https://www.scipy.org/)

Todas estas librerías y software se pueden obtener en un solo paquete compacto instalando [Anaconda Python](https://www.anaconda.com/download). Se recomienda bajar e instalar la versión que trae Python 3.6 :

<center>
<a href="https://www.anaconda.com/download" class="btn btn-primary btn-lg" role="button">
Anaconda Linux
</a>
</center>

La intención de este instructivo es introducir solo algunos ejemplos básicos que permitan hacer análisis de datos. Para mayor información se proporcionarán links de referencia.


## Interfaz, uso básico y tipos de datos

El siguietne es un ejemplo de la interfáz gráfica de Spyder:

![spyder_ejemplo]({{ site.baseurl }}/img/spyder_ejemplo.png "spyder_ejemplo")

Escencialmente vamos a usar dos pestañas: La de **edición de archivos** y la de **línea de comandos**. En la primera se escriben *scripts*, trozos de código a ejecutar. En la segunda, se puede ejecutar código como comandos individuales.

Para ejecutar código de un archivo se pueden usar las siguientes opciones:
  - La tecla `F5`, que ejecuta el archivo entero
  - La tecla `F9` que ejectuda lo que esté seleccionado en la pantalla con el cursor
  - Las teclas `Ctrl+Enter`, que ejecuta un bloque. Un bloque es lo que se encuentra entre una línea empezada por `#%% ` hasta la siguiente línea que empieza por `#%% `.

Al utilizar librerías gráficas, los resultados suelen aparacer en una ventana extra o empotrados en la línea de comandos.

### Variables, operadores, tipos de datos y funciones

Como en cualquier lenguaje de programación, Python utilizan *variables, operadores y funciones*. Las **variables** son formas de nombrar a la información que se guarda y procesa. Nos interesa en particular guardar números, vectores o matrices, pero tambien pueden ser texto u otros objetos.

A las variables se les asignan valores con el operador “=”, que quiere decir “asignarle tal valor a esta variable” y no tiene nada que ver con el concepto de igualdad matemática.

Ejemplo:

```python
a = 11
b = 2
print(a+b)
# imprime: 13
print(a*b)
# imprime: 22
print(b**a)
# imprime 2 elevado a la 11, osea: 2048
a = a + 5
print(a)
# Se reemplaza el valor de a por el de "a+5". Al imprimir a se ve: 16
```

El comando `print()` permite imprimir en en la línea de comandos un resultado o el contenido de una variable.

Los **operadores** definen operaciones entre variables, como puede ser una suma o multiplicación, o asignar un valor.

Operadores aritméticos:

| operador   | descripcion                     |
|------------|---------------------------------|
| `+`        | suma                            |
| `-`        | resta                           |
| `*`        | multiplicación                  |
| `/`        | división con decimales          |
| `//`       | división entera                 |
| `**`       | potenciación                    |
| `%`        | módulo (resto de la división)   |

Operadores de comapración:

| operador   | descripcion                     |
|------------|---------------------------------|
| `==`       | es igual a ... ?                |
| `!=`       | es diferente a...?              |
| `>`        | mayor                           |
| `>=`       | mayor o igual                   |
| `<`        | menor                           |
| `<=`       | menor o igual                   |

Hay múltiples **tipos de datos** que pueden contener una variable. Acá algunos ejemplos :

```python
numero_entero  =  3    # Ejemplo de número entero
num1           =  3.8  # Ejemplo de número real
num2           = -2.0  # Otro número real
num3           = 5.2e9 # Otro número real: 5.2 x 10^9
texto          = 'esto es un texto'
lista          = [1,2,3,4,5,6]  # Esto es una lista... un conjunto
                                # ordenado de valores, en este caso
                                # de tipo int
```

Las **funciones** sun rutinas que realizan algún procedimiento (como algún cálculo, por ejemplo) y devuelven (o no) un resultado.
Pueden tener uno a varios parámetros, que son los datos de entrada (que irán entre paréntesis). Se puede asignar la salida o
resultado de dicho procedimiento a una variable. Por ejemplo, la función `max()` halla el valor máximo de una lista de valores:

```python
lista   = [-20,50,3,-91,8]
max_val = max(lista)
print('De la lista:', lista )
print('El valor máximo es:', max_val)
```

## Numpy y cálculos vectoriales

Para hacer cálculos más sofisticados necesitamos de funciones y objetos mas complejos.
Diferentens conjuntos de funciones y objetos son agrupadas en *librerías* para realizar tareas específicas.
En particular, la librería de `numpy` incluye herramientas para trabajar con vecotres y matrices.

Para usar las librerías es necesario imporarlas con la instrucción `import`:
```python
import numpy

vector_a = numpy.array( [ 1.2, 3.4, -1.0] )
vector_b = numpy.array( [10.0,   0,  2.0] )
print('vector_a:',vector_a)
print('vector_b:',vector_b)
print('vector_a*vector_b:',  vector_a*vector_b  )
```

Se puede importar usando un alias, para facilitar la escritura:

```python
import numpy as np

a = np.array( [ 1.2, 3.4, -1.0] )
b = np.array( [10.0,   0,  2.0] )
print('a:',a)
print('b:',b)
print('a*b:',  a*b  )
```

Tambien se pueden importar sólo algunas fuciones en específico:
```python
from numpy import array,sin,cos,pi

a = array( [ 0 , pi/2 , pi] )
b = cos( a )
c = sin( a )

print('a:', a )
print('b:', b )
print('c:', c )
```

<div class="alert alert-info" role="alert" >
  <strong>Aviso:</strong> Notar que hay valores que debieran dar CERO y no son estrictamente CERO.
  El cálculo numérico no es del todo preciso, maneja una precisión limitada por la cantidad de bits que usa
  el procesador para procesar los datos.
</div>

Tambien se pueden cargar todas juntas las funciones sin usar el contenerdor `numpy` ni un alias como `np`:
```python
from numpy import *

a = array( [ 0 , pi/2 , pi] )
b = cos( a )
c = sin( a )
```

<div class="alert alert-info" role="alert" >
  <strong>Aviso:</strong> Este uso no es el más recomendable, especialemente porque diferentes librerías
  pueden usar los mismos nombres para funciones diferentes, y si se las importan así se PISAN entre ellas.
  De todos modos, para facilitar la lectura, vamos a usar esta forma de improtar Numpy en estes instructivo
  y vamos a importar el resto de las librerías usando un alias.
</div>

El tipo de dato `array` nos permite crear vectores y matrices a partir de listas, con las que podemos
hacer operaciones de cálculo.
A continuación algunos ejemplos de cálculo:

<table width="100%">
<thead><tr><th>Cálculo</th><th>Python</th></tr></thead>
<tbody>
<tr><td colspan="2"><center>    Asignación    </center></td></tr>
<tr><td>
$$
  a =
  \begin{pmatrix}
    1 & 0 & 1
  \end{pmatrix}
$$

$$
  b =
  \begin{pmatrix}
    2 & 1 & 3
  \end{pmatrix}
$$

$$
  c =
  \begin{bmatrix}
    -1 \\ 2 \\ 0
  \end{bmatrix}
$$

$$
  A =
  \begin{bmatrix}
    1 & 1 & 1 \\
    2 & 2 & 2 \\
    3 & 3 & 3
  \end{bmatrix}
$$
</td><td><div markdown="1">
```python
from numpy import *

a = array( [ 1 , 0 , 1] )
b = array( [ 2 , 1 , 3] )
c = array( [[ -1 , 2 , 0]] ).T

A = array( [[1,1,1],[2,2,2],[3,3,3]] )
A = array([[1, 1, 1],
           [2, 2, 2],
           [3, 3, 3]])
```
</div></td></tr>
<tr><td colspan="2"><center>    Operaciones elemento a elemento    </center></td></tr>
<tr><td>
$$
  \begin{pmatrix}
    a_0 \cdot b_0 & a_1 \cdot b_1 & a_2 \cdot b_2
  \end{pmatrix}
$$

$$
  \begin{bmatrix}
    a_0 \cdot c_0 & a_1 \cdot c_0 & a_2 \cdot c_0\\
    a_0 \cdot c_1 & a_1 \cdot c_1 & a_2 \cdot c_1\\
    a_0 \cdot c_2 & a_1 \cdot c_2 & a_2 \cdot c_2
  \end{bmatrix}
$$

$$
\begin{pmatrix}
  \frac{a_0}{b_0} & \frac{a_1}{b_1} & \frac{a_2}{b_2}
\end{pmatrix} =
\begin{pmatrix}
  \frac{1}{2} & 0 & \frac{1}{3}
\end{pmatrix}
$$

$$
a + b =
\begin{pmatrix}
  3 & 1 & 4
\end{pmatrix}
$$

$$
  A^2 =
  \begin{bmatrix}
    1 & 1 & 1 \\
    4 & 4 & 4 \\
    9 & 9 & 9
  \end{bmatrix}
$$

$$
  \begin{pmatrix}
    b_0^{b_0} & b_1^{b_1} & b_2^{b_2}
  \end{pmatrix}
$$
</td><td><div markdown="1">
```python
a*b

a*c

a+b

a/b

A**2

b**b
```
</div></td></tr>
<tr><td colspan="2"><center>    Operaciones vectoriales / matriciales    </center></td></tr>
<tr><td>
$$
a \cdot b = 5
$$

$$
a \cdot c =
  \begin{bmatrix}
    -1
  \end{bmatrix}
$$

$$
a \times b =
  \begin{bmatrix}
    -1 & -1 & 1
  \end{bmatrix}
$$

$$
a \cdot A =
  \begin{bmatrix}
    4 & 4 & 4
  \end{bmatrix}
$$

$$
A \cdot c =
  \begin{bmatrix}
    1 \\ 2 \\ 3
  \end{bmatrix}
$$

$$
c^\text{T} \cdot  A^2 \cdot c =
  \begin{bmatrix}
    7
  \end{bmatrix}
$$
</td><td><div markdown="1">
```python
a.dot(b)

a.dot(c)

cross(a,b)

a.dot(A)

A.dot(c)

c.T.dot(A**2).dot(c)
```
</div></td></tr>
</tbody>
</table>


Pero el uso más habitual que le vamos a dar al tipo de dato `array` es guardar y procesar *tiras de datos*,
generalmente resultados de un experimento o de una adquisición, aunque tambien pueden ser datos generados
por nosotros mismos para *simular* el comportamiento de un modelo.

Aqúi algunos ejemplos de generación de datos y de aplicación de funciones.

```python
n = arange(10)   # Lista de los primeros 10 enteros
# array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

n = arange(10)   # Lista de los primeros 10 enteros
# array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

n2 = n**2 - 9    # realizamos cálculo con esos enteros
# array([-9, -8, -5,  0,  7, 16, 27, 40, 55, 72])

x = linspace(0,2*pi,9)   # Generamos 9 numeros entre 0 y pi para el array x
# array([ 0.        ,  0.78539816,  1.57079633,  2.35619449,  3.14159265,
#         3.92699082,  4.71238898,  5.49778714,  6.28318531])

y = 3*sin(x)             # Calculamos el seno de x por 3
y.round(5)               # Con esto nos devuelve los numeros redondeados al decimal 5
# array([ 0.     ,  2.12132,  3.     ,  2.12132,  0.     , -2.12132,
#        -3.     , -2.12132, -0.     ])

sin(x**2)/x              # Ojo con dividir por cero!
# __main__:1: RuntimeWarning: invalid value encountered in true_divide
# array([        nan,  0.73652934,  0.39742005, -0.28351271, -0.13696913,
#         0.07201305, -0.04536937, -0.16888007,  0.15570773])
```

En este ejemplo, para el primer valor de x que es 0 hay una división por cero, que nos devuelve el elemento `nan`: **Not a Number**. Hay que tener cuidado con los cálculos realizados para evitar encontrarse con cuentas imposibles como esta.

## Gráficos con Matplotlib

Para hacer gráficos simples vamos a recurrir a la librería
`matplolib`. De ella, importamos el `pyplot` con el alias `plt`. `plt` incluye funciones para crear los gráficos con bastante detalle de control.
Para un gráfico bidimensional clásico solo hace falta el comando `plt.plot(vec_x, vec_y)``, donde `vec_x` es un vector con las coordenadas x de cada punto a graficar y `vec_y` será un vector con las coordenadas y. Veamos un ejemplo.

```Python
from numpy import *
import matplotlib.pyplot as plt

# cargamos una tira de datos de ejemplo
# Dolar en argentina durante 2018, día por día
dolar = [18.4, 18.45, 18.65, 18.85, 18.85, 18.85, 19.05, 18.95, 18.6, 18.7, 18.7, 18.7,
        18.7, 18.75, 18.9, 18.85, 18.85, 19.0, 19.0, 19.0, 19.1, 19.35, 19.65, 19.55,
        19.55, 19.55, 19.55, 19.55, 19.6, 19.65, 19.4, 19.5, 19.5, 19.5, 19.5, 19.6,
        19.65, 19.95, 20.0, 20.0, 20.0, 20.0, 20.0, 19.9, 19.7, 19.75, 19.75, 19.75,
        19.9, 19.85, 19.9, 19.95, 19.95, 19.95, 19.95, 20.2, 20.2, 20.1, 20.15, 20.25,
        20.25, 20.25, 20.2, 20.35, 20.4, 20.4, 20.25, 20.25, 20.25, 20.2, 20.2, 20.2,
        20.35, 20.2, 20.2, 20.2, 20.2, 20.25, 20.3, 20.25, 20.2, 20.2, 20.2, 20.2,
        20.2, 20.15, 20.15, 20.15, 20.15, 20.15, 20.15, 20.15, 20.2, 20.2, 20.2, 20.2,
        20.2, 20.2, 20.2, 20.15, 20.2, 20.2, 20.2, 20.2, 20.2, 20.2, 20.2, 20.15, 20.2,
        20.2, 20.2, 20.25, 20.25, 20.25, 20.55, 20.55, 20.55, 20.55, 20.55, 20.55,
        21.2, 23.0, 21.8, 21.8, 21.8, 21.9, 22.4, 22.7, 22.7, 23.2, 23.2, 23.2, 24.8,
        24.0, 24.3, 24.3, 24.4, 24.4, 24.4, 24.4, 24.3, 24.4, 24.6, 24.6, 24.6, 24.6,
        24.7, 24.9, 24.9, 24.9, 24.9, 24.9, 24.9, 24.9, 24.9, 24.9, 24.9, 25.3, 25.3,
        25.3, 26.0, 25.8, 26.0, 27.7, 28.3, 28.3, 28.3, 27.6, 27.7, 27.7, 27.5, 27.0,
        27.0, 27.0, 27.0, 27.1, 27.4, 28.1, 28.9, 28.9, 28.9, 28.3, 27.8, 28.1, 28.0,
        27.9, 27.9, 27.9, 27.9, 27.3, 27.4, 27.2, 27.2, 27.2, 27.2, 27.3, 27.5, 27.6,
        27.7, 27.6, 27.6, 27.6, 27.6, 27.5, 27.4, 27.4, 27.4, 27.4, 27.4, 27.3, 27.4,
        27.5, 27.5, 27.3, 27.3, 27.3, 27.4, 27.4, 27.6, 28.1, 29.2, 29.2, 29.2, 30.0,
        29.6, 30.0, 29.8, 29.8, 29.8, 29.8, 29.8, 30.0, 30.2, 30.5, 30.9, 30.9, 30.9,
        30.9, 31.4, 34.0, 37.6, 36.8, 36.8, 36.8, 37.4, 39.0]

dia = arange(2,248)  # días de 1 a 247, aka 4 de septiembre

plt.plot(dia, dolar)
# plt.savefig('01_01_dolar.png')
```

![grafico](01_01_dolar.png "grafico")

Veamos algunas características útiles de `pyplot` y de los datos en formato `array`. Primero, veamos que se pueden mejorar mucho los gráficos:

```python
real  = [5.57, 5.92, 6.02, 6.14, 6.19, 6.1, 5.9, 6.18, 6.63, 6.48, 7.26, 7.01, 7.37, 7.63]
dia_r = [1, 18, 36, 53, 71, 88, 106, 123, 141, 158, 176, 193, 211, 228]

plt.plot(dia  , dolar , '-')
plt.plot(dia_r, real  , 'o-')
plt.xlabel('Día del año [1 = 1ro de Enero ]')
plt.ylabel('Dolar [Pesos Arg]')
plt.title('Evolucion del dolar en 2018')
plt.grid(b=True)
# plt.savefig('01_02_dolar.png')
```

![grafico](01_02_dolar.png "grafico")

```python
#%% Ejemplos de manipulación de vectores y mas gráficos

dolar = array(dolar)

plt.subplot(3,1,1)   # figura con 3 filas de graficos, 1 columna, me posiciono en la primera
plt.plot(dia         , dolar        , '-')
plt.plot(dia[0:115]  , dolar[0:115] , '-', color='blue' , linewidth=2)
plt.plot(dia[219:]   , dolar[219:]  , '-', color='red'  , linewidth=2)
#plt.xlabel('Día del año [1 = 1ro de Enero ]')
plt.ylabel('Dolar\n[Pesos Arg]')
plt.grid(b=True)

plt.subplot(3,1,2)   # fme posiciono en la segunda
plt.plot( dia         , dolar/dolar[0] * 100 - 100       , '-')
#plt.xlabel('Día del año [1 = 1ro de Enero ]')
plt.ylabel('Aumento\nanual [%]')
plt.grid(b=True)

plt.subplot(3,1,3)   # fme posiciono en la segunda
plt.plot( dia[1:]         , diff(dolar)/dolar[1:] *100       , '-')
plt.xlabel('Día del año [1 = 1ro de Enero ]')
plt.ylabel('Aumento\ndiario [%]')
plt.grid(b=True)

plt.tight_layout()

# plt.savefig('01_03_dolar.png')
```

![grafico](01_03_dolar.png "grafico")


## Sistema de archivos, carga y guardado de datos

Para saber donde estamos trabajando, en la línea de comando ejecutamos el comando `pwd`. Allí se guardaran los archivos y desde allí se cargaran datos si uno no especifica una ruta.
Los comandos `ls` y `cd` permiten respectivamente listar los archivos de la carpeta de trabajo y cambiar de directorio.

Vemos como guardar datos.

- <a data-toggle="collapse" href="#ayuda_guardar_numpy" aria-expanded="false" aria-controls="ayuda_guardar_numpy">Guardar y cargar datos en el formato de NumPy<span class="caret"></span></a>

<div id="ayuda_guardar_numpy" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

### Guardar datos
En Python
se debe decir explícitamente qué variables se quiere guardar. Para ello se usa el comado
de NumPy `np.savez()`, cuya [documentación está aquí](https://docs.scipy.org/doc/numpy/reference/generated/numpy.savez.html).

**Syntaxis del comando:**
Si quiero guardar las variables `varX`, `varY` y `texto_mio` en el archivo
`datos.npy` puedo escribir:

```python
savez('datos.npz', varX=varX, varY=varY, texto_mio=texto_mio)
```
El primer argumento es el nombre del archivo en formato de texto.
Luego, cada argumento que sige es una variable a guardar. Se lee así:
`varX=varX` significa "con el nombre `varX` (lo que está antes del igual)
guardá el objeto llamando `varX` (lo que está después del igual)"

Recordar que, si no se especifica la ruta completa, el archivo será creado en la carpeta de trabajo actual (que se puede averiguar ejecutando el comando `pwd`).

### Recuperar datos
En Python, NumPy lee los archivos `.npz` con la instrucción `np.load` y los carga
en un objeto nuevo con nombre.
Por ejemplo, si se trata de recuperar el archivo guardado en el ejemplo anterior:

```python
datos = load('datos.npz')
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
savez('datos.npz', varX=varX, varY=varY, texto_mio=texto_mio)

```

Luego los recuperamos en el objeto `datos`:

```python
datos = load('datos.npz')

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



- <a data-toggle="collapse" href="#ayuda_guardar_matlab" aria-expanded="false" aria-controls="ayuda_guardar_matlab">Guardar y cargar datos en el formato de Matlab<span class="caret"></span></a>

<div id="ayuda_guardar_matlab" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

Para guardar un archivo de forma que lo pueda leer Matlab u Octvave, es necesario
guardar los datos en un Diccionario y luego usar librerías de `scipy`.

```python
import scipy.io as sio    # input / output de SciPy

# Creamos un diccionario
adict = {}
adict['vector1'] = vector_que_queremos_guardar
adict['texto_2'] = 'este es un texto'
adict['nombre_de_matris'] = matris_que_queremos_guardar

sio.savemat('NOMBRE_DEL_ARCHIVO.mat', adict)

# Para recupearar los datos:
bdict = io.loadmat('NOMBRE_DEL_ARCHIVO.mat')
```

</div>

- <a data-toggle="collapse" href="#ayuda_guardar_txt" aria-expanded="false" aria-controls="ayuda_guardar_txt">Guardar y cargar datos en el formato de texto<span class="caret"></span></a>

<div id="ayuda_guardar_txt" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

Para guardar datos en un archivo, concatenamos los arrays en un array y guardamos con `savetxt`

```python
datos = array([velocidad,error,aceleracion ])
savetxt('datos.txt', datos.T , delimiter=',', newline='\n', header='', footer='', comments='# ')
```

Lo recuperamos con `loadtxt`

**datos.txt**
```
# Datos de velocidad y aceleracion
#
#  Velocidad [m/s]        Error velocidad [m/s]     Aceleracion [m/s2]
1.490837831787444889e+00,2.778988422540417114e-01,1.490837831787444889e+00
5.520673232195780145e+01,1.743462121778538154e-01,1.625414884985131536e+00
1.093351066876646769e+02,1.586915024865563906e-01,1.351293850645653771e+00
1.456974175099817330e+02,1.727037889438612361e-01,7.753017980600711567e-01
1.620603843035981697e+02,1.450515660269059148e-01,1.910305665224660276e-01
1.630704786086546960e+02,1.517261340087170951e-01,-1.156524575701078960e-03
```

```python
datos = loadtxt('datos.txt', comments='#', delimiter=',')

velocidad   = datos[0,:]
vel_error   = datos[1,:]
aceleracion = datos[2,:]
```

</div>

## Funciones útiles para hacer cálculos

Las funciones `sum`, `mean` y `std` nos permiten obtener rápidamente la suma completa, el promedio y la desviación estándar de todos los elementos de un vector.

```python
datos = array([ 4,  0,  4,  2, 19, 15,  4,  8,  2,  9])

print('promedio',            mean(datos)  )
print('suma',                 sum(datos)  )
print('desviacion estandar',  std(datos)  )
print('Num elementos',        len(datos)  )
```

La función diff nos devuelve un vector con la resta entre elementos consecutivos del vector de entrada (osea la diferencia entre cada elemento y su siguiente).

```python
diff(datos)
#  array([ -4,   4,  -2,  17,  -4, -11,   4,  -6,   7])
```

La combinación de `diff` con operaciones nos permite, por ejemplo, calcular la derivada

```python
#%%
datos = loadtxt('datos.txt', comments='#', delimiter=',')

tiempo      = datos[:,0]
velocidad   = datos[:,1]
vel_error   = datos[:,2]
aceleracion = datos[:,3]

plt.plot(tiempo  , aceleracion , 'o' , label='datos')
plt.plot( (tiempo[:-1]+tiempo[1:])/2  , diff(velocidad)/diff(tiempo) , '-' , label='calculado' )
plt.xlabel('tiempo [seg]')
plt.ylabel('Aceleracion [m/s2]')
plt.legend()
plt.grid(b=True)

# plt.savefig('01_04_derivada.png')
```

![grafico](01_04_dolar.png "grafico")

También se puede realizar la integral numérica con el comando `trapz` (el área debajo de la curva) y `cumsum` (parecido, pero acumulativo para cada punto):

```python
plt.subplot(2,1,1)
plt.fill_between(tiempo  , zeros(len(tiempo)) ,velocidad , alpha=0.5 )
plt.plot(tiempo  , velocidad , 'o-' )
plt.ylabel('velocidad [m/s]')
plt.xlabel('tiempo [seg]')
plt.grid(b=True)

plt.subplot(2,1,2)
plt.plot(tiempo  , cumsum(velocidad * mean(diff(tiempo)) ) , '.-' , label='datos')
plt.xlabel('tiempo [seg]')
plt.ylabel('recorrido [m]')
plt.grid(b=True)

plt.tight_layout()
# plt.savefig('01_05_integral.png')
```

![grafico](01_05_integral.png "grafico")


## Estructuras de programación
No es el objetivo de este instructivo enseñar a programar. Pero vale la pena mencionar que existen todas las estructuras de programación clásicas en Python. Solo como ejemplo mencionaremos la del condicional (if/elif/else) y la de iteración (for). Por ejemplo, el condicional siguiente:

```python
if CONDICION:
    print('se cumplió la condicion')
elif CONDICION2:
    print('se cumplió la condicion 2')
else:
    print('NO se cumplió ninguna')
```

Los bloques de código se identifican por *identación* , osea, por cuantos *tab* tienen por delante. Lo mismo ocurre para el `for`, un bucle que se repite una vez por cada elemento que se le ingresa como entrada:

```python
for numero in [5,6,9,7,1,5,6,8]:
    print('El número en esta iteración es: ', numero)
    print('El número al cuadrado es:', numero**2 )
```

Las iteraciones y condicionales se pueden combinar para realizar procesamiento en masa.


```python

numeros_menores_al_anterior = []

for i,numero in enumerate([5,6,9,7,1,5,4,8]):
    if i>0:
        if numero <= numero_anterior:
            numeros_menores_al_anterior.append(  numero  )
    numero_anterior = numero

print( numeros_menores_al_anterior )
# [7, 1, 4]
```

## Funciones definidas por el usuario

La instrucción `def` nos permite definir funciones hechas por el usuario para utilizar en el codigo.
Se deben incluir los parámetros de entrada y explicitar con `return` lo que devuelve a la salida.

```python

def sinc_cuadrada(x):
    if x!=0:
        rta = sin(x) / x
        rta = rta**2
    else:
        rta = 1
    return rta

sinc_cuadrada(12)
# 0.0019993784467465382

sinc_cuadrada(0)
# 1
```


{% include page_navbar.html up=1 %}
