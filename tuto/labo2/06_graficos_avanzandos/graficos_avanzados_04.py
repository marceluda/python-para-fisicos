#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gráficos avanzados
"""

from numpy import *
import numpy as np
import matplotlib.pyplot as plt


#%% Anotaciones
"""
Anotaciones. Cómo agragar texto a un gráfico.

Basado en:
    https://matplotlib.org/3.5.0/tutorials/text/annotations.html
"""

plt.rcParams.update({'font.size': 14})


# Datos y función a dibujar
xx    = linspace(-15,15,500)+5

def gaussiana(x,sig,mu):
    return exp( - ((x-mu)/sig)**2/2 ) / sig / sqrt(2*pi)

sig, mu  = 2 , 5   # Parámetros


# Figura ######################################################################
fig, ax = plt.subplots(1, 1, figsize=(8,5), constrained_layout=True)

ax.plot( xx , gaussiana(xx,sig,mu) , color='black')
ax.set_xlim(0,10)
ax.set_ylim(0,0.23)
ax.set_xlabel('valores [unidad]')
ax.set_ylabel('densidad de probabilidad')


# Relleno en color
x2    = linspace(mu-sig,mu+sig,100)
ax.fill_between( x2,  gaussiana(x2,sig,mu) , 0 , color='C1' , alpha=0.3 )

# Valor máximo
max_val = gaussiana(mu,sig,mu)

# Línea horizontal en la mitad del máximo, con texto
ax.axhline( max_val/2 , color='gray' , lw=1 , ls='--')
ax.text( 0, max_val/2, "Mitad de altura\n(Half Maximum)", ha="left", va="bottom", size=12,
            transform=ax.get_yaxis_transform())

# ax.get_yaxis_transform() permite usar coordenadas x del axis (entre 0 y 1)
# y coordenadas y en data (mismas unidades de los datos)

# Línea horizontal en el máximo, con texto
ax.axhline(  gaussiana(mu,sig,mu) , color='gray' , lw=2  , ls=':')
ax.text( 0,   max_val, "Máxima altura", ha="left", va="bottom", size=12,
            transform=ax.get_yaxis_transform())

# Líneas verticales en valores relevantes
ax.axvline( mu     , color='C0' , lw=3 )
ax.axvline( mu+sig , color='C1' , lw=3 )
ax.axvline( mu-sig , color='C1' , lw=3 )

# Ecuación en LaTeX
ecuacion = r"$\frac{1}{\sigma \, \sqrt{2\pi}} \; e^{- \frac{ (x-\mu)^2}{2\,\sigma^2} }$"
ax.annotate(ecuacion,
            xy=    ( 7.60, 0.083 ), xycoords  ='data',
            xytext=(  0.8,   0.7 ), textcoords='axes fraction',
            color='black', weight='bold', size=18,
            arrowprops=dict(arrowstyle="->", lw=1, color='black',
                            connectionstyle="angle3"),
            )



# Flecha que señala mu
ax.annotate("$\mu$",
            xy=    ( mu, max_val*1.1 ),
            xytext=(0.6,         0.9 ), textcoords='axes fraction',
            color='C0', weight='bold', size=14,
            arrowprops=dict(arrowstyle="->", lw=3, color='C0',
                            connectionstyle="angle3"),
            )


# Flechas que señalan el ancho FWHM
fwhm=sqrt(2*log(2))*sig
ax.annotate("",
            xy=    (mu-fwhm, max_val/2 ), xycoords  ='data',
            xytext=(mu+fwhm, max_val/2 ), textcoords='data',
            arrowprops=dict(arrowstyle="<->", lw=1, color='black',
                            connectionstyle="arc3"),
            )
ax.text(mu, max_val/2, "FWHM", ha="center", va="center", size=15,
    bbox=dict(boxstyle="square,pad=0.3", fc="white", ec="black", lw=2))



# Flechas que señalan sigma
ax.annotate("",
            xy=    (mu    , max_val/3 ), xycoords  ='data',
            xytext=(mu+sig, max_val/3 ), textcoords='data',
            arrowprops=dict(arrowstyle="<->", lw=2, color='C1',
                            connectionstyle="arc3"),
            )
ax.text(mu+sig/2, max_val/3, "$\sigma$", ha="center", va="center", size=15, color='C1',
    bbox=dict(boxstyle="square,pad=0.3", fc="white", ec="C1", lw=2))


# Texto del árean
ax.text(mu-sig/2, max_val/3, "68%", ha="center", va="center", size=18, color='C1',
        weight='bold')

# Título
ax.set_title('Distribución Normal', size=16, weight='bold')

# fig.savefig('04_anotaciones.png')

