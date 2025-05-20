---
title: Análisis de datos y Ajustes
description: Herramientas de análisis y Ajsutes
layout: page
mathjax: true
navbar: labo2
---


{% include page_navbar.html %}

## Introducción al análisis de datos

En física **analizamos los fenómenos** proponiendo **modelos matemáticos** que pueden describirlos cualitativa y cuantitativamente para hacer **predicciones** luego. El fenómeno es descripto recolectando datos de **diferentes variables de interés** a las que después se le buscan relaciones. La mayoría de **las leyes físicas son relaciones funcionales entre variables de un sistema**. Por ende, al desarrollar modelos buscamos encontrar funciones que vinculen las diferentes variables y que sean consistentes con los datos que relevamos.

Dado un conjunto de datos puede haber diferentes funciones que los puedan describir cualitativamente. La pregunta que nos queremos responder es: **Dados dos modelos: ¿cual se corresponde mejor con los datos?**. Buscamos poder evaluar cuantitativamente la fidelidad de un modelo con los datos hallados. Para eso vamos a utilizar algunas herramientas matemáticas del análisis de variables aleatorias y métodos numéricos de análisis. Vamos a introducir esas herramientas para luego ver como las utilizaremos.


## Media, Varianza y Desviación estándar

Supongamos que tenemos un experimento/sistema estable en el cual medimos varias veces el valor de una variable obteniendo diferentes resultados en forma aleatoria. Si no cambiamos ninguna variable del sistema, la aleatoriedad proviene de alguna fuente que no controlamos. Entonces necesitamos hacer algo de análisis para extraer el dato que nos interesa. Por ejemplo, si notamos que la mayoría de los valores obtenidos se acumulan en algún lugar es razonable tomar el promedio de los valores obtenidos como el valor de la variable que queríamos medir. Si tenemos un conjunto de N datos $x_i$ resultantes de las mediciones de una variable $A$, asumimos que el valor de $A$ es:

$$
\huge
A  \leftarrow  \bar{x} \equiv \sum_i \frac{x_i}{N}
$$

<a data-toggle="collapse" href="#datos_simulados" aria-expanded="false" aria-controls="datos_simulados">preparación datos simulados<span class="caret"></span></a>

<div id="datos_simulados" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

```python
from numpy import *
import matplotlib.pyplot as plt

# Generador de aleatoriedad
random.seed(1024)

# Preparamos datos simulados
datos = ( random.randn(850)*100-150   ).astype(int).tolist()
datos+= ( random.randn(150)*30 +10   ).astype(int).tolist()
datos = array(datos)
datos = datos[ random.permutation( len(datos) ) ]

x = datos.copy()
```
</div>

```python
sum(x)/len(x)
# -126.417

mean(x)
# -126.417
```

Veamos cómo se ven los datos:

```python
plt.plot(                   x , arange(len(x)), '.' , label='datos')
plt.plot( ones(len(x))*mean(x), arange(len(x)), '-' , label='media', linewidth=5 , alpha=0.7)
plt.yticks([])
plt.legend()
plt.xlabel('x')
# plt.savefig('02_01_media.png')
```
![grafico](02_01_media.png "grafico")


Para ponerle una cota de error de esa variable es necesario analizar cuanto se dispersan los datos respecto del valor promedio. Esto se puede hacer, por ejemplo, calculando la *desviación estándar* $\sigma = \sqrt{var(x)}$ , que es la raíz cuadrada de la varianza:

$$
\large
Err_A  \leftarrow  \sigma_x \equiv \sqrt{ \sum_i \frac{(x_i - \bar x)^2}{N} }
$$

```python
varA = sum(  (x - mean(x))**2  )/len(x)
varA = var(x)
# 12250.093111

devA = sqrt(varA)
devA = std(x)
# 110.68013873771572


plt.plot(                   x , arange(len(x)), '.' , label='datos')
plt.plot( ones(len(x))*mean(x), arange(len(x)), '-' , label='media', linewidth=5 , alpha=0.7)
plt.fill_between( [ mean(x)-std(x), mean(x)+std(x) ]  , [0,0] , [len(x)]*2 , label='std', alpha=0.5 , zorder=1)

plt.yticks([])
plt.legend()
plt.xlabel('x')
# plt.savefig('02_02_std.png')
```

![grafico](02_02_std.png "grafico")


