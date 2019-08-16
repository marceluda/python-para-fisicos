# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 11:09:22 2019

@author: lolo
"""

from numpy import *
import matplotlib.pyplot as plt


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




<div class="alert alert-danger" role="alert" >
  <strong>Aviso:</strong> La página está en construcción.
</div>

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

















