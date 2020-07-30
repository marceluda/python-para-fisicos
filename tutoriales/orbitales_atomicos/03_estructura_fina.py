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
cmap_fase_up = LinearSegmentedColormap.from_list('faseUp','darkblue,darkblue,C0,C0,C0,C0,darkblue,darkblue'.split(','))
cmap_fase_down = LinearSegmentedColormap.from_list('faseDown','darkred,darkred,C1,C1,C1,C1,darkred,darkred'.split(','))


from orbitales_atomicos import coordenada_maxima
## LEER
#   https://en.wikipedia.org/wiki/Atomic_orbital
#   https://www.wikiwand.com/en/Hydrogen-like_atom    


#%% Estados de '5P3/2'

from orbitales_atomicos import autoestado_SO


# Armamos 4 estados diferentes para graficar

estados = [ autoestado_SO('5P3/2',m=ms) for ms in arange(-3/2,3/2+1) ]

# Creamos la figura y los ejes en 3D
fig = plt.figure(figsize=(14,9) )

axx = []
for ii in range(4):
    axx.append(  fig.add_subplot(2,2,ii+1,projection='3d')  )

# Parámetros para mallas
clim   = max([ coordenada_maxima(estado,umbral=0.08) for estado in estados ])  # Maxima extensión de ejes
N      = 50                      # la grilla tendrá 50³ puntos
umbral = 0.1                     # umbral para el cálculo de superficies: límite 10% de probabilidad

# Definimos una grilla de coordenadas cartesianas 
# desde -clim hasta +clim con N pts, para cada coordenada
X,Y,Z       = mgrid[-clim:clim:N*1j,-clim:clim:N*1j,-clim:clim:N*1j]

# Transformamos a coordenadas esféricas
r,phi,theta = sqrt( X**2 + Y**2 + Z**2 ) , arctan2(Y,X)  ,  arctan2( sqrt(X**2+Y**2) , Z  )

# Recorremos los estados
for ii,psi,ax in zip(range(len(estados)),estados,axx):
    
    # Calculamos densidad de probabilidad
    WF = abs(psi(r,phi,theta))**2
    
    # Buscamos superficies de contorno spin UP
    verts_UP, faces_UP,_,_ = measure.marching_cubes_lewiner(WF[0], WF.max()*umbral , allow_degenerate=False  ) if WF[0].max()>0 else (array([]),array([]),0,0)
    
    # Buscamos superficies de contorno spin DOWN
    verts_DW, faces_DW,_,_ = measure.marching_cubes_lewiner(WF[1], WF.max()*umbral , allow_degenerate=False  ) if WF[1].max()>0 else (array([]),array([]),0,0)
    
    # Convertimos indices a coordenadas 
    verts_UP = verts_UP/N*clim*2-clim   if WF[0].max()>0 else array([])
    verts_DW = verts_DW/N*clim*2-clim   if WF[1].max()>0 else array([])
    
    # apilamos superficies a graficar
    vertices = array(  verts_UP.tolist() + verts_DW.tolist()                          )
    caras    = array(  faces_UP.tolist() + (faces_DW+verts_UP.shape[0]).tolist()      )
    colores  =        [ 'C0'     , 'C1'     ]
    id_color = array( [0]* faces_UP.shape[0] + [1]* faces_DW.shape[0]                 )
    
    # Creamos un colormap con los colores acumulados
    cmap = mpl.colors.ListedColormap(colores)
    
    
    # Graficamos la superficie
    sup = ax.plot_trisurf(vertices[:, 0], vertices[:,1], caras, vertices[:, 2],
                          cmap=cmap, 
                          lw=0.5 , alpha=0.5)
    
    
    # Asignamos los valores de identificación de color a cada triángulo
    sup.set_array( id_color )
    
    # Re-escalamos el colormap para que coincida con los valores asignados
    #sup.autoscale()
    sup.set_clim(0,1)
    
    ax.set_xlabel('x [Å]')
    ax.set_ylabel('y [Å]')
    ax.set_zlabel('z [Å]')

    #sup.set_edgecolor([ f'C{ii}' for ii in id_color ] )

    ax.set_xlim(-5,5)
    ax.set_ylim(-5,5)
    ax.set_zlim(-5,5)
    
    
    ax.set_title('$5^{2}P_{3/2}$ ' + f'm={-3+ii*2}/2'  + '\n' + str(psi) )


#
#for ax in axx:
#    ax.azim = 90
#    ax.elev = 0
#plt.draw()