<div class="alert alert-info" role="alert" >
  <strong>OJO!:</strong> Estrictamente, para poder decir QUÉ información nos da $\sigma_x$ sobre el error de la variable $A$ necesitamos conocer la distribución estadística asociada a esa variable. Por ejemplo, para una distribución Normal (algo que es muy habitual) el 68.27% de las veces que se mida el valor estará entre $\bar x - \sigma_x$ y $\bar x + \sigma_x$.
</div>

Para visualizar mejor los datos, con mayor detalle, se puede recurrir a herramientas gráficas. Por ejemplo, hacer un
**histograma** con `plt.hist` es una forma rápida de tener una idea de la distribución de los datos.

```python
plt.subplot(211)
plt.plot(                   x , arange(len(x)), '.' , label='datos')
plt.plot( ones(len(x))*mean(x), arange(len(x)), '-' , label='media', linewidth=5 , alpha=0.7)
plt.fill_between( [ mean(x)-std(x), mean(x)+std(x) ]  , [0,0] , [len(x)]*2 , label='std', alpha=0.5 , zorder=1)

plt.yticks([])
plt.legend()
plt.xlabel('x')
plt.grid(True)

plt.subplot(212)
plt.hist(x,30)
plt.ylabel('Conteo')
plt.xlabel('valores x')
plt.grid(True)

plt.tight_layout()
# plt.savefig('02_03_hist.png')
```

![grafico](02_03_hist.png "grafico")


## Covarianza y Correlación


Ahora supongamos que tenemos un experimento en el que medimos varias veces dos variables al mismo tiempo; por ejemplo x e y. Cada una de estas variables muestran un comportamiento aleatorio, aunque pueden mostrar cierta tendencia en su evolución temporal (Ej: x tiende a crecer con el tiempo). Nos interesa saber si comparten información sobre el sistema o si son variables que evolucionan de forma independiente. Si para cada medición $i$ obtuvimos valores $x_i$ y $y_i$ podemos graficar uno respecto del otro. Estos son posibles ejemplos de resultados:

```python
x1 = random.randn(100)*10
y1 = (random.rand(100)-0.5)*10+8

plt.subplot(2,2,1)
plt.plot(x1,y1,'.')
plt.ylabel('y1')
plt.xlabel('x1')

plt.subplot(2,2,2)
plt.plot(x1,'.', label='x1')
plt.plot(y1,'.', label='y1')
plt.ylabel('valor')
plt.xlabel('posicion')
plt.legend()


plt.subplot(2,2,3)
plt.hist(x1,20)
plt.yticks([])
plt.xlabel('x1')

plt.subplot(2,2,4)
plt.hist(y,20)
plt.yticks([])
plt.xlabel('y1')

plt.tight_layout()
# plt.savefig('02_04_cov.png')
```

![grafico](02_04_cov.png "grafico")


En el ejemplo no se puede apreciar una dependencia clara de una variable sobre otra. Veamos otro ejemplo:

```python
random.seed(1024)
t = linspace(0,5*pi,100)
x2 = (sin(t)+1)+t/2 + random.randn(100)/2
y2 = ((sin(t)+1)+t/2)*2.1+3 + random.randn(100)/2

plt.subplot(2,2,1)
plt.plot(x2,y2,'.')
plt.ylabel('y2')
plt.xlabel('x2')

plt.subplot(2,2,2)
plt.plot(x2,'.', label='x2')
plt.plot(y2,'.', label='y2')
plt.ylabel('valor')
plt.xlabel('posicion')
plt.legend()


plt.subplot(2,2,3)
plt.hist(x2,20)
plt.yticks([])
plt.xlabel('x2')

plt.subplot(2,2,4)
plt.hist(y2,20)
plt.yticks([])
plt.xlabel('y2')

plt.tight_layout()
# plt.savefig('02_05_cov.png')
```

![grafico](02_05_cov.png "grafico")

En este conjunto de datos, en cambio, pareciera haber una relación lineal entre x e y, un tanto distorsionada. Para poder caracterizar cuantitativamente este hecho se puede calcular la **covarianza** que mide el cambio mutuo entre las variables:

$$
\large
covarianza(x,y) \equiv
\sum_i
\frac{ (x_i - \bar x) \cdot (y_i - \bar y) }{N}
$$

```python
cov_xy2 = sum( ( x2-mean(x2) )*( y2-mean(y2) )  ) / ( len(x2)-1 )
# 11.986200769263622

cov(x2,y2)

# array([[  6.01124359,  11.98620077],
#        [ 11.98620077,  25.33765995]])

cov_xy2 = cov(x2,y2)[0,1]
# 11.986200769263622

cov_xy1 = cov(x1,y1)[0,1]
# 8.823807524442465
```

