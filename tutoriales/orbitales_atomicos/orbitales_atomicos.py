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
from scipy.integrate import quad

import os

a = 0.52917720859  # radio de Bhor en Amnstrongs

from decimal import Decimal as D

from fractions import Fraction as fr

def adivinar_forma(x):
    
    opciones = [ (a,b, fr(abs(x)**a*pi**b).limit_denominator() ) for a in [-2,-1,1,2] for b in range(-2,3)  ]
    
    # Me quedo con la de menos denominador
    rta      = list(sorted(opciones , key=lambda x: (x[2].denominator,x[2].numerator)))[0]
    
    a,b,rta_frac   =  rta 
    signo = '-' if sign(x)==-1 else '+'
    frac  = str(rta_frac) if a>0 else str(1/rta_frac)
    pival = '' if b==0 else '*pi' if b>0 else '/pi'
    if abs(a)==2:
        if abs(b)==1:
            return f'{signo}sqrt({frac}{pival})'
        else:
            return f'{signo}sqrt({frac}){pival}'
    else:
        return f'{signo}{frac}{pival}' 
    






def CG(J,M,j1,j2,m1,m2):
    """
    Cálculo de los CLEBSCH-GORDAN  <j1,j2;m1,m2|j1,j2;J,M>
    Definidos según el algoritmo de: https://en.wikipedia.org/wiki/Table_of_Clebsch%E2%80%93Gordan_coefficients
    Chequeado con las tablas del Griffiths
    """
    if J>j1+j2 or J<abs(j1-j2):
        raise ValueError(f'J,j1,j2 deben cumplir:  |j1-j2|<=J<=j1+j2\nJ={J},j1={j1},j2={j2}')
    
    #if not ( J>0 and (j1>0 or j2>0)):
    #    return 0
        #raise ValueError('Los coeficientes deben J,j1,j2 deben ser mayores a cero')
    
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




def W3j(A):
    """
    Calucla los coeficientes de Wigner 3-j:
        ( j1 , j2 , j3 )
        ( m1 , m2 , m3 )
    Referencia: https://en.wikipedia.org/wiki/3-j_symbol
    """
    A = array(A)
    
    if not A.shape == (2,3):
        raise ValueError('El argumento debe tener un shape==(2,3)')
    j1,j2,j3 = A[0]
    m1,m2,m3 = A[1]
    
    # Prueba:   W3j([[1,2,3],[0,1,-1]])             debería ser    sqrt(2/105)*2
    #           W3j([[1,1/2,3/2],[1,-1/2,-1/2]])    deberia ser   -sqrt(1/3)/2
    #           W3j([[1,2,3],[-1,-2,3]])            deberia ser   sqrt(1/7)
    
    # Chequeado con http://www-stone.ch.cam.ac.uk/cgi-bin/wigner.cgi?symbol=3j&j1=1&j2=2&j3=3&m1=-1&m2=-2&m3=3
    for jj,mm in zip(A[0],A[1]):
        #   -j <= m <= j
        if not round(mm,2) in arange(-jj,jj+1).round(2):
            #print('no cumple mm E +-jj')
            return 0
    # m1+m2+m3 == 0
    if not round(sum(A[1]),2) == 0:
        #print('no cumple sum mm ==0')
        return 0
    
    # |j1-j2| <= j3 <= j1+j2
    if not ( abs(j1-j2)<= j3 and j3<= j1+j2  ):
        #print('no cumple jj E  j-j , jj')
        return 0
    
    # Chequeamos reglas de selección:
    return (-1)**int(round(j1-j2-m3)) *1/sqrt(2*j3+1) * CG(j3,-m3,j1,j2,m1,m2)



def _fmt_val(x,max_den=16):
    rta = fractions.Fraction(x**2).limit_denominator(max_den)
    if rta.numerator == 1:
        return f'/√{str(rta.denominator)})'
    else:
        return f'√({str(rta)})'


class Ψ():
    """
    Clase para generar autoestados del Hamiltoniano más elemental del átomo de Hidróngeno
    Ψ(n,l,m[,s,I,mi,A=1,lr=l])(r,phi,theta)
    
    n  : números principal
    l  : Momento angular orbital
    m  : proyección en z del momento angular orbital
    s  : poryección del spin del electrón. Puede ser: -0.5,0,0.5
         Un valor de s=0 implica que no se incluye el subespacio del spin en la función de onda.
    I  : Spin total del nucleo. Si es cero, se desestima el subespacio del spin nuclear
    mi : proyección del Spin del nucleo en z. Debe ser: -I <= mi <= I
    A  : Factor multiplicativo. Por defecto, A=1.
    lr : Para uso de los operadores. Es el l que usa Rnl, en caso que no coincida con el de Y_l^m
    """
    def __init__(self,n=1,l=0,m=0,s=0,I=0,mi=0,A=1,lr=False):
        
        valido = True
        
        if l>=n:
            print('Guarda: l>n no es un autoestado válido! ')
            valido = False
            #raise ValueError('l,n debe ser tal que: 0<=l<n')
        if abs(m)>l:
            raise ValueError('l,m debe ser tal que: |m|<=l')
        if abs(mi)>I:
            raise ValueError('I,mi debe ser tal que: |mi|<=I')
        if (not I==0) and s==0:
            raise ValueError('Sólo se permite definir el spin nuclear si se define el spin electrónico (s!=0)')
        if I>0:
            if not round(mi,2) in arange(-I,I+1):
                raise ValueError(f'mi={mi} no pertenece a los valores permitidos para I={I}')
        
        if type(s)==str and s in '↓↑':
            s = '↓↑'.index(s)-1/2    
                
        self.n  = n
        self.l  = l
        self.m  = m
        self.A  = A
        self.s  = s
        self.I  = I
        self.mi = mi
        
        self.lr = l if lr is False else lr
        self.valido = valido if self.lr==self.l else False

    def vec(self,no_indep=False):
        """
        Imprimir en forma de tuple los números que definen al estado: (n,l,m[,s,I,mi]). No incluye la amplitud A
        
        Si se especifica no_indep=True se agrega lr como número. Esto sólo tiene utilidad al trabajar con estados
        que no son autoestados válidos del Hamiltoniano del átomo de hidrógeno (como puede ser el resultado de aplicar 
        un operador estado váido).
        """
        
        rta = [self.n, self.l, self.m]
        if no_indep:
            rta += [self.lr]
        if not self.s==0:
            rta += [ self.s ]
        if not self.I==0:
            rta += [ self.I , self.mi ]
        
        return tuple(rta)
    
    def pprint(self,fmt='repr'):
        if fmt=='repr':
            return adivinar_forma( self.A).replace('pi','π').replace('sqrt','√') +'*' + repr(self.copy(A=1))
        else:
            return adivinar_forma( self.A) +'*' + str(self.copy(A=1))
    
    def __str__(self):
        if self.A==1:
            strA = ''
        else:
            strA = str(array([self.A]).round(2)[0]) + ' '
        
        primar = ''  if self.valido else '`'
        rta = f'{strA}Ψ{primar}(n={self.n},l={self.l},m={self.m}'
        if not self.s==0:
            rta += f',s={self.s}'
        if not self.I==0:
            rta += f',I={self.I},mi={self.mi}'
        
        rta += ')'
        return rta
    
    def __repr__(self):
        # ↑ ↓
        f = lambda x: str(fr(x).limit_denominator(2))
        if self.A==1:
            strA = ''
        else:
            strA = str(array([self.A]).round(2)[0]) + ' '
        
        primar = ''  if self.valido else '`'
        rta = f'{strA}Ψ{primar}({f(self.n)},{f(self.l)},{f(self.m)}'
        if not self.I==0:
            rta += f',{f(self.mi)}'
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
    

    
    def R(self,r):
        """
        Función radial del estado
        Ecuación 4.89 y 4.75 de Griffiths
        El factor de normalización no es exacto el de 4.89 de GRiffiths,
        fue modificado para adaptarse a cómo genera SciPy los Laguerre Generalizados.
        """
        n,l,m = self.n, self.lr, self.m
        #return exp(-r/n/a) * (2*r/n/a)**l  *  (genlaguerre(n-l-1,2*l+1) * math.factorial( n+l))( r/n/a )
        #return exp(-r/n/a) * (2*r/n/a)**l  *  genlaguerre(n-l-1,2*l+1)( r/n/a )
        return genlaguerre(n-l-1,2*l+1)(2*r/n/a)     * exp(-r/n/a) *       (2*r/n/a)**l * sqrt(math.factorial(n-l-1)/(math.factorial(n+l) * (2*n))*(2/n/a)**3 )  
    
    
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
        return Ψ(n=self.n,l=self.l,m=self.m,s=self.s,A=A,I=self.I,mi=self.mi,lr=self.lr)
    
    def __call__(self,r,phi,theta,A=0):
        if A==0:
            A=self.A
        rta = A * self.R(r) * self.Y(phi,theta)
        
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
        
        # self.psi_vec = psi_vec
        # Guarde mejor una verisón ordenada
        self.psi_vec = sorted(psi_vec, key=lambda x: (x.n,x.l,-x.m,x.I,-x.mi) )
        
        self._corregir_duplicados()
    def bases(self,no_indep=False):
        """
        Devuelte la lista de bases (n,l,m[,s,I,mi]) en que se escribe el estado de superposición
        """
        return [ p.vec(no_indep) for p in self.psi_vec ]
    
    
    def coef(self):
        """
        Devuelte los coeficientes de la base con que se escribe el estado de superposición
        """
        return array([ p.A for p in self.psi_vec ])
    
    def _corregir_duplicados(self):
        psi_vec = []
        for base in set(self.bases(True)):
            dd = dict( n=base[0], l=base[1], m=base[2], lr=base[3])
            if len(base)>4: # Si tenemos Spin electrónico
                dd['s']= base[4]
            if len(base)>5: # Si tenemos spin nuclear
                dd['I' ] = base[5]
                dd['mi'] = base[6]
            dd['A'] = sum([ p.A for p in self.psi_vec if p.vec(True)==base ]) 
            if abs(dd['A'])>0:
                psi_vec.append( Ψ( **dd )  ) 
        self.psi_vec = psi_vec
    
    def pprint(self,fmt='repr'):
        return ' '.join( [ p.pprint(fmt) for p in self.psi_vec ] )
    
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



