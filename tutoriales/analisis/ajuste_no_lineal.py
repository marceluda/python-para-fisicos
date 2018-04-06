#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#%% Importaciones

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


###############################################################################
#%% Fiteo usando curve_fit

# Referencia de curve_fit
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html

def modelo(x, a, b, c, d):
    return np.exp(-(x-a)**2/b**2)+np.exp(-(x-c)**2/d**2)


x_datos  = np.linspace(0, 10, 100)
y_exacto = modelo(x_datos, 2.8, 0.5, 4.8, 1.5)


np.random.seed(1729)
y_ruido = 0.05 * np.random.normal(size=x_datos.size)
y_datos = y_exacto + y_ruido

plt.figure()
plt.plot(x_datos, y_datos, 'o', label='datos')
plt.legend(loc='best')
plt.xlabel('x')
plt.ylabel('y')
plt.tight_layout()

#%%

parametros_iniciales=[2, 1, 6, 1]

popt, pcov = curve_fit(modelo, x_datos, y_datos, p0=parametros_iniciales)
popt


plt.clf()
plt.plot(x_datos, y_datos, 'o', label='datos')
plt.plot(x_datos, modelo(x_datos, *popt), 'r-',
         label='fit: a=%5.3f, b=%5.3f, c=%5.3f, d=%5.3f' % tuple(popt))
plt.legend(loc='best')
plt.xlabel('x')
plt.ylabel('y')
plt.tight_layout()


# popt tiene los parámetros hallados
popt


# De la matris de covarinza podemos obtener los valores de desviacion estandar
# de los parametrso hallados
pstd = np.sqrt(np.diag(pcov))

print('Parámetros hallados:')
for i,param in enumerate(popt):
    print('parametro[{:d}]: {:5.3f} ± {:5.3f}'.format(i,param,pstd[i]/2))





###############################################################################
#%% Fiteo usando Least squares

# Documentacion:
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html

from scipy.optimize import least_squares

def modelo(p,x):
    # p es un vector con los parámetros
    # x es el vector de datos x
    return np.exp(-(x-p[0])**2/p[1]**2)+np.exp(-(x-p[2])**2/p[3]**2)

def residuos(p, x, y):
    # p es un vector con los parámetros
    # x es el vector de datos x
    # y es el vector de datos y
    y_modelo = modelo(p, x) 
    plt.clf()
    plt.plot(x,y,'o',x,y_modelo,'-')
    plt.pause(0.05)
    return y_modelo - y



parametros_iniciales=[2, 1, 6, 1]
res = least_squares(residuos, parametros_iniciales, args=(x_datos, y_datos), verbose=1)


# Estos son los parámetros hallados
res.x


# Calculamos la matris de covarianza
# https://stackoverflow.com/questions/40187517/getting-covariance-matrix-of-fitted-parameters-from-scipy-optimize-least-squares

def calcular_cov(res,y_datos):
    U, S, V = np.linalg.svd(res.jac, full_matrices=False)
    threshold = np.finfo(float).eps * max(res.jac.shape) * S[0]
    S = S[S > threshold]
    V = V[:S.size]
    pcov = np.dot(V.T / S**2, V)
    
    s_sq = 2 * res.cost / (y_datos.size - res.x.size)
    pcov = pcov * s_sq
    return pcov


pcov = calcular_cov(res,y_datos)

# De la matris de covarinza podemos obtener los valores de desviacion estandar
# de los parametrso hallados
pstd = np.sqrt(np.diag(pcov))

print('Parámetros hallados:')
for i,param in enumerate(res.x):
    print('parametro[{:d}]: {:5.3f} ± {:5.3f}'.format(i,param,pstd[i]/2))


y_modelo = modelo(res.x, x_datos)

plt.figure()
plt.plot(x_datos, y_datos , 'o', markersize=4, label='datos')
plt.plot(x_datos, y_modelo, '-',               label='modelo fiteado')
plt.xlabel("x")
plt.ylabel("y")
plt.legend(loc='best')
plt.tight_layout()