Si los valores de x e y tienden a aumentar y disminuir conjuntamente, la covarianza será un numero positivo. Si cuando una de las variables aumenta la otra disminuye, entonces será negativa. Si los comportamientos son independientes tendera a ser cero. Vale notar que la “auto-covarianza” es la varianza:
$covarianza(x,x) =$ `cov(x,x)` $= var(x) =$ `var(x)`.
De los ejemplos anteriores, en el primer caso $covarianza(x,y)=8.82$ y en el segundo $covarianza(x,y)=11.98$.

La covarianza nos da una idea de si dos variables comparten información de algún modo, pero su valor absoluto es poco útil, pues varía mucho entre diferentes conjuntos de datos. Para evitar este problema se puede usar la **correlación** o
**coeficiente de correlación de Pearson** $r$ (`corrcoef`).

$$
correlacion(x,y) = \frac{covarianza(x,y)}{ \sigma_x \sigma_y }
$$

```python
corrcoef(x1,y1)
# array([[ 1.        ,  0.29015905],
#        [ 0.29015905,  1.        ]])

corrcoef(x2,y2)
# array([[ 1.        ,  0.97121668],
#        [ 0.97121668,  1.        ]])

cor1 = cov_xy1/( std(x1,ddof=1) * std(y1,ddof=1) )
cor1 = corrcoef(x1,y1)[0,1]
# 0.29015904574546342

cor2 = cov_xy2/( std(x2,ddof=1) * std(y2,ddof=1) )
cor2 = corrcoef(x2,y2)[0,1]
# 0.97121668087762869
```

Se puede demostrar fácilmente que si x e y tienen una dependencia lineal del tipo $y_i = A \cdot x_i + B$ entonces la correlación da:

$$
r =
correlacion(x,y) =
\frac{covarianza(x, A x + B)}{\sigma_x \sigma_y} =
\frac{ A \,\cdot covarianza(x,x) } { \sigma_x \; |A|\sigma_x } =
\frac{A}{|A|}=
\pm 1
$$

Cuando $r=1$ se puede decir que hay una perfecta *correlación* lineal entre las
variables y cuando $r=-1$ hay una perfecta *anticorrelación*.

Cuando se tienen los conjuntos de valores medidos $x_i$ e $y_i$ y se realiza un ajuste lineal de los datos con el modelo
$f_i = A \cdot x_i + B$, **el cuadrado de la correlación entre los datos medidos $y_i$ y los valores del ajuste $f_i$**:
$r^2 = correlacion(y,f)^2$
es denominado **coeficiente de determinación**. $r^2$ puede ser interpretado como “el porcentaje de la varianza de  y que se puede explicar a partir de x”. Muchos programas de  análisis de datos ofrecen funciones para hacer una regresión lineal de los datos y reportan el valor de $r^2$ entre los resultados. **Para modelos no lineales el coeficiente de determinación no coincide con esta definición** y esta interpretación deja de ser estrictamente válida.

$r^2$ es una estimación buena sobre **“cuan bien son explicados los datos por un modelo lineal”**, pero no alcanza por si solo para saber si una particular elección de parámetros A y B hacen un buen ajuste. Para ello hay que tener en cuenta otras consideraciones que se comentan a continuación.

## Ajuste de datos mediante cuadrados mínimos

El método de cuadrados mínimos es uno de los más usados para ajustar los parámetros de una función que intenta modelar un conjunto de datos. El método consiste en lo siguiente:

Se tienen N pares de valores de mediciones asociadas a un fenómeno: $x_i$ e $y_i$ .
Se tiene una función $F$ que depende de alguna cantidad de parámetros (propongamos por ejemplo que depende de A y B)
y se quieren encontrar los parámetros A y B tal que los valores
$f_i = F_{A,B}(x_i)$ aproximen *"lo mejor posible"* a $y_i$.
El método de cuadrados mínimos propone minimizar la cantidad $s^2$, que consiste en la suma cuadrática de los residuos:

$$
res_i = y_i-f_i
$$

$$
s^2(A,B) =
\sum_i {res_i\,}^2 =
\sum_i (y_i-f_i)^2 =
\sum_i \left[ y_i-F_{A,B}(x_i) \right]^2
$$