class Operador():
    def __init__(self,nombre,funcion=False):
        self.nombre = nombre
        
        if callable(funcion):
            self.funcion = funcion
        else:
            raise ValueError('Se debe definir una función u objeto callable')
    def __repr__(self):
        return self.nombre
    
    def __call__(self,psi):
        if type(psi)==Ψ:
            return self.funcion(psi)
        elif type(psi)==WaveFunction:
            rta = sum( [  self.funcion(p) for p in psi.psi_vec  ] ,0  )
            return rta if type(rta)==WaveFunction else WaveFunction([rta])
        else:
            raise ValueError('el argumento no es una función de onda: Ψ o WaveFunction -->'+ str(type(psi)))

    def __mul__(self,psi):
        if type(psi)==Ψ or type(psi)==WaveFunction:
            return self(psi)
        elif type(psi)==Operador:
            return Operador(nombre=self.nombre+'·'+psi.nombre, funcion=lambda x: self(psi(x)) )
        elif isreal(psi) or iscomplex(psi):
            return Operador(nombre=str(psi)+'·'+self.nombre, funcion=lambda x: self(x)*psi )
        else:
            return ValueError('No es una funcion de onda ni un operador: '+ str(type(psi)))
    
    def __rmul__(self,factor):
        if isreal(factor) or iscomplex(factor):
            return self.__mul__(factor)
        else:
            raise ValueError('no es un número')
    
    def __add__(self,O):
        return Operador(nombre=self.nombre+' + '+O.nombre, funcion=lambda x: self(x) + O(x) )
    
    def __neg__(self):
        return Operador(nombre='-'+self.nombre, funcion=lambda x: (-1)*self(x)  )
    
    def __sub__(self,O):
        return Operador(nombre=self.nombre+' - '+O.nombre, funcion=lambda x: self(x) - O(x) )
        


L2 = Operador( 'L', lambda x: x*(x.l*(x.l+1)) )
Lz = Operador('Lz', lambda x: x*x.m )
S2 = Operador( 'S', lambda x: x*(1/2*(1/2+1)) )
Sz = Operador('Lz', lambda x: x*x.s )
#N  = Operador( 'N', lambda x: x*x.n )
I2  = Operador( 'I', lambda x: x*(x.I*(x.I+1)) )
Iz = Operador('Iz', lambda x: x*x.mi )

J2  = L2 + S2
J2.nombre='J'

Jz = Lz + Sz
Jz.nombre = 'Jz'


def contract_Ylm(l1,m1,l2,m2):
    """
    Regla de contracción de Ylm según:
        https://en.wikipedia.org/wiki/Spherical_harmonics#Contraction_rule
    
    devuelve una lista con los Ylm * coef excritos como:
        [(li,mi,coef)]
    """
    
    rta = []
    for c in arange(abs(l1-l2),l1+l2+1):
        for g in arange(-c,c+1):
            #print(c,g)
            coef = sqrt( (2*l1+1)*(2*l2+1)/4/pi ) * (-1)**abs(g) * sqrt(2*c+1) * W3j([[l1,l2,c],[m1,m2,-g]]) * W3j([[l1,l2,c],[0,0,0]])
            #print(CG(c,0,l1,0,l2,0))
            # version de https://sahussaintu.files.wordpress.com/2014/03/spherical_harmonics.pdf
            #coef = sqrt( (2*l1+1)*(2*l2+1)/(2*pi*(2*c+1) ) ) * CG(c,g,l1,l2,m1,m2) * CG(c,0,l1,l2,0,0)
            
            if abs(coef) > 1e-6: # esto es parche
                rta.append( (c,g,coef)  )
    
    return rta


# contract_Ylm(1,0,1,-1)


#%

def _Z(psi):
    """
    \hat{z} = - sqrt{4 \pi / 3} \cdot  Y_1^0
    """
    if type(psi)==Ψ:
        psi = WaveFunction([psi])
    
    if not type(psi)==WaveFunction:
        raise ValueError('La entrada no es una funcion de onda')
    
    rta = sum([  sqrt(4*pi/3)*WaveFunction([ Ψ(n=p.n,l=T[0], m=T[1], A=p.A*T[2], s=p.s, I=p.I, mi=p.mi , lr=p.lr) for T in contract_Ylm(1,0,p.l,p.m) ]  )     for p in psi.psi_vec  ] , 0)
    
    return rta

# _Z(Ψ(2,1,-1))


Z = Operador('Z',funcion=_Z)



def _X(psi):
    """
    \hat{x} = - sqrt{2 \pi / 3} \cdot ( Y_1^1 - Y_1^{-1} )
    """
    if type(psi)==Ψ:
        psi = WaveFunction([psi])
    
    if not type(psi)==WaveFunction:
        raise ValueError('La entrada no es una funcion de onda')
    
    # Hago la contracción con Y
    rta  = sum([ (-sqrt(2*pi/3))* WaveFunction([ Ψ(n=p.n,l=T[0], m=T[1], A=p.A*T[2], s=p.s, I=p.I, mi=p.mi , lr=p.lr) for T in contract_Ylm(1,1,p.l,p.m) ]  )     for p in psi.psi_vec  ] , 0)
    
    rta += sum([ ( sqrt(2*pi/3))* WaveFunction([ Ψ(n=p.n,l=T[0], m=T[1], A=p.A*T[2], s=p.s, I=p.I, mi=p.mi , lr=p.lr) for T in contract_Ylm(1,-1,p.l,p.m) ]  )     for p in psi.psi_vec  ] , 0)
    
    return rta

X = Operador('X',funcion=_X)


