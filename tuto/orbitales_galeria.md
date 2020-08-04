---
title: Galería de orbitales atómicos
description: Galería de orbitales atómicos
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

<div class="alert alert-info" role="alert" >
  <strong>Comentario:</strong> Se grafican los estados para todos los L y m posibles... y las superposiciones de estados con m y -m.
</div>



## Figuras estados n=1


![grafico](orb_gal_01.png "grafico")


<div id="orb_plot_1" class="plotly-graph-div" style="height:800px; width:800px;"></div>

<p>


<script type="text/javascript">
  window.PLOTLYENV=window.PLOTLYENV || {};

  if (document.getElementById("orb_plot_1")) {
      Plotly.d3.json( "orbitales_06_10300.json", function(err, fig) {
        Plotly.plot("orb_plot_1", fig.data, fig.layout);
      });
  };  
</script>

<a href='javascript:Plotly.purge("orb_plot_1");Plotly.d3.json( "orbitales_06_10300.json", function(err, fig) { Plotly.plot("orb_plot_1", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(1,0,0)
</a>
</p>






## Figuras estados n=2


![grafico](orb_gal_02.png "grafico")


<div id="orb_plot_2" class="plotly-graph-div" style="height:800px; width:800px;"></div>

<p>

<script type="text/javascript">
  window.PLOTLYENV=window.PLOTLYENV || {};

  if (document.getElementById("orb_plot_2")) {
      Plotly.d3.json( "orbitales_06_20300.json", function(err, fig) {
        Plotly.plot("orb_plot_2", fig.data, fig.layout);
      });
  };  
</script>

<a href='javascript:Plotly.purge("orb_plot_2");Plotly.d3.json( "orbitales_06_20300.json", function(err, fig) { Plotly.plot("orb_plot_2", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(2,0,0)
</a>
<a href='javascript:Plotly.purge("orb_plot_2");Plotly.d3.json( "orbitales_06_21290.json", function(err, fig) { Plotly.plot("orb_plot_2", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(2,1,-1)
</a>
<a href='javascript:Plotly.purge("orb_plot_2");Plotly.d3.json( "orbitales_06_21300.json", function(err, fig) { Plotly.plot("orb_plot_2", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(2,1,0)
</a>
<a href='javascript:Plotly.purge("orb_plot_2");Plotly.d3.json( "orbitales_06_21310.json", function(err, fig) { Plotly.plot("orb_plot_2", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(2,1,1)
</a>
<a href='javascript:Plotly.purge("orb_plot_2");Plotly.d3.json( "orbitales_06_21311.json", function(err, fig) { Plotly.plot("orb_plot_2", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71 Ψ(2,1,-1) + 0.71 Ψ(2,1,1)
</a>
<a href='javascript:Plotly.purge("orb_plot_2");Plotly.d3.json( "orbitales_06_21312.json", function(err, fig) { Plotly.plot("orb_plot_2", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71j Ψ(2,1,-1) -0.71j Ψ(2,1,1)
</a>
</p>






## Figuras estados n=3


![grafico](orb_gal_03.png "grafico")


<div id="orb_plot_3" class="plotly-graph-div" style="height:800px; width:800px;"></div>

<p>

<script type="text/javascript">
  window.PLOTLYENV=window.PLOTLYENV || {};

  if (document.getElementById("orb_plot_3")) {
      Plotly.d3.json( "orbitales_06_30300.json", function(err, fig) {
        Plotly.plot("orb_plot_3", fig.data, fig.layout);
      });
  };  
</script>

