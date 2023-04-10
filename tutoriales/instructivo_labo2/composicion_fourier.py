#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cálculo de los componentes de serie de Fourier a partir de integración numérica
"""


# from numpy import *
# Importo de NumPy lo que voy a usar
from numpy import pi, iterable, array, arange,cos,sin,ones,zeros,linspace

# Librería para graficar
import matplotlib.pyplot as plt

# Integración numérica con quad
from scipy.integrate import quad

# Herramientas para interactividad
from matplotlib.widgets import Slider


#%% Definiciones y funciones auxiliares

T          = 0.1              # Periodo en segundos
frecuencia = 1/T              # Frecuencia
omega      = 2*pi*frecuencia  # Frecuencia angular

def funcion_periodica(t):
    """
    Función definida entre 0 y T que se repite con periodo T
    """

    # Para facilitar el cálculo, convierto t en un array
    if not iterable(t):
        t = array([t])

    # Contruyo periodicidad T
    t_periodico = t % T

    return array([ 1 if x< T/2 else -1 for x in  t_periodico ])



def serie_fourier(funcion, num_de_armonicos=5):
    """
    Usando la función `funcion` calcula los coeficientes
    de la serie de fouerier.
    Parámetros:
        funcion : función periódica de periodo T
        num_de_armonicos: número de armónico máximo a calcular
    Devuelve:
        A : Lista de coeficientes a_n asociados a cosenos
        B : Lista de coeficientes b_n asociados a senos
    """
    A = []
    B = []

    for n in arange(num_de_armonicos+1):

        producto_cos = lambda t: funcion(t)*cos(n * omega * t )
        producto_sin = lambda t: funcion(t)*sin(n * omega * t )

        a_n = quad( producto_cos , 0 , T, limit=500)[0] * 2/T
        b_n = quad( producto_sin , 0 , T, limit=500)[0] * 2/T

        A.append( a_n )
        B.append( b_n )

    return A,B



def componer_fourier(t,A,B):
    """
    A partir de las componentes de fourer de las listas A y B
    compone la función resultante
    """
    rta = ones(len(t))* A[0]/2

    for n,a_n,b_n in zip(arange(1,len(A)),A[1:],B[1:]):
        rta += a_n*cos(n*omega*t) + b_n*sin(n*omega*t)

    return rta


#%% Imprimir tabla y graficar

# https://en.wikipedia.org/wiki/Fourier_series#Table_of_common_Fourier_series


# Parámetros del problema
ORDEN      = 10

T          = 0.1              # Periodo en segundos
frecuencia = 1/T              # Frecuencia
omega      = 2*pi*frecuencia  # Frecuencia angular


# Definimos la función periódica
def funcion_periodica(t):
    """
    Función definida entre 0 y T que se repite con periodo T
    """

    if not iterable(t):
        t = array([t])

    # Para facilitar el cálculo, convierto t en un array
    t_periodico = t % T

    D = 1/3

    dutty      = array([ 1 if x< T*D else 0 for x in  t_periodico ])
    centrado   = array([ 1 if abs(x-T/2)< T/4 else -1 for x in  t_periodico ])
    sierra     = t_periodico / T
    triangular = abs(t_periodico-T/2)

    return dutty


# Obtenemos coeficientes de la serie de Fourier
A,B = serie_fourier( funcion_periodica , ORDEN )


# Tabla de valores (redondeados al decimal 5)
print("Tabla de coeficientes")
print('| n |   a_n    |   b_n    |')
print('---------------------------')

for n,a,b in zip(arange(len(A)),A,B):
    print(f'|{n:2d} | {a:8.5f} | {b:8.5f} |')




# Gráficos #####################

# Creo eje temporal con 1000 puntos en 3 periodos
t = linspace(0,3*T,1000, endpoint=False)

# Figura
fig, ax = plt.subplots(1,1, figsize=(10,7) ,  constrained_layout=True )

# Funcion y composición de Fourier
ax.plot( t ,  funcion_periodica(t) )
ax.plot( t ,  componer_fourier(t,A,B) )

# Nombres de los ejes y grid
ax.set_xlabel('Tiempo [s]')
ax.set_ylabel('Señal [V]')
ax.grid(b=True,linestyle=':',color='lightgray')




#%% ###########################################################################
#%% Interactivo ###############################################################



# Parámetros del problema
ORDEN      = 10

T          = 0.1              # Periodo en segundos
frecuencia = 1/T              # Frecuencia
omega      = 2*pi*frecuencia  # Frecuencia angular


# Definimos la función periódica
def funcion_periodica(t):
    """
    Función definida entre 0 y T que se repite con periodo T
    """

    if not iterable(t):
        t = array([t])

    # Para facilitar el cálculo, convierto t en un array
    t_periodico = t % T

    D = 1/3

    dutty      = array([ 1 if x< T*D else 0 for x in  t_periodico ])
    centrado   = array([ 1 if abs(x-T/2)< T/4 else -1 for x in  t_periodico ])
    sierra     = t_periodico / T
    triangular = abs(t_periodico-T/2)

    return dutty


# Obtenemos coeficiente de la serie de Fourier
A,B = serie_fourier( funcion_periodica , ORDEN )

A = array(A)
B = array(B)

# Gráficos #####################

# Creo un eje del tiempo
t = linspace(0,3*T,1000, endpoint=False)

# un figura doble ...
fig, ax = plt.subplots(2,1, figsize=(10,7) ,  constrained_layout=True , sharex=True)
ax[0].plot( t ,  funcion_periodica(t) , color='black', lw=3)
linea_serie = ax[0].plot( t ,  componer_fourier(t,A,B) , color='gray', lw=1.5)

# En la segundo subfigura dibujo las componentes por separado
lineas_componentes = []
for n in range(ORDEN+1):
    mask = zeros(len(A))
    mask[n]=1
    lineas_componentes += ax[1].plot( t ,  componer_fourier(t,A*mask,B*mask) , '-' , color=f'C{n}')

# Nombres de ejes y grid
ax[1].set_xlabel('Tiempo [s]')
ax[0].set_ylabel('Señal [V]')
ax[1].set_ylabel('Componente [V]')

for axx in ax:
    axx.grid(b=True,linestyle=':',color='lightgray')


# Figura aparte para el slider
figc, axc = plt.subplots(1,1, figsize=(2,7) ,  constrained_layout=True )

slider_orden = Slider( axc , "Orden" , 0, ORDEN , valinit=0, orientation='vertical',valstep=1)


def update(val):
    "Función de actualización del slider"
    linea_serie[0].set_ydata(  componer_fourier(t,A[0:val+1],B[0:val+1])  )

    for jj,linea in enumerate(lineas_componentes):
        if jj <= val:
            linea.set_visible(True)
            linea.set_alpha( 1 if jj==val else 0.6 )
            linea.set_linewidth( 3 if jj==val else 1.5 )
        else:
            linea.set_visible(False)

    fig.canvas.draw_idle()

slider_orden.on_changed(update)


# Arranco en 0
update(0)





#%% ###########################################################################
#%% Relacion con FFT ##########################################################


from numpy import *


#% Análisis en Fourier

def fourier(y,dt=1,norm=False):
    # Si me pasan un vector de tiempos
    if iterable(dt):
        dt = abs(dt[1]-dt[0])
    N      = len(y)
    #Norma  = 2/N
    Norma  = dt
    if norm:
        Norma  =  exp(-1j*arange(N//2)*pi/N)  * 2/N

    Y      = fft.rfft( y )[0:N//2] * Norma
    ff     = fft.rfftfreq( N , d=dt  )[0:N//2]

    return ff,Y



tiempo = linspace(0, 100*T, 2**18, endpoint=False)


senial = funcion_periodica(tiempo )

senial = senial + random.normal(size=len(tiempo))/3

# fig, ax = plt.subplots(1,1, figsize=(10,7) ,  constrained_layout=True , sharex=True)
# ax.plot(tiempo, senial )


ff, Y = fourier(senial, diff(tiempo[0:2])[0])


fig, ax = plt.subplots(2,1, figsize=(10,7) ,  constrained_layout=True , sharex=True)
ax[0].plot( ff, real(Y) , label='Re(FFT)')
ax[1].plot( ff, imag(Y) , label='Im(FFT)' )

ax[1].set_xlim(-3, (len(A)+1)/T)

# Factor de escala
C = interp(1/T,ff,real(Y))/A[1]

ax[0].plot( arange(len(A))/T , A * C , '-o', alpha=0.7 , label='+ A' )

ax[1].plot( arange(len(A))/T , -B * C , '-o', alpha=0.7 , label='- B')

ax[1].set_xlabel('Frecuencia [Hz]')


for axx in ax:
    axx.legend()
    axx.grid(b=True,linestyle=':',color='lightgray')