def _Y(psi):
    """
    \hat{x} = - sqrt{2 \pi / 3} \cdot ( Y_1^1 + Y_1^{-1} )/i
    """
    if type(psi)==Ψ:
        psi = WaveFunction([psi])
    
    if not type(psi)==WaveFunction:
        raise ValueError('La entrada no es una funcion de onda')
    
    # Hago la contracción con Y
    rta  = sum([ (1j*sqrt(2*pi/3))* WaveFunction([ Ψ(n=p.n,l=T[0], m=T[1], A=p.A*T[2], s=p.s, I=p.I, mi=p.mi , lr=p.lr) for T in contract_Ylm(1,1,p.l,p.m) ]  )     for p in psi.psi_vec  ] , 0)
    
    rta += sum([ (1j*sqrt(2*pi/3))* WaveFunction([ Ψ(n=p.n,l=T[0], m=T[1], A=p.A*T[2], s=p.s, I=p.I, mi=p.mi , lr=p.lr) for T in contract_Ylm(1,-1,p.l,p.m) ]  )     for p in psi.psi_vec  ] , 0)
    
    return rta

Y = Operador('Y',funcion=_Y)


# prod_int_Rnl = load('prod_int_Rnl.npz',allow_pickle=True)['prod_int_Rnl'].tolist()

try:
    from prod_int_Rnl import prod_int_Rnl
except:
    prod_int_Rnl = {}
    NT=10
    for n1 in range(1,NT):
        for l1 in arange(0,n1):
            tmp = []
            for n2 in range(1,NT):
                for l2 in arange(0,n2):
                    key = tuple(sorted( ((n1,l1),(n2,l2)) ))
                    if key in prod_int_Rnl.keys():
                        continue
                    if n1==n2 and l1==l2:
                        prod_int_Rnl[key] = 1
                    elif l1==l2:
                        prod_int_Rnl[key] = 0
                    else:
                        p_i = quad( lambda r: Ψ(n1,l1,0).R(r)*Ψ(n2,l2,0).R(r) * r**2 , 0, inf )
                        
                        prod_int_Rnl[key] = p_i[0] if abs(p_i[0])>1e-10 else 0
            print('.',end='')
    
    
    #with open('prod_int_Rnl.py', 'w') as aa:
    #    aa.write('#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n\nprod_int_Rnl = ')
    #    aa.write(str(prod_int_Rnl).replace(', ((',',\n(('))


def int_rnl(n1,l1,n2,l2):
    if n1==n2 and l1==l2:
        return 1
    elif l1==l2 and not n1==n2:
        return 0
    else:
        key = tuple(sorted( ((n1,l1),(n2,l2)) ))
        if key in prod_int_Rnl.keys():
            return prod_int_Rnl[key]
        else:
            return quad( lambda r: Ψ(n1,l1,0).R(r)*Ψ(n2,l2,0).R(r) * r**2 , 0, inf )[0]


from scipy.integrate import tplquad

def prod_interno(bra,ket,funcion=False,grilla=False):
    """
    Calcula producto interno de estados WaveFunction y Ψ
    
     - prod_interno(bra,ket)     calcula el producto interno <bra|ket> deforma algebraica (sin integrales)
    
     - prod_interno(bra,ket,O)   calcula <bra|O|ket>  si O es un Operador
    
     - prod_interno(bra,ket,fun) calcula el enbraketamiento de forma integral:
                                 ∫ bra*(r,theta,phi) · fun(r,theta,phi) · ket(r,theta,phi) · r^2 · sin(theta) ·dr dtheta dphi
    
    """
    
    if type(bra)==Ψ:
        bra = WaveFunction([bra])
    if type(ket)==Ψ:
        ket = WaveFunction([ket])
    
    if not ( type(bra)==WaveFunction  and type(ket)==WaveFunction):
        return ValueError('Tanto bra como ket deben ser funciones de onda WaveFunction o Ψ')
    
    if type(funcion)==Operador:
        ket     = funcion(ket)
        funcion = False
    
    
    
    # Producto interno algebráico ---------------------------------------------
    if not callable(funcion):
        # Usamos operacion algebráica
        bases = set(ket.bases() + bra.bases())
        
        #rta = [ conj(bra.coef()[bra.bases().index(b)])* ket.coef()[ket.bases().index(b)] 
        #        for b in bases if (b in ket.bases()) and (b in bra.bases())  ]
        
        rta = [ conj(b.A)*k.A *( 1 if b.lr==k.lr else int_rnl(b.n,b.lr,k.n,k.lr) )    
                for b in bra.psi_vec for k in ket.psi_vec if b.vec()[1:]==k.vec()[1:]  ]   
        
        return sum(rta)
    
    # Producto interno integral numérica --------------------------------------
    if grilla is False:
        # Si se definió una función...
        
        if bra(1,1,1).shape == ():
            S_real = tplquad( lambda r,phi,theta: real(   conj(bra(r,phi,theta))*ket(r,phi,theta) * funcion(r,phi,theta) )*r**2*sin(theta) , 0, pi, -pi, pi, 0,100 )[0]
            S_imag = tplquad( lambda r,phi,theta: imag(   conj(bra(r,phi,theta))*ket(r,phi,theta) * funcion(r,phi,theta) )*r**2*sin(theta) , 0, pi, -pi, pi, 0,100 )[0]
            
            return S_real + 1.j*S_imag
        else:
            rta = ones(bra(1,1,1).shape).astype(complex)
            print(f'Cálculo pesado de {rta.shape[0]*rta.shape[1]} pasos')
            nn = 0
            for jj in range(rta.shape[0]):
                for kk in range(rta.shape[1]):
                    print(nn,end=' ')
                    S_real = tplquad( lambda r,phi,theta: real(   conj(bra(r,phi,theta)[jj,kk])*ket(r,phi,theta)[jj,kk] * funcion(r,phi,theta) )*r**2*sin(theta) , 0, pi, -pi, pi, 0,100 )[0]
                    S_imag = tplquad( lambda r,phi,theta: imag(   conj(bra(r,phi,theta)[jj,kk])*ket(r,phi,theta)[jj,kk] * funcion(r,phi,theta) )*r**2*sin(theta) , 0, pi, -pi, pi, 0,100 )[0]
                    rta[jj,kk] *= S_real + 1.j*S_imag
                    
                    nn+=1
            
            return rta
    

#    ket =  (Ψ(3,2,1,1/2)*1        +   Ψ(3,2,-1,-1/2)*sqrt(3))/sqrt(4)
#    bra =  (Ψ(3,2,1,1/2)*sqrt(2)  +   Ψ(3,2,0,1/2)  *sqrt(3)  )/sqrt(5)
#    
#    base = (3, 2, 1, 0.5)
#    
#    
#    prod_interno(bra,ket)
#    
#    
#    prod_interno(Ψ(3,2,2),Ψ(3,2,2), L2)
#    
#    prod_interno(Ψ(3,2,2),Ψ(3,2,2), lambda r,theta,phi: 1 )




#    psi = Ψ(3,2,1,1/2)  +   Ψ(3,2,-1,-1/2)
#    
#    
#    psi = Ψ(3,2,1,1/2,3/2,1/2)  +   Ψ(3,2,-1,-1/2,3/2,-1/2)
#    
#    Z * Ψ(2,1,-1)
#    #  0.45 Ψ(2,2,-1)
#    
#    X * Ψ(2,1,-1)
#    # + 0.45 Ψ(2,2,-2) -0.18 Ψ(2,2,0)
#    
#    
#    Y * Ψ(2,1,-1)
#    
#    (X + 1j*Y)*psi





#%% Crear autoestados de Estructura fina 



# Los estados se escriben de la forma:
#
# Rb 5^{2} P_{3/2}
#    | |   |   |-----> J 
#    | |   |------> L = S(0), P(1), D(2), F(3)
#    | |------> 2S+2: Multiplicidad del Spin. Para Alkalis es simpre 2
#    |----> n: Nivel   n=1 .... inf



def autoestado_SO(estado,m=False,I=0,mi=0):
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

    return sum([ CG(J,M,L,1/2,ml,ms)* Ψ(n=n,l=L,m=ml,s=ms,I=I,mi=mi) for ml in arange(-L,L+1) for ms in arange(-S,S+1) if round(ml+ms,1)==round(M,2)])


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
    
    
    return  sum([  CG(F,mf,I,J,mi,mj)* autoestado_SO(estado,m=mj,I=I,mi=mi)  for mi in arange(-I,I+1) for mj in arange(-J,J+1) if round(mi+mj,2)==round(mf,2)])




