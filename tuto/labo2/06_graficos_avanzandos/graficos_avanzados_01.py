#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gráficos avanzados
"""

from numpy import *
import numpy as np
import matplotlib.pyplot as plt

#%% Cuatro gráficos en grilla
"""
Estos gráficos comparten el eje Y en cada fila y el eje X en cada columna
"""


fig, axx = plt.subplots(2,3, figsize=(12,6),  constrained_layout=True, sharex='col', sharey='row')
fig.set_constrained_layout_pads(w_pad=2/72, h_pad=2/72, hspace=0, wspace=0)

# Modelo
# http://hyperphysics.phy-astr.gsu.edu/hbase/oscda.html#c4

# Amortiguado #################################################################
t       = linspace(0,5,1000) # tiempo
g, A, w = 6/10 , 3 , 2*pi*2  # parámetros

ax = axx[0,0] #####################################
ax.plot( t , A*exp(-g*t)*cos(w*t) ,  '-',  label='oscilador' , lw=2 )
ax.plot( t , A*exp(-g*t)          , '--', label='envolvente' , color='C3' )
ax.plot( t ,-A*exp(-g*t)          , '--',                      color='C3' )

ax.set_ylabel('posición [cm]')
ax.set_title('sub amortiguado')

ax = axx[1,0] #####################################
ax.plot( t , A  *exp(-g*t)*( -g*cos(w*t) + w*sin(w*t) ) , lw=2 )
ax.plot( t , A*w*exp(-g*t)          , '--' , color='C3' )
ax.plot( t ,-A*w*exp(-g*t)          , '--' , color='C3' )

ax.set_ylabel('velocidad [cm/s]')
ax.set_xlabel('tiempo [s]')


# Simple ######################################################################
t    = linspace(0,2,1000) # tiempo
A, w =  3 , 2*pi*2        # parámetros

ax = axx[0,1] #####################################
ax.plot( t , A*cos(w*t) ,  '-',  label='oscilador' , lw=2 )
ax.axhline( A , ls='--', color='C3' , label='envolvente')
ax.axhline(-A , ls='--', color='C3')

ax.set_title('simple')

ax = axx[1,1] #####################################
ax.plot( t , A *w*sin(w*t)  , lw=2 )
ax.axhline( w*A , ls='--', color='C3')
ax.axhline(-w*A , ls='--', color='C3')

ax.set_xlabel('tiempo [s]')


# Sobreamortiguado ############################################################
t       = linspace(0,0.6,1000) # tiempo
g, A, w = 18 , 3 , 2*pi*2  # parámetros
g1      = g + sqrt(g**2-w**2)
g2      = g - sqrt(g**2-w**2)
B       = A*g
ax = axx[0,2] #####################################
ax.plot( t , A/2*(exp(-g1*t) + exp(-g2*t)),  '-', lw=2, color='C1' ,  label='sobre amortiguado' )
ax.plot( t , exp(-g*t)*(A+g*A*t),  '-', lw=2, color='C2' ,  label='amortiguado crítico' )

ax.set_title('sobre amortiguado')

ax = axx[1,2] #####################################
ax.plot( t , A/2*(-g1*exp(-g1*t) -g2*exp(-g2*t)),  '-', lw=2, color='C1'  )
ax.plot( t , exp(-g*t)*(-g*(A+B*t) + B),  '-', lw=2, color='C2'  )

ax.set_ylim(-42,42)
ax.set_xlabel('tiempo [s]')


# Gráfico general #############################################################
fig.suptitle('Oscilador armónico')

axx[0,0].legend()
#axx[0,1].legend()
axx[0,2].legend()


# Agregamos una grilla a TODOS los gráficos
for ax in axx.flatten():
    ax.grid(b=True, ls= ':', color='lightgray')

for ax in axx.flatten():
    ax.axhline(0 , color='gray' , lw=1 , zorder=-1)

# Esto es para alinear los nombres de los ejes y:
fig.align_ylabels(axx[:,0])

# fig.savefig('01_subplots.png')

