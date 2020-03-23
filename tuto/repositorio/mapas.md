---
title: Mapas
description: Mapas
layout: page
navbar: repo
mathjax: true
---

<div class="alert alert-info" role="alert" >
  <strong>Archivo:</strong> <a href="../extra_01_mapas.py"> extra_01_mapas.py </a>
</div>
Ejemplos de producción de Mapas con matplotlib y Basemap.
Para poder realizar los ejemplso hay que instalar, usando `pip` o `conda` los siguientes
paquetes:

(codigo para Linux)

`$HOME/anaconda3/bin/conda install -c anaconda basemap`

`$HOME/anaconda3/bin/conda install -c anaconda basemap-data-hires`

`$HOME/anaconda3/bin/pip install shapelib`
## Ejemplo del mapa planetario con referencia horaria

Esto está tomado de la web de [basemap](https://matplotlib.org/basemap/users/examples.html)
y modificado para poder hacer zoom en un area deseada.

![grafico](extra_graficos_000.png "extra_graficos_000.png")

<a data-toggle="collapse" href="#desplegable000" aria-expanded="false" aria-controls="desplegable000">ver código<span class="caret"></span></a>

<div id="desplegable000" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

```python

from numpy import *
import matplotlib.pyplot as plt
import os
os.environ['PROJ_LIB'] = os.environ['HOME']+'/anaconda3/share/proj'
from mpl_toolkits.basemap import Basemap

from datetime import datetime


# Creamos na figura 
fig, ax = plt.subplots( 1,1, figsize=(10,7))


# Creamos un mapa del mundo con proyección miller
m = Basemap(projection='mill',lon_0=0, ax=ax)

# Dibujamos las costas
m.drawcoastlines()

# Dibujamos paralelos y meridianos
m.drawparallels(arange(-90,90,30),labels=[1,0,0,0])
m.drawmeridians(arange(m.lonmin,m.lonmax+30,60),labels=[0,0,0,1])

# Dibujamos límites de países
m.drawcountries()

# Le ponemos límites al mapa y color al agua
m.drawmapboundary(fill_color='aqua')

# Le ponemos color a la tierra
m.fillcontinents(color='white',lake_color='aqua')


# Agregamos la penumbra de la noche para el horario actual
date = datetime.utcnow()
CS=m.nightshade(date)
plt.title('Día/Noche para {:s} (UTC)'.format( date.strftime("%d %b %Y %H:%M:%S") ) )
plt.show()

plt.pause(0.5)

print('Luego de usar la herraminta de zoom para delimitar el area del mapa que se desea, ejecute esta parte del código a continuación')

coord_x_pu = ax.get_xlim()
coord_y_pu = ax.get_ylim()

# Obtenemos los límites de los ejes y los convertimos a latitudes y longitudes
llcrnrlon,llcrnrlat = m( coord_x_pu[0] , coord_y_pu[0] , inverse=True )
urcrnrlon,urcrnrlat = m( coord_x_pu[1] , coord_y_pu[1] , inverse=True )

# imprimimos las coordenadas
coordenadas = dict(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat, 
                   urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat)

print('Estas son las coordenadas que deberá usar en un nuevo mapa para obtener la zona marcada:\n')

print('coordenadas=' + repr(coordenadas))


# plt.savefig('extra_graficos_000.png')
```
</div>


## Ejemplo de mapa de Sudamérica

Este mapa fue realizado partiendo de las coordenada tomadas del mapa anterior

![grafico](extra_graficos_001.png "extra_graficos_001.png")

<a data-toggle="collapse" href="#desplegable001" aria-expanded="false" aria-controls="desplegable001">ver código<span class="caret"></span></a>

<div id="desplegable001" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

```python

from numpy import *
import matplotlib.pyplot as plt
import os
os.environ['PROJ_LIB'] = os.environ['HOME']+'/anaconda3/share/proj'
from mpl_toolkits.basemap import Basemap


coordenadas = {  'llcrnrlon': -94.26844086640133,
                 'llcrnrlat': -59.165673270203285,
                 'urcrnrlon': -33.54487376284925,
                 'urcrnrlat': 14.828935756198176}

# Creamos figura para el mapa
fig, ax = plt.subplots( 1,1, figsize=(10,7))


# Creamos mapa con proyección de miller y resolución Low
m = Basemap(projection='mill', ax=ax , 
            resolution='l',   # Opciones válidas: c l i h f
            **coordenadas  )

# Repasemos algunos parámetros útiles y opciones
# Con esto varias los km^2 de resolucion de los lagos

# Con esto coloco un umbral en km^2 para qué lagos se grafican y cuales no
m.area_thresh = 100000

# Con esto grafico paralelos y meridianos cada 10 grados, solo en la region del mapa
span = 10
paralelos  = m.drawparallels(arange(round(m.latmin,-1),round(m.latmax,-1)+span,span),
                             labels=[1,0,0,0], color='gray')
meridianos = m.drawmeridians(arange(round(m.lonmin,-1),round(m.lonmax,-1)+span,span),
                             labels=[0,0,0,1], color='gray')

# Con esto dibujo ríos y le pongo color
m.drawrivers(color='lightblue')

# Dibujo límites de países
m.drawcountries(color='lightgray', linewidth=1)

# Por ahora no grafico la topografía
# m.etopo()  # topografia

m.drawcoastlines(color='gray', linewidth=0.5)

# Bordes del mapa y color de la tierra
m.drawmapboundary(fill_color='lightblue')
m.fillcontinents(color='white',lake_color='lightblue')

# Etiqueda de los ejes
ax.set_ylabel('Latitud',labelpad=40)
ax.set_xlabel('Longitud',labelpad=20)

# por último, le pongo transparencia a los meridianos y paralelos
for val,mer in meridianos.items():
    for linea in mer[0]:
        linea.set_alpha(0.5)

for val,par in paralelos.items():
    for linea in par[0]:
        linea.set_alpha(0.5)
# y reemplazo en los textos de los bordes algunas letras para castellanizar el mapa
for val,mer in meridianos.items():
    for txt in mer[1]:
        txt.set_text( txt.get_text().replace('W','O') )


# plt.savefig('extra_graficos_001.png')
```
</div>


## Ejemplo de mapa topográfico

Es igual que el ejemplo anterior pero con copografía

![grafico](extra_graficos_002.png "extra_graficos_002.png")

<a data-toggle="collapse" href="#desplegable002" aria-expanded="false" aria-controls="desplegable002">ver código<span class="caret"></span></a>

<div id="desplegable002" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

```python

from numpy import *
import matplotlib.pyplot as plt
import os
os.environ['PROJ_LIB'] = os.environ['HOME']+'/anaconda3/share/proj'
from mpl_toolkits.basemap import Basemap


coordenadas = {  'llcrnrlon': -94.26844086640133,
                 'llcrnrlat': -59.165673270203285,
                 'urcrnrlon': -33.54487376284925,
                 'urcrnrlat': 14.828935756198176}

# Creamos figura para el mapa
fig, ax = plt.subplots( 1,1, figsize=(10,7))


# Creamos mapa con proyección de miller y resolución Low
m = Basemap(projection='mill', ax=ax , 
            resolution='l',   # Opciones válidas: c l i h f
            **coordenadas  )

# Repasemos algunos parámetros útiles y opciones
# Con esto varias los km^2 de resolucion de los lagos

# Con esto coloco un umbral en km^2 para qué lagos se grafican y cuales no
m.area_thresh = 100000

# Con esto grafico paralelos y meridianos cada 10 grados, solo en la region del mapa
span = 10
paralelos  = m.drawparallels(arange(round(m.latmin,-1),round(m.latmax,-1)+span,span),
                             labels=[1,0,0,0], color='gray')
meridianos = m.drawmeridians(arange(round(m.lonmin,-1),round(m.lonmax,-1)+span,span),
                             labels=[0,0,0,1], color='gray')

# Con esto dibujo ríos y le pongo color
# m.drawrivers(color='blue')

# Dibujo límites de países
m.drawcountries(color='black', linewidth=1)

# graficamos topografica
m.etopo()  # topografia

m.drawcoastlines(color='black', linewidth=0.5)

# Bordes del mapa y color de la tierra
#m.drawmapboundary(fill_color='lightblue')
#m.fillcontinents(color='white',lake_color='lightblue')

# Etiqueda de los ejes
ax.set_ylabel('Latitud',labelpad=40)
ax.set_xlabel('Longitud',labelpad=20)

# por último, le pongo transparencia a los meridianos y paralelos
for val,mer in meridianos.items():
    for linea in mer[0]:
        linea.set_alpha(0.5)

for val,par in paralelos.items():
    for linea in par[0]:
        linea.set_alpha(0.5)
# y reemplazo en los textos de los bordes algunas letras para castellanizar el mapa
for val,mer in meridianos.items():
    for txt in mer[1]:
        txt.set_text( txt.get_text().replace('W','O') )


# plt.savefig('extra_graficos_002.png')
```
</div>


## Ejemplo de mapa con datos agregados desde base de datos georeferenciales: Nombres de pases

En este ejemplo vamos a agregar al mapa información procedente de archivos georeferenciales
(los que se usan para vincular bases de datos con mapas).

Un formato habitual para ello es que un sitio proporcione dos archivos:

  - Un archivo `.dbf` que es una base de datos, con campos y registros
  - Un archivo `.shp` que contienes posiciones, formas y puntos en algun sistema de referencia (en nuestro caso, longitud y latitud)

Con el paquete `shapefile` vamos a leer estos archivos y extraer los datos relevantes

Vamos a usar archivos extraidos de la web [naturalearthdata.com](http://www.naturalearthdata.com/downloads/)
  * [ne_10m_admin_0_countries.dbf](ne_10m_admin_0_countries.dbf)
  * [ne_10m_admin_0_countries.shp](ne_10m_admin_0_countries.shp)
  * [.shp](.shp)
  * [.dbf](.dbf)
  * [ne_10m_admin_0_countries.shp](ne_10m_admin_0_countries.shp)
  * [ne_10m_admin_0_countries.dbf](ne_10m_admin_0_countries.dbf)

![grafico](extra_graficos_003.png "extra_graficos_003.png")

<a data-toggle="collapse" href="#desplegable003" aria-expanded="false" aria-controls="desplegable003">ver código<span class="caret"></span></a>

<div id="desplegable003" class="collapse" markdown="1" style="padding: 10px; border: 1px solid gray; border-radius: 5px;">

```python

from numpy import *
import matplotlib.pyplot as plt
import os
os.environ['PROJ_LIB'] = os.environ['HOME']+'/anaconda3/share/proj'
from mpl_toolkits.basemap import Basemap

# Importamos shapefile
import shapefile

# Nueavmente vamos a trabajar con sudamérica
coordenadas = {  'llcrnrlon': -94.26844086640133,
                 'llcrnrlat': -59.165673270203285,
                 'urcrnrlon': -33.54487376284925,
                 'urcrnrlat': 14.828935756198176}

# Si tenemos los archivos que necesitamos descargados, los usamos:
if os.path.isfile('ne_10m_admin_0_countries.dbf') and os.path.isfile('ne_10m_admin_0_countries.shp'):
    myshp = open("ne_10m_admin_0_countries.shp", "rb")
    mydbf = open("ne_10m_admin_0_countries.dbf", "rb")
    
else: # Sino, los descargamos o los leemos desde la web
    from io import BytesIO
    from zipfile import ZipFile
    from urllib.request import urlopen
    
    # descargamos el archivo .zip
    respuesta = urlopen("https://naciscdn.org/naturalearth/10m/cultural/ne_10m_admin_0_countries.zip")
    zipfile   = ZipFile(BytesIO(respuesta.read()))
    for archivo in zipfile.namelist():
        if archivo[-4:]=='.shp' or archivo[-4:]=='.dbf':
            print(f'Archivo descargado: {archivo}')
            # con esta linea extraemos el archivo en el directorio actual
            zipfile.extract(archivo)
            
    # pero tambien podemos leer los desde la memoria directamente
    myshp = zipfile.open('ne_10m_admin_0_countries.shp')
    mydbf = zipfile.open('ne_10m_admin_0_countries.dbf')

# juntamos las formas y la base de datos para procesarlas
sfa = shapefile.Reader(shp=myshp, dbf=mydbf)


# Podemos desde la consola ver el contenido de la base de datos con las siguientes instrucciones:
sfa.fields    # Lista de campos de la tabla de datos
sfa.records() # Lista de todos los registros de la tabla

# ejemplo, el registro 5 es la Argentina
sfa.record(5)

# Es más facil de visualizar si lo vemos como un diccionario:
sfa.record(5).as_dict()

# Cada registro tiene in Object ID que sirve para identificar la forma asociada:
sfa.record(5).oid

# Luego podemos acceder a las formas asociadas
sfa.shape( sfa.record(5).oid )

# En este caso, la forma asociada es un polígono
sfa.shape( sfa.record(5).oid ).shapeTypeName

# El polígono esta compuesto de estos puntos
sfa.shape( sfa.record(5).oid ).points

# Aca hay una lista de partes que nos dice entre que indice y que indice estan los puntos de cada parte del polígono
sfa.shape( sfa.record(5).oid ).parts

# Dibujamos el mapa de sudamérica como hicimos antes

fig, ax = plt.subplots( 1,1, figsize=(10,7))
m = Basemap(projection='mill', ax=ax , 
            resolution='l',   # Opciones válidas: c l i h f
            **coordenadas  )
span = 10
paralelos  = m.drawparallels(arange(round(m.latmin,-1),round(m.latmax,-1)+span,span),
                             labels=[1,0,0,0], color='gray')
meridianos = m.drawmeridians(arange(round(m.lonmin,-1),round(m.lonmax,-1)+span,span),
                             labels=[0,0,0,1], color='gray')

# m.drawrivers(color='lightblue')
m.drawcountries(color='lightgray', linewidth=1)
m.drawcoastlines(color='gray', linewidth=0.5)
m.drawmapboundary(fill_color='lightblue')
m.fillcontinents(color='white',lake_color='lightblue')
ax.set_ylabel('Latitud',labelpad=40)
ax.set_xlabel('Longitud',labelpad=20)
for val,mer in meridianos.items():
    for linea in mer[0]:
        linea.set_alpha(0.5)
for val,par in paralelos.items():
    for linea in par[0]:
        linea.set_alpha(0.5)
for val,mer in meridianos.items():
    for txt in mer[1]:
        txt.set_text( txt.get_text().replace('W','O') )


# Ahora si, vamos a procesar la base de datos para obtener la información que queremos
# Agreguemos los nombres de los países

# Armamos una función auxiliar que nos dice si una coordenada determinada
# está dentro e nuestro mapa actual o no
def esta_adentro(m,coord):
    lon, lat = coord
    if m.lonmin<lon and lon< m.lonmax:
        if m.latmin<lat and lat<m.latmax:
            return True
    return False


# recorremos la base de datos
for r in sfa.shapeRecords():
    # Calculamos el centro promedio de las coordenadas de los paises
    centro_de_coordenadas = array([ [p[0],p[1]] for p in r.shape.points ]).mean(0)
    
    # Si el centro de coordenadas está dentro de nuestro mapa, procesamos
    if esta_adentro(m , centro_de_coordenadas):
        # Extraemos nombre
        nombre        = r.record.as_dict()['NAME_ES']
        poblacion     = r.record.as_dict()['POP_EST']
        tamaño        = interp(poblacion , [0,220e6], [8,14]  )
        # Obtenemos tamaño de letra segun la población del país
        
        # obtenemos coordenadas del grafico:
        xx, yy = m( *centro_de_coordenadas )
        
        # Escribimos los nombres de los paises con población mayor a 1 millón
        if poblacion > 1e6:
            # graficamos el nombre
            ax.text( xx , yy , nombre,
                horizontalalignment = 'center',
                verticalalignment   = 'center',
                fontsize            =  tamaño, 
                color               = 'black', 
                alpha               = 0.8  ) 
        # print(nombre,poblacion,tamaño)


# plt.savefig('extra_graficos_003.png')
```
</div>

