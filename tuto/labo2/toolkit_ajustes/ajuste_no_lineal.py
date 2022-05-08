#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Ajuste de funciones no lineales con interfaz gráfica (para Spyder)

"""



from numpy import *
import numpy as np

import matplotlib.pyplot as plt


from scipy.optimize import least_squares
# Documentacion: 
# 

# Doc de ayuda:
#  - https://scipy-cookbook.readthedocs.io/items/robust_regression.html
#  - http://kitchingroup.cheme.cmu.edu/blog/category/data-analysis/3/

# Filtros útiles:
from scipy.signal import savgol_filter as savgol


# Funciones y librerías auxiliares necesarias
from scipy.stats.distributions import  t as t_student


from matplotlib.widgets import Slider, Button
from matplotlib.ticker import AutoLocator




#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%% Modelo Para el fiteo ######################################################
def modelo(x,params):
    """
    Modelo que se va a usar para ajustar los datos
        x: valores del eje x
        params: lista o vector de parámetros
    devuelve:
        valores del eje y
        """
    m,y0,A,x0,w0,x1,w1 = params
    
    if not type(x)==ndarray:
        x = array(x)
    
    y = m*x+y0
    y+= A/( 1+ ( (x-x0)/w0  )**2 )
    y+= A/( 1+ ( (x-x1)/w1  )**2 )
    
    return y

# Acá ponemos la info de los parámetros 
nombres              = "m,y0,A,x0,w0,x1,w1".split(',')
parametros_iniciales = [      0 ,        0 ,    10 ,    30 ,   10 ,    70 ,   10 ]
limites              = [[-10,10],[-100,100],[0,100],[0,100],[0,40],[0,100],[0,40]]


# Opciones de ajuste 
GRAFICAR_PASO_A_PASO = True   # Ver en cada paso del algoritmo el gráfico
AJUSTAR_CON_LIMITES  = True   # Utilizar límites para el ajuste de parámetros
AJUSTAR_CON_ESCALAS  = True 

USAR_DATOS_FICTICIOS = True

if USAR_DATOS_FICTICIOS:
    random.seed(0)
    parametros_reales = [-0.3, 30, 25, 40,5,47,3]
    datos_x  = linspace(20,80,80)
    datos_y  = modelo(datos_x , parametros_reales )
    datos_y += random.normal(size=len(datos_y))

else:
    datos_x  =  array([0,1])
    datos_y  =  array([0,1])


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%% Funciones para calcular convarianza a partir de lo que devuelve least_squares
def calcular_cov_curve_fit(res):
    """
    Sacado de cómo calcula la covarianza el propio curve_fit
    https://github.com/scipy/scipy/blob/2526df72e5d4ca8bad6e2f4b3cbdfbc33e805865/scipy/optimize/minpack.py#L739
    """
    U, S, V = np.linalg.svd(res.jac, full_matrices=False)
    threshold = np.finfo(float).eps * max(res.jac.shape) * S[0]
    S = S[S > threshold]
    V = V[:S.size]
    pcov = np.dot(V.T / S**2, V)
    
    s_sq = 2 * res.cost / (res.fun.size - res.x.size)
    pcov = pcov * s_sq
    return pcov

def calcular_cov_wiki(res):
    """
    La otra version es sacarlo del Jacoviano
    https://en.wikipedia.org/wiki/Ordinary_least_squares#Finite_sample_properties
    El jacoviano es una aproximacion de X en el link de arriba
    Luego, se siguí lo de esa pag. Da muy parecido a lo anterior
    """
    
    J     = res.jac
    pcov  = np.linalg.inv(J.T.dot(J)) * sum(res.fun**2)/len(residuos(res.x))
    return pcov

def ajustar_modelo():
    """
    Realiza el ajuste del modelo usando la función least_squares
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html
    """
    # definimos la función de residuos
    def residuos_ls(params):
        rta = datos_y - modelo( datos_x ,params )
        
        # Opcionalmente, graficamos paso a paso
        if GRAFICAR_PASO_A_PASO:
            graficar_parametros(params)
            plt.pause(0.05)
        return rta
    
    # Definimos otros parámetros opcionales
    otros_params = {}
    global limites
    if AJUSTAR_CON_LIMITES:
        otros_params['bounds'] = array(limites).T
    
    if AJUSTAR_CON_ESCALAS:
        otros_params['x_scale'] = [ abs(diff(l).mean()/20) for l in limites ]
    
    # Realizamos ajuste
    res = least_squares( residuos_ls, 
                         x0      = parametros_obtenidos , 
                         loss    = 'soft_l1' ,  #  'linear' 'soft_l1' 'cauchy'
                         verbose = 1,
                         **otros_params)
    
    # Guardamos resultados del ajuste en una variable global
    global resultados
    resultados['parametros'] = res.x
    resultados['N']          = len(res.fun)
    resultados['P']          = len(res.x)
    resultados['COV']        = calcular_cov_curve_fit(res)
    resultados['SE']         = sqrt(diag(  resultados['COV']  ))
    resultados['SSE']        = sum(( res.fun )**2)
    resultados['SST']        = sum(( datos_y - mean(datos_y))**2)
    #  http://en.wikipedia.org/wiki/Coefficient_of_determination
    resultados['Rsq']        =  1 - resultados['SSE']/resultados['SST']
    resultados['Rsq_adj']    = 1-(1-resultados['Rsq'])* (len(res.fun)-1)/(len(res.fun)-len(res.x)-1)
    
    global residuos
    residuos = datos_y - modelo(datos_x,res.x)
    return res




def print_res(alpha=0.05):
    """
    Imprimir datos fiteo realizado en forma entendible
    """
    print('Datos del fiteo:\n')
    
    global resultados

    for par in ['N', 'P', 'SSE', 'SST', 'Rsq', 'Rsq_adj']:
        print('{:15s}: {:8.5f}'.format( par , resultados[par]) )
    
    SE = resultados['SE']
    N  = resultados['N']
    P  = resultados['P']
    
    print('\n')
    print('Parámetros con su Error Estandar:')
    for val,par,err in zip(resultados['parametros'], nombres ,  SE  ):
        #print(par.name.ljust(15) + ': ' + str(val) )
        print('{:15s}: {:8.3f} ± {:8.3f}'.format(par,val,err))
    
    print('\nIntervalos de confianza:\n')
    #alpha = 0.05 # 100*(1 - alpha) confidence level
    print('Confianza: {:5.2f}%   | alpha={:5.3f}'.format( (1-alpha)*100  , alpha ) )
    
    sT = t_student.ppf(1.0 - alpha/2.0, N - P ) # student T multiplier
    CI = sT * SE
    
    for nn, par, ci in zip(nombres,resultados['parametros'], CI):
        print( '{4:15s}: {2: 8.3f} ± {3: 8.3f} [{0: 8.3f} : {1: 8.3f}]'.format(par - ci, par + ci, par, ci, nn) )
        
    print('\n'*4 + '-'*20 + '\n'*2)
    print('Si querés repetir este ajuste, partiste de los parámetros iniciales:')
    print(parametros_obtenidos)



def graficar_parametros_ajuste():
    """
    Esta función grafica 3 relaciones útiles para entender el ajuste
     - La matriz de correlación entre parámetros: https://en.wikipedia.org/wiki/Correlation
     - La matriz de covarianza entre parámetros
     - Comparación entre el histograma de residuos y una distribución normal (del mismo STD)
    """
     
    def corrMat(data):
        rows, cols = data.shape
        
        corr_mat = data * 0
        for i in range(rows):
            for j in range(cols):
                x_dev = sqrt(data[i,i])
                y_dev = sqrt(data[j,j])
                corr_mat[i][j] = data[i,j] / ( x_dev * y_dev )
        return corr_mat
    
    
    fig, (ax1,ax2,ax3) = plt.subplots(1,3, figsize=(14,4),  constrained_layout=True)
    fig.set_constrained_layout_pads(w_pad=2/72, h_pad=2/72, hspace=0, wspace=0.2)
    
    global resultados
    global residuos
    cov_matrix = resultados['COV']
    cor_matrix = corrMat(cov_matrix)
    
    
    img = ax1.imshow(cor_matrix, cmap='bwr')
    img.set_clim(-1,1)
    ax1.xaxis.tick_top()
    ax1.set_xticks( arange(len(nombres)) )
    ax1.set_xticklabels( nombres   )
    ax1.set_yticks( arange(len(nombres)) )
    ax1.set_yticklabels( nombres   )
    fig.colorbar(img,ax=ax1,shrink=0.7,aspect=30)
    ax1.set_title('Matriz de correlación')
    
    img = ax2.imshow(cov_matrix, cmap='bwr')
    img.set_clim(-abs(cov_matrix).max(),abs(cov_matrix).max())
    ax2.xaxis.tick_top()
    ax2.set_xticks( arange(len(nombres)) )
    ax2.set_xticklabels( nombres   )
    ax2.set_yticks( arange(len(nombres)) )
    ax2.set_yticklabels( nombres   )
    fig.colorbar(img,ax=ax2,shrink=0.7,aspect=30)
    ax2.set_title('Matriz de covarianza')
    
    ax3.hist(residuos,density=True)
    ax3.set_title('Residuos')
    lim    = ax3.get_xlim()
    ww     = std(residuos     )
    xx_dat = linspace( lim[0], lim[1] )
    yy_dat = 1/sqrt(2*pi)/ww * exp( - (xx_dat/ww)**2 /2 )
    ax3.plot(xx_dat, yy_dat, color='red')
    ax3.set_xlim(lim)
    ax3.set_xlabel('Residuos')
    ax3.set_ylabel('Densidad de probabilidad')


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%% Para fitear a mano ********************************************************


# Armamos arrays del modelo
modelo_x = datos_x
modelo_y = modelo( modelo_x , parametros_iniciales)
residuos = modelo_y - datos_y





# En esta figura graficamos los datos y residuos
fig, axx = plt.subplots( 2,1, figsize=(12,6) ,  constrained_layout=True, 
                        sharex=True, gridspec_kw={'height_ratios': [1,0.2]} )    

plt_datos, = axx[0].plot(  datos_x,  datos_y , '.' , color='C0'  )
plt_model, = axx[0].plot( modelo_x, modelo_y , '-' , color='C3' )

plt_zero  = axx[1].axhline( 0 , ls='-' , color='C3' )
plt_res,  = axx[1].plot(     datos_x,  residuos , '.' , color='C0'  )

axx[0].set_ylabel('datos_y [unidad]')
axx[1].set_ylabel('residuos [unidad]')
axx[1].set_xlabel('datos_x [unidad]')

# Ponemos un grid
for ax in axx:
    ax.grid(b=True,linestyle= ':',color='lightgray')





# En esta figura colocamos los controles de los parámetros
fig_control, ax_control = plt.subplots( len(parametros_iniciales)+1,1, figsize=(6,4) ,  constrained_layout=True)

# Vector de los objetos sliders que vamos a crear
vector_sliders = []

# Creamos los objetos
for ax,nombre,limite,par_inicial in zip(ax_control[:-1],nombres,limites,parametros_iniciales):
    vector_sliders.append( 
                Slider(ax, nombre , min(limite), max(limite) , valinit=par_inicial)
            )
    ax.xaxis.set_major_locator(AutoLocator())

# En esta lista vamos a guardar los parámetros obtenidos
parametros_obtenidos = []

# Funcion para actualizar los parámetros en la figura de datos
def graficar_parametros(params):
    """
    Actualiza los parámetros del modelo en el gráfico
    """
    plt_model.set_ydata(  modelo(datos_x, params )  )
    plt_res.set_ydata(    modelo(datos_x, params )- datos_y  )
    
    # Acomodamos los ejes a los nuevos máximos y mínimos
    for ax in axx:
        maxY = max( [ max(linea.get_ydata()) for linea in ax.get_lines() ] )
        minY = min( [ min(linea.get_ydata()) for linea in ax.get_lines() ] )
        DY   = maxY - minY
        ax.set_ylim( minY-DY/10  , maxY+DY/10  )

# Esta funcion controla que hacer cuando cambiamos valores en el slider
def update(val=0):
    global parametros_obtenidos
    params = [ y.val for y in vector_sliders ]
    parametros_obtenidos = params.copy()
    graficar_parametros(params)
    fig.canvas.draw_idle()

# Asignamos la función de los widget sliders
for sl in vector_sliders:
    sl.on_changed(update)

# Corremos un update inicial
update()

# Agregamos un botón para hacer ajustes
button = Button(ax_control[-1], 'Ajustar', color='lightblue', hovercolor='lightgreen')


resultados = {}


def fitear(event):
    plt.close(fig_control)
    ajustar_modelo()
    print_res()
    graficar_parametros_ajuste()


button.on_clicked(fitear)




#%% Trozos de código para correr al hacer pruebas *****************************
# Estan dentro de un if False para evitar que se ejecuten al correr el script entero

#%% Ejemplo de datos iniciales que dan bien
if False:
    par_inicio = [-0.29979, 30.61889, 28.46908, 40.69042,  2.49234, 46.93352, 1.31628]
    
    for sl,val in zip(vector_sliders,par_inicio):
        sl.set_val(val)


#%% Ejemplo de datos iniciales feos pero que dan bien
if False:
    par_inicio = [-0.16627,  7.30926, 29.9    , 45.29889, 13.93422, 43.32468, 13.77628]
    
    for sl,val in zip(vector_sliders,par_inicio):
        sl.set_val(val)

#%% Ejemplo de datos iniciales que DAN MAL
if False:
    par_inicio = [0, 0, 10, 30, 10, 70, 10]
    
    for sl,val in zip(vector_sliders,par_inicio):
        sl.set_val(val)



