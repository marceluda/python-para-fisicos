#!/home/lolo/anaconda3/bin/python3
# -*- coding: utf-8 -*-
"""
script para armar la web de REPOSITORIO

"""

from numpy import *
import matplotlib.pyplot as plt

from glob import glob

import re

prefijo = 'repositorio'


import os

os.chdir('/home/lolo/Dropbox/Doctorado/github/python-para-fisicos_pages/tuto/repositorio/')

source_folder = '/home/lolo/Dropbox/Doctorado/github/python-para-fisicos_pages'
dest_folder   = '/var/www/html/python-para-fisicos/'
update_cmd = f'jekyll build --source {source_folder} --destination {dest_folder}'

def update_local():
    os.system( update_cmd )



#%% Archivo Base

BASE_HEAD = """
---
title: Repositorio de ejemplos prácticos
description: Referencia rápida de código
layout: page
navbar: repo
---

<div class="alert alert-danger" role="alert" >
  <strong>Aviso:</strong> La página está en construcción.
</div>
"""

BASE_HEAD = BASE_HEAD.strip() + '\n\n\n'


#  * **[Ejemplos para graficar datos](repo_tutos_graficos/)**: Se presentan a continuación ejemplos de graficación de datos incluyendo las opciones mas habituales.
#  * **[Ejemplos para cargar y guardar datos](repo_tutos_IO/)**: En este archivo se muestran ejemplos prácticos para leer datos desde  diferentes formatos de archivos y para guardarlos en diferentes formatos.
#  * **[Ejemplos para realizar ajustes de datos](repo_tutos_ajustes/)**: Se presentan ejemplos de ajustes lineales, polinomiales y no lineales para uso general.











#%% Procesar páginas

# Reglas:

# El primer bloque es la intro
# Cada bloque, luego del #%% viene el titulo
# luego del siguiente % vienen opciones separadads por comas



def extraer_main(txt,main_opt=True):
    textos   = '\n'.join([ y.strip() for y in txt.split('"""')[1::2] ])
    if main_opt:
        opciones = { y[1:].split(':')[0].strip() : y[1:].split(':')[1].strip() for y in txt.split('\n') if bool( re.match('^# +[A-Z]+: .*$', y )) } 
    else:
        opciones = {}
    return textos,opciones

def extraer_codigo(txt,codigo_opt=True):
    textos   = '\n'.join([ y.strip() for y in txt.split('"""')[1::2] ])
    if codigo_opt:
        codigo = '\n'.join([ y.strip() for y in txt.split('"""')[0::2] ])
    else:
        codigo = ''
    return textos,codigo




HEAD = """
---
title: {0:s}
description: {0:s}
layout: page
navbar: repo
mathjax: true
---

<div class="alert alert-info" role="alert" >
  <strong>Archivo:</strong> <a href="../{1:s}"> {1:s} </a>
</div>
"""
HEAD = HEAD.strip() + '\n'


CODIGO ="""
<a data-toggle="collapse" href="#desplegable{0:03d}" aria-expanded="false" aria-controls="desplegable{0:03d}">ver código<span class="caret"></span></a>

<div id="desplegable{0:03d}" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

```python
{1:s}
```
</div>

"""


filetype =  'mat,xls,xlsx,csv,npz,shp,dbf'.split(',')


intros = ['### Ejemplos introductorios']
intros.append('\n<hr />\n### Ejemplos no relacionados con física\n' )

prefs = ['repositorio','extra']

with open(f'../{prefijo}.md', 'w') as base_writer:
    base_writer.write(BASE_HEAD)
    
    for entrada,pref in zip(intros,prefs):
        base_writer.write(entrada)
        base_writer.write('\n')
        
        fns = sort(glob(f'{pref}_*.py')).tolist()
        for fn in fns:
            with open(fn, 'r') as reader:
                lines = reader.readlines()
            
            archivo = fn[len(pref)+4:-3] + '.md'
            
            # Separamos en bloques
            bloques = ''.join(lines).split('#%%')
            
            # Apertura
            texto_apertura , opt = extraer_main(  bloques.pop(0) )
            titulo  = opt['TITULO']  if 'TITULO'  in opt.keys() else archivo[:-3]
            resumen = opt['RESUMEN'] if 'RESUMEN' in opt.keys() else texto_apertura.split('\n')[0]
            url     = archivo[:-3]
            os.system(f'mkdir -p {url}')
            base_writer.write(f'  * **[{titulo}]({url}/)**: {resumen}\n')
            #  * **[Ejemplos para graficar datos](repo_tutos_graficos/)**: Se presentan a continuación ejemplos de graficación de datos incluyendo las opciones mas habituales.
    
            with open( archivo , 'w') as writer:
                writer.write( HEAD.format(titulo , fn) )
                
                writer.write( texto_apertura  )
                
                for numero,bloque in enumerate([ y.split('\n') for y in bloques ]):
                    titulo = bloque.pop(0).strip()
                    
                    writer.write( f'\n## {titulo}\n' )
                    
                    texto, codigo = extraer_codigo( '\n'.join(bloque)  )
                    writer.write( f'\n{texto}\n' )
                    
                    for archivo_adj in unique([ y for y in codigo.split("'") if y.split('.')[-1].lower() in filetype and len(y)>4]) :
                        if os.path.isfile(archivo_adj):
                            os.system(f'mv "{archivo_adj}" "{url}/"')
                        writer.write( f'  * [{archivo_adj}]({archivo_adj})\n' )
                    
                    for imagen in [ y for y in codigo.split('\n') if ( 'plt.savefig' in y ) ]:
                        imgname= imagen.split("'")[1]
                        if os.path.isfile(imgname):
                            os.system(f'mv "{imgname}" "{url}/"')
                        writer.write( f'\n![grafico]({imgname} "{imgname}")\n' )
                        #print(imgname)
                    
                    writer.write( CODIGO.format(numero,codigo) )
                
            print( f'{fn} --> {archivo}' )

    
    

    

update_local()



#%%
from datetime import datetime

fecha = datetime.now().isoformat()

os.system('git add .')
os.system(f'git add ../{prefijo}.md')
os.system(f'git commit -m "ACTUALIZACION AUTOMATICA {fecha}"')
os.system('git push')








