#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Librería para el cálculo de orbitales atómicos
Siguiendo el capítulo 4 de:
Griffiths, D. J. (2005). Introduction to quantum mechanics. Upper Saddle River, NJ: Pearson Prentice Hall.
"""
from numpy import *
#import matplotlib.pyplot as plt


from scipy.special import sph_harm
from scipy.special import genlaguerre


a = 0.52917720859  # radio de Bhor en Amnstrongs


class Ψ():
    """
    Clase para generar autoestados del Hamiltoniano más elemental del átomo de Hidróngeno
    Ψ(n,l,m)(r,phi,theta)
    """
    def __init__(self,n=1,l=0,m=0,A=1):
        
        if l>=n:
            raise ValueError('l,n debe ser tal que: 0<=l<n')
        if abs(m)>l:
            raise ValueError('l,m debe ser tal que: |m|<=l')
        
        self.n = n
        self.l = l
        self.m = m
        self.A = A

    def vec(self):
        """
        Imprimir en forma de tuple los números que definen al estado: (n,l,m)
        """
        return (self.n, self.l, self.m)
    
    def __repr__(self):
        if self.A==1:
            strA = ''
        else:
            strA = str(self.A) + ' '
        return f'{strA}Ψ(n={self.n},l={self.l},m={self.m})'

    def __mul__(self,otro):
        if not ( isreal(otro) or iscomplex(otro) ):
            raise ValueError('usar numeros')
        return Ψ(n=self.n,l=self.l,m=self.m,A=self.A*otro)
    
    def __truediv__(self,otro):
        return self.__mul__(1/otro)
    
    def __rmul__(self,otro):
        return self.__mul__(otro)
    
    def __add__(self,otro):
        if type(otro) ==  Ψ:
            return WaveFunction([self,otro])
        elif type(otro) == WaveFunction:
            aa = otro.psi_vec.copy()
            aa.append(self)
            return WaveFunction( aa )
        else:
            raise ValueError('No es una funcion de onda Ψ')
    
    def __neg__(self):
        return Ψ(n=self.n,l=self.l,m=self.m,A=-self.A)
    
    def __sub__(self,otro):
        return self.__add__(- otro)
    
    def Norma(self):
        """
        Función de normalización del del estado (n,m,l)
        Ecuación 4.89 de GRiffiths
        """
        #print(f'norma: n={n}, l={l}')
        n,l,m = self.n, self.l, self.m
        return sqrt(  (2/n/a)**3 * math.factorial(n-l-1) / ( 2*n* math.factorial(n+l)**3  )   )
    
    def R(self,r):
        """
        Función radial del estado
        Ecuación 4.89 y 4.75 de Griffiths
        """
        #print(f'R_nl: n={n}, l={l}')
        n,l,m = self.n, self.l, self.m
        return exp(-r/n/a) * (2*r/n/a)**l  *  (genlaguerre(n-l-1,2*l+1) * math.factorial( n+l))( r/n/a )
    
    
    def Y(self,phi,theta):
        """
        Esférico armónico del estado
        Tomado de la ecuación 4.32 de Griffiths
        Equivalentes a los mencionados en Wikipedia con Condon–Shortley phase:
            https://en.wikipedia.org/wiki/Spherical_harmonics#Condon%E2%80%93Shortley_phase
        """
            
        #print(f'Y_lm: m={m}, l={l}')
        n,l,m = self.n, self.l, self.m
        return ((-1)**m if m>=0 else 1) * sph_harm( m, l, phi, theta )
    
    def __call__(self,r,phi,theta,A=0):
        if A==0:
            A=self.A
        return A * self.Norma() * self.R(r) * self.Y(phi,theta)


class WaveFunction():
    """
    Suma de distintos autoestados
    Es útil para devolver la suma/resta de autoestados como estados de superposición
    """
    
    def __init__(self,psi_vec):
        self.psi_vec = psi_vec
        self._corregir_duplicados()
    def bases(self):
        """
        Devuelte la lista de bases (n,l,m) en que se escrive el estado de superposición
        """
        return [ (p.n,p.l,p.m) for p in self.psi_vec ]
    
    def _corregir_duplicados(self):
        psi_vec = []
        for base in set(self.bases()):
            psi_vec.append( Ψ( *base , sum([ p.A for p in self.psi_vec if p.vec()==base ]) )  )
        self.psi_vec = psi_vec
    
    def __repr__(self):
        return 'WaveFunction: ' + ' '.join([ repr(p) if p.A<0 else '+ '+repr(p) for p in self.psi_vec ])

    def __mul__(self,otro):
        if not ( isreal(otro) or iscomplex(otro) ):
            raise ValueError('usar numeros')
        
        return WaveFunction( [ otro*p for p in self.psi_vec ] )

    def __truediv__(self,otro):
        return self.__mul__(1/otro)

    def __add__(self,otro):
        if type(otro) ==  Ψ:
            return WaveFunction([ *self.psi_vec ,otro ])
        elif type(otro) == WaveFunction:
            aa = otro.psi_vec.copy()
            aa += self.psi_vec.copy()
            return WaveFunction( aa )
        else:
            raise ValueError('No es una funcion de onda Ψ')

    def __neg__(self):
        return WaveFunction( [ -p for p in self.psi_vec ] )

    def __sub__(self,otro):
        return self.__add__( - otro )

    def __call__(self,r,phi,theta,normalizar=False):
        N = linalg.norm( [  p.A for p in self.psi_vec  ] ) if normalizar else 1
        return sum(  [  p(r,phi,theta) for p in self.psi_vec  ]  ,0) / N

