#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gráficos avanzados
"""

from numpy import *
import numpy as np
import matplotlib.pyplot as plt


#%% Ejes dobles
"""
Dos ejemplos, compartir el eje x y el eje y 
"""

# Colores para cada eje Y
col1 = 'C0'
col2 = 'C3'

# Parámetros del modelo
t       = linspace(0,5,500) # tiempo
g, A, w = 6/10 , 3 , 5  # parámetros

# Creamos una figura de un solo axis
fig, ax = plt.subplots(1,1, figsize=(6,4),  constrained_layout=True)

# Graficamos posición
ax.plot( t , A*exp(-g*t)*cos(w*t) ,  label='posición' , lw=2, color=col1 )
ax.set_ylabel('posición [cm]')
ax.set_xlabel('tiempo [s]')
ax.grid(b=True, ls= ':', color='lightgray')


# Creamos otro axis que comparta el eje X con ax
ax2 = ax.twinx()
# graficamos velocidad
ax2.plot( t , A  *exp(-g*t)*( -g*cos(w*t) + w*sin(w*t) ) , label='velocidad' , lw=2, color=col2  )
ax2.set_ylabel('velocidad [cm/s]')

# Creamos otro axis que comparta el eje Y con ax
ax3 = ax.twiny()
ax3.set_frame_on(False)

# En este no graficamos nada... sólo agregamos una escala diferente
ax3.set_xlim( array(ax.get_xlim())*w/pi )
ax3.set_xticks( arange(9) )
# Reemplazamos las etiquetas por textos con latex
ax3.set_xticklabels( ['0','$\pi$'] + [ f'{l}$\pi$' for l in range(2,9)] )
ax3.set_xlabel('Fase [rad]')

# Si ajustamos los límites adecuadamente, los tiks de ambos ejes van a coincidir
ax.set_ylim(  -2.2,3.1)
ax2.set_ylim(  -2.2*w,3.1*w)


# Coloreamos ejes, ticks y etiquetas para identificar cada gráfico con su eje
ax.yaxis.label.set_color(col1)
ax.spines[ "left"].set_edgecolor(col1)
ax.tick_params(axis='y', colors=col1)

ax2.yaxis.label.set_color(col2)
ax2.spines["left"].set_edgecolor(col1)
ax2.spines["right" ].set_edgecolor(col2)
ax2.tick_params(axis='y', colors=col2)


# fig.savefig('02_twin_axis.png')