Osea, minimizar la suma cuadrática de los “residuos”. **Eso reduce el problema de “buscar los parámetros de un modelo que ajuste los datos”
a un problema de minimización**. Hay que notar que la función $s^2$
se construye a partir de los N datos medidos pero sólo tiene como variables a los parámetros (en este caso, $A$  y $B$).
Por ejemplo, si el modelo es una recta $F_{A,B}(x)\,=\, A \cdot x + B$
la función $s^2$ será una combinación de térmicos con $A$, $B$, $A^2$ y $B^2$ (un paraboloide en 3D) y se deberá hallar las coordenadas del mínimo.

![grafico](02_06_chi2.png "grafico")


Para el caso lineal existen métodos muy eficientes para hallar los  parámetros que corresponden al mínimo global.
Pero cuando se utilizan modelos no lineales la función $s^2$ puede resultar más compleja.
Si se usan dos o más parámetros, $s^2$ puede ser una superficie con varios mínimos locales y no es trivial hallar el mínimo global.
No nos vamos a detener a explicar cómo funcionan los diferentes algoritmos de minimización, tema que se trata extensamente en la materia
"Elementos de calculo numérico". Simplemente es necesario ser conscientes de cómo funciona el método.
Se parte de un conjunto de parámetros iniciales y se recorre el camino de mayor pendiente hacia el mínimo.
En los casos de ajustes no lineales, encontrar el mínimo global dependerá de la elección de esos parámetros iniciales.

El valor de $s^2$ puede usarse para estimar la bondad de un ajuste. Si se comparan varios modelos sobre un mismo conjunto de datos,
el que tenga menor $s^2$ será, en principio, un mejor ajuste. Sin embargo, $s^2$ no puede usarse para saber si un modelo en sí mismo es un buen modelo,
pues su valor absoluto no tiene un significado intrínseco.

Si se quiere tener en cuenta que algunos datos fueron medidos con mayor precisión que otros se puede construir la función *(weighted s^2)*:


$$
\large
{s_{w}}^2(A,B) =
\sum_i \frac{(y_i-f_i)^2}{ {\delta y_i}^2 }
$$

A los efectos prácticos de esta guía, se presentara a continuación un ejemplo de como ajustar una serie de datos con dos modelos diferentes usando una implementación de cuadrados mínimos.

## Ejemplo de Ajuste Lineal

Funciones simples para ajustes polinómicos: `polyfit` y `polyval`:

```python
#%%  Ejemplo de ajuste lineal simple

param = polyfit(x2,y2,1)

print('A*x+B')
print('A:',param[0] , '   B:',param[1])

# A*x+B
# A: 1.99396357831    B: 3.39185944525

mod = polyval(param,x2)

#plt.plot(x2, y2   ,'.', label='datos')
plt.errorbar(x2, y2, yerr=0.5, fmt='.', label='datos')
plt.plot(x2, mod  ,'-', label='modelo')

plt.xlabel('x2')
plt.ylabel('y2')
plt.legend()
plt.grid(True)

plt.tight_layout()
# plt.savefig('02_07_ajuste_lineal.png')

chi2 = sum( (y2 - mod)**2 )
# 142.3236051732523
r    = corrcoef(x2,y2)[0,1]
# 0.97121668087762869

r2   = r**2
# 0.9432618412149576
```

![grafico](02_07_ajuste_lineal.png "grafico")







## Estimadores de bondad de ajuste e intervalos de confianza

<div class="alert alert-info" role="info" >
<strong>Atención:</strong>
A continuación se comentarán algunos conceptos estadísticos útiles para
poder valorar de forma CUANTITATIVA qué tan buenos es un ajuste o qué tan bien
pudimos estimar los parámetros de ese ajuste. Entender algunas de estas herramientas
requiere un estudio más profundo de estadística y probabilidad, que quedará fuera
de los alcances de este instructivo. Pero se tratarán de introducir los conceptos
básicos de forma que se pueda dar uso a las herramientas, aunque no se explique por
qué o cómo funcionan.
</div>


