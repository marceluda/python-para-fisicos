#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#%% Importaciones

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit,least_squares


###############################################################################
#%% Generamos los datos a fitear



# Generamos tiras de datos que simulan ser resultados de modiciones
# Pensamos en algún fenomeno que da como resultado de una medición dos
# campanas gaussianas superpuestas. La forma de esas campanas depende de 
# 4 valores que fijamos de forma exacta para fabricarnos los datos
# Si el ajuste funciona bien, deberíamos recuperarlos luego.

# En el eje x, 100 valores equiespaciados entre 0 y 10
x_datos  = np.linspace(0, 10, 100)

# En el eje y, las gaussianas superpuestas, calculadas a partir de x
y_exacto = np.exp(-(x_datos-2.8)**2/0.5**2)+np.exp(-(x_datos-4.8)**2/1.5**2)

# Pare comparar despues
# Parametros en orden de aparición: 
parametros_reales = [2.8, 0.5, 4.8, 1.5]

# Agregamos algo de "ruido" para darle realismo
np.random.seed(1729)

# Ruido con distribución normal escalado a 0.05
y_ruido = 0.05 * np.random.normal(size=x_datos.size)

# Agregamos el ruido para tener la serie de datso de y que simula ser
# el resultadod e un experimento
y_datos = y_exacto + y_ruido


# Esta es la comparación entre los valoers exatos del fenómeno que uno desea 
# analizar y los que "logramos medir", con el ruido incluido.


plt.figure()
plt.plot(x_datos,  y_datos, 'o', label='datos medidos')
plt.plot(x_datos, y_exacto, '-', label='curva exacta')
plt.legend(loc='best')
plt.xlabel('x')
plt.ylabel('y')
plt.tight_layout()
# plt.savefig('datos-originales.png',dpi=150)


###############################################################################
#%% Ajuste de datos usando curve_fit
# Referencia de curve_fit
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html

# Definimos un modelo. Es una función, cuyo primer argumento son los valores
# del eje x y el resto de los argumentos son los parámetros a hallar

def modelo(x, a, b, c, d):
    return np.exp(-(x-a)**2/b**2)+np.exp(-(x-c)**2/d**2)

# Parámetros iniciales con los que vamos a iniciar el proceso de fiteo
parametros_iniciales=[2, 1, 6, 1]

# Hacemos el ajuste con curve_fit
popt, pcov = curve_fit(modelo, x_datos, y_datos, p0=parametros_iniciales)

# curve_fit devuelve dos resultados. El primero (popt) son los
# parámetros óptimos hallados. El segundo (pcov) es la matris de 
# covarianza de los parametros hallados.

x_modelo  = np.linspace(0, 10, 1000)


plt.figure()
plt.plot( x_datos,                 y_datos,  'o', label='datos')
plt.plot(x_modelo, modelo(x_modelo, *popt), 'r-', label='modelo ajustado')
plt.legend(loc='best')
plt.xlabel('x')
plt.ylabel('y')
plt.tight_layout()
# plt.savefig('ajuste-con-curve_fit.png',dpi=150)


# popt tiene los parámetros hallados en orden
print(popt)

print('\n')

# De la matris de covarinza podemos obtener los valores de desviacion estandar
# de los parametros hallados
pstd = np.sqrt(np.diag(pcov))

nombres_de_param=['a','b','c','d']
print('Parámetros hallados:')
for i,param in enumerate(popt):
    print('{:s} = {:5.3f} ± {:5.3f}'.format( nombres_de_param[i] , param , pstd[i]/2) )



###############################################################################
#%% Fiteo usando Least squares

# Documentacion:
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html

from scipy.optimize import least_squares

def modelo(p,x):
    # p es un vector con los parámetros
    # x es el vector de datos x
    return np.exp(-(x-p[0])**2/p[1]**2)+np.exp(-(x-p[2])**2/p[3]**2)

param_list = []

