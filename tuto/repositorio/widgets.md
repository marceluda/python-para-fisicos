---
title: Widgets
description: Widgets
layout: page
navbar: repo
mathjax: true
---

<div class="alert alert-info" role="alert" >
  <strong>Archivo:</strong> <a href="../repositorio_05_widgets.py"> repositorio_05_widgets.py </a>
</div>
Se presentan a continuación un ejemplo de un modelo cuyos parámetros se
controlan mediantes widgets
## Ejemplo de modelo para ajustar parámetros a mano

Usando Widgets se pueden controlar los parámetros de un modelo
y compararlo con los datos


[![Watch the video](https://img.youtube.com/vi/-y2uimNWyrs/maxresdefault.jpg)](https://youtu.be/-y2uimNWyrs)


<a data-toggle="collapse" href="#desplegable000" aria-expanded="false" aria-controls="desplegable000">ver código<span class="caret"></span></a>

<div id="desplegable000" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

```python

from numpy import *
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons




# Primero creamos una figura y graficamos los datos ###########################
fig, ax = plt.subplots()




# Inventamos datos ruidosos con numpy.random
random.seed(1)
x_datos   = linspace(0.0, 1.0, 100 )
y_datos   = 0.35 * sin( x_datos * 2*pi * 3.7 + pi/3 ) + random.normal(size=100)/40

plt.plot( x_datos , y_datos , '.' , label='Datos originales', ms=5 )
plt.xlabel('tiempo [s]')
plt.ylabel('datos [V]')


# Luego usamos una función de modelo y la graficamos

def modelo( t , frecuencia, amplitud , fase ):
    return amplitud * sin( t*2*pi*frecuencia + fase )

tiempo     = linspace(0.0, 1.0, 5000 )
pl_modelo, = plt.plot( tiempo , modelo(tiempo,10,1,0) , '-' , color='C3', label='modelo', lw=2, alpha=0.7  )

# el objeto pl_modelo permite actualizar los valores del grafico posterioremente

plt.legend(loc=1)
plt.tight_layout()



# Ahora creamos otra figura para contener los controles #######################
fig_controles, axs = plt.subplots( 5 ,1 )

# Cada axis de la figura de 5 subplots es un contenedor para un widget

# a los primeros 3 contenedores les asignamos Sliders
slider_frecuencia = Slider( axs[0], 'Frecuencia',  0.1, 30.0, valinit=10 )
slider_amplitud   = Slider( axs[1], 'Amplitud'  ,  0.1, 10.0, valinit=1 )
slider_fase       = Slider( axs[2], 'Fase'      ,    0, 2*pi, valinit=0 )

# Al slider de fase le ponemos valores para verlo bonito
axs[2].set_xticks(      [0, pi/2 , pi, 3/2*pi , 2*pi ] )
axs[2].set_xticklabels( ['0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3}{2}\pi$', r'$2\pi$'] )


# Creamos una funcion de actualización para que se ejecute cada vez que un
# controlador cambia un valor

def update(val):
    # En vez de usar el valor val, directamente tomamos los valores de cada control
    amplitud   = slider_amplitud.val
    frecuencia = slider_frecuencia.val
    fase       = slider_fase.val

    # Luego usamos el objeto pl_modelo para actulizar los valors Y del gráfico
    pl_modelo.set_ydata(   modelo(tiempo,frecuencia,amplitud,fase)    )
    fig.canvas.draw_idle()

# asignamos esa función a los objetos slider
slider_frecuencia.on_changed(update)
slider_amplitud.on_changed(update)
slider_fase.on_changed(update)


# Podemos tambien crear un objeto Botón
boton = Button( axs[3] , 'Resetear', color='red', hovercolor='pink')

def reset(event):
    slider_frecuencia.reset()
    slider_amplitud.reset()
    slider_fase.reset()
boton.on_clicked(reset)


# Y un radio select
radio = RadioButtons( axs[4] , ('C0', 'C1', 'C2'), active=0)

def colorfunc(label):
    pl_modelo.set_color(label)
    fig.canvas.draw_idle()
radio.on_clicked(colorfunc)

plt.tight_layout()
plt.show()


# plt.savefig('repositorio_widget_000.png')
```
</div>
