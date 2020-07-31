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
    
    if not ( J>0 and (j1>0 or j2>0)):
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



def _fmt_val(x,max_den=16):
    rta = fractions.Fraction(x**2).limit_denominator(max_den)
    if rta.numerator == 1:
        return f'/√{str(rta.denominator})'
    else:
        return f'√({str(rta)})'


class Ψ():
    """
    Clase para generar autoestados del Hamiltoniano más elemental del átomo de Hidróngeno
    Ψ(n,l,m[,s,I,A])(r,phi,theta)
    
    n  : números principal
    l  : Momento angular orbital
    m  : proyección en z del momento angular orbital
    s  : poryección del spin del electrón. Puede ser: -0.5,0,0.5
         Un valor de s=0 implica que no se incluye el subespacio del spin en la función de onda.
    I  : Spin total del nucleo. Si es cero, se desestima el subespacio del spin nuclear
    mi : proyección del Spin del nucleo en z. Debe ser: -I <= mi <= I
    """
    def __init__(self,n=1,l=0,m=0,s=0,I=0,A=1,mi=0):
        
        if l>=n:
            raise ValueError('l,n debe ser tal que: 0<=l<n')
        if abs(m)>l:
            raise ValueError('l,m debe ser tal que: |m|<=l')
        if abs(mi)>I:
            raise ValueError('I,mi debe ser tal que: |mi|<=I')
        if (not I==0) and s==0:
            raise ValueError('Sólo se permite definir el spin nuclear si se define el spin electrónico (s!=0)')
        if I>0:
            if not round(mi,2) in arange(-I,I+1):
                raise ValueError(f'mi={mi} no pertenece a los valores permitidos para I={I}')
        
        
        self.n  = n
        self.l  = l
        self.m  = m
        self.A  = A
        self.s  = s
        self.I  = I
        self.mi = mi

    def vec(self):
        """
        Imprimir en forma de tuple los números que definen al estado: (n,l,m[,s,I,mi]). No incluye la amplitud A
        """
        rta = [self.n, self.l, self.m]
        if not self.s==0:
            rta += [ self.s ]
        if not self.I==0:
            rta += [ self.I , self.mi ]
        return tuple(rta)
    
    def __str__(self):
        if self.A==1:
            strA = ''
        else:
            strA = str(array([self.A]).round(2)[0]) + ' '
        
        rta = f'{strA}Ψ(n={self.n},l={self.l},m={self.m}'
        if not self.s==0:
            rta += f',s={self.s}'
        if not self.I==0:
            rta += f',I={self.I},mi={self.mi}'
        
        rta += ')'
        return rta
    
    def __repr__(self):
        # ↑ ↓
        if self.A==1:
            strA = ''
        else:
            strA = str(array([self.A]).round(2)[0]) + ' '
        rta = f'{strA}Ψ({self.n},{self.l},{self.m}'
        if not self.I==0:
            rta += f',{self.mi}'
        rta += ')'
        if not self.s==0:
            rta += ('↑' if self.s>0 else '↓' )
        return rta

    def __mul__(self,otro):
        # Que pasas si multiplico:  Ψ * otro
        if not ( isreal(otro) or iscomplex(otro) ):
            raise ValueError('usar numeros')
        return self.copy(A=self.A*otro)
    
    def __truediv__(self,otro):
        return self.__mul__(1/otro)
    
    def __rmul__(self,otro):
        return self.__mul__(otro)
    
    def __add__(self,otro):
        
        if type(otro) ==  Ψ:
            if abs(otro.s)==abs(self.s) and otro.I==self.I:
                return WaveFunction([self,otro])
            else:
                raise ValueError('No se pueden superponer estados con diferentes subespacios de spin electrónico o nuclear')
        elif type(otro) == WaveFunction:
            aa = otro.psi_vec.copy()
            aa.append(self)
            return WaveFunction( aa )
        else:
            raise ValueError('No es una funcion de onda Ψ')
    
    def __neg__(self):
        return self.copy(A=-self.A)
    
    def __sub__(self,otro):
        return self.__add__(- otro)
    
    def Norma(self):
        """
        Función de normalización del del estado (n,m,l)
        Ecuación 4.89 de GRiffiths
        """
        n,l,m = self.n, self.l, self.m
        return sqrt(  (2/n/a)**3 * math.factorial(n-l-1) / ( 2*n* math.factorial(n+l)**3  )   )
    
    def R(self,r):
        """
        Función radial del estado
        Ecuación 4.89 y 4.75 de Griffiths
        """
        n,l,m = self.n, self.l, self.m
        return exp(-r/n/a) * (2*r/n/a)**l  *  (genlaguerre(n-l-1,2*l+1) * math.factorial( n+l))( r/n/a )
    
    
    def Y(self,phi,theta):
        """
        Esférico armónico del estado
        Tomado de la ecuación 4.32 de Griffiths
        Equivalentes a los mencionados en Wikipedia con Condon–Shortley phase:
            https://en.wikipedia.org/wiki/Spherical_harmonics#Condon%E2%80%93Shortley_phase
        """            
        n,l,m = self.n, self.l, self.m
        return ((-1)**m if m>=0 else 1) * sph_harm( m, l, phi, theta )
    
    def copy(self,A=False):
        if A is False:
            A = self.A
        return Ψ(n=self.n,l=self.l,m=self.m,s=self.s,A=A,I=self.I,mi=self.mi)
    
    def __call__(self,r,phi,theta,A=0):
        if A==0:
            A=self.A
        rta = A * self.Norma() * self.R(r) * self.Y(phi,theta)
        
        if abs(self.s)>0:
            rta = [rta,rta*0] if self.s>0 else [rta*0,rta]
        if self.I>0:
            valores_mi = arange(self.I, -self.I-1, -1).round(2)
            rta = [ rta if round(self.mi,2)==mi else (array(rta)*0).tolist() for mi in valores_mi ]
        return array(rta)


