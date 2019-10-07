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


filetype =  'mat,xls,xlsx,csv,npz'.split(',')





fns = sort(glob(f'{prefijo}_*.py')).tolist()

with open(f'../{prefijo}.md', 'w') as base_writer:
    base_writer.write(BASE_HEAD)

    for fn in fns:
        with open(fn, 'r') as reader:
            lines = reader.readlines()
        
        archivo = fn[len(prefijo)+4:-3] + '.md'
        
        # Separamos en bloques
        bloques = ''.join(lines).split('#%%')
        
        # Apertura
        texto_apertura , opt = extraer_main(  bloques.pop(0) )
        titulo  = opt['TITULO'] if 'TITULO' in opt.keys() else archivo[:-3]
        resumen = opt['RESUMEN'] if 'RESUMEN' in opt.keys() else texto_apertura.split('\n')[0]
        url     = archivo[:-3]
        os.system(f'mkdir -p {url}')
        base_writer.write(f'  * **[{titulo}]({url}/)**: {resumen}\n')
        #  * **[Ejemplos para graficar datos](repo_tutos_graficos/)**: Se presentan a continuación ejemplos de graficación de datos incluyendo las opciones mas habituales.

        with open( archivo , 'w') as writer:
            writer.write( HEAD.format(titulo , fn) )
            
            for numero,bloque in enumerate([ y.split('\n') for y in bloques ]):
                titulo = bloque.pop(0).strip()
                
                writer.write( f'\n## {titulo}\n' )
                
                texto, codigo = extraer_codigo( '\n'.join(bloque)  )
                writer.write( f'\n{texto}\n' )
                
                for archivo_adj in [ y for y in codigo.split("'") if y.split('.')[-1].lower() in filetype ] :
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





 
 
#%%








random.seed(0)
xx = linspace(-5,15)
yy = exp(-xx/5) * (10 + random.normal(size=len(xx)))/10
ey = exp(-xx/5)/10 + 0.1 + random.normal(size=len(xx))/30

plt.plot(xx,yy)

plt.plot(xx,yy+ey)
plt.plot(xx,yy-ey)

#%%
with open('decaimiento.csv', 'a') as archivo:
    for x,y,ee in zip(xx,yy,ey):
        txt='{:5.2f},{:4.2f},{:4.2f}'
        print( txt.format(x,y,ee) )
        archivo.write(txt.format(x,y,ee)+'\n' )

#%%
random.seed(0)

x0 = linspace(0,10,1000)
y0 = ( 1+sin(xx*5) ) * ( 1 + xx**2 )

x1 = arange(10)
y1 = 100 - x1 * 15.5 + random.normal(size=10)*8
e1 = 20+random.normal(size=10).round(1)

x2 = arange(10)
y2 = exp(x2)/8000*200 -50

plt.plot(x0,y0)
plt.errorbar(x1,y1,yerr=e1)
plt.plot(x2,y2,'o')



#%% Generar archivos
from glob import glob

head = """---
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


insertar_codigo ="""
<a data-toggle="collapse" href="#desplegable{0:03d}" aria-expanded="false" aria-controls="desplegable{0:03d}">ver código<span class="caret"></span></a>

<div id="desplegable{0:03d}" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

```python
{1:s}
```
</div>


"""


repo_txt = """---
title: Repositorio de ejemplos prácticos
description: Referencia rápida de código
layout: page
navbar: repo
---

<div class="alert alert-danger" role="alert" >
  <strong>Aviso:</strong> La página está en construcción.
</div>


"""

filetype =  'mat,xls,xlsx,csv,npz'.split(',')

for fn in glob('repo_tutos_*.py'):
    print(fn)
    with open(fn, 'r') as reader:
        lines = reader.readlines()
    
    comentarios = [ y.strip() for y in  ''.join(lines).split('"""')[1::2]  ]
    codigos     = [ y.strip() for y in  ''.join(lines).split('"""')[4::2]  ]
    titulos     = [ y[3:].strip() for y in lines if '#%%'==y[:3] ]
    
    header       = comentarios.pop(0).split('\n')
    titulo       = header.pop(0)
    header_texto = '\n'.join(header)
    
    repo_txt += '  * **[{0:s}]({1:s})**: {2:s}\n'.format( titulo, fn[:-3]+'/' , header_texto.replace('\n',' ') )
    
    
    with open(fn[:-3]+'.md', 'w') as writer:
        writer.write( head.format( titulo , fn  ) )
        
        writer.write( header_texto + '\n\n'  )
        
        for comentario,codigo,titulo,i in zip(comentarios,codigos,titulos,arange(len(codigos))):
            writer.write('## ' + titulo + '\n\n')
            writer.write( comentario + '\n\n')
            print(i)
            
            for archivo in [ y for y in codigo.split("'") if y.split('.')[-1].lower() in filetype ] :
                writer.write( '  * [{0:s}]({0:s})\n'.format(archivo) )
            
            for imagen in [ y for y in codigo.split('\n') if ( 'plt.savefig' in y ) ]:
                imgname= imagen.split("'")[1]
                writer.write( '\n![grafico](../{0:s} "{0:s}")\n'.format(imgname) )
                print(imgname)
            writer.write(insertar_codigo.format( i, codigo.split('#%%')[0] )  )
            print('')
            
            
 

#print(repo_txt)

with open('../repo.md', 'w') as writer:
    writer.write(repo_txt)


#%%

for fn in glob('repo*.py'):
    print(fn)
    with open(fn, 'r') as reader:
        with open(fn[:-3]+'.md', 'w') as writer:
            
            writer.write( head )
            
            for line in reader:
                #print(line, end='')
                
                writer.write( line )

















