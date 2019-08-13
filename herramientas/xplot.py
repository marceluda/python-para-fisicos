# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 11:56:41 2018

@author: lolo
"""

from numpy import *
import matplotlib.pyplot as plt


#%%


def smooth(x, window_len=11, window='hanning'):
    s=r_[2*x[0]-array(x[window_len:1:-1]), x, 2*x[-1]-array(x[-1:-window_len:-1])]
    w = ones(window_len,'d')
    y = convolve(w/w.sum(), s, mode='same')
    return y[window_len-1:-window_len+1]

class xplot():
    """Clase para realizar gráficos rápidos con múltiples filas que comparten el eje X.

    Referencia:
        xplot(N=1, figsize=(10,6), nox=False)

    N       :   Cantidad de filas
    figsize :   Parámetro figsize para la creación del fig
    nox     :   Si es True, cada fila tiene un eje x independiente

    Métodos y propiedades:
        add()          :   Agrega un nuevo subfig
        fig            :   Acceso a la figura creada
        ax             :   Lista de todos los subplot axis creados
        all            :   Meta clase para ejecutar métodos en todos los axis de self.ax
        tight_layout() :   Ejecuta plt.tight_layout() en la figura self.fig

    Ejemplo:

        xx = linspace(0,4,1000)
        yy = sin(xx)

        ax = xplot(3)  # Creacion de un plot de tres filas

        ax.plot(xx, yy)
        ax.set_ylabel('Seno')

        ax.add()
        ax.plot(xx, -yy, '.-', alpha=0.7 , color='C2')

        ax.add()
        ax.plot(xx/2, yy**2)

        ax[1].plot(xx,-yy**2/max(yy))

        ax.all.grid(b=True,linestyle='--',color='lightgray')

    """
    def __init__(self,N=1,figsize=(10,6),nox=False):
        self.fig            = plt.figure(figsize=figsize)
        self.ax             = [ plt.subplot2grid((N,1), (0, 0) )]
        self.N              = N
        self.i              = 0
        self.title          = ''
        self.xlabel         = ''
        self.set_ax(self.i)
        self.all            = self.all_class( dir(self.ax[0]) )
        self.tight_layout   = self.fig.tight_layout
        self.nox            = nox

        for name in self.all.names:
            pppp = self.A(name,self.ax)
            setattr(self.all,name , pppp )

    class all_class:
        def __init__(self,names):
            self.names  = []
            for name in names:
                if name[0]=='_':
                    continue
                self.names.append(name)

    class A:
        def __init__(self,name,axx):
            self.name = name
            self.axx   = axx
        def __call__(self,*argv,**kwargs):
            print("call " + self.name)
            rta=[]
            for ax in self.axx:
                rta.append( getattr(ax,self.name)(*argv,**kwargs)  )
            return rta

    def __repr__(self):
        return 'xplot(N={:d},i={:d})'.format(self.N,self.i)

    def __getitem__(self, key):
        if type(key)==int:
            return self.ax[key]

    def add(self):
        if len(self.ax) >= self.N :
            raise ValueError('Número de axis supera el máximo')
        self.i  += 1
        if self.nox:
            self.ax.append( plt.subplot2grid((self.N,1), (self.i, 0)   )  )
        else:
            self.ax.append( plt.subplot2grid((self.N,1), (self.i, 0) , sharex=self.ax[0]  )  )
        self.set_ax(self.i)

    #def plot(self,*argv,**kwargs):
    #    return self.ax[-1].plot(*argv,**kwargs)

    def set_ax(self,n):
        for name in dir(self.ax[n]):
            if name[0]=='_':
                continue
            setattr(self,name, getattr(self.ax[n], name ) )

if __name__ == '__main__':
    xx = linspace(0,4,1000)
    yy = sin(xx)

    ax = xplot(3)  # Creacion de un plot de tres filas

    ax.plot(xx, yy)
    ax.set_ylabel('Seno')

    ax.add()
    ax.plot(xx, -yy, '.-', alpha=0.7 , color='C2')
    ax.set_ylabel('menos Seno')

    ax.add()
    ax.plot(xx/2, yy**2)

    ax[1].plot(xx,-yy**2/max(yy))

    ax.all.grid(b=True,linestyle='--',color='lightgray')


