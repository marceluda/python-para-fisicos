---
title: Orbitales atómicos
description: Graficar orbitales atómicos
layout: page
mathjax: true
plotly: true
navbar: labo2
---

<div class="alert alert-danger" role="alert" >
  <strong>Aviso:</strong> La página está en construcción.
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


$$
\huge
A  \leftarrow  \bar{x} \equiv \sum_i \frac{x_i}{N}
$$

Armónicos esféricos:

$$
Y^m_n(\theta,\phi) = \epsilon \sqrt{\frac{2n+1}{4\pi} \frac{(n-m)!}{(n+m)!}}
      e^{i m \theta} P^m_n(\cos(\phi))
$$

## Graficar orbitales atómicos
<div class="alert alert-danger" role="alert" >
  <strong>Aviso:</strong> Acá va ir la descripción matemática de los orbitales atómicos
</div>




![grafico](orbitales_01.png "grafico")


### Veriosn Ploy.ly 3D

<!--

<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>    

-->

<div id="e7578db5-5986-4d0a-9b38-29ac6aa08644" class="plotly-graph-div" style="height:800px; width:800px;"></div>


<script type="text/javascript">
  window.PLOTLYENV=window.PLOTLYENV || {};

  if (document.getElementById("e7578db5-5986-4d0a-9b38-29ac6aa08644")) {
      Plotly.d3.json( "orbitales_02_3D.json", function(err, fig) {
        Plotly.plot("e7578db5-5986-4d0a-9b38-29ac6aa08644", fig.data, fig.layout);
      });
  };  
</script>
