---
title: Análisis de datos
description: Código para analizar y procesar datos
layout: page
---


<div class="alert alert-danger" role="alert" >
  <strong>Aviso:</strong> La página está en construcción.
</div>


## Graficar orbitales atómicos

<div class="alert alert-danger" role="alert" >
  <strong>Aviso:</strong> Acá va ir la descripción matemática de los orbitales atómicos
</div>


<center>
<a href="https://github.com/marceluda/python-para-fisicos/tree/master/tutoriales/orbitales_atomicos" class="btn btn-primary btn-lg" role="button">
Scripts python
</a>
</center>

![grafico](orbitales_01.png "grafico")


### Veriosn Ploy.ly 3D
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>    
<div id="e7578db5-5986-4d0a-9b38-29ac6aa08644" class="plotly-graph-div" style="height:800px; width:800px;"></div>

<script type="text/javascript">
  window.PLOTLYENV=window.PLOTLYENV || {};

  if (document.getElementById("e7578db5-5986-4d0a-9b38-29ac6aa08644")) {
      Plotly.d3.json( "lolo.json", function(err, fig) {
        Plotly.plot("e7578db5-5986-4d0a-9b38-29ac6aa08644", fig.data, fig.layout);
      });
  };  
</script>
