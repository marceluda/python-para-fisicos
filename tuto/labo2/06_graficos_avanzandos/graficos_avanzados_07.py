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


def filtro_butterworth(ff,fc=1,n=2,G=1):
    rta = ones(len(ff))+ G
    
    for jj in arange(n):
        ss  = 2*pi*fc*exp( 1j*pi/2/n * (2*jj+n+1) )
        rta = rta*2*pi*fc/(1j*2*pi*ff - ss )
    return rta/2


def filtro_bandstop(ff,f0=1,ll=1):
    s   = 2*pi*1j*ff
    a0  = (2*pi*f0)**2
    a1  = ll
    return (s**2 + a0)/(s**2+a1*s+a0)


f_stop = 50e3
f_cut  = 25e3

ff  = logspace(3,6,1000).tolist()
ff += ( linspace(-1000,1000,51) + f_stop ).tolist()
ff  = sort(ff)

f1 = filtro_butterworth(ff , fc=f_cut)*1.2
f2 = filtro_bandstop(   ff , f0=f_stop, ll=100e3 )

# Creo la figura
fig, axx = plt.subplots(2, 1, figsize=(8,5), constrained_layout=True, sharex=True )

ax = axx[0]
ax.plot( ff , 20*log10(abs(f1)) , label='butterworth' )
ax.plot( ff , 20*log10(abs(f2)) , label='bandstop' )

ax.set_ylabel('$|G|$ [dB]')
ax.legend()





ax = axx[1]
ax.plot( ff , unwrap(angle(f1))*180/pi )

I=ff<f_stop
ax.plot( ff[I] , unwrap(angle(f2))[I]*180/pi )
I=ff>f_stop
ax.plot( ff[I] , unwrap(angle(f2))[I]*180/pi , color='C1')

ax.set_ylabel(r'$\Delta \phi$ [${}^\circ$]')
ax.semilogx()

ax.set_yticks( arange(-180,181,30) )
ax.set_ylim( -180 , 100 )
ax.set_xlabel('frecuencia [Hz]')


# Grid
for ax in axx:
    ax.grid(True, ls=':', color='lightgray')
    ax.grid(True, ls=':', color='lightgray', which ='minor', axis='x', alpha=0.6)

    ax.axvline( f_cut  , ls='--' , color='C0', alpha=0.5, lw=1 )
    ax.axvline( f_stop , ls='--' , color='C1', alpha=0.5, lw=1 )


axx[0].text( f_cut,   0, "3 dB", ha="right", va="bottom", size=12,
             transform=axx[0].get_xaxis_transform(), rotation=90 , color='C0')

axx[0].text( f_stop,  0, "f stop", ha="right", va="bottom", size=12,
             transform=axx[0].get_xaxis_transform(), rotation=90 , color='C1')


# fig.savefig('07_bode.png')

