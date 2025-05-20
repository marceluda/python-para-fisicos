#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TITULO: Varianza de Allan con allantools
# RESUMEN: Cálculo de la varianza de Allan unsado las herramientas de allantools

"""
Para usar los ejemplos del paquete hay que instalar `allantools`. 

En linux y con Anaconda Python, correr esto desde la consola:
    
```bash
/home/$USER/anaconda3/bin/pip install allantools
``` 

"""

#%%  Varianza de Allan
"""
Cálculo de la varianza de allan más usual

Para FASE es:
    
$$ \sigma^2_{ADEV}(\tau) = { 1 \over 2 \tau^2 }
        \langle ( {x}_{n+2} - 2x_{n+1} + x_{n} )^2 \rangle
        = { 1 \over 2 (N-2) \tau^2 }
        \sum_{n=1}^{N-2} ( {x}_{n+2} - 2x_{n+1} + x_{n} )^2 $$

Para FRECUENCIA es:
    
 $$      \sigma^{2}_{ADEV}(\tau) =  { 1 \over 2 }
        \langle ( \bar{y}_{n+1} - \bar{y}_n )^2 \rangle $$

  - [Fuente de las fórmulas](https://www.nist.gov/publications/handbook-frequency-stability-analysis)
  - [Código que utiliza la función](https://github.com/aewallin/allantools/blob/master/allantools/allantools.py)

"""

from numpy import *
import matplotlib.pyplot as plt
import allantools as at


# Referencia bibliográfica:
# https://www.nist.gov/publications/handbook-frequency-stability-analysis

random.seed(0)
t = logspace(0, 3, 50)     # valores de Tau de 1 a 1000
y = at.noise.white(10000)  # Generamos datos de ruido
r = 12.3                   # sample rate de los datos fabricados/adquiridos


(t2, ad, ade, adn) = at.adev(y, rate=r, data_type="freq", taus=t)  # Calculamos la Desviación de Allan


fig, ax = plt.subplots()


ax.loglog(t2, ad, '.-') # Plot the results
ax.errorbar( t2, ad , yerr=ade , color='C0' , alpha=0.5 , ms=0, mew=10)
ax.grid(True,linestyle='--',color='lightgray')
ax.grid(True,linestyle='--',color='lightgray', which='minor', alpha=0.2)
ax.set_xlabel(r'$\tau$')
ax.set_ylabel(r'$\sigma^2_{ADEV}(\tau) $')


# plt.savefig('repositorio_allan_000.png')



#%%  Varianza de Allan con superposición (overlap)
"""
Cálculo de la varianza de allan "con overlap"

  - [Fuente de las fórmulas](https://www.nist.gov/publications/handbook-frequency-stability-analysis)
  - [Código que utiliza la función](https://github.com/aewallin/allantools/blob/master/allantools/allantools.py)


![grafico](oadev.png "oadev.png")


"""

from numpy import *
import matplotlib.pyplot as plt
import allantools as at


# Referencia bibliográfica:
# https://www.nist.gov/publications/handbook-frequency-stability-analysis

random.seed(0)
t = logspace(0, 3, 50)     # valores de Tau de 1 a 1000
y = at.noise.white(10000)  # Generamos datos de ruido
r = 12.3                   # sample rate de los datos fabricados/adquiridos



fig, ax = plt.subplots()


(t2, ad, ade, adn) = at.adev(y, rate=r, data_type="freq", taus=t)  # Calculamos la Desviación de Allan
ax.plot(t2, ad, '.-', color='C0' , label='adev')
ax.fill_between( t2, ad-ade, ad+ade , color='C0' , alpha=0.5 )
ax.semilogx()  # Escala logarítmica en X
ax.semilogy()  # Escala logarítmica en Y


(t2, ad, ade, adn) = at.oadev(y, rate=r, data_type="freq", taus=t)  # Calculamos la Desviación de Allan con superposición
ax.plot(t2, ad, '.-', color='C1' , label='oadev')
ax.fill_between( t2, ad-ade, ad+ade , color='C1' , alpha=0.5 )


ax.grid(True,linestyle='--',color='lightgray')
ax.grid(True,linestyle='--',color='lightgray', which='minor', alpha=0.2)
ax.set_xlabel(r'$\tau$')
ax.set_ylabel(r'$\sigma^2_{y}(\tau) $')
ax.legend(loc='best')


# plt.savefig('repositorio_allan_001.png')




