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

from decimal import Decimal as D


def CG(J,M,j1,j2,m1,m2):
    """
    Cálculo de los CLEBSCH-GORDAN  <j1,j2;m1,m2|j1,j2;J,M>
    Definidos según el algoritmo de: https://en.wikipedia.org/wiki/Table_of_Clebsch%E2%80%93Gordan_coefficients
    Chequeado con las tablas del Griffiths
    """
    if J>j1+j2 or J<abs(j1-j2):
        raise ValueError('J,j1,j2 deben cumplir:  |j1-j2|<=J<=j1+j2')
    
    if not ( J>0 and j1>0 and j2>0):
        raise ValueError('Los coeficientes deben J,j1,j2 deben ser mayores a cero')
    
    if not M==m1+m2:
        return 0
    
    if not all( [ int(2*x) == round(2*x,2) for x in (J,M,j1,j2,m1,m2)] ):
        raise ValueError('Los parámetros deben ser enteros o semienteros')
    
    factorial = lambda x: math.factorial(int(x)) if int(x)==round(x,2) else False

    factores = lambda k: [k,j1+j2-J-k,j1-m1-k,j2+m2-k,J-j2+m1+k,J-j1-m2+k]
    
    p1 = (2*J+1) * factorial(J+j1-j2)*factorial(J+j2-j1)*factorial(-J+j1+j2)/factorial(J+j1+j2+1)
    
    p2 = factorial(J+M)*factorial(J-M)*factorial(j1+m1)*factorial(j1-m1)*factorial(j2+m2)*factorial(j2-m2)
    
    p3 = sum([ (-1)**k / product([ factorial(y) for y in factores(k) ]) for k in range(int(-J-j1-j2),int(J+j1+j2+1)) if all([ y>=0 for y in factores(k) ]) ])

    return sqrt(p1*p2)*p3




class Ψ():
    """
    Clase para generar autoestados del Hamiltoniano más elemental del átomo de Hidróngeno
    Ψ(n,l,m)(r,phi,theta)
    """
    def __init__(self,n=1,l=0,m=0,A=1,s=0.5):
        
        if l>=n:
            raise ValueError('l,n debe ser tal que: 0<=l<n')
        if abs(m)>l:
            raise ValueError('l,m debe ser tal que: |m|<=l')
        
        self.n = n
        self.l = l
        self.m = m
        self.A = A
        self.s = 0.5

    def vec(self):
        """
        Imprimir en forma de tuple los números que definen al estado: (n,l,m)
        """
        return (self.n, self.l, self.m, self.s)
    
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
    
    def copy(self,A=False):
        if A is False:
            A = self.A
            
        return Ψ(n=self.n,l=self.l,m=self.m,s=self.s,A=A)
    
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
        return [ (p.n,p.l,p.m,p.s) for p in self.psi_vec ]
    
    def _corregir_duplicados(self):
        psi_vec = []
        for base in set(self.bases()):
            psi_vec.append( Ψ( n=base[0], l=base[1], m=base[2] , s=base[3], A=sum([ p.A for p in self.psi_vec if p.vec()==base ]) )  )
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
    
    def copy(self):
        return WaveFunction( [ p.copy() for p in self.psi_vec ] )
    def __call__(self,r,phi,theta,normalizar=False):
        N = linalg.norm( [  p.A for p in self.psi_vec  ] ) if normalizar else 1
        return sum(  [  p(r,phi,theta) for p in self.psi_vec  ]  ,0) / N




#%% Crear autoestados de Estructura fina 



# Los estados se escriben de la forma:
#
# Rb 5^{2} P_{3/2}
#    | |   |   |-----> J 
#    | |   |------> L = S(0), P(1), D(2), F(3)
#    | |------> 2S+2: Multiplicidad del Spin. Para Alkalis es simpre 2
#    |----> n: Nivel   n=1 .... inf



def autoestado_SO(estado,m=False):
    """
    Defino estado en notación espectral
    Si m no está definido, tomo el m más alto posible.
    """
    
    #estado = '5P3/2'
    
    n = int(estado[0])
    L = 's p d f g h i j k'.split().index( estado[1].lower() )
    J = eval(estado[2:])
    S = 1/2
    
    posibles_M = arange(-J,J+1)

    if m in posibles_M:
        M=m
    else:
        if m is False:
            M = posibles_M[-1]
        else:
            raise ValueError(f'm no es un valor válido para J={J}')

    return sum([ CG(J,M,L,1/2,ml,ms)* Ψ(n=n,l=L,m=ml,s=ms) for ml in arange(-L,L+1) for ms in arange(-S,S+1) if round(ml+ms,1)==round(M,2)])


# Ejemplo de uso:
# psi0 = autoestado_SO('5P3/2', m=1/2)



