<a href='javascript:Plotly.purge("orb_plot_3");Plotly.d3.json( "orbitales_06_30300.json", function(err, fig) { Plotly.plot("orb_plot_3", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(3,0,0)
</a>
<a href='javascript:Plotly.purge("orb_plot_3");Plotly.d3.json( "orbitales_06_31290.json", function(err, fig) { Plotly.plot("orb_plot_3", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(3,1,-1)
</a>
<a href='javascript:Plotly.purge("orb_plot_3");Plotly.d3.json( "orbitales_06_31300.json", function(err, fig) { Plotly.plot("orb_plot_3", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(3,1,0)
</a>
<a href='javascript:Plotly.purge("orb_plot_3");Plotly.d3.json( "orbitales_06_31310.json", function(err, fig) { Plotly.plot("orb_plot_3", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(3,1,1)
</a>
<a href='javascript:Plotly.purge("orb_plot_3");Plotly.d3.json( "orbitales_06_31311.json", function(err, fig) { Plotly.plot("orb_plot_3", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71 Ψ(3,1,-1) + 0.71 Ψ(3,1,1)
</a>
<a href='javascript:Plotly.purge("orb_plot_3");Plotly.d3.json( "orbitales_06_31312.json", function(err, fig) { Plotly.plot("orb_plot_3", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71j Ψ(3,1,-1) -0.71j Ψ(3,1,1)
</a>
<a href='javascript:Plotly.purge("orb_plot_3");Plotly.d3.json( "orbitales_06_32280.json", function(err, fig) { Plotly.plot("orb_plot_3", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(3,2,-2)
</a>
<a href='javascript:Plotly.purge("orb_plot_3");Plotly.d3.json( "orbitales_06_32290.json", function(err, fig) { Plotly.plot("orb_plot_3", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(3,2,-1)
</a>
<a href='javascript:Plotly.purge("orb_plot_3");Plotly.d3.json( "orbitales_06_32300.json", function(err, fig) { Plotly.plot("orb_plot_3", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(3,2,0)
</a>
<a href='javascript:Plotly.purge("orb_plot_3");Plotly.d3.json( "orbitales_06_32310.json", function(err, fig) { Plotly.plot("orb_plot_3", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(3,2,1)
</a>
<a href='javascript:Plotly.purge("orb_plot_3");Plotly.d3.json( "orbitales_06_32311.json", function(err, fig) { Plotly.plot("orb_plot_3", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71 Ψ(3,2,-1) + 0.71 Ψ(3,2,1)
</a>
<a href='javascript:Plotly.purge("orb_plot_3");Plotly.d3.json( "orbitales_06_32312.json", function(err, fig) { Plotly.plot("orb_plot_3", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71j Ψ(3,2,-1) -0.71j Ψ(3,2,1)
</a>
<a href='javascript:Plotly.purge("orb_plot_3");Plotly.d3.json( "orbitales_06_32320.json", function(err, fig) { Plotly.plot("orb_plot_3", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(3,2,2)
</a>
<a href='javascript:Plotly.purge("orb_plot_3");Plotly.d3.json( "orbitales_06_32321.json", function(err, fig) { Plotly.plot("orb_plot_3", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
+ 0.71 Ψ(3,2,2) -0.71 Ψ(3,2,-2)
</a>
<a href='javascript:Plotly.purge("orb_plot_3");Plotly.d3.json( "orbitales_06_32322.json", function(err, fig) { Plotly.plot("orb_plot_3", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71j Ψ(3,2,2) -0.71j Ψ(3,2,-2)
</a>
</p>






## Figuras estados n=4


![grafico](orb_gal_04.png "grafico")


<div id="orb_plot_4" class="plotly-graph-div" style="height:800px; width:800px;"></div>

<p>

<script type="text/javascript">
  window.PLOTLYENV=window.PLOTLYENV || {};

  if (document.getElementById("orb_plot_4")) {
      Plotly.d3.json( "orbitales_06_40300.json", function(err, fig) {
        Plotly.plot("orb_plot_4", fig.data, fig.layout);
      });
  };  
</script>

<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_40300.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(4,0,0)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_41290.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(4,1,-1)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_41300.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(4,1,0)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_41310.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(4,1,1)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_41311.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71 Ψ(4,1,-1) + 0.71 Ψ(4,1,1)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_41312.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71j Ψ(4,1,-1) -0.71j Ψ(4,1,1)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_42280.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(4,2,-2)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_42290.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(4,2,-1)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_42300.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(4,2,0)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_42310.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(4,2,1)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_42311.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
+ 0.71 Ψ(4,2,1) -0.71 Ψ(4,2,-1)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_42312.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71j Ψ(4,2,1) -0.71j Ψ(4,2,-1)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_42320.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(4,2,2)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_42321.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
+ 0.71 Ψ(4,2,2) -0.71 Ψ(4,2,-2)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_42322.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71j Ψ(4,2,2) -0.71j Ψ(4,2,-2)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_43270.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(4,3,-3)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_43280.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(4,3,-2)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_43290.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(4,3,-1)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_43300.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(4,3,0)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_43310.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(4,3,1)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_43311.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71 Ψ(4,3,-1) + 0.71 Ψ(4,3,1)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_43312.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71j Ψ(4,3,-1) -0.71j Ψ(4,3,1)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_43320.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(4,3,2)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_43321.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71 Ψ(4,3,-2) + 0.71 Ψ(4,3,2)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_43322.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71j Ψ(4,3,-2) -0.71j Ψ(4,3,2)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_43330.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(4,3,3)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_43331.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
+ 0.71 Ψ(4,3,3) -0.71 Ψ(4,3,-3)
</a>
<a href='javascript:Plotly.purge("orb_plot_4");Plotly.d3.json( "orbitales_06_43332.json", function(err, fig) { Plotly.plot("orb_plot_4", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71j Ψ(4,3,3) -0.71j Ψ(4,3,-3)
</a>
</p>






