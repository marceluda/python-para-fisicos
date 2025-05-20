#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gráficos avanzados
"""

from numpy import *
import numpy as np
import matplotlib.pyplot as plt

# Tamaño del texto por defecto
plt.rcParams.update({'font.size': 12})


#%% Mapas de colores
"""
Mapa de colores para distintas curvas
"""

# Ejemplo con radiación del cuerpo negro

h = 4.135667696e-15    # eV/Hz
k = 8.617333262145e-5  # eV/K
c = 299792458          # m/s

def CNnu(nu,T=273.15):
    """
    Densidad de radiancia espectral del cuerpo negro
        https://en.wikipedia.org/wiki/Planck's_law#Different_forms
    nu: frecuencia
    T: temperatura en kelvin. Por defecto: 273.15
    """
    nu = array(nu)
    return 2*(nu/c)**2 * h*nu /( exp(h*nu/k/T)-1 )

def CNlamb(lamb,T=273.15):
    """
    Densidad de radiancia espectral del cuerpo negro
        https://en.wikipedia.org/wiki/Planck's_law#Different_forms
    lamb: longitud de onda en metros
    T:    temperatura en kelvin. Por defecto: 273.15
    """
    lamb = array(lamb)
    return 2*h*c**2/lamb**5 /( exp(h*c/k/T/lamb)-1 )


# Frecuencia óptica y temperatura
nu           = logspace(12 , 14, 200)*1.5
Temperaturas = linspace(300, 1000, 8).astype(int)
nu_THz       = nu/1e12  # Para graficar uso una escala más legible, en THz

# Elijo un colormap (cm) y una función de normalización lineal
import matplotlib as mpl
cm = plt.cm.get_cmap('jet')
cn = mpl.colors.Normalize(Temperaturas.min(), Temperaturas.max())

# Creo la figura
fig, ax = plt.subplots(1, 1, figsize=(8,5), constrained_layout=True)

# Para cada tempertura grafico una curva en un color asociado a la temperatura
for T in Temperaturas:
    Bb = CNnu(nu,T)*1.6022e-19 *1e9 # Transformo eV a J y luego a nJ
    ax.plot( nu_THz , Bb , color=cm(cn(T)) )
    
    # Obtengo el máximo de la curva y lo uso para escribir el valor te temperatura
    max_ind = Bb.argmax()
    ax.text(nu_THz[max_ind], Bb[max_ind], f"{T}"+r"${}^\circ$K", 
            ha="center", va="bottom", size=8 , color=cm(cn(T))  )

# Límites de los ejes
ax.set_xlim( 0 , max(nu_THz) )
ax.set_ylim( 0 , ax.get_ylim()[1] )

# Grid
ax.grid(True,ls=':',color='lightgray')

# Genero una barra de color de referencia
fig.colorbar( mpl.cm.ScalarMappable(cmap=cm, norm=cn ) , 
             ax=ax , aspect=40 , label=r'Temperatura [${}^\circ$K]')

# Etiquetas de los ejes
ax.set_xlabel(r'$\nu$ [THz]')
ax.set_ylabel(r'densidad de radiancia espectral  $ \left[ n\mathrm{W} / \mathrm{m}^2 \right] $')


# fig.savefig('06_colormap_a.png')

#%% Mapa de colores para un array de imágenes
"""
Acá hacemos un gráfico 2D donde la dimensión vertical está coloreada
"""

# Extiendo el número de temperaturas a graficar
Temperaturas = linspace(300, 1000, 100).astype(int)

# Contenedor de a imagen
img  = []

# Para cada temperatura genero los valores de densidad de radiancia y los
# apilo en img
for T in Temperaturas:
    Bb = CNnu(nu,T)*1.6022e-19 *1e9 # Transforme eV a J y luego a nJ
    img.append( Bb.tolist() )

# Lo paso a array sólo para facilitar cálculos e isnpección de datos
img = array(img)

# Creo la figura
fig, ax = plt.subplots(1, 1, figsize=(8,5), constrained_layout=True)

# Defino la escala de colroes
escala_de_color = mpl.colors.LogNorm(1e-3,img.max())

# Grafico la imagen usando la escala de colores.
# Con extent defino los límites de a imagen
img_ax = ax.imshow(img , extent=[nu_THz.min(),nu_THz.max(),Temperaturas.min(),Temperaturas.max()],
                      origin='lower', aspect='auto',
                      norm=escala_de_color, cmap='jet')

# Etiquetas de los ejes
ax.set_xlabel(r'$\nu$ [THz]')
ax.set_ylabel(r'Temperatura [${}^\circ$K]')


# Genero una barra de color de referencia
fig.colorbar(img_ax, ax=ax,label=r'densidad de radiancia espectral  $ \left[ n\mathrm{W} / \mathrm{m}^2 \right] $')


ax.set_title('Radiación de cuerpo negro')


# fig.savefig('06_colormap_b.png')
