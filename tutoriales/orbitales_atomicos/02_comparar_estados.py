#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
En este archivo graficamos distintos estados de forma tal que se puedan comparar
unos con otros en 3D
La complejidad radica en las limitaciones de matplotlib para el 3D.
Se generarán los polígilos de las distintas superficies y se los graficará como una sola
cambiando el colora para diferenciarlos.
"""


from numpy import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import matplotlib as mpl

from orbitales_atomicos import Ψ,WaveFunction

from skimage import measure  # Para obtener superficies en 3D
from matplotlib.colors import ListedColormap, LinearSegmentedColormap   # Para generar mapas de color a mano


#%% Funciones auxiliares para graficar

# Mapa de color que usaremos para colorear la fase de la función de onda
cmap_fase = LinearSegmentedColormap.from_list('fase','blue,C0,C0,red,red,C1,C1,blue'.split(','))


from orbitales_atomicos import coordenada_maxima


#%% Grafico de estados apilados

# Armamos 3 estados diferentes para graficar
psi0 = ( Ψ(2,1,-1) + 1j*Ψ(2,1,1) ) /sqrt(2)
psi1 = ( Ψ(3,2,1) - Ψ(3,2,-1) ) /sqrt(2)/1j
psi2 = Ψ(1,0,0)


# Para facilitar, los agrupamos en un tuple
estados = (psi0,psi1,psi2)


# Creamos la figura y los ejes en 3D
fig, ax = plt.subplots(1,1, figsize=(12,8) )
ax.remove()
ax=fig.add_subplot(1,1,1,projection='3d')


    
# Parámetros para mallas
clim   = max([ coordenada_maxima(estado,umbral=0.4) for estado in estados ])  # Maxima extensión de ejes
N      = 50                      # la grilla tendrá 50³ puntos
umbral = 0.5                     # umbral para el cálculo de superficies: límite 10% de probabilidad


# Definimos una grilla de coordenadas cartesianas 
# desde -clim hasta +clim con N pts, para cada coordenada
X,Y,Z       = mgrid[-clim:clim:N*1j,-clim:clim:N*1j,-clim:clim:N*1j]

# Transformamos a coordenadas esféricas
r,phi,theta = sqrt( X**2 + Y**2 + Z**2 ) , arctan2(Y,X)  ,  arctan2( sqrt(X**2+Y**2) , Z  )





# Armamos listas donde vamos a acumular las caras, vértives y colores de las
# superficies que vamos a calcular
vertices = []
caras    = []
colores  = []
id_color = []
last_index = 0


# Recorremos los estados
for ii,psi in enumerate(estados):
    
    # Calculamos densidad de probabilidad
    WF = abs(psi(r,phi,theta))**2
    
    # Buscamos superficies de contorno
    verts, faces,_,_ = measure.marching_cubes_lewiner(WF, WF.max()*umbral , allow_degenerate=False  )
    
    # Convertimos indices a coordenadas 
    verts = verts/N*clim*2-clim
    
    # Guardamos los vértices y las caras de los triángulos en las estructuras que definimos
    vertices     += verts.tolist()
    caras        += (faces + last_index).tolist()
    colores      += [ f'C{ii}' ]
    id_color     += [ii]* faces.shape[0]
    last_index   += verts.shape[0]
    

vertices = array(vertices, dtype=float32)
caras    = array(caras   , dtype=int32)
id_color = array(id_color)


# Creamos un colormap con los colores acumulados
cmap = mpl.colors.ListedColormap(colores)


# Graficamos la superficie
sup = ax.plot_trisurf(vertices[:, 0], vertices[:,1], caras, vertices[:, 2],
                      cmap=cmap, 
                      lw=0.5 , alpha=0.5)


# Asignamos los valores de identificación de color a cada triángulo
sup.set_array( id_color )

# Re-escalamos el colormap para que coincida con los valores asignados
sup.autoscale()


sup.set_edgecolor([ f'C{ii}' for ii in id_color ] )

ax.set_xlim(-5,5)
ax.set_ylim(-5,5)
ax.set_zlim(-5,5)

ax.set_xlabel('x [Å]')
ax.set_ylabel('y [Å]')
ax.set_zlabel('z [Å]')


ax.set_title('Estados:\n' + '\n'.join([ str(p) for p in estados ]) )






#%%##############################################################################


#%% Veriosn Plot.ly 3D

import plotly.io as pio
pio.renderers.default='browser'

import plotly.graph_objects as go
from plotly.tools import FigureFactory as FF



x,y,z = zip(*vertices)  

colores =  cmap(  mpl.colors.Normalize(vmin=min(id_color),vmax=max(id_color))( id_color ) )

fig = FF.create_trisurf(x=x,
                        y=y, 
                        z=z, 
                        plot_edges  = False,
                        simplices   = caras,
                        color_func  = [ f'rgb({int(c[0]*255)}, {int(c[1]*255)}, {int(c[2]*255)})' for c in colores.tolist() ],
                        title       = 'estados varios')

fig['data'][0].update(opacity=0.5)
for eje in 'x y z'.split():
    fig['layout']['scene'][f'{eje}axis']['title']=f'{eje} [Å]'
    fig['layout']['scene'][f'{eje}axis']['range']=[-5,5]

fig.show()

# fig.write_json('orbitales_04_3D.json')

