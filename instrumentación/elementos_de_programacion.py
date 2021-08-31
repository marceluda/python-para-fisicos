#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estructuras de programación básicas y alguans referencias para 
empezar a programar pronto

Basado en:
https://marceluda.github.io/python-para-fisicos/tuto/labo2/01_intro_python/
"""


import time

from matplotlib import pyplot as plt
import numpy as np


print(__doc__)


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Definir datos e imprimirlos 

conteo = 24        # Valor entero 
tiempo = 8.2741e-3 # float : 8.2741 ms


print(f'Se leyeron {conteo} datos en {tiempo} segundos')


# Versiones con formateo de números
print(f'Se leyeron {conteo:04d} datos en {tiempo:7.4f} segundos')
print(f'Se leyeron {conteo: 4d} datos en {tiempo:3.1E} segundos')




#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Formas de convertir variables a texto

# Formato de Python 3.7 en adelante 
print(f'Se leyeron {conteo} datos en {tiempo:3.1E} segundos')

# Formato de Python 3.0 en adelante 
print('Se leyeron {0} datos en {1:3.1E} segundos'.format(conteo,tiempo) )

# Formato de Python 2 en adelante 
print('Se leyeron %d datos en %3.1E segundos' % (conteo,tiempo) )



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Ejemplo de iteración FOR y condifcional IF

# range(a,b) es un iterador que genera números enteros entre a y b-1
# range(b) genera b números enteros entre 0 y b-1

print('multiplos de 3')
for jj in range(1,30):
    if jj%3==0:
        print(jj)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Ejemplo de acumulación de datos en listas

# esto es una lista de dos números
lista = [1,4,5]

print(f'El primer elemento de la lista es {lista[0]}')
print(f'El tercer elemento de la lista es {lista[2]}')

# Durante 30 iteraciones vamos a agregar un elemento a la lista que 
# sea la suma de los dos anteriores:

for jj in range(2,32):
    lista.append(  lista[jj] + lista[jj-1]  )

print(lista)


# a las listas se las puede acceder de a partes
print('\n')
print(f'Primeros 5 elementos de la lista: {lista[:5]}')
print(f'Últimos  5 elementos de la lista: {lista[-5:]}')
print(f'Elementos del 4 al 9            : {lista[4:10]}')
print(f'Último valor de la lista        : {lista[-1]}')

# Las listas, si se las suman, se concatenan
lista2 = [-10,-20,-30]
print('\nConcatenación:\n')
print(lista2 + lista[:5])


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Generación de arrays / vectores

# De forma taxativa, desde una lista:
vec1 = np.array([1,2,3,4,5])
vec2 = np.array([-1,1,0,9,3])

# Los array se suman o restan elemento a elemento
print(vec1+vec2)
print(vec1-vec2)

# Lo mismo para la multiplicación o división
print(vec1*vec2)
print(vec2/vec1)

# O para potenciar
print(vec1**2)
print(10**vec1)



# Generar un vector de valores espaciados en "paso" que arrancan en 
# a, y terminan en el último valor menor a b

vec3 = np.arange(3,5,0.1)

# Generar vector lineal de 20 valores entre 3 y 15
vec4 = np.linspace(3,15,20)

# Generar vector logarítmico de 20 valores que va de 10^2=100 a 845834
vec5 = np.logspace(2,np.log10(845834),20)


# Se puede iterar dentro de los elementos de un vector o de una lista
print('\n')
print('Iteramos sobre los elementos de vec1')
for elemento in vec1:
    print(elemento)

# Obteniendo el índice:
print('\n')
print('Iteramos sobre los elementos de vec2 con enumerate')
for ii,elemento in enumerate(vec2):
    print(f'El elemento {ii} de vec2 es: {elemento}')


# Iterando de a pares de elementos
print('\n')
print('Iteramos sobre los elementos de vec1 y vec2 juntos')
print('| vec1 | vec2 |')
for elem1,elem2 in zip(vec1,vec2):
    print(f'| {elem1:3d}  | {elem2:3d}  |')



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Funciones con procedimientos programados

# Podemos definir funciones para juntar mucho código en un bloque simple


def calcular_elemento_fibonacci(N):
    
    a = 1
    b = 2
    
    if N==1:
        return a
    if N==2:
        return b
    else:
        tmp = 0
        for _ in range(N-2):
            tmp = a+b
            a   = b
            b   = tmp
        return tmp


print( calcular_elemento_fibonacci(8) )





