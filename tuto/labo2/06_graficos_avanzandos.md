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

<div class="alert alert-danger" role="alert" >
  <strong>Contenido pendiente</strong>
</div>

------

## Inclusión de barras o áreas de error

<div class="alert alert-danger" role="alert" >
  <strong>Contenido pendiente</strong>
</div>

------

## Ejemplos de mapa de colores

<div class="alert alert-danger" role="alert" >
  <strong>Contenido pendiente</strong>
</div>



{% include page_navbar.html up=1 %}