# Ejemplo de uso:
# psi0 = autoestado_HF('5P1/2', F=1, I=3/2, mf=0)


#%%
# Funcion para hallar la máxima extensión en r de un estado

def coordenada_maxima(psi,umbral=0.01,maximo=True):
    """
    Función para hallar la máxima extensión en r de un estado, cortando en el umbral
    Si maximo==True se interpreta el borde donde Ψ.R()^2 * r^2 == Ψ.R().max()*umbral
    Sino, se intepreta umbral como el borde donde la integral cubre (1-umbral) del area de Ψ.R()^2 * r^2
    """
    
    # Buscamos el estado de mayor extensión en r
    if type(psi) == Ψ:
        Ψmax = psi
    else:
        Ψmax = [ pp for pp in sorted(psi.psi_vec, key=lambda x: x.n*100 + x.l ) ][-1]
    maxima_raiz = max(   (Ψmax.n+Ψmax.l + (Ψmax.n-Ψmax.l-2)* sqrt(Ψmax.n+Ψmax.l))*Ψmax.n*0.5/2   ,  1 )
    
    
    if maximo:
        # Obtenemos el valor en que se vuelve menos al [umbra]% del máximo
        x0          = linspace(0,maxima_raiz*10,10000)
        y0          = Ψmax.R(x0)**2 / (Ψmax.R(x0).max()**2)
        r_max_001   = x0[nonzero(y0>umbral)[0][-1]]
        
        return    r_max_001*1.1  # le damos un 10% extra
    else:
        x0          = linspace(0,maxima_raiz*10,10000)
        y0          = cumsum(Ψmax.R(x0)**2*x0**2)
        r_max_001   = x0[nonzero(y0>(1-umbral))[0][-1]]
        return r_max_001*1.1


#%%
if __name__ == "__main__":
    print('Algunos chequeos de consistencia -----------------------------'+ '\n'*3 )
    
    from scipy.integrate import tplquad,dblquad,quad
    from scipy.special import genlaguerre
    
           
    print('Normalización:')
    print('    *: producto interno de una grilla')
    print('    R: Integral int_0^inf Rnl(r) * r^2 dr')
    print('    Y: Integral del Ylm en todo el ángulo sólido')
    print('    S: Integral compuesta del estaoso completo ')
    
    print('\n'*2)
    
    for n in range(10):
        for l in arange(0,n):
            psi0 = Ψ(n,l,0)
            
            clim   = coordenada_maxima(psi0)*2
            N      = 100
            umbral = 0.1 
            
            X,Y,Z       = mgrid[-clim:clim:N*1j,-clim:clim:N*1j,-clim:clim:N*1j]
            r,phi,theta = sqrt( X**2 + Y**2 + Z**2 ) , arctan2(Y,X)  ,  arctan2( sqrt(X**2+Y**2) , Z  )
            xx, yy, zz  = X[:,0,0], Y[0,:,0], Z[0,0,:]        
            
            WF   = psi0(r,phi,theta)
            prob = (diff(xx)*diff(yy)*diff(zz)).mean() * sum(  conj(WF)*WF    )
            
            print(f'{repr(psi0)} | *: '    , round( abs(prob) , 4 ) )
            print(f'{repr(psi0)} | R: ', round(    quad( lambda r: (psi0.R(r))**2*r**2 ,0,100 )[0]                                                     , 4 ) )
            print(f'{repr(psi0)} | Y: ', round( dblquad( lambda phi,theta: abs(psi0.Y(phi,theta))**2*sin(theta) , 0, pi, -pi, pi )[0]                  , 4 ) )  
            print(f'{repr(psi0)} | S: ', round( tplquad( lambda r,phi,theta: abs(psi0(r,phi,theta))**2*r**2*sin(theta) , 0, pi, -pi, pi, 0,100 )[0]    , 4 ) )  
                
        print('\n'*2)


    print('Ortogonalidad:')
    print('Integral como en S de un estado y el conjugado de otro')
    
    print('\n'*2)
     
    for n1 in range(7):
        for l1 in range(0,n1):
            for n2 in range(n1,5):
                for l2 in range(0,n2):
                    if not ( n1==n2 and l1==l2):
                        psi1 = Ψ(n1,l1,0)
                        psi2 = Ψ(n2,l2,0)
                        WF   = conj(psi1(r,phi,theta))*psi2(r,phi,theta)
                        prob = (diff(xx)*diff(yy)*diff(zz)).mean() * sum(  WF    )
                        
                        S_real = tplquad( lambda r,phi,theta: real(   conj(psi1(r,phi,theta))*psi2(r,phi,theta)   )*r**2*sin(theta) , 0, pi, -pi, pi, 0,100 )[0]
                        S_imag = tplquad( lambda r,phi,theta: imag(   conj(psi1(r,phi,theta))*psi2(r,phi,theta)   )*r**2*sin(theta) , 0, pi, -pi, pi, 0,100 )[0]
                        print(f'<{repr(psi1)}|{repr(psi2)}> | *: '    , round( abs(prob) , 4 ) )
                        print(f'<{repr(psi1)}|{repr(psi2)}> | S: ', round(  S_real,4) + 1j*round(S_imag   , 4 ) )
                        print('-----------------------')
                
        print('\n')



    # Prueba de ortogonalidad de los Rnl(r) 
    print('Prueba de ortogonalidad de los Rnl(r) para distintos n\n')
    for n1 in range(1,20):
        for n2 in range(1,20):
            p_i = quad( lambda r: Ψ(n1,0,0).R(r)*Ψ(n2,0,0).R(r) * r**2 , 0, 1000 )
            print(f'{int(round(p_i[0])):2}',end=' ')
        print('')

    print('\n'*2)
    
    print('Prueba de ortogonalidad de los Rnl(r) para distintos n y l (redondeado)\n')
    rta          = []
    prod_int_Rnl = {}    
    NT=10
    refn = '  '.join([ str(n) for n in range(1,NT) for l in range(0,n) ]) 
    refl = '  '.join([ str(l) for n in range(1,NT) for l in range(0,n) ]) 
    
    print(' n|'+refn)
    print(' l|'+refl)
    
    print( 'nl|' + '-'*(len(ref)))
    
    for n1 in range(1,NT):
        for l1 in arange(0,n1):
            tmp = []
            print(f'{n1}{l1}|',end='')
            for n2 in range(1,NT):
                for l2 in arange(0,n2):
                    p_i = quad( lambda r: Ψ(n1,l1,0).R(r)*Ψ(n2,l2,0).R(r) * r**2 , 0, inf )
                    print(f'{int(sign(p_i[0])) if abs(round(p_i[0],5))>0 else 0:2}',end=' ')
                    tmp += [p_i[0]]
                    prod_int_Rnl[(n1,l1,n2,l2)] = p_i[0]
            print('')
            rta += [ tmp ]




