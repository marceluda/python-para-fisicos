# -*- coding: utf-8 -*-
"""
Simulaciones de realimentación
"""

import sys
print(sys.executable)


from numpy import *
import matplotlib.pyplot as plt

import scipy.signal as s

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Ejemplo simple de un bloque pasabajos de 1er orden
# --------------------------------------------------

"""
Vamos a simular la respuesta de un oscilador armónico
"""


# Lo primero y mas fundametnal es definir el paso temporal
dt  = 1e-6

# Defino un sistema simple, de pasabajos orden 1
f0     = 10e3
w0     = 2*pi*f0
gamma  = 2000

# Defino un sistema de orden dos equivalente a un oscilador armónico
# dx^2/dt^2 + gamma * dx/dt + w0^2 * x = F(t)

s1  = s.lti([w0**2],[1,gamma,w0**2]).to_ss()

sist = s1

# Si quiero ver el resultado de dos sistemas tipo oscilador amrtiguado
# concatenados hay que DESCOMENTAR la siguiente línea

# sist = s1*s1


# Función de excitación de tipo escalón
n0 = 1000
tt = arange(100e3)*dt

u1       = ones(len(tt))
u1[0:n0] = 0        # los primeros n0 valores son CERO
t0       = tt[n0]

# Simulación
_, y1, x1 = s.lsim(sist, U=u1, T=tt)

# Grafico respuesta escalón

fig, axx = plt.subplots(1,2, figsize=(14,6),  constrained_layout=True)
ax = axx[0]
ax.plot(tt, u1 , label='entrada' )
ax.plot(tt, y1 , label='salida')


ax.set_xlim(0 , 5e-3)

ax.plot(tt[n0:], 1+exp(-gamma/2 * (tt[n0:]-tt[n0]) ) , label='Curva teorica exp(-gamma/2 * t)')

ax.axhline(1+exp(-1), color='C3', ls='--', label="límite de caida a 1/e")



ax.legend()
ax.set_xlabel('tiempo [s]')
ax.set_ylabel('valor')
ax.grid(True,ls=':',color='lightgray')
ax.set_title('Step Response')









#% Análisis en Fourier

def fourier(y,dt=1,norm=False):
    # Si me pasan un vector de tiempos
    if iterable(dt):
        dt = abs(dt[1]-dt[0])
    N      = len(y)
    Norma  = dt
    if norm:
        Norma  =  exp(-1j*arange(N//2)*pi/N)  * 2/N

    Y      = fft.rfft( y )[0:N//2] * Norma
    ff     = fft.rfftfreq( N , d=dt  )[0:N//2]

    return ff,Y


# Calculo la tranformada de Fourier para los valores a partir del tiempo del escalón
ff, Y1 = fourier(y1[n0:],dt)


ax = axx[1]

# Calculo la FFT al cuadrado (modulo) y saco el valor de la constante inicial
fft_abs = abs(Y1)[1:]**2
ff      = ff[1:]

ax.plot( ff , fft_abs/fft_abs.max() , label='$|FFT|^2$ normalizada')
ax.axhline(0.5, color='C3', ls='--', label="Mitad de altura")

# Lorentziana teórica:
# https://www.phys.ufl.edu/courses/phy4803L/group_III/sat_absorbtion/Lorentzian.pdf
ax.plot( ff, 1/(1+4*(ff-f0)**2/(gamma/2/pi)**2) , ':', lw=3 , label="curva teórica Lorentziana")

ax.set_xlim(6e3 , 14e3)
ax.set_xlabel('frecuencia [Hz]')
ax.set_ylabel('$|FFT|^2$')
ax.grid(True,ls=':',color='lightgray')
ax.set_title('Transformada de fourier (normalizada)')

ax.legend()




#%% Diferencia entre dos puntos

datos = array(plt.ginput(2))

print( diff(datos[:,0]) )
