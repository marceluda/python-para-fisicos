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

"""

from numpy import *
import matplotlib.pyplot as plt
import allantools as at


# Referencie bibliográfica:
# https://www.nist.gov/publications/handbook-frequency-stability-analysis


t = logspace(0, 3, 50)  # tau values from 1 to 1000
y = at.noise.white(10000)  # Generate some frequency data
r = 12.3  # sample rate in Hz of the input data
(t2, ad, ade, adn) = at.adev(y, rate=r, data_type="freq", taus=t)  # Compute the overlapping ADEV


fig, ax = plt.subplots()


ax.loglog(t2, ad, '.-') # Plot the results
ax.errorbar( t2, ad , yerr=ade , color='C0' , alpha=0.5 , ms=0, mew=10)
ax.grid(b=True,linestyle='--',color='lightgray')
ax.grid(b=True,linestyle='--',color='lightgray', which='minor', alpha=0.2)
ax.set_xlabel(r'$\tau$')
ax.set_ylabel(r'$\sigma^2_{ADEV}(\tau) $')


# plt.savefig('repositorio_allan_000.png')




