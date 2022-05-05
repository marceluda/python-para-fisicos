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
Escalas logarítmicas

Basado en:
    https://matplotlib.org/stable/gallery/scales/log_demo.html
"""


# Datos
t = arange(0.01, 20.0, 0.01)

# Figura
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10,6), constrained_layout=True)

# log y 
ax1.plot(t, np.exp(-t / 5.0))
ax1.semilogy()
ax1.set_title('semilogy', y=0.7 , bbox=dict(boxstyle="square",ec='black', fc='white' ))
ax1.grid(b=True, ls= ':', color='lightgray')
ax1.set_xlabel('eje x [unidades]')
ax1.set_ylabel('eje y [unidades]')


# log x
ax2.plot(t, np.sin(2 * np.pi * t))
ax2.semilogx()
ax2.set(title='')
ax2.set_title('semilogx', y=0.7 , bbox=dict(boxstyle="square",ec='black', fc='white' ))
ax2.grid(b=True, ls= '-', color='lightgray')
ax2.grid(b=True, ls= ':', color='lightgray',which ='minor', axis='x', alpha=0.7)
ax2.set_xlabel('eje x en log10 [unidades]')
ax2.set_ylabel('eje y [unidades]')


# log x + log y
ax3.plot(t, 20 * np.exp(-t / 10.0))
ax3.semilogy()
ax3.semilogx()
ax3.set_xscale('log', basex=2)
ax3.set_yscale('log', basey=2)
ax3.set_title('loglog en base 2', y=0.7 , bbox=dict(boxstyle="square",ec='black', fc='white' ))
ax3.grid(b=True, ls= ':', color='lightgray')
ax3.set_xlabel('eje x en log2 [unidades]')
ax3.set_ylabel('eje y en log2 [unidades]')

# Ponemos barras de error
x = 10.0**np.linspace(0.0, 2.0, 20)
y = x**2.0

ax4.set_xscale("log", nonposx='clip')
ax4.set_yscale("log", nonposy='clip')
ax4.set_title('Barras de error negativas', y=0.85 , bbox=dict(boxstyle="square",ec='black', fc='white' ))
ax4.errorbar(x, y, xerr=0.1 * x, yerr=5.0 + 0.75 * y)
# Se debe configurar ylim despues de agregar las barras de error
ax4.set_ylim(bottom=0.1)
ax4.grid(b=True, ls= '-', color='lightgray')
ax4.grid(b=True, ls= ':', color='lightgray',which ='minor', alpha=0.7)
ax4.set_xlabel('eje x en log10 [unidades]')
ax4.set_ylabel('eje y en log10 [unidades]')


# Formato general

# Cambiamos posicion de los ejes X en los de arriba
for ax in [ax1,ax2]:
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top') 

# Cambiamos posicion de los ejes Y en los de la derecha
for ax in [ax2,ax4]:
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position('right') 

# Alineamos labels
fig.align_ylabels([ax1,ax3])
fig.align_ylabels([ax2,ax4])


# fig.savefig('03_loglog.png')