#    Normalización:
#        *: producto interno de una grilla
#        R: Integral int_0^inf Rnl(r) * r^2 dr
#        Y: Integral del Ylm en todo el ángulo sólido
#        S: Integral compuesta del estaoso completo 
#    
#    
#    
#    
#    
#    Ψ(1,0,0) | *:  0.9993
#    Ψ(1,0,0) | R:  1.0
#    Ψ(1,0,0) | Y:  1.0
#    Ψ(1,0,0) | S:  1.0
#    
#    
#    
#    Ψ(2,0,0) | *:  0.9982
#    Ψ(2,0,0) | R:  1.0
#    Ψ(2,0,0) | Y:  1.0
#    Ψ(2,0,0) | S:  1.0
#    Ψ(2,1,0) | *:  1.0
#    Ψ(2,1,0) | R:  1.0
#    Ψ(2,1,0) | Y:  1.0
#    Ψ(2,1,0) | S:  1.0
#    
#    
#    
#    Ψ(3,0,0) | *:  0.4362
#    Ψ(3,0,0) | R:  1.0
#    Ψ(3,0,0) | Y:  1.0
#    Ψ(3,0,0) | S:  1.0
#    Ψ(3,1,0) | *:  1.0
#    Ψ(3,1,0) | R:  1.0
#    Ψ(3,1,0) | Y:  1.0
#    Ψ(3,1,0) | S:  1.0
#    Ψ(3,2,0) | *:  1.0
#    Ψ(3,2,0) | R:  1.0
#    Ψ(3,2,0) | Y:  1.0
#    Ψ(3,2,0) | S:  1.0
#    
#    
#    
#    Ψ(4,0,0) | *:  0.1343
#    Ψ(4,0,0) | R:  1.0
#    Ψ(4,0,0) | Y:  1.0
#    Ψ(4,0,0) | S:  1.0
#    Ψ(4,1,0) | *:  1.0001
#    Ψ(4,1,0) | R:  1.0
#    Ψ(4,1,0) | Y:  1.0
#    Ψ(4,1,0) | S:  1.0
#    Ψ(4,2,0) | *:  1.0
#    Ψ(4,2,0) | R:  1.0
#    Ψ(4,2,0) | Y:  1.0
#    Ψ(4,2,0) | S:  1.0
#    Ψ(4,3,0) | *:  1.0
#    Ψ(4,3,0) | R:  1.0
#    Ψ(4,3,0) | Y:  1.0
#    Ψ(4,3,0) | S:  1.0
#    
#    
#    
#    Ψ(5,0,0) | *:  0.0613
#    Ψ(5,0,0) | R:  1.0
#    Ψ(5,0,0) | Y:  1.0
#    Ψ(5,0,0) | S:  1.0
#    Ψ(5,1,0) | *:  1.0003
#    Ψ(5,1,0) | R:  1.0
#    Ψ(5,1,0) | Y:  1.0
#    Ψ(5,1,0) | S:  1.0
#    Ψ(5,2,0) | *:  0.9998
#    Ψ(5,2,0) | R:  1.0
#    Ψ(5,2,0) | Y:  1.0
#    Ψ(5,2,0) | S:  1.0
#    Ψ(5,3,0) | *:  1.0
#    Ψ(5,3,0) | R:  1.0
#    Ψ(5,3,0) | Y:  1.0
#    Ψ(5,3,0) | S:  1.0
#    Ψ(5,4,0) | *:  1.0
#    Ψ(5,4,0) | R:  1.0
#    Ψ(5,4,0) | Y:  1.0
#    Ψ(5,4,0) | S:  1.0
#    
#    
#    
#    Ψ(6,0,0) | *:  0.0336
#    Ψ(6,0,0) | R:  1.0
#    Ψ(6,0,0) | Y:  1.0
#    Ψ(6,0,0) | S:  1.0
#    Ψ(6,1,0) | *:  1.0006
#    Ψ(6,1,0) | R:  1.0
#    Ψ(6,1,0) | Y:  1.0
#    Ψ(6,1,0) | S:  1.0
#    Ψ(6,2,0) | *:  0.999
#    Ψ(6,2,0) | R:  1.0
#    Ψ(6,2,0) | Y:  1.0
#    Ψ(6,2,0) | S:  1.0
#    Ψ(6,3,0) | *:  1.0
#    Ψ(6,3,0) | R:  1.0
#    Ψ(6,3,0) | Y:  1.0
#    Ψ(6,3,0) | S:  1.0
#    Ψ(6,4,0) | *:  1.0
#    Ψ(6,4,0) | R:  1.0
#    Ψ(6,4,0) | Y:  1.0
#    Ψ(6,4,0) | S:  1.0
#    Ψ(6,5,0) | *:  1.0
#    Ψ(6,5,0) | R:  1.0
#    Ψ(6,5,0) | Y:  1.0
#    Ψ(6,5,0) | S:  1.0
#    
#    
#    
#    Ψ(7,0,0) | *:  0.0205
#    Ψ(7,0,0) | R:  1.0
#    Ψ(7,0,0) | Y:  1.0
#    Ψ(7,0,0) | S:  1.0
#    Ψ(7,1,0) | *:  0.7151
#    Ψ(7,1,0) | R:  1.0
#    Ψ(7,1,0) | Y:  1.0
#    Ψ(7,1,0) | S:  1.0
#    Ψ(7,2,0) | *:  0.9963
#    Ψ(7,2,0) | R:  1.0
#    Ψ(7,2,0) | Y:  1.0
#    Ψ(7,2,0) | S:  1.0
#    Ψ(7,3,0) | *:  1.0003
#    Ψ(7,3,0) | R:  1.0
#    Ψ(7,3,0) | Y:  1.0
#    Ψ(7,3,0) | S:  1.0
#    Ψ(7,4,0) | *:  0.9999
#    Ψ(7,4,0) | R:  1.0
#    Ψ(7,4,0) | Y:  1.0
#    Ψ(7,4,0) | S:  1.0
#    Ψ(7,5,0) | *:  1.0
#    Ψ(7,5,0) | R:  1.0
#    Ψ(7,5,0) | Y:  1.0
#    Ψ(7,5,0) | S:  1.0
#    Ψ(7,6,0) | *:  1.0
#    Ψ(7,6,0) | R:  1.0
#    Ψ(7,6,0) | Y:  1.0
#    Ψ(7,6,0) | S:  1.0
#    
#    
#    
#    Ψ(8,0,0) | *:  0.0133
#    Ψ(8,0,0) | R:  0.9999
#    Ψ(8,0,0) | Y:  1.0
#    Ψ(8,0,0) | S:  0.9999
#    Ψ(8,1,0) | *:  0.3312
#    Ψ(8,1,0) | R:  1.0
#    Ψ(8,1,0) | Y:  1.0
#    Ψ(8,1,0) | S:  1.0
#    Ψ(8,2,0) | *:  0.9917
#    Ψ(8,2,0) | R:  1.0
#    Ψ(8,2,0) | Y:  1.0
#    Ψ(8,2,0) | S:  1.0
#    Ψ(8,3,0) | *:  1.0011
#    Ψ(8,3,0) | R:  1.0
#    Ψ(8,3,0) | Y:  1.0
#    Ψ(8,3,0) | S:  1.0
#    Ψ(8,4,0) | *:  0.9994
#    Ψ(8,4,0) | R:  1.0
#    Ψ(8,4,0) | Y:  1.0
#    Ψ(8,4,0) | S:  1.0
#    Ψ(8,5,0) | *:  1.0
#    Ψ(8,5,0) | R:  1.0
#    Ψ(8,5,0) | Y:  1.0
#    Ψ(8,5,0) | S:  1.0
#    Ψ(8,6,0) | *:  1.0
#    Ψ(8,6,0) | R:  1.0
#    Ψ(8,6,0) | Y:  1.0
#    Ψ(8,6,0) | S:  1.0
#    Ψ(8,7,0) | *:  1.0
#    Ψ(8,7,0) | R:  1.0
#    Ψ(8,7,0) | Y:  1.0
#    Ψ(8,7,0) | S:  1.0
#    
#    
#    
#    Ψ(9,0,0) | *:  0.0092
#    Ψ(9,0,0) | R:  0.9906
#    Ψ(9,0,0) | Y:  1.0
#    Ψ(9,0,0) | S:  0.9906
#    Ψ(9,1,0) | *:  0.2051
#    Ψ(9,1,0) | R:  0.9916
#    Ψ(9,1,0) | Y:  1.0
#    Ψ(9,1,0) | S:  0.9916
#    Ψ(9,2,0) | *:  0.9892
#    Ψ(9,2,0) | R:  0.9932
#    Ψ(9,2,0) | Y:  1.0
#    Ψ(9,2,0) | S:  0.9932
#    Ψ(9,3,0) | *:  1.0023
#    Ψ(9,3,0) | R:  0.9951
#    Ψ(9,3,0) | Y:  1.0
#    Ψ(9,3,0) | S:  0.9951
#    Ψ(9,4,0) | *:  0.9966
#    Ψ(9,4,0) | R:  0.997
#    Ψ(9,4,0) | Y:  1.0
#    Ψ(9,4,0) | S:  0.997
#    Ψ(9,5,0) | *:  1.0002
#    Ψ(9,5,0) | R:  0.9985
#    Ψ(9,5,0) | Y:  1.0
#    Ψ(9,5,0) | S:  0.9985
#    Ψ(9,6,0) | *:  1.0
#    Ψ(9,6,0) | R:  0.9994
#    Ψ(9,6,0) | Y:  1.0
#    Ψ(9,6,0) | S:  0.9994
#    Ψ(9,7,0) | *:  1.0
#    Ψ(9,7,0) | R:  0.9998
#    Ψ(9,7,0) | Y:  1.0
#    Ψ(9,7,0) | S:  0.9998
#    Ψ(9,8,0) | *:  1.0
#    Ψ(9,8,0) | R:  1.0
#    Ψ(9,8,0) | Y:  1.0
#    Ψ(9,8,0) | S:  1.0
#    
#    
#    
#    Ortogonalidad:
#    Integral como en S de un estado y el conjugado de otro
#    
#    
#    
#    
#    
#    <Ψ(1,0,0)|Ψ(2,0,0)> | *:  0.1105
#    <Ψ(1,0,0)|Ψ(2,0,0)> | S:  0j
#    -----------------------
#    <Ψ(1,0,0)|Ψ(2,1,0)> | *:  0.0
#    <Ψ(1,0,0)|Ψ(2,1,0)> | S:  0j
#    -----------------------
#    <Ψ(1,0,0)|Ψ(3,0,0)> | *:  0.0368
#    <Ψ(1,0,0)|Ψ(3,0,0)> | S:  0j
#    -----------------------
#    <Ψ(1,0,0)|Ψ(3,1,0)> | *:  0.0
#    <Ψ(1,0,0)|Ψ(3,1,0)> | S:  0j
#    -----------------------
#    <Ψ(1,0,0)|Ψ(3,2,0)> | *:  0.0
#    <Ψ(1,0,0)|Ψ(3,2,0)> | S:  0j
#    -----------------------
#    <Ψ(1,0,0)|Ψ(4,0,0)> | *:  0.0189
#    <Ψ(1,0,0)|Ψ(4,0,0)> | S:  0j
#    -----------------------
#    <Ψ(1,0,0)|Ψ(4,1,0)> | *:  0.0
#    <Ψ(1,0,0)|Ψ(4,1,0)> | S:  0j
#    -----------------------
#    <Ψ(1,0,0)|Ψ(4,2,0)> | *:  0.0
#    <Ψ(1,0,0)|Ψ(4,2,0)> | S:  0j
#    -----------------------
#    <Ψ(1,0,0)|Ψ(4,3,0)> | *:  0.0
#    <Ψ(1,0,0)|Ψ(4,3,0)> | S:  0j
#    -----------------------
#    
#    
#    <Ψ(2,0,0)|Ψ(2,1,0)> | *:  0.0
#    <Ψ(2,0,0)|Ψ(2,1,0)> | S:  0j
#    -----------------------
#    <Ψ(2,0,0)|Ψ(3,0,0)> | *:  0.0819
#    <Ψ(2,0,0)|Ψ(3,0,0)> | S:  0j
#    -----------------------
#    <Ψ(2,0,0)|Ψ(3,1,0)> | *:  0.0
#    <Ψ(2,0,0)|Ψ(3,1,0)> | S:  0j
#    -----------------------
#    <Ψ(2,0,0)|Ψ(3,2,0)> | *:  0.0
#    <Ψ(2,0,0)|Ψ(3,2,0)> | S:  0j
#    -----------------------
#    <Ψ(2,0,0)|Ψ(4,0,0)> | *:  0.0506
#    <Ψ(2,0,0)|Ψ(4,0,0)> | S:  0j
#    -----------------------
#    <Ψ(2,0,0)|Ψ(4,1,0)> | *:  0.0
#    <Ψ(2,0,0)|Ψ(4,1,0)> | S:  0j
#    -----------------------
#    <Ψ(2,0,0)|Ψ(4,2,0)> | *:  0.0
#    <Ψ(2,0,0)|Ψ(4,2,0)> | S:  0j
#    -----------------------
#    <Ψ(2,0,0)|Ψ(4,3,0)> | *:  0.0
#    <Ψ(2,0,0)|Ψ(4,3,0)> | S:  0j
#    -----------------------
#    <Ψ(2,1,0)|Ψ(2,0,0)> | *:  0.0
#    <Ψ(2,1,0)|Ψ(2,0,0)> | S:  0j
#    -----------------------
#    <Ψ(2,1,0)|Ψ(3,0,0)> | *:  0.0
#    <Ψ(2,1,0)|Ψ(3,0,0)> | S:  0j
#    -----------------------
#    <Ψ(2,1,0)|Ψ(3,1,0)> | *:  0.0864
#    <Ψ(2,1,0)|Ψ(3,1,0)> | S:  0j
#    -----------------------
#    <Ψ(2,1,0)|Ψ(3,2,0)> | *:  0.0
#    <Ψ(2,1,0)|Ψ(3,2,0)> | S:  0j
#    -----------------------
#    <Ψ(2,1,0)|Ψ(4,0,0)> | *:  0.0
#    <Ψ(2,1,0)|Ψ(4,0,0)> | S:  0j
#    -----------------------
#    <Ψ(2,1,0)|Ψ(4,1,0)> | *:  0.0671
#    <Ψ(2,1,0)|Ψ(4,1,0)> | S:  0j
#    -----------------------
#    <Ψ(2,1,0)|Ψ(4,2,0)> | *:  0.0
#    <Ψ(2,1,0)|Ψ(4,2,0)> | S:  0j
#    -----------------------
#    <Ψ(2,1,0)|Ψ(4,3,0)> | *:  0.084
#    <Ψ(2,1,0)|Ψ(4,3,0)> | S:  0j
#    -----------------------
#    
#    
#    <Ψ(3,0,0)|Ψ(3,1,0)> | *:  0.0
#    <Ψ(3,0,0)|Ψ(3,1,0)> | S:  0j
#    -----------------------
#    <Ψ(3,0,0)|Ψ(3,2,0)> | *:  0.0
#    <Ψ(3,0,0)|Ψ(3,2,0)> | S:  0j
#    -----------------------
#    <Ψ(3,0,0)|Ψ(4,0,0)> | *:  0.0156
#    <Ψ(3,0,0)|Ψ(4,0,0)> | S:  0j
#    -----------------------
#    <Ψ(3,0,0)|Ψ(4,1,0)> | *:  0.0
#    <Ψ(3,0,0)|Ψ(4,1,0)> | S:  0j
#    -----------------------
#    <Ψ(3,0,0)|Ψ(4,2,0)> | *:  0.0
#    <Ψ(3,0,0)|Ψ(4,2,0)> | S:  0j
#    -----------------------
#    <Ψ(3,0,0)|Ψ(4,3,0)> | *:  0.0
#    <Ψ(3,0,0)|Ψ(4,3,0)> | S:  0j
#    -----------------------
#    <Ψ(3,1,0)|Ψ(3,0,0)> | *:  0.0
#    <Ψ(3,1,0)|Ψ(3,0,0)> | S:  0j
#    -----------------------
#    <Ψ(3,1,0)|Ψ(3,2,0)> | *:  0.0
#    <Ψ(3,1,0)|Ψ(3,2,0)> | S:  0j
#    -----------------------
#    <Ψ(3,1,0)|Ψ(4,0,0)> | *:  0.0
#    <Ψ(3,1,0)|Ψ(4,0,0)> | S:  0j
#    -----------------------
#    <Ψ(3,1,0)|Ψ(4,1,0)> | *:  0.0621
#    <Ψ(3,1,0)|Ψ(4,1,0)> | S:  0j
#    -----------------------
#    <Ψ(3,1,0)|Ψ(4,2,0)> | *:  0.0
#    <Ψ(3,1,0)|Ψ(4,2,0)> | S:  0j
#    -----------------------
#    <Ψ(3,1,0)|Ψ(4,3,0)> | *:  0.0408
#    <Ψ(3,1,0)|Ψ(4,3,0)> | S:  0j
#    -----------------------
#    <Ψ(3,2,0)|Ψ(3,0,0)> | *:  0.0
#    <Ψ(3,2,0)|Ψ(3,0,0)> | S:  0j
#    -----------------------
#    <Ψ(3,2,0)|Ψ(3,1,0)> | *:  0.0
#    <Ψ(3,2,0)|Ψ(3,1,0)> | S:  0j
#    -----------------------
#    <Ψ(3,2,0)|Ψ(4,0,0)> | *:  0.0
#    <Ψ(3,2,0)|Ψ(4,0,0)> | S:  0j
#    -----------------------
#    <Ψ(3,2,0)|Ψ(4,1,0)> | *:  0.0
#    <Ψ(3,2,0)|Ψ(4,1,0)> | S:  0j
#    -----------------------
#    <Ψ(3,2,0)|Ψ(4,2,0)> | *:  0.151
#    <Ψ(3,2,0)|Ψ(4,2,0)> | S:  0j
#    -----------------------
#    <Ψ(3,2,0)|Ψ(4,3,0)> | *:  0.0
#    <Ψ(3,2,0)|Ψ(4,3,0)> | S:  0j
#    -----------------------
#    
#    
#    <Ψ(4,0,0)|Ψ(4,1,0)> | *:  0.0
#    <Ψ(4,0,0)|Ψ(4,1,0)> | S:  0j
#    -----------------------
#    <Ψ(4,0,0)|Ψ(4,2,0)> | *:  0.0
#    <Ψ(4,0,0)|Ψ(4,2,0)> | S:  0j
#    -----------------------
#    <Ψ(4,0,0)|Ψ(4,3,0)> | *:  0.0
#    <Ψ(4,0,0)|Ψ(4,3,0)> | S:  0j
#    -----------------------
#    <Ψ(4,1,0)|Ψ(4,0,0)> | *:  0.0
#    <Ψ(4,1,0)|Ψ(4,0,0)> | S:  0j
#    -----------------------
#    <Ψ(4,1,0)|Ψ(4,2,0)> | *:  0.0
#    <Ψ(4,1,0)|Ψ(4,2,0)> | S:  0j
#    -----------------------
#    <Ψ(4,1,0)|Ψ(4,3,0)> | *:  0.0237
#    <Ψ(4,1,0)|Ψ(4,3,0)> | S:  0j
#    -----------------------
#    <Ψ(4,2,0)|Ψ(4,0,0)> | *:  0.0
#    <Ψ(4,2,0)|Ψ(4,0,0)> | S:  0j
#    -----------------------
#    <Ψ(4,2,0)|Ψ(4,1,0)> | *:  0.0
#    <Ψ(4,2,0)|Ψ(4,1,0)> | S:  0j
#    -----------------------
#    <Ψ(4,2,0)|Ψ(4,3,0)> | *:  0.0
#    <Ψ(4,2,0)|Ψ(4,3,0)> | S:  0j
#    -----------------------
#    <Ψ(4,3,0)|Ψ(4,0,0)> | *:  0.0
#    <Ψ(4,3,0)|Ψ(4,0,0)> | S:  0j
#    -----------------------
#    <Ψ(4,3,0)|Ψ(4,1,0)> | *:  0.0237
#    <Ψ(4,3,0)|Ψ(4,1,0)> | S:  0j
#    -----------------------
#    <Ψ(4,3,0)|Ψ(4,2,0)> | *:  0.0
#    <Ψ(4,3,0)|Ψ(4,2,0)> | S:  0j
#    -----------------------
#
#
#    Prueba de ortogonalidad de los Rnl(r) para distintos n
#    
#     1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 
#     0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 
#     0  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 
#     0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 
#     0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0 
#     0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0 
#     0  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0 
#     0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0 
#     0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0 
#     0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0 
#     0  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0 
#     0  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0 
#     0  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0 
#     0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0 
#     0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0 
#     0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0 
#     0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0 
#     0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0 
#     0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1 
#    
#    Prueba de ortogonalidad de los Rnl(r) para distintos n y l (redondeado)
#    
#     n|1  2  2  3  3  3  4  4  4  4  5  5  5  5  5  6  6  6  6  6  6  7  7  7  7  7  7  7  8  8  8  8  8  8  8  8  9  9  9  9  9  9  9  9  9
#     l|0  0  1  0  1  2  0  1  2  3  0  1  2  3  4  0  1  2  3  4  5  0  1  2  3  4  5  6  0  1  2  3  4  5  6  7  0  1  2  3  4  5  6  7  8
#    nl|-------------------------------------------------------------------------------------------------------------------------------------
#    10| 1  0  1  0  1  1  0  1  1  1  0  1  1  1  1  0  1  1  1  1  1  0  1  1  1  1  1  1  0  1  1  1  1  1  1  0  0  1  1  1  1  1  1  0  0 
#    20| 0  1 -1  0  1 -1  0  1 -1 -1  0  1 -1 -1 -1  0  1 -1 -1 -1 -1  0  1 -1 -1 -1 -1 -1  0  1 -1 -1 -1 -1 -1 -1  0  1 -1 -1 -1 -1 -1 -1 -1 
#    21| 1 -1  1 -1  0  1 -1  0  1  1 -1  0  1  1  1 -1  0  1  1  1  1 -1  0  1  1  1  1  1 -1  0  1  1  1  1  1  1 -1  0  1  1  1  1  1  1  1 
#    30| 0  0 -1  1 -1  1  0  1 -1  1  0  1 -1  1  1  0  1 -1  1  1  1  0  1 -1  1  1  1  1  0  1 -1  1  1  1  1  1  0  1 -1  1  1  1  1  1  1 
#    31| 1  1  0 -1  1 -1 -1  0  1 -1 -1  0  1 -1 -1 -1  0  1 -1 -1 -1 -1  0  1 -1 -1 -1 -1 -1  0  1 -1 -1 -1 -1 -1 -1  0  1 -1 -1 -1 -1 -1 -1 
#    32| 1 -1  1  1 -1  1  1 -1  0  1  1 -1  0  1  1  1 -1  0  1  1  1  1 -1  0  1  1  1  1  1 -1  0  1  1  1  1  1  1 -1  0  1  1  1  1  1  1 
#    40| 0  0 -1  0 -1  1  1 -1  1 -1  0  1 -1  1 -1  0  1 -1  1 -1 -1  0  1 -1  1  1 -1 -1  0  1 -1  1  1 -1 -1 -1  0  1 -1  1  1 -1 -1 -1 -1 
#    41| 1  1  0  1  0 -1 -1  1 -1  1 -1  0  1 -1  1 -1  0  1 -1  1  1 -1  0  1 -1 -1  1  1 -1  0  1 -1 -1  1  1  1 -1  0  1 -1 -1  1  1  1  1 
#    42| 1 -1  1 -1  1  0  1 -1  1 -1  1 -1  0  1 -1  1 -1  0  1 -1 -1  1 -1  0  1 -1 -1 -1  1 -1  0  1 -1 -1 -1 -1  1 -1  0  1 -1 -1 -1 -1 -1 
#    43| 1 -1  1  1 -1  1 -1  1 -1  1 -1  1 -1  0  1 -1  1 -1  0  1  1 -1  1 -1  0  1  1  1 -1  1 -1  0  1  1  1  1 -1  1 -1  0  1  1  1  1  1 
#    50| 0  0 -1  0 -1  1  0 -1  1 -1  1 -1  1 -1  1  0  1 -1  1 -1  1  0  1 -1  1 -1 -1  1  0  1 -1  1 -1 -1  1  1  0  1 -1  1 -1 -1  1  1  1 
#    51| 1  1  0  1  0 -1  1  0 -1  1 -1  1 -1  1 -1 -1  0  1 -1  1 -1 -1  0  1 -1  1  1 -1 -1  0  1 -1  1  1 -1 -1 -1  0  1 -1  1  1 -1 -1 -1 
#    52| 1 -1  1 -1  1  0 -1  1  0 -1  1 -1  1 -1  1  1 -1  0  1 -1  1  1 -1  0  1 -1 -1  1  1 -1  0  1 -1 -1  1  1  1 -1  0  1 -1 -1  1  1  1 
#    53| 1 -1  1  1 -1  1  1 -1  1  0 -1  1 -1  1 -1 -1  1 -1  0  1 -1 -1  1 -1  0  1 -1 -1 -1  1 -1  0  1  1 -1 -1 -1  1 -1  0  1  1 -1 -1 -1 
#    54| 1 -1  1  1 -1  1 -1  1 -1  1  1 -1  1 -1  1  1 -1  1 -1  0  1  1 -1  1 -1  0  1  1  1 -1  1 -1  0  1  1  1  1 -1  1 -1  0  1  1  1  1 
#    60| 0  0 -1  0 -1  1  0 -1  1 -1  0 -1  1 -1  1  1 -1  1 -1  1 -1  0  1 -1  1 -1  1 -1  0  1 -1  1 -1  1  1 -1  0  1 -1  1 -1 -1  1 -1 -1 
#    61| 1  1  0  1  0 -1  1  0 -1  1  1  0 -1  1 -1 -1  1 -1  1 -1  1 -1  0  1 -1  1 -1  1 -1  0  1 -1  1 -1 -1  1 -1  0  1 -1  1  1 -1  1  1 
#    62| 1 -1  1 -1  1  0 -1  1  0 -1 -1  1  0 -1  1  1 -1  1 -1  1 -1  1 -1  0  1 -1  1 -1  1 -1  0  1 -1  1  1 -1  1 -1  0  1 -1  1  1 -1 -1 
#    63| 1 -1  1  1 -1  1  1 -1  1  0  1 -1  1  0 -1 -1  1 -1  1 -1  1 -1  1 -1  0  1 -1  1 -1  1 -1  0  1 -1 -1  1 -1  1 -1  0  1 -1 -1  1  1 
#    64| 1 -1  1  1 -1  1 -1  1 -1  1 -1  1 -1  1  0  1 -1  1 -1  1 -1  1 -1  1 -1  0  1 -1  1 -1  1 -1  0  1 -1 -1  1 -1  1 -1  0  1  1 -1 -1 
#    65| 1 -1  1  1 -1  1 -1  1 -1  1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  0  1 -1  1 -1  1 -1  0  1  1 -1  1 -1  1 -1  0  1  1  1 
#    70| 0  0 -1  0 -1  1  0 -1  1 -1  0 -1  1 -1  1  0 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1  0  1 -1  1 -1  1 -1  1  0  1 -1  1 -1  1  1 -1  1 
#    71| 1  1  0  1  0 -1  1  0 -1  1  1  0 -1  1 -1  1  0 -1  1 -1  1 -1  1 -1  1 -1  1 -1 -1  0  1 -1  1 -1  1 -1 -1  0  1 -1  1 -1 -1  1 -1 
#    72| 1 -1  1 -1  1  0 -1  1  0 -1 -1  1  0 -1  1 -1  1  0 -1  1 -1  1 -1  1 -1  1 -1  1  1 -1  0  1 -1  1 -1  1  1 -1  0  1 -1  1  1 -1  1 
#    73| 1 -1  1  1 -1  1  1 -1  1  0  1 -1  1  0 -1  1 -1  1  0 -1  1 -1  1 -1  1 -1  1 -1 -1  1 -1  0  1 -1  1 -1 -1  1 -1  0  1 -1  1  1 -1 
#    74| 1 -1  1  1 -1  1  1 -1 -1  1 -1  1 -1  1  0 -1  1 -1  1  0 -1  1 -1  1 -1  1 -1  1  1 -1  1 -1  0  1 -1  1  1 -1  1 -1  0  1 -1 -1  1 
#    75| 1 -1  1  1 -1  1 -1  1 -1  1 -1  1 -1 -1  1  1 -1  1 -1  1  0 -1  1 -1  1 -1  1 -1 -1  1 -1  1 -1  0  1 -1 -1  1 -1  1 -1  0  1  1 -1 
#    76| 1 -1  1  1 -1  1 -1  1 -1  1  1 -1  1 -1  1 -1  1 -1  1 -1  1  1 -1  1 -1  1 -1  1  1 -1  1 -1  1 -1  0  1  1 -1  1 -1  1 -1  0  1  1 
#    80| 0  0 -1  0 -1  1  0 -1  1 -1  0 -1  1 -1  1  0 -1  1 -1  1 -1  0 -1  1 -1  1 -1  1  1 -1  1 -1  1 -1  1 -1  0  1 -1  1 -1  1 -1  1 -1 
#    81| 1  1  0  1  0 -1  1  0 -1  1  1  0 -1  1 -1  1  0 -1  1 -1  1  1  0 -1  1 -1  1 -1 -1  1 -1  1 -1  1 -1  1 -1  0  1 -1  1 -1  1 -1  1 
#    82| 1 -1  1 -1  1  0 -1  1  0 -1 -1  1  0 -1  1 -1  1  0 -1  1 -1 -1  1  0 -1  1 -1  1  1 -1  1 -1  1 -1  1 -1  1 -1  0  1 -1  1 -1  1 -1 
#    83| 1 -1  1  1 -1  1  1 -1  1  0  1 -1  1  0 -1  1 -1  1  0 -1  1  1 -1  1  0 -1  1 -1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  0  1 -1  1 -1  1 
#    84| 1 -1  1  1 -1  1  1 -1 -1  1 -1  1 -1  1  0 -1  1 -1  1  0 -1 -1  1 -1  1  0 -1  1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  0  1 -1  1 -1 
#    85| 1 -1  1  1 -1  1 -1  1 -1  1 -1  1 -1  1  1  1 -1  1 -1  1  0  1 -1  1 -1  1  0 -1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  0  1 -1  1 
#    86| 1 -1  1  1 -1  1 -1  1 -1  1  1 -1  1 -1  1  1 -1  1 -1 -1  1 -1  1 -1  1 -1  1  0  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  0  1 -1 
#    87| 0 -1  1  1 -1  1 -1  1 -1  1  1 -1  1 -1  1 -1  1 -1  1 -1  1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  0  1 
#    90| 0  0 -1  0 -1  1  0 -1  1 -1  0 -1  1 -1  1  0 -1  1 -1  1 -1  0 -1  1 -1  1 -1  1  0 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1 
#    91| 1  1  0  1  0 -1  1  0 -1  1  1  0 -1  1 -1  1  0 -1  1 -1  1  1  0 -1  1 -1  1 -1  1  0 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1 
#    92| 1 -1  1 -1  1  0 -1  1  0 -1 -1  1  0 -1  1 -1  1  0 -1  1 -1 -1  1  0 -1  1 -1  1 -1  1  0 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1 
#    93| 1 -1  1  1 -1  1  1 -1  1  0  1 -1  1  0 -1  1 -1  1  0 -1  1  1 -1  1  0 -1  1 -1  1 -1  1  0 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1 
#    94| 1 -1  1  1 -1  1  1 -1 -1  1 -1  1 -1  1  0 -1  1 -1  1  0 -1 -1  1 -1  1  0 -1  1 -1  1 -1  1  0 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1 
#    95| 1 -1  1  1 -1  1 -1  1 -1  1 -1  1 -1  1  1 -1  1  1 -1  1  0  1 -1  1 -1  1  0 -1  1 -1  1 -1  1  0 -1  1 -1  1 -1  1 -1  1 -1  1 -1 
#    96| 1 -1  1  1 -1  1 -1  1 -1  1  1 -1  1 -1  1  1 -1  1 -1  1  1  1 -1  1  1 -1  1  0 -1  1 -1  1 -1  1  0 -1  1 -1  1 -1  1 -1  1 -1  1 
#    97| 0 -1  1  1 -1  1 -1  1 -1  1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1  1  1 -1  1 -1  1 -1  1  0 -1  1 -1  1 -1  1 -1  1 -1 
#    98| 0 -1  1  1 -1  1 -1  1 -1  1  1 -1  1 -1  1 -1  1 -1  1 -1  1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1  1 -1  1 -1  1 -1  1 -1  1 
#    


