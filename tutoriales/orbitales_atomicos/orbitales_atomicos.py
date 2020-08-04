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
        return f'/√{str(rta.denominator)})'
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
    

    
    def R(self,r):
        """
        Función radial del estado
        Ecuación 4.89 y 4.75 de Griffiths
        El factor de normalización no es exacto el de 4.89 de GRiffiths,
        fue modificado para adaptarse a cómo genera SciPy los Laguerre Generalizados.
        """
        n,l,m = self.n, self.l, self.m
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
        return Ψ(n=self.n,l=self.l,m=self.m,s=self.s,A=A,I=self.I,mi=self.mi)
    
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

#%%

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
            return sum( [  self.funcion(p) for p in psi.psi_vec  ] ,0  )
        else:
            raise ValueError('el argumento no es una función de onda: Ψ o WaveFunction -->'+ str(type(psi)))

    def __mul__(self,psi):
        if type(psi)==Ψ or type(psi)==WaveFunction:
            return self(psi)
        elif type(psi)==Operador:
            return Operador(nombre=self.nombre+'·'+psi.nombre, funcion=lambda x: self(psi(x)) )
        else:
            return ValueError('No es una funcion de onda ni un operador: '+ str(type(psi)))
        
    def __add__(self,psi):
        return Operador(nombre=self.nombre+' + '+psi.nombre, funcion=lambda x: self(x) + psi(x) )


psi = Ψ(3,2,1)  +   Ψ(3,2,-1)

L  = Operador( 'L', lambda x: x*x.l )
Lz = Operador('Lz', lambda x: x*x.m )
S  = Operador( 'S', lambda x: x*(1/2) )
Sz = Operador('Lz', lambda x: x*x.s )
N  = Operador( 'N', lambda x: x*x.n )
I  = Operador( 'I', lambda x: x*x.I )
Iz = Operador('Iz', lambda x: x*x.mi )

J  = L + S
J.nombre='J'







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