Para poder reportar que el "modelo propuesto ajusta adecuadamente los datos" debemos
poder valorar en forma numérica la **bondad de ese ajuste**. Una de las formas más usuales para el acso lineal es una herramienta que ya vimos:
*calcular la correlación entre la predicción del modelo y los datos medidos*.
Este estimador de bondad es reportado como el [`r` de Pearson ](https://es.wikipedia.org/wiki/Coeficiente_de_correlaci%C3%B3n_de_Pearson).
En el ejemplo de abajo guardaremos este valor en la variable `r = corrcoef(y2,prediccion_modelo)[0,1]`.
Para el caso de un ajuste lineal, `r` nos dice que mientras más cercano a `1` sea más se parecen los datos a un modelo lineal. Pero **OJO**: Este estimador no nos garantiza que los parámetros hallados para el modelo lineal sean óptimos. Sólo nos asegura que el comportamiento de los datos es lineal.

Una herramienta útil para analizar es calcular y estudiar los residuos. Si los datos que
tenemos son resultados de un modelo que realmente es lineal más  "puro ruido" (no vamos a ser muy precisos en la definición de esto) los residuos deberían estar distribuidos en
torno a cero... con masomenos la misma cantidad de datos positivos que negativos.
Un estimador útil, que no se suele reportar pero nos sirve a nosotros para evaluar, es
calcular el promedio de los residuos y ver si es cercano a cero.

Un estimador de bondad de ajuste que se usa muy seguido (y que sirve para casos de
ajuste polinomiales y no lineales) es el [**Coeficiente de determinación `R2`**](https://es.wikipedia.org/wiki/Coeficiente_de_determinaci%C3%B3n)
( por $R^2$ ). Este estimador compara la _varianza de los residuos_ `SSE`
(por _Resitual Sum of Squares_) con la _varianza de los datos_ `SST`
(por _Total Sum of Squares_) de la forma:

`R2 = 1 - SSE/SST `

Esta cantidad representa "la proporción de la varianza total de los datos que es explicada por el modelo propuesto". Si el valor se acerca a 1, quiere decir que el 100% de la varianza la puede explicar nuestro modelo de forma exitosa. Mientras más cercano a
`1` sea `R2`, mejor es la descripción que nuestro modelo hace de los datos.

**Solamente en el caso de ajustes lineales** el Coeficiente de determinación es igual a el cuadrado de `r` de Pearson: $R^2 = r^2$ . Esto es una igualdad matemática que surge del cálculo de esas cantidades. Para otro tipo de ajustes estos valores no tienen por que coincidir.

Por último, el resultado de un ajuste a los datos nos proporciona un conjunto de
parámetros que mejor permiten predecir los datos con ese modelo.
Pero: **¿Que tan bien determinados están esos parámetros?**. Queremos poder asignarle
un valor de certeza a los parámetros hallados. Una cantidad numérica que nos represente cuanto sabemos sobre el valor más probable de ese parámetro (si suponemos que el modelo describe razonablemente bien lo datos).

Para poder hacer eso debemos primero obtener el **Error Estandar** de los parámetros hallados. Esta información se halla disponible en la **Matriz de Covarianza de los parámetros** (`pcov` en el código). Cuando tenemos modelos complejos con muchos parámetros, esta matriz permite identificar parámetros redundantes o que no son del todo independientes. Pero en este caso, sólo nos interesa la diagonal de esa matriz. En la diagonal esta la "auto-covarianza"  de cada parámetro, que como dijimos, es la **varianza**. Por ende, calculando la raíz raíz de los valores de la diagonal podemos obtener los Errores Estandar de cada parámetro.

Pero falta un detalle más. El Error Estándar (`SE` por la siglas en inglés) es una cantidad estadística que nos permite establecer un intervalo para un parámetro $a$:
$(\bar a - SE_a ,\bar a + SE_a )$. **Dentro de este intervalo hay una determinada probabilidad de que se halle el valor REAL del parámetro $a$**. Estamos haciendo una diferencia entre el valor "real" del parámetro $a$ (que desconocemos) y el valor estimado que tenemos $\bar a$. Ahora, esa "determinado probabilidad" depende de la
distribución estadística del parámetro.

Si se cumple que:
  * Nuestros datos tienen todos **Errores Normales** ...
  * Lo que implica que los residuos van a tener errores normales (**centrados en cero!**)
  * Entonces los **parámetros del ajuste lineal** van a tener una **distribución estadística llamada T-Student**

Esta información nos permite relacionar el Error Estandar de los parámetros hallados con
un intervalo que podemos fabricar para que contenga con una probabilidad arbitraria
el valor real de nuestro parámetro. Usando todo esto, tenemos:



![grafico](02_09_ajuste_lineal.png "grafico")


Resultados obtenidos:

```txt
A: 1.9939635783103946    B: 3.3918594452493016
R-squared     0.9432618412149577
R-sq_adjusted 0.9420919822709363
r-pearson     0.9712166808776282

Error Estandard (SE):
parametro[  0]:  1.9939635783103946  ±  0.049399854487291284
parametro[  1]:  3.3918594452493016  ±  0.2801405695864281

Intervalo de confianza al 95.0%:
parametro[  0]:  1.9939635783103946  ±  0.09803240348344393
parametro[  1]:  3.3918594452493016  ±  0.5559298430088225
```



```python
#%%  Ejemplo de ajuste lineal con intervalos de confianza

# Con la misma serie de datos que antes, hacemos un ajute por un
# polinomio de grado 1 (lineal), pidiendo la información de la
# COVARIANZA de LOS PARÁMETROS
parametros , pcov = polyfit(x2,y2,1 , cov=True)

# parametros: parametros ajustados.  Y = parametros[0] * X + parametros[1]
# pcov      : Matris de covarianza DE LOS PARÁMETROS

print('A*x+B')
print('A:',parametros[0] , '   B:',parametros[1])

# A*x+B
# A: 1.993963578310395    B: 3.391859445249304

# Calculamos la predicción que hace el modelo para los parámetros hallados
prediccion_modelo = polyval(parametros,x2)

# Graficamos datos y modelo ajustado
plt.subplot(211)
plt.errorbar(x2, y2, yerr=0.5,   fmt='.', label='datos')
plt.plot(    x2, prediccion_modelo  ,'-', label='modelo')
#plt.xlabel('x2')
plt.ylabel('y2')
plt.legend()
plt.grid(True)

I        = x2.argsort()          # Esto es solo para ordenar los valores de x2 en forma creciente
residuos = y2-prediccion_modelo  # Calculamos los residuos

# Graficamos residuos
plt.subplot(212)
plt.plot(    x2[I], residuos[I]  ,'.-', label='residuos')
plt.xlabel('x2')
plt.ylabel('y2')
plt.legend()
plt.grid(True)

plt.tight_layout()
# plt.savefig('02_08_ajuste_lineal_cov.png')

# La suma de cudrática de los residuos nos permite comparar ESTE ajuste
# con OTROS ajustes para EL MISMO CONJUNTO DE DATOS
chi2 = sum( residuos**2 )
# 142.3236051732523


# Calculamos el r-Pearson
r    = corrcoef(y2,prediccion_modelo)[0,1]  # Coeficiente de Pearson
# 0.9712166808776288

r2   = r**2
# 0.9432618412149578


# Calculamos alguna cantidades que nos sirven para algunos estimadores
N         = len(y2)   # Número de pares de datos ajustados
P         = 2         # Cantidad de parámetros del modelo. Para una lineal, son dos: a y b
SSE       = sum(( y2 - prediccion_modelo )**2 )    # Resitual Sum of Squares
SST       = sum(( y2 - mean(y2))**2)               # Total Sum of Squares

# http://en.wikipedia.org/wiki/Coefficient_of_determination
# Expresa el porcentaje de la varianza que logra explicar el modelos propuesto
R2        =  1 - SSE/SST                           # Coeficiente de determinación
R2_adj    = 1-(1-R2) * (N-1)/(N-P-1)              # Coeficiente de determinación Ajustado   

# El coeficiente R2 ajustado hace una corrección para evitar un sesgo que se produce
# Cuando tenemos un número de parámetros alto comparado con el número de datos.
# Es el que suele ser reportado en un informe de laboratorio

# El error estandar es la raiz de la varianza
# En la diagonal de la matris de covarianza de los parámetros está la varianza de
# cada parámetro en particular. Extrayendo la diagonal y calculando la raíz tenemos
# el Error Estandar
SE        = sqrt(diag( pcov  ))                        # Standar Error / Error estandar de los parámetros


# Cargamos función estadística t-student que nos permite calcular a partir de
# el error estandar cual es el intervalo de confianza de un parámetro
from scipy.stats.distributions import  t


# Para un intervalo de 95% de confianza, necesitamos un alpha de 5% == 0.05
alpha=0.05

sT = t.ppf(1.0 - alpha/2.0, N - P ) # student T multiplier
CI = sT * SE

print('R-squared    ',R2)
print('R-sq_adjusted',R2_adj)
#print('chi2_test    ',chi2_test)
print('r-pearson    ',r)
#print('p-value      ',p_val)
print('')
print('Error Estandard (SE):')
for i in range(P):
    print('parametro[{:3d}]: '.format(i) , parametros[i], ' ± ' , SE[i])
print('')
print('Intervalo de confianza al '+str((1-alpha)*100)+'%:')
for i in range(P):
    print('parametro[{:3d}]: '.format(i) , parametros[i], ' ± ' , CI[i])

```













{% include page_navbar.html up=1 %}
