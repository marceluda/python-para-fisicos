#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gráficos avanzados
"""

from numpy import *
import numpy as np
import matplotlib.pyplot as plt

# Tamaño del texto por defecto
plt.rcParams.update({'font.size': 11})


#%% Mapas de colores
"""
Mapa de colores para distintas curvas
"""


random.seed(0)

# Fabrico datos
datos_x  = linspace(0,3*pi,500)
datos_y  = 1.2*cos(2*datos_x+pi/3)

datos_x += random.normal(size=len(datos_x))*0.03
datos_y += random.normal(size=len(datos_y))*0.1

# Realizamos el ajuste
modelo = lambda x,f,x0,A: A*cos(f*x+x0)

from scipy.optimize import curve_fit
popt, pcov = curve_fit(modelo, datos_x, datos_y, p0=[1.9,1,1] )

modelo_y = modelo(datos_x,*popt)


# Creo la figura
fig, axx = plt.subplots(2, 2, figsize=(8,5), constrained_layout=True, 
                        sharex='col', sharey='row', 
                        gridspec_kw={'height_ratios': [0.7,0.3] , 'width_ratios': [0.8,0.2]} )
fig.set_constrained_layout_pads(w_pad=2/72, h_pad=2/72, hspace=0, wspace=0)


# Datos y modelo  *************************************************************
ax=axx[0,0]
ax.plot(datos_x, datos_y, '.', ms=2 , label='datos')
ax.plot(datos_x, modelo_y, '-', color='red', lw=1, alpha=0.7 , label='ajuste')

ax.legend()
ax.set_ylabel('desplazamiento [cm]')
ax.set_title('Medición')

# Residuos ********************************************************************
ax=axx[1,0]
ax.plot(datos_x, datos_y-modelo_y, '.', ms=2)
ax.axhline( 0, color='red', lw=1, alpha=0.7 )
ax.set_ylabel('residuos [cm]')
ax.set_xlabel('tiempo [s]')

# Distribucion de los residuos ************************************************
ax=axx[1,1]
hh=ax.hist( datos_y-modelo_y, 30, orientation='horizontal', alpha=0.7 )

ax.set_xlabel('conteo')

# graficamos la gaussiana de la densidad de probabilidad, normalizada a la 
# cantidad de datos que tenemos 
lim = ax.get_ylim()
yy  = linspace(lim[0],lim[1],300)
ss  = std(datos_y-modelo_y)
ax.plot( exp(-(yy/ss)**2/2)/ss/sqrt(2*pi)*len(datos_y)*diff(hh[1]).mean()  , yy , color='red') 
ax.set_ylim(lim)

# Distribucion de los datos ***************************************************
ax=axx[0,1]
ax.hist( datos_y, bins=30, orientation='horizontal',  alpha=0.7 )

# graficamos la densidad de probabilidad, normalizada a la 
# cantidad de datos que tenemos 
yy = linspace(-1,1,300)[1:-1]*popt[2]
Norma = diff(yy).mean()/pi/2*len(datos_y)
ax.plot( 1/(1-(yy/popt[2])**2)/popt[2]*Norma , yy , color='red')

ax.set_title('Estadística')

# Grid ************************************************************************
for ax in axx.flatten():
    ax.grid(b=True, ls=':', color='lightgray')

# fig.savefig('08_residuos.png')