#  https://medium.com/@pnpsegonne/animating-a-3d-scatterplot-with-matplotlib-ca4b676d4b55
#  https://pythonmatplotlibtips.blogspot.com/2018/11/animation-3d-surface-plot-funcanimation-matplotlib.html



#%%##############################################################################

#%% Estados de '5P1/2'


from orbitales_atomicos import autoestado_SO


# Armamos 4 estados diferentes para graficar

estados = [ autoestado_SO('5P1/2',m=ms) for ms in arange(-1/2,1/2+1) ]



# Creamos la figura y los ejes en 3D
fig = plt.figure(figsize=(14,9) )

axx = []
for ii in range(2):
    axx.append(  fig.add_subplot(1,2,ii+1,projection='3d')  )


# Parámetros para mallas
clim   = max([ coordenada_maxima(estado,umbral=0.4) for estado in estados ])  # Maxima extensión de ejes
N      = 50                      # la grilla tendrá 50³ puntos
umbral = 0.5                     # umbral para el cálculo de superficies: límite 10% de probabilidad


# Definimos una grilla de coordenadas cartesianas 
# desde -clim hasta +clim con N pts, para cada coordenada
X,Y,Z       = mgrid[-clim:clim:N*1j,-clim:clim:N*1j,-clim:clim:N*1j]

# Transformamos a coordenadas esféricas
r,phi,theta = sqrt( X**2 + Y**2 + Z**2 ) , arctan2(Y,X)  ,  arctan2( sqrt(X**2+Y**2) , Z  )


# Recorremos los estados
for ii,psi,ax in zip(range(len(estados)),estados,axx):
    
    # Calculamos densidad de probabilidad
    WF = abs(psi(r,phi,theta))**2
    
    # Buscamos superficies de contorno spin UP
    verts_UP, faces_UP,_,_ = measure.marching_cubes_lewiner(WF[0], WF.max()*umbral , allow_degenerate=False  ) if WF[0].max()>0 else (array([]),array([]),0,0)
    
    # Buscamos superficies de contorno spin DOWN
    verts_DW, faces_DW,_,_ = measure.marching_cubes_lewiner(WF[1], WF.max()*umbral , allow_degenerate=False  ) if WF[1].max()>0 else (array([]),array([]),0,0)
    
    # Convertimos indices a coordenadas 
    verts_UP = verts_UP/N*clim*2-clim   if WF[0].max()>0 else array([])
    verts_DW = verts_DW/N*clim*2-clim   if WF[1].max()>0 else array([])
    
    # apilamos superficies a graficar
    vertices = array(  verts_UP.tolist() + verts_DW.tolist()                          )
    caras    = array(  faces_UP.tolist() + (faces_DW+verts_UP.shape[0]).tolist()      )
    colores  =        [ 'C0'     , 'C1'     ]
    id_color = array( [0]* faces_UP.shape[0] + [1]* faces_DW.shape[0]                 )
    
    # Creamos un colormap con los colores acumulados
    cmap = mpl.colors.ListedColormap(colores)
    
    
    # Graficamos la superficie
    sup = ax.plot_trisurf(vertices[:, 0], vertices[:,1], caras, vertices[:, 2],
                          cmap=cmap, 
                          lw=0.5 , alpha=0.5)
    
    
    # Asignamos los valores de identificación de color a cada triángulo
    sup.set_array( id_color )
    
    # Re-escalamos el colormap para que coincida con los valores asignados
    #sup.autoscale()
    sup.set_clim(0,1)
    
    ax.set_xlabel('x [Å]')
    ax.set_ylabel('y [Å]')
    ax.set_zlabel('z [Å]')

    #sup.set_edgecolor([ f'C{ii}' for ii in id_color ] )

    ax.set_xlim(-5,5)
    ax.set_ylim(-5,5)
    ax.set_zlim(-5,5)
    
    
    ax.set_title('$5^{2}P_{1/2}$ ' + f'm={-1+ii*2}/2' )



#%%##############################################################################

#%% Estados de '5P3/2' Coloreando las fases con dos colores

# AZUL: Spin UP
# ROJO: Spin DOWN

from orbitales_atomicos import autoestado_SO


# Armamos 4 estados diferentes para graficar

estados = [ autoestado_SO('5P3/2',m=ms) for ms in arange(-3/2,3/2+1) ]

# Creamos la figura y los ejes en 3D
fig = plt.figure(figsize=(14,9) )

axx = []
for ii in range(4):
    axx.append(  fig.add_subplot(2,2,ii+1,projection='3d')  )

