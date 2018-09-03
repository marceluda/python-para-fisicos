# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 11:56:41 2018

@author: lolo
"""

from numpy import *
import matplotlib.pyplot as plt

from xplot import xplot

#%%




def fft_plot(y1,*argv,t_step=1,ax=None,amp_units='amp',phase_units='grad',**kwargs):
    if ax==None:
        ax = xplot(2)
        ax.add()
    elif not type(ax)==xplot:
        print('pasame un xplot')
        return False
    
    N      = len(y1)
    ii     = arange(N)
    Norma  = sinc(ii/N) * exp(-1j*ii*pi/N)  * 2/N
    Y1     = fft.rfft( y1 )[0:N//2] * Norma[0:N//2]
    ff     = fft.fftfreq( N , d=t_step  )[0:N//2]
    
    if   amp_units.lower()[0:3]=='db':
        ax[0].plot( ff , 20 * log10(abs(Y1))          , *argv, **kwargs )
        ax[0].set_ylabel('Amplitud [dB]')
    elif amp_units.lower()[0:4]=='pow':
        ax[0].plot( ff , (abs(Y1))**2          , *argv, **kwargs )
        ax[0].semilogy()
        ax[0].set_ylabel('Power Amplitud')
    else:
        ax[0].plot( ff , abs(Y1)          , *argv, **kwargs )
        ax[0].semilogy()
        ax[0].set_ylabel('Amplitud')
    
    if phase_units.lower()[0:5]=='grad':
        ax[1].plot( ff , angle(Y1)*180/pi , *argv, **kwargs )
        ax[1].set_yticks([-180, -135, -90, -45, 0, 45, 90, 135, 180])
        ax[1].set_ylabel('fase [grad]')
    elif phase_units.lower()[0:4]=='rad':
        ax[1].plot( ff , angle(Y1) , *argv, **kwargs )
        ax[1].set_yticks([-pi, -pi*3/4, -pi/2, -pi/4, 0, pi/4, pi/2, pi*3/4, pi])
        ax[1].set_yticklabels('-π,-π3/4,-π/2,-π/4,0,π/4,π/2,π3/4,π'.split(','))
        ax[1].set_ylabel('fase [rad]')
    
    ax[0].semilogx()
    ax.set_xlabel('Frecuencia [Hz]')
    ax.all.grid(b=True,linestyle='--',color='lightgray')
    ax.tight_layout()
    return(ax)


#%%

if __name__ == '__main__':
    
    tt = linspace(0,100,100000)  # En segundos
    random.seed(1024)
    ts = (max(tt)-min(tt))/(len(tt)-1)
    
    y1 = sin(tt*2*pi)*20
    y2 = y1 + random.randn( len(tt) )
    
    
    ax = fft_plot(y1, '.-',t_step=ts)
    ax = fft_plot(y2,      t_step=ts,ax=ax, alpha=0.7)
    
    
    ax[0].set_ylim(1e-6,100)
    ax.tight_layout()
    

    
    
    
    