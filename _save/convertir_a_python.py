# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 11:21:17 2018

@author: lolo
"""

#from numpy import *
#import matplotlib.pyplot as plt

import os
import re

from glob import glob

#%%

os.chdir('/home/lolo/Dropbox/Doctorado/github/python-para-fisicos_pages/tuto/labo2')

for md in glob('*.md'):
    print(md)

    with open(md) as inp:
        contenido = inp.read()

    bloque=[]
    cargar=False
    for i,linea in enumerate(contenido.split('\n')):
        if linea[0:9]=='```python':
            bloque.append('#%% linea '+str(i) + '\n')
            cargar = True
            continue
        elif linea[0:4]=='```':
            
            cargar = False
        if cargar:
            bloque[-1] += linea + '\n'
    
    with open( md[:-3]+'.py' ,'w') as output:
        output.write( '\n\n\n'.join( bloque )  )
