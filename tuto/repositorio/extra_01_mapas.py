#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TITULO: Mapas
# RESUMEN: Ejemplos de producción de Mapas con matplotlib y Basemap

"""
Ejemplos de producción de Mapas con matplotlib y Basemap.
Para poder realizar los ejemplso hay que instalar, usando `pip` o `conda` los siguientes
paquetes:

(codigo para Linux)

`$HOME/anaconda3/bin/conda install -c anaconda basemap`

`$HOME/anaconda3/bin/conda install -c anaconda basemap-data-hires`

`$HOME/anaconda3/bin/pip install shapelib`

"""

#%%  Ejemplo del mapa planetario con referencia horaria
"""
Esto está tomado de la web de [basemap](https://matplotlib.org/basemap/users/examples.html)
y modificado para poder hacer zoom en un area deseada.
"""
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


#%%  Ejemplo de mapa de Sudamérica
"""
Este mapa fue realizado partiendo de las coordenada tomadas del mapa anterior
"""
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




#%%  Ejemplo de mapa topográfico
"""
Es igual que el ejemplo anterior pero con copografía
"""
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