## Figuras estados n=5


![grafico](orb_gal_05.png "grafico")


<div id="orb_plot_5" class="plotly-graph-div" style="height:800px; width:800px;"></div>

<p>

<script type="text/javascript">
  window.PLOTLYENV=window.PLOTLYENV || {};

  if (document.getElementById("orb_plot_5")) {
      Plotly.d3.json( "orbitales_06_50300.json", function(err, fig) {
        Plotly.plot("orb_plot_5", fig.data, fig.layout);
      });
  };  
</script>

<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_50300.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(5,0,0)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_51290.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(5,1,-1)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_51300.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(5,1,0)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_51310.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(5,1,1)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_51311.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
+ 0.71 Ψ(5,1,1) -0.71 Ψ(5,1,-1)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_51312.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71j Ψ(5,1,1) -0.71j Ψ(5,1,-1)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_52280.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(5,2,-2)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_52290.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(5,2,-1)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_52300.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(5,2,0)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_52310.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(5,2,1)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_52311.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71 Ψ(5,2,-1) + 0.71 Ψ(5,2,1)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_52312.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71j Ψ(5,2,-1) -0.71j Ψ(5,2,1)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_52320.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(5,2,2)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_52321.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71 Ψ(5,2,-2) + 0.71 Ψ(5,2,2)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_52322.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71j Ψ(5,2,-2) -0.71j Ψ(5,2,2)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_53270.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(5,3,-3)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_53280.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(5,3,-2)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_53290.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(5,3,-1)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_53300.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(5,3,0)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_53310.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(5,3,1)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_53311.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
+ 0.71 Ψ(5,3,1) -0.71 Ψ(5,3,-1)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_53312.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71j Ψ(5,3,1) -0.71j Ψ(5,3,-1)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_53320.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(5,3,2)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_53321.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
+ 0.71 Ψ(5,3,2) -0.71 Ψ(5,3,-2)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_53322.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71j Ψ(5,3,2) -0.71j Ψ(5,3,-2)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_53330.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(5,3,3)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_53331.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
+ 0.71 Ψ(5,3,3) -0.71 Ψ(5,3,-3)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_53332.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71j Ψ(5,3,3) -0.71j Ψ(5,3,-3)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_54260.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(5,4,-4)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_54270.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(5,4,-3)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_54280.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(5,4,-2)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_54290.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(5,4,-1)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_54300.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(5,4,0)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_54310.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(5,4,1)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_54311.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71 Ψ(5,4,-1) + 0.71 Ψ(5,4,1)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_54312.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71j Ψ(5,4,-1) -0.71j Ψ(5,4,1)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_54320.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(5,4,2)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_54321.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
+ 0.71 Ψ(5,4,2) -0.71 Ψ(5,4,-2)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_54322.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71j Ψ(5,4,2) -0.71j Ψ(5,4,-2)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_54330.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(5,4,3)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_54331.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
+ 0.71 Ψ(5,4,3) -0.71 Ψ(5,4,-3)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_54332.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71j Ψ(5,4,3) -0.71j Ψ(5,4,-3)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_54340.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
Ψ(5,4,4)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_54341.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
+ 0.71 Ψ(5,4,4) -0.71 Ψ(5,4,-4)
</a>
<a href='javascript:Plotly.purge("orb_plot_5");Plotly.d3.json( "orbitales_06_54342.json", function(err, fig) { Plotly.plot("orb_plot_5", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
-0.71j Ψ(5,4,4) -0.71j Ψ(5,4,-4)
</a>
</p>

## Referencia de colores de fase

La fase está graficada siguiedo el siguiente código de colores:

![grafico](referencia_colores.png "grafico")
