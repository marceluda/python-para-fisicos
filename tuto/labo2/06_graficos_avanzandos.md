---
title: Gráficos Avanzados
description: Gráficos Avanzados
layout: page
mathjax: true
navbar: labo2
---


{% include page_navbar.html %}

<div class="alert alert-danger" role="alert" >
  <strong>Aviso:</strong> La página está en construcción.
</div>


<div class="alert alert-info" role="info" >
  <strong>Referencias Matplotlib:</strong>
    <ul>
        <li><a href="https://matplotlib.org/2.0.2/gallery.html">Matplotlib Gallery 2.0</a></li>
        <li><a href="https://matplotlib.org/stable/gallery/index.html">Matplotlib Examples Stable</a></li>
        <li><a href="https://github.com/rougier/matplotlib-tutorial">Tutorial</a></li>
    </ul>
</div>

-------

## Múltiples gráficos con  `plt.subplots()`

![grafico](01_subplots.png "grafico")

<center>
<p> <a href="https://github.com/marceluda/python-para-fisicos/blob/gh-pages/tuto/labo2/06_graficos_avanzandos/graficos_avanzados_01.py" class="btn btn-primary btn-lg" role="button">
Código Fuente
</a> </p>
</center>

Con el comando `plt.subplots()` se pueden hacer grillas de ejes para graficar en cada una algo distinto.
En este ejemplos las escalas de los ejes se comparten en filas y columnas y se grafican una sola vez.
También se incluyen algunas líneas horizontales auxiliares con `ax.axhline()`.

------

## Múltiples ejes con `ax.twinx()` y `ax.twiny()`

![grafico](02_twin_axis.png "grafico")

<center>
<p> <a href="https://github.com/marceluda/python-para-fisicos/blob/gh-pages/tuto/labo2/06_graficos_avanzandos/graficos_avanzados_02.py" class="btn btn-primary btn-lg" role="button">
Código Fuente
</a> </p>
</center>

En este ejemplo se superponen dos gráficos de magnitudes diferentes en un mismo espacio, con el eje X compartido y el eje Y separado para cada uno. Los ejes se clonan con `ax.twinx()` para crear un nuevo eje de coordenadas con el mismo X. Se hace los mismo con `ax.twiny()`, pero aquí no se grafica nada. Sólo se representa una escala diferente.

Para identificar cada grafico con su eje se colorearon los ticks, labels y slices .

------

## Escalas logarítmicas con `ax.semilogx()` y `ax.semilogy()`

![grafico](03_loglog.png "grafico")

<center>
<p> <a href="https://github.com/marceluda/python-para-fisicos/blob/gh-pages/tuto/labo2/06_graficos_avanzandos/graficos_avanzados_03.py" class="btn btn-primary btn-lg" role="button">
Código Fuente
</a> </p>
</center>

En ese ejemplo se combinan distintas funciones para mostrar gráficos logarítmicos. Entre ellas se puede ver:
  - Eje logaritmico decimal en X y en Y
  - Ambos ejes en escala logarítmica
  - Ejes en logaritmo base 2
  - Cambio de posición de los ejes (top y right)
  - Cambio de posición y formato del título
  - Formato de la grilla para gráficos logarítmicos (con subgrilla)

------

## Anotaciones en un gráfico

![grafico](04_anotaciones.png "grafico")

<center>
<p> <a href="https://github.com/marceluda/python-para-fisicos/blob/gh-pages/tuto/labo2/06_graficos_avanzandos/graficos_avanzados_04.py" class="btn btn-primary btn-lg" role="button">
Código Fuente
</a> </p>
</center>

Ejemplos de cómo incluir anotaciones
  - textos con [`ax.text()`](https://matplotlib.org/3.5.0/api/_as_gen/matplotlib.pyplot.text.html)
  - flechas con [`ax.annotate()`](https://matplotlib.org/3.5.0/api/_as_gen/matplotlib.pyplot.annotate.html)
  - uso de LaTeX con `$$`
  - líneas verticales con `ax.axvline()`
  - líneas horizontales con `ax.axhline()`



------

## Inclusión de barras o áreas de error


![grafico](05_errores_a.png "grafico")

Ejemplo de gráficos en los que se expresan los errores de la medición

Cuando son pocos datos es conveniente usar barras de error con `ax.errorbar()`.
Esto permite incluir errores en X y en Y.

Por otro lado, cuando se tienen muchos datos, graficar con `ax.errorbar()` puede dar resultados inentendibles.
En ese caso se pueden usar otros recursos como `ax.fill_between()`


![grafico](05_errores_b.png "grafico")

También puede ocurrir que en un gráfico se quieran diferenciar los errores de medición
de las incertezas de la predicción de un modelo (lo que coloquialmente también le decimos error).

<center>
<p> <a href="https://github.com/marceluda/python-para-fisicos/blob/gh-pages/tuto/labo2/06_graficos_avanzandos/graficos_avanzados_05.py" class="btn btn-primary btn-lg" role="button">
Código Fuente
</a> </p>
</center>

------

## Ejemplos de mapa de colores

![grafico](06_colormap_a.png "grafico")

Los mapas de colores permite codificar información de los gráficos en los colores.
Puede servir para cuando se muestra la respuesta de un sistema ante dos parámetros (como frecuencia y temperatura).
Una forma de utilizarlo es asignando el color directamente a cada curva.

![grafico](06_colormap_b.png "grafico")

Otra forma de usarlo es generando imágenes 2D en la que una tercera dimensión a mostrar está codificada en el color. Para ello se puede usar [`ax.imshow()`](https://matplotlib.org/3.5.0/api/_as_gen/matplotlib.pyplot.imshow.html).


<center>
<p> <a href="https://github.com/marceluda/python-para-fisicos/blob/gh-pages/tuto/labo2/06_graficos_avanzandos/graficos_avanzados_06.py" class="btn btn-primary btn-lg" role="button">
Código Fuente
</a> </p>
</center>

------

## Ejemplo de BODE

![grafico](07_bode.png "grafico")


Ejemplo de un grafico tipo BODE para análisis de filtros. Arriba se grafica el módulo de la función de transferencia. Abajo, la fase.
Se suele expresar la amplitud en dB y la fase en grados.

<center>
<p> <a href="https://github.com/marceluda/python-para-fisicos/blob/gh-pages/tuto/labo2/06_graficos_avanzandos/graficos_avanzados_07.py" class="btn btn-primary btn-lg" role="button">
Código Fuente
</a> </p>
</center>


## Ejemplo de residuos con  histograma

![grafico](08_residuos.png "grafico")


Ejemplo ajuste de datos con residuos. Es un ejemplo también de `subplots` con proporciones distintas.

<center>
<p> <a href="https://github.com/marceluda/python-para-fisicos/blob/gh-pages/tuto/labo2/06_graficos_avanzandos/graficos_avanzados_08.py" class="btn btn-primary btn-lg" role="button">
Código Fuente
</a> </p>
</center>




{% include page_navbar.html up=1 %}