def residuos(p, x, y):
    # p es un vector con los parámetros
    # x es el vector de datos x
    # y es el vector de datos y
    y_modelo = modelo(p, x) 
    plt.clf()
    plt.plot(x,y,'o',x,y_modelo,'r-')
    plt.pause(0.05)
    param_list.append(p)
    return y_modelo - y


# Otros parámetros iniciales
# parametros_iniciales=[0, 3, 10, 3]  # No ajusta
# parametros_iniciales=[0, 3, 8, 3]  # Ajusta mal

parametros_iniciales=[1, 2, 8, 3]  # Ajusta

res = least_squares(residuos, parametros_iniciales, args=(x_datos, y_datos), verbose=1)

# Estos son los parámetros hallados
print(res.x)


# Calculamos la matriz de covarianza
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

# De la matriz de covarinza podemos obtener los valores de desviacion estandar
# de los parametrso hallados
pstd = np.sqrt(np.diag(pcov))

print('Parámetros hallados:')
for i,param in enumerate(res.x):
    print('parametro[{:d}]: {:5.3f} ± {:5.3f}'.format(i,param,pstd[i]/2))


y_modelo = modelo(res.x, x_datos)

plt.figure()
plt.plot(x_datos, y_datos ,  'o', markersize=4, label='datos')
plt.plot(x_datos, y_modelo, 'r-',               label='modelo fiteado')
plt.xlabel("x")
plt.ylabel("y")
plt.legend(loc='best')
plt.tight_layout()



###############################################################################
#%% Animacion que reconstruye los pasos de cuadrados mínimos

from matplotlib.animation import FuncAnimation

param_list = np.array(param_list)

num_params = param_list[0,:].size
len_params = param_list[:,0].size

fig = plt.figure(figsize=(10,6))
fig.set_tight_layout(True)


ax = []
ax.append( plt.subplot2grid((1,num_params*2), (0, 0), colspan=num_params ) )
curva_param = []
for i in range(num_params):
    ax.append( plt.subplot2grid((1,num_params*2), (0, num_params+i) ) )
    ax[-1].set_ylim(len_params,0)
    ax[-1].set_yticks([])
    max_err = np.max(np.abs(param_list[:,i]-parametros_reales[i]))
    ax[-1].set_xlim(parametros_reales[i]-max_err,parametros_reales[i]+max_err)
    ax[-1].set_xticks([parametros_reales[i]-max_err,parametros_reales[i],parametros_reales[i]+max_err])
    ax[-1].set_xticklabels(['','p'+str(i),''])
    ax[-1].plot( [parametros_reales[i]]*2 , [0,len_params], '-')
    curva_param.append( ax[-1].plot( param_list[:,i] , np.arange(len_params) , 'r.-') )
    ax[-1].set_xlabel('{:3.3f}'.format(param_list[-1,i]))
curva_datos  = ax[0].plot(x_datos, y_datos ,  'o', markersize=4, label='datos')
curva_modelo = ax[0].plot(x_datos, y_modelo, 'r-',               label='modelo fiteado')

ax[0].set_xlabel("x")
ax[0].set_ylabel("y")
ax[0].legend(loc='best')


def actualizar(i):
    etiqueta = 'paso {:>2d}'.format(i)
    print(etiqueta)
    curva_modelo[0].set_ydata( modelo(param_list[i], x_datos) )
    for j in range(num_params):
        curva_param[j][0].set_ydata( np.arange(0,1+i) )
        curva_param[j][0].set_xdata( param_list[0:i+1,j] )
        ax[1+j].set_xlabel('{:3.3f}'.format(param_list[i,j]))
        
    ax[0].set_title(etiqueta)
    return [curva_modelo[0]]+ [y[0] for y in curva_param] + ax


anim = FuncAnimation(fig, actualizar, frames=np.arange(len_params), interval=250)

# anim.save('ajuste-least_squares.gif', dpi=80, writer='imagemagick')






















