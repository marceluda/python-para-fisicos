#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gráficos avanzados
"""

from numpy import *
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 12})

from scipy.special import erf

from scipy.signal import savgol_filter as savgol

#%% Errores
"""
Formas de graficar el error o la incerteza.
"""



fig, axx = plt.subplots(1, 2, figsize=(12,6), constrained_layout=True)



# Errores con errorbar ########################################################
ax = axx[0]


# Armamos datos simulando mediciones con errores
random.seed(2)

xx         = linspace(-3,3,12)
yy         = erf(xx)

xx_err     = ( ones(len(xx)) + 4*random.uniform(size=len(xx)) )/15
yy_err     = ( ones(len(xx)) + 2*random.uniform(size=len(xx)) )/40

datos_x    = xx + array([ random.normal(0,err) for err in xx_err])
datos_y    = yy + array([ random.normal(0,err) for err in yy_err])
################


# Graficamos el modelo ideal
ax.plot(linspace(-3,3,100), erf(linspace(-3,3,100)) , '-', 
        color='gray', alpha=0.5  , label='ideal')

# Graficamos los datos medidos con errores
ax.errorbar( datos_x, datos_y, xerr=xx_err, yerr=yy_err, 
            fmt='s', mfc='none', elinewidth = 1, capsize=3 , label='datos')

# Configuraciones generales
ax.set_xlabel('datos x [unidades]')
ax.set_ylabel('datos y [unidades]')
ax.grid(b=True, ls= ':', color='lightgray')
ax.set_title('Errores con errorbar()')

ax.legend()



# Errores con fill_between ####################################################
ax = axx[1]


# Armamos datos simulando mediciones con errores sólo en Y
random.seed(5)
xx         = linspace(-6,6,300)
yy         = sinc(xx)

# El error que estimamos que hubo en la medición
yy_err     = abs(yy)**(1/2) * 0.2

# El error que tuvimos al medir (y desconocemos)
yy_err_med = savgol( random.normal(size=len(xx))*yy_err , 15, 1 )*2
datos_y    = yy + yy_err_med
################



ax.plot( xx, datos_y  , '-', 
        color='C0', lw=2  , label='datos')

ax.fill_between( xx , datos_y-yy_err , datos_y+yy_err , 
                alpha=0.3 , color='C0' , label='errores')

# Configuraciones generales
ax.set_xlabel('datos x [unidades]')
ax.set_ylabel('datos y [unidades]')
ax.grid(b=True, ls= ':', color='lightgray')
ax.set_xlim(-6,6)

ax.set_title('Errores con fill_between()')

ax.legend()

# fig.savefig('05_errores_a.png')


#%% Errores de un ajuste
"""
Errores de datos y incerteza de predicción de un ajuste
"""


# Armamos datos simulando mediciones con errores
random.seed(7)

xx         = linspace(0,10,10)
yy         = 3.2*xx+1.4

# Asumimos un error de medición fijo para el eje x de 0.6
# Asumimos un error de medición fijo para el eje x de 3

# Errores de los datos
xx_err     = random.uniform(size=len(xx))*0.6
yy_err     = random.uniform(size=len(xx))*3

datos_x    = xx + array([ random.normal(0,err) for err in xx_err])
datos_y    = yy + array([ random.normal(0,err) for err in yy_err])
################

# Graficamos los datos con sus errores
fig, ax = plt.subplots(1, 1, figsize=(8,5), constrained_layout=True)


# Graficamos los datos medidos
ax.errorbar( datos_x, datos_y, xerr=0.6, yerr=3, 
            fmt='s', mfc='none', elinewidth = 1, capsize=3 , label='datos')

# Guardo los límites actuales
lim = ax.get_xlim()


# Ajustamos un modelo  y = A*x+B
par, pcov    = polyfit(datos_x , datos_y, 1 , cov=1)
A,B          = par
A_err, B_err = sqrt(diag(pcov))

print("Resultado del ajuste: y = A*x+B")
print(f"A = {A} ± {A_err}")
print(f"B = {B} ± {B_err}")
print("\n")


# Calculamos valores que predice el modelo y sus incertezas
modelo_x     = linspace(lim[0],lim[1],300)
modelo_y     = A*modelo_x+B
# Ver:  https://stats.stackexchange.com/a/145220
modelo_y_err = sqrt( pcov[0,0] * modelo_x**2  + pcov[1,1] + 2*modelo_x*pcov[0,1] )



# Graficamos el ajuste
ax.plot( modelo_x,  modelo_y, color='C3' , lw=2 , label='modelo ajustado')

# Graficamos la incerteza del ajuste
ax.fill_between( modelo_x , modelo_y-modelo_y_err , modelo_y+modelo_y_err , 
                alpha=0.2 , color='C3' , label='incerteza modelo')


ax.set_xlabel('datos x [unidades]')
ax.set_ylabel('datos y [unidades]')
ax.grid(b=True, ls= ':', color='lightgray')
ax.legend()

ax.set_xlim(lim)


# fig.savefig('05_errores_b.png')