# Parámetros para mallas
clim   = max([ coordenada_maxima(estado,umbral=0.08) for estado in estados ])  # Maxima extensión de ejes
N      = 50                      # la grilla tendrá 50³ puntos
umbral = 0.1                     # umbral para el cálculo de superficies: límite 10% de probabilidad

# Definimos una grilla de coordenadas cartesianas 
# desde -clim hasta +clim con N pts, para cada coordenada
X,Y,Z       = mgrid[-clim:clim:N*1j,-clim:clim:N*1j,-clim:clim:N*1j]

# Transformamos a coordenadas esféricas
r,phi,theta = sqrt( X**2 + Y**2 + Z**2 ) , arctan2(Y,X)  ,  arctan2( sqrt(X**2+Y**2) , Z  )

# Recorremos los estados
for ii,psi,ax in zip(range(len(estados)),estados,axx):
    
    # Calculamos densidad de probabilidad
    WF = abs(psi(r,phi,theta))**2
    
    # Buscamos superficies de contorno spin UP
    verts_UP, faces_UP,_,_ = measure.marching_cubes_lewiner(WF[0], WF.max()*umbral , allow_degenerate=False  ) if WF[0].max()>0 else (array([]),array([]),0,0)
    
    # Buscamos superficies de contorno spin DOWN
    verts_DW, faces_DW,_,_ = measure.marching_cubes_lewiner(WF[1], WF.max()*umbral , allow_degenerate=False  ) if WF[1].max()>0 else (array([]),array([]),0,0)
    
    # Convertimos indices a coordenadas 
    verts_UP = verts_UP/N*clim*2-clim   if WF[0].max()>0 else array([])
    verts_DW = verts_DW/N*clim*2-clim   if WF[1].max()>0 else array([])
    
    fase_UP, fase_DW = array([]), array([])
    # Obtenemos colores de laa fases
    if WF[0].max()>0:
        x_tri, y_tri, z_tri     = array([  mean([ verts_UP[i] for i in cara ],0) for cara in faces_UP ]).T
        r_tri,phi_tri,theta_tri = sqrt( x_tri**2 + y_tri**2 + z_tri**2 ) , arctan2(y_tri,x_tri)  ,  arctan2( sqrt(x_tri**2+y_tri**2) , z_tri  )
        fase_UP                 = angle( psi(r_tri,phi_tri,theta_tri) )[0]
    if WF[1].max()>0:
        x_tri, y_tri, z_tri     = array([  mean([ verts_DW[i] for i in cara ],0) for cara in faces_DW ]).T
        r_tri,phi_tri,theta_tri = sqrt( x_tri**2 + y_tri**2 + z_tri**2 ) , arctan2(y_tri,x_tri)  ,  arctan2( sqrt(x_tri**2+y_tri**2) , z_tri  )
        fase_DW                 = angle( psi(r_tri,phi_tri,theta_tri) )[1]
    

    id_color = array( fase_UP.tolist() + (fase_DW+2*pi).tolist() )
    
    # apilamos superficies a graficar
    vertices = array(  verts_UP.tolist() + verts_DW.tolist()                          )
    caras    = array(  faces_UP.tolist() + (faces_DW+verts_UP.shape[0]).tolist()      )
    
    # Creamos un colormap con los colores acumulados
    #cmap = mpl.colors.ListedColormap(colores)
    cmap_spin = LinearSegmentedColormap.from_list('fase_spin','darkblue,C0,C0,darkblue,darkred,C1,C1,darkred'.split(','))

    
    # Graficamos la superficie
    sup = ax.plot_trisurf(vertices[:, 0], vertices[:,1], caras, vertices[:, 2],
                          cmap=cmap_spin, 
                          lw=0.5 , alpha=0.5)
    
    # Asignamos los valores de identificación de color a cada triángulo
    sup.set_array( id_color )
    
    # Re-escalamos el colormap para que coincida con los valores asignados
    sup.set_clim(-pi,3*pi)
    
    ax.set_xlabel('x [Å]')
    ax.set_ylabel('y [Å]')
    ax.set_zlabel('z [Å]')

    #sup.set_edgecolor([ f'C{ii}' for ii in id_color ] )

    ax.set_xlim(-5,5)
    ax.set_ylim(-5,5)
    ax.set_zlim(-5,5)
    
    
    ax.set_title('$5^{2}P_{3/2}$ ' + f'm={-3+ii*2}/2'  + '\n' + str(psi) )

