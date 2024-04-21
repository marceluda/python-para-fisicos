---
title: Orbitales atómicos
description: Graficar orbitales atómicos
layout: page
mathjax: true
plotly: true
navbar: labo2
---

<div class="alert alert-danger" role="alert" >
  <strong>Aviso:</strong> La página está en construcción. El contenido está basado en reportar los contenidos básicos
  necesarios para visualizar estados electrónicos usando Python.
  La rigurosidad de algunas afirmaciones teórica está sujeta aún a una revisión más exhaustiva.
</div>


Uno de los grandes éxitos de la teoría de la mecánica cuántica fue poder modelar de forma correcta el átomo de hidógeno,
resolviendo múltiples problemas de los modelos previos. No voy a describir acá el detalle de dicho modelo ni hacer una introducción
a la mecánica cuántica. Simplemente, voy a enumerar conceptos, ecuaciones y métodos que nos permiten visualizar cómo se distribuyen
los electrones dentro de un átomo según el [modelo de Schrödinger](https://en.wikipedia.org/wiki/Hydrogen_atom#Schr%C3%B6dinger_equation).

Repositorio de archivos programados en python:

<center>
<a href="https://github.com/marceluda/python-para-fisicos/tree/master/tutoriales/orbitales_atomicos" class="btn btn-primary btn-lg" role="button">
Scripts python
</a>
</center>


## Modelo atómico

El modelo atómico de Schrödinger parte de resolver la ecuación de Schrödinger en 3D para un potencial central para un electrón:

La ecuación de Schrödinger en 3D es:

$$
i \hbar \frac{\partial \psi}{\partial t}
=
\left ( - \frac{\hbar^2}{2m} \nabla^2  + V(r) \right) \psi
$$

Al proponer una solución en esféricas separable $\psi(r,\theta,\phi) = R(r) \cdot Y(\theta)$ , y depejar $Y$ obtenemos los armónicos esféricos.
De esta forma se puede separar la ecuación diferencial en dos partes, una que depende de $r$ y otra de los ángulos.
Ambas partes son equivalentes a una constante que depende de números cuánticos $n$ y $l$.


Por su lado, los Armónicos esféricos requieren un número cuántico más para describir su solución: $m$:

$$
Y^m_l(\phi,\theta) = \epsilon \sqrt{\frac{2n+1}{4\pi} \frac{(l-m)!}{(l+m)!}}
      e^{i m \phi} P^m_l(\cos(\theta))
$$

donde $\epsilon = (-1)^m$ para $m>=0$ y $1$ para $m$ negativos, lo que se conoce como la [fase de Condon-Shortley](https://en.wikipedia.org/wiki/Spherical_harmonics#Condon%E2%80%93Shortley_phase).
$P^m_l(x)$ son los [Polinomios Asociados de Legendre](https://en.wikipedia.org/wiki/Associated_Legendre_polynomials).

Esto modela la dependencia angular (en coordenadas esféricas) de la función de onda.



Luego, se propone un $V(r)$ culombiano:

$$
V(r) = - \frac{e^2}{4 \pi \epsilon_0} \, \frac{1}{r}
$$

La solución de la parte radial para este potencial da:

$$
\tilde{R}_{n,l} = \left( \frac{2 r}{n\,a} \right)^l e^{-\frac{r}{n\,a}} L_{n-l-1}^{2l+1} \left( \frac{2r}{n\,a} \right)
$$

con $a$ el radio de Bohr y $L_{n-l-1}^{2l+1}$ son los [Polinomios Asociados de Laguerre](https://en.wikipedia.org/wiki/Laguerre_polynomials#Generalized_Laguerre_polynomials):

$$
a = \frac{ 4 \pi \epsilon_0 \hbar^2}{m \, e^2} = 0.529 \,\, \unicode{xC5}
$$

Finalmente, hay que agregar un factor de normalización:

$$
N_{n,l} =
\sqrt{  \left( \frac{2}{n\,a} \right)^3  \frac{(n-l-1)!}{2n[(n+l)!]} }
$$

De modo que las soluciones $R_{n l}$ sean ortonormales:

$$
 R_{n,l} = N_{n,l} \cdot \tilde{R}_{n,l}
$$

De forma tal de tener la solución:

$$
\psi_{n,l,m}=
R_{n,l} \,\cdot\, Y^m_l(\phi,\theta)
$$


donde $n,l,m$ son los números cuánticos que caracterizan al estado. $n$ es el nivel, $l$ es el orbital y $m$ es la orientación del orbital.

  - $l$ está asociado a el momento angular total del electrón en el átomo
  - $m$ es la proyección sobre $\hat z$ del momento angular
  - $n$ es el nivel. Al orden más bajo la energía del electrón en el estado $\psi_{n,l,m}$ sólo depende de $n$: $E_n$.
  - Al incorporar términos al hamiltoniano la energía empieza a depender de otros números cuánticos

Con la norma definida así, vale la siguiente relación de ortonormalidad:

$$
\int \psi_{n,l,m}^* \psi_{n^\prime,l^\prime,m^\prime} \;\; r^2 sin(\theta) \, d\theta d\phi dr
=
\delta_{l \, l^\prime} \, \delta_{m \, m^\prime}\, \delta_{n \, n^\prime}
$$

Que viene de la condición de ortonormalidad de $R_{n,l}$ (para un mismo $l$) :

$$
\int_0^\infty R_{n,l}(r)^* R_{n^\prime,l}(r)  \, r^2 \, dr =  \delta_{n \, n^\prime}
$$

Condición de normalización de los armónicos esféricos:

$$
\int_0^{2 \pi} \int_0^{\pi}
Y_l^m(\theta,\phi)^* \,\cdot\,
Y_{l^\prime}^{m^\prime}(\theta,\phi)
\;\;\;
sin(\theta) \, d\theta \, d\phi
=
\delta_{l \, l^\prime} \, \delta_{m \, m^\prime}
$$



## Graficar orbitales atómicos (con fase en color)

En el archivo [orbitales_atomicos.py](https://github.com/marceluda/python-para-fisicos/blob/master/tutoriales/orbitales_atomicos/orbitales_atomicos.py) está programado el cálculo de estas funciones $\psi_{n,m,l}$ para cada estado (n,l,m).

Luego, en [01_graficar_3d.py](https://github.com/marceluda/python-para-fisicos/blob/master/tutoriales/orbitales_atomicos/01_graficar_3d.py) se muestra cómo graficar.

A continuación el ejemplo para el estado: $\psi_{5,2,1} + i \cdot \psi_{5,2,-1}$


![grafico](orbitales_01.png "grafico")


### Veriosn Ploy.ly 3D

<div id="e7578db5-5986-4d0a-9b38-29ac6aa08644" class="plotly-graph-div" style="height:800px; width:800px;"></div>


<script type="text/javascript">
  window.PLOTLYENV=window.PLOTLYENV || {};

  if (document.getElementById("e7578db5-5986-4d0a-9b38-29ac6aa08644")) {
      Plotly.d3.json( "orbitales_02_3D.json", function(err, fig) {
        Plotly.plot("e7578db5-5986-4d0a-9b38-29ac6aa08644", fig.data, fig.layout);
      });
  };  
</script>


## Comparar orbitales atómicos (diferenciados por color)

En el archivo [02_comparar_estados.py](https://github.com/marceluda/python-para-fisicos/blob/master/tutoriales/orbitales_atomicos/02_comparar_estados.py) se grafican 3 estados en simultaneo con diferentes colores:

Gráficos de los estados
$(\psi_{2,1,-1} + i \cdot \psi_{2,1,1})/\sqrt{2}$ (celeste),
$-i \cdot (\psi_{3,2,-1} - \psi_{3,2,-1})/\sqrt{2}$ (naranja),
$\psi_{1,0,0}$ (verde) :


![grafico](orbitales_03.png "grafico")

### Veriosn Ploy.ly 3D de varios estados


<div id="ed77c4d8-e3f3-4bbe-a21d-b637f61b416a" class="plotly-graph-div" style="height:800px; width:800px;"></div>


<script type="text/javascript">
  window.PLOTLYENV=window.PLOTLYENV || {};

  if (document.getElementById("ed77c4d8-e3f3-4bbe-a21d-b637f61b416a")) {
      Plotly.d3.json( "orbitales_04_3D.json", function(err, fig) {
        Plotly.plot("ed77c4d8-e3f3-4bbe-a21d-b637f61b416a", fig.data, fig.layout);
      });
  };  
</script>


## Estructura fina e hiperfina
La estructura fina e hiperfina de la configuración electrónica depende de
el acoplamiento del Spin electrónico con el momento angular orbital ($L \cdot S$) y de todo esto
con el spin nuclear ($I$).
Para describir (y graficar) estos estados se debe extender el espacio de Hilbert contemplando las posibles
proyecciones del Spin electrónico y Nuclear.

En el repositorio de github se incluyen ejemplos para la creación de autoestados del hamiltoniano con acoplamiento $L\cdot S $
(estructura fina, archivo [03_estructura_fina.py](https://github.com/marceluda/python-para-fisicos/blob/master/tutoriales/orbitales_atomicos/03_estructura_fina.py))
y para el hamiltoniano con acoplamiento $J \cdot I$
(estructura hiperfina, archivo [04_estructura_HiperFina.py](https://github.com/marceluda/python-para-fisicos/blob/master/tutoriales/orbitales_atomicos/04_estructura_HiperFina.py)).

Por ejemplo, a continuación se puede ver una representación gráfica del estado ${}^{87}Rb\,5P_{3/2} \; F=1,mf=1$ :

<div id="86222a18-3078-4973-919f-faa48dc9c961" class="plotly-graph-div" style="height:800px; width:800px;"></div>


<script type="text/javascript">
  window.PLOTLYENV=window.PLOTLYENV || {};

  if (document.getElementById("86222a18-3078-4973-919f-faa48dc9c961")) {
      Plotly.d3.json( "orbitales_05_3D.json", function(err, fig) {
        Plotly.plot("86222a18-3078-4973-919f-faa48dc9c961", fig.data, fig.layout);
      });
  };  
</script>


En el archivo
[04_estructura_HiperFina.py](https://github.com/marceluda/python-para-fisicos/blob/master/tutoriales/orbitales_atomicos/04_estructura_HiperFina.py)
también hay un ejemplo sobre cómo generar animaciones, útiles para ver transiciones entre estados. Esta es una simulación (muy rudimentaria)
de una transición por oscilaciones de Rabi entre el estado

${}^{87}Rb\,5S_{1/2}\;F=1,mf=0$ y el estado  ${}^{87}Rb\,5S_{3/2}\;F=1,mf=1$

![grafico](transicion3.gif "animacion")



## Galería de estados


Con el script
[05_galeria_de_estados_3d.py](https://github.com/marceluda/python-para-fisicos/blob/master/tutoriales/orbitales_atomicos/05_galeria_de_estados_3d.py)
se generó una galería de estados orbitales hasta el nivel 3:

<center>
<p> <a href="{{ site.baseurl }}/tuto/orbitales_galeria/" class="btn btn-primary btn-lg" role="button">
Galería de Orbitales atómicos
</a></p>
</center>