class WaveFunction():
    """
    Suma de distintos autoestados
    Es útil para devolver la suma/resta de autoestados como estados de superposición
    """
    
    def __init__(self,psi_vec):
        
        # chequeamos que todos tengan la misma dimencionalidad
        if len(set( [ len(p.vec()) for p in psi_vec ] ))>1:
            raise ValueError('Las funciones de onda que se busca superponer tienen una dimensionalidad distinta.')
        if len(set( [ p.I for p in psi_vec ]  ))>1:
            raise ValueError('Las funciones de onda tienen distintos valores de spin nuclear I')
        
        self.psi_vec = psi_vec
        self._corregir_duplicados()
    def bases(self):
        """
        Devuelte la lista de bases (n,l,m[,s,I,mi]) en que se escribe el estado de superposición
        """
        return [ p.vec() for p in self.psi_vec ]
    
    def _corregir_duplicados(self):
        psi_vec = []
        for base in set(self.bases()):
            dd = dict( n=base[0], l=base[1], m=base[2])
            if len(base)>3: # Si tenemos Spin electrónico
                dd['s']= base[3]
            if len(base)>4: # Si tenemos spin nuclear
                dd['I' ] = base[4]
                dd['mi'] = base[5]
            dd['A'] = sum([ p.A for p in self.psi_vec if p.vec()==base ]) 
            psi_vec.append( Ψ( **dd )  ) 
        self.psi_vec = psi_vec
    
    def __repr__(self):
        return 'WaveFunction: ' + ' '.join([ repr(p) if p.A<0 else '+ '+repr(p) for p in self.psi_vec ])
    
    def __str__(self):
        return ' '.join([ str(p) if p.A<0 else '+ '+str(p) for p in self.psi_vec ])

    def __mul__(self,otro):
        if not ( isreal(otro) or iscomplex(otro) ):
            raise ValueError('usar numeros')
        
        return WaveFunction( [ otro*p for p in self.psi_vec ] )
    
    def __rmul__(self,otro):
        return self.__mul__(otro)
    
    def __truediv__(self,otro):
        return self.__mul__(1/otro)

    def __add__(self,otro):
        if type(otro) ==  Ψ:
            return WaveFunction([ *self.psi_vec , otro ])
        elif type(otro) == WaveFunction:
            return WaveFunction( [ p.copy() for p in self.psi_vec ] + [ p.copy() for p in otro.psi_vec ] )
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
        rta = sum(  [  p(r,phi,theta) for p in self.psi_vec  ]  ,0)
        return rta/N if normalizar else rta




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
    
    #estado = '5P1/2'
    
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




#%% Autoestados para Hiperfina:

# Tomamos ideas de: doi=10.1.1.704.8856  
#    Atomic physics: structure, interactions, and entanglement
#    M. Saffman


# Autoestados de la forma: 
# |IJFM>  =  Sum_mi,mj CG(F,mf,I,mi,J,mj) |I,mi>|J,mj>
# Con F = J + I         |J-I| <= F <= |J+I| 

def autoestado_HF(estado,F=1,I=3/2,mf=False):

    #    estado = '5P1/2'
    #    m = False
    #    F = 1  # 2
    #    I = 3/2
    
    n = int(estado[0])
    L = 's p d f g h i j k'.split().index( estado[1].lower() )
    J = eval(estado[2:])
    S = 1/2
    posibles_MF = arange(-F,F+1)
    
    if not mf in posibles_MF:
        if mf is False:
            mf = posibles_MF[-1]
        else:
            raise ValueError(f'mf no es un valor válido para F={F}')
    
    
    return  sum([  CG(F,mf,I,J,mi,mj)* autoestado_SO(estado,m=mj)  for mi in arange(-I,I+1) for mj in arange(-J,J+1) if round(mi+mj,2)==round(mf,2)])


# Ejemplo de uso:
# psi0 = autoestado_HF('5P1/2', F=1, I=3/2, mf=0)


#%%
# Funcion para hallar la máxima extensión en r de un estado
def coordenada_maxima(psi,umbral=0.01):
    """
    Función para hallar la máxima extensión en r de un estado, cortando al 1% del máximo.
    """
    
    # Buscamos el estado de mayor extensión en r
    if type(psi) == Ψ:
        Ψmax = psi
    else:
        Ψmax = [ pp for pp in sorted(psi.psi_vec, key=lambda x: x.n*100 + x.l ) ][-1]
    maxima_raiz = max(   (Ψmax.n+Ψmax.l + (Ψmax.n-Ψmax.l-2)* sqrt(Ψmax.n+Ψmax.l))*Ψmax.n*0.5/2   ,  1 )
    
    # Obtenemos el valor en que se vuelve menos al [umbra]% del máximo
    x0          = linspace(0,maxima_raiz*10,10000)
    y0          = Ψmax.R(x0)**2 / (Ψmax.R(x0).max()**2)
    r_max_001   = x0[nonzero(y0>umbral)[0][-1]]
    
    return    r_max_001*1.1  # le damos un 10% extra








