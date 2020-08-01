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


#%% Estados Hiperfinos separando Spin nuclear en colores

from orbitales_atomicos import autoestado_SO,autoestado_HF



# Armamos 4 estados diferentes para graficar

psi = autoestado_HF('5P3/2',F=1,mf=1,I=3/2) 
#estados = autoestado_HF('5S1/2',F=1,mf=0,I=3/2) 


# Creamos la figura y los ejes en 3D
fig = plt.figure(figsize=(14,9) )

ax = fig.add_subplot(1,1,1,projection='3d')  


# Parámetros para mallas
clim   = coordenada_maxima(psi,umbral=0.08)  # Maxima extensión de ejes
N      = 30                      # la grilla tendrá 50³ puntos
umbral = 0.1                     # umbral para el cálculo de superficies: límite 10% de probabilidad

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


# Calculamos densidad de probabilidad
WF = abs(psi(r,phi,theta))**2

# Recorremos los estados
for wf,ii in zip(WF,range(len(WF))):
    print(ii)

    verts_UP,faces_UP,verts_DW, faces_DW = array([]),array([]), array([]),array([])
    
    # Si tiene componente SPIN UP
    if wf[0].max()>0:
        verts_UP, faces_UP,_,_ = measure.marching_cubes_lewiner(wf[0], WF.max()*umbral , allow_degenerate=False  )
    
    # Si tiene componente SPIN DOWN
    if wf[1].max()>0:
        verts_DW, faces_DW,_,_ = measure.marching_cubes_lewiner(wf[1], WF.max()*umbral , allow_degenerate=False  )
    
    # Convertimos indices a coordenadas 
    verts_UP = verts_UP/N*clim*2-clim   if wf[0].max()>0 else array([])
    verts_DW = verts_DW/N*clim*2-clim   if wf[1].max()>0 else array([])
    
    # apilamos superficies a graficar
    verts    = array(  verts_UP.tolist() + verts_DW.tolist()                          )
    faces    = array(  faces_UP.tolist() + (faces_DW+verts_UP.shape[0]).tolist()      )
    color    = [ mpl.colors.to_rgb(f'C{ii}')    , tuple((array(mpl.colors.to_rgb(f'C{ii}'))/2).tolist())     ]
    
    
    # Guardamos los vértices y las caras de los triángulos en las estructuras que definimos
    vertices     += verts.tolist()
    caras        += (faces + last_index).tolist()
    colores      += color
    id_color     += [ii*2]* faces_UP.shape[0] + [ii*2+1]* faces_DW.shape[0]
    last_index   += verts.shape[0]
    

vertices = array(vertices, dtype=float32)
caras    = array(caras   , dtype=int32)
id_color = array(id_color)


# Creamos un colormap con los colores acumulados
cmap = mpl.colors.ListedColormap(colores)


# Graficamos la superficie
sup = ax.plot_trisurf(vertices[:, 0], vertices[:,1], caras, vertices[:, 2],
                      cmap=cmap, 
                      lw=0.5 , alpha=0.2)


# Asignamos los valores de identificación de color a cada triángulo
sup.set_array( id_color )

# Re-escalamos el colormap para que coincida con los valores asignados
sup.autoscale()
sup.set_clim(0,ii*2+1)

# sup.set_edgecolor([ f'C{ii}' for ii in id_color ] )

ax.set_xlim(-5,5)
ax.set_ylim(-5,5)
ax.set_zlim(-5,5)

ax.set_xlabel('x [Å]')
ax.set_ylabel('y [Å]')
ax.set_zlabel('z [Å]')


#ax.set_title('Estados:\n' + '\n'.join([ str(p) for p in estados ]) )



#%% Estados Hiperfinos separando Spin electronico en colores

from orbitales_atomicos import autoestado_SO,autoestado_HF




psi = autoestado_HF('5P3/2',F=1,mf=1,I=3/2) 

# Creamos la figura y los ejes en 3D
fig = plt.figure(figsize=(14,9) )
ax  = fig.add_subplot(1,1,1,projection='3d')  


# Parámetros para mallas
clim   = coordenada_maxima(psi,umbral=0.08)  # Maxima extensión de ejes
N      = 30                      # la grilla tendrá 50³ puntos
umbral = 0.1                     # umbral para el cálculo de superficies: límite 10% de probabilidad

X,Y,Z       = mgrid[-clim:clim:N*1j,-clim:clim:N*1j,-clim:clim:N*1j]
r,phi,theta = sqrt( X**2 + Y**2 + Z**2 ) , arctan2(Y,X)  ,  arctan2( sqrt(X**2+Y**2) , Z  )

# Armamos listas donde vamos a acumular las caras, vértives y colores de las
# superficies que vamos a calcular
vertices = []
caras    = []
colores  = []
id_color = []
last_index = 0

WF = abs(psi(r,phi,theta))**2

# Recorremos los estados
for wf,ii in zip(WF,range(len(WF))):
    print(ii)
    # Calculamos densidad de probabilidad
    
    
    verts_UP,faces_UP,verts_DW, faces_DW = array([]),array([]), array([]),array([])
    
    # Si tiene componente SPIN UP
    if wf[0].max()>0:
        verts_UP, faces_UP,_,_ = measure.marching_cubes_lewiner(wf[0], wf.max()*umbral , allow_degenerate=False  )
    
    # Si tiene componente SPIN DOWN
    if wf[1].max()>0:
        verts_DW, faces_DW,_,_ = measure.marching_cubes_lewiner(wf[1], wf.max()*umbral , allow_degenerate=False  )
    
    # Convertimos indices a coordenadas 
    verts_UP = verts_UP/N*clim*2-clim   if WF[0].max()>0 else array([])
    verts_DW = verts_DW/N*clim*2-clim   if WF[1].max()>0 else array([])
    
    # apilamos superficies a graficar
    verts    = array(  verts_UP.tolist() + verts_DW.tolist()                          )
    faces    = array(  faces_UP.tolist() + (faces_DW+verts_UP.shape[0]).tolist()      )
    
    
    # Guardamos los vértices y las caras de los triángulos en las estructuras que definimos
    vertices     += verts.tolist()
    caras        += (faces + last_index).tolist()
    id_color     += [0]* faces_UP.shape[0] + [1]* faces_DW.shape[0]
    last_index   += verts.shape[0]
    

vertices = array(vertices, dtype=float32)
caras    = array(caras   , dtype=int32)
id_color = array(id_color)


# Creamos un colormap con los colores acumulados
cmap = mpl.colors.ListedColormap([ 'C0'    , 'C1'     ])


# Graficamos la superficie
sup = ax.plot_trisurf(vertices[:, 0], vertices[:,1], caras, vertices[:, 2],
                      cmap=cmap, 
                      lw=0.5 , alpha=0.2)


# Asignamos los valores de identificación de color a cada triángulo
sup.set_array( id_color )

# Re-escalamos el colormap para que coincida con los valores asignados
#sup.autoscale()
sup.set_clim(0,1)

# sup.set_edgecolor([ f'C{ii}' for ii in id_color ] )

ax.set_xlim(-5,5)
ax.set_ylim(-5,5)
ax.set_zlim(-5,5)

ax.set_xlabel('x [Å]')
ax.set_ylabel('y [Å]')
ax.set_zlabel('z [Å]')








#%% Simulación de una transición óptica entre estados hiperfinos

from orbitales_atomicos import autoestado_SO,autoestado_HF

from matplotlib.animation import FuncAnimation


# Creamos la figura y los ejes en 3D
fig = plt.figure(figsize=(14,9) )
ax2 = fig.add_subplot(2,1,2                , position=[0.05,0.05,0.9,0.25])  
ax  = fig.add_subplot(2,1,1,projection='3d', position=[0.05,0.3,0.9,0.7])  


# Parámetros para mallas
clim   = 7
N      = 40                      # la grilla tendrá 50³ puntos
umbral = 0.1                     # umbral para el cálculo de superficies: límite 10% de probabilidad


X,Y,Z       = mgrid[-clim:clim:N*1j,-clim:clim:N*1j,-clim:clim:N*1j]
r,phi,theta = sqrt( X**2 + Y**2 + Z**2 ) , arctan2(Y,X)  ,  arctan2( sqrt(X**2+Y**2) , Z  )


psi_fun_g      = autoestado_HF('5S1/2',F=1,mf=0,I=3/2) 
psi_fun_e      = autoestado_HF('5P3/2',F=1,mf=1,I=3/2)



WT = linspace(0,pi)

umbral_abs = 8e-5 / 2

rabi0, = ax2.plot(WT-pi/2, sin(WT-pi/2)**2 , lw=3 )
rabi1, = ax2.plot(WT[0:1], sin(WT[0:1])**2 , 'o', markersize=10 )

ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
#ax2.spines['bottom'].set_visible(False)
#ax2.spines['left'].set_visible(False)
ax2.set_yticks([])
ax2.set_xticks([])



#%
def update(jj):
    ax.cla()
    print(jj)
    wt = WT[jj]
    
    rabi0.set_ydata( sin(WT-pi/2+wt)**2  )
    rabi1.set_ydata( sin(WT[0:1]+wt)**2  )
    
    
    psi = psi_fun_g*cos(wt) + 1j*psi_fun_e*sin(wt)
    
    # Armamos listas donde vamos a acumular las caras, vértives y colores de las
    # superficies que vamos a calcular
    vertices = []
    caras    = []
    colores  = []
    id_color = []
    last_index = 0
    
    WF = abs(psi(r,phi,theta))**2
    
    for wf,ii in zip(WF,range(len(WF))):

        verts_UP,faces_UP,verts_DW, faces_DW = array([]),array([]), array([]),array([])
        
        # Si tiene componente SPIN UP
        try:
            verts_UP, faces_UP,_,_ = measure.marching_cubes_lewiner(wf[0], umbral_abs , allow_degenerate=False  )
            UP=True
        except:
            UP=False
            #print(ii,'up false')
        # Si tiene componente SPIN DOWN
        try:
            verts_DW, faces_DW,_,_ = measure.marching_cubes_lewiner(wf[1], umbral_abs , allow_degenerate=False  )
            DW=True
        except:
            DW=False
            #print(ii,'dw false')
        # Convertimos indices a coordenadas 
        verts_UP = verts_UP/N*clim*2-clim   if UP else array([])
        verts_DW = verts_DW/N*clim*2-clim   if DW else array([])
        
        # apilamos superficies a graficar
        verts    = array(  verts_UP.tolist() + verts_DW.tolist()                          )
        faces    = array(  faces_UP.tolist() + (faces_DW+verts_UP.shape[0]).tolist()      )
        
        
        # Guardamos los vértices y las caras de los triángulos en las estructuras que definimos
        vertices     += verts.tolist()
        caras        += (faces + last_index).tolist()
        id_color     += [0]* faces_UP.shape[0] + [1]* faces_DW.shape[0]
        last_index   += verts.shape[0]
        
    
    vertices = array(vertices, dtype=float32)
    caras    = array(caras   , dtype=int32)
    id_color = array(id_color)
    
    
    # Creamos un colormap con los colores acumulados
    cmap = mpl.colors.ListedColormap([ 'C0'    , 'C1'     ])
    
    
    # Graficamos la superficie
    sup = ax.plot_trisurf(vertices[:, 0], vertices[:,1], caras, vertices[:, 2],
                          cmap=cmap, 
                          lw=0.5 , alpha=0.2)
    
    
    # Asignamos los valores de identificación de color a cada triángulo
    sup.set_array( id_color )
    
    # Re-escalamos el colormap para que coincida con los valores asignados
    #sup.autoscale()
    sup.set_clim(0,1)

    # sup.set_edgecolor([ f'C{ii}' for ii in id_color ] )
    
    ax.set_xlim(-5,5)
    ax.set_ylim(-5,5)
    ax.set_zlim(-5,5)
    
    ax.set_xlabel('x [Å]')
    ax.set_ylabel('y [Å]')
    ax.set_zlabel('z [Å]')
    
    
    #ax.set_title('Estados:\n' + '\n'.join([ str(p) for p in estados ]) )



update(0)

#%

anim = FuncAnimation(fig, update, frames=range(len(WT)), interval=100, repeat=True)

anim.save(f'transicion3.gif', dpi=80, writer='imagemagick')




#%% Simulación de una transición óptica entre estados hiperfinos
###  Acá sumo las probabilidades de cada componente de proyección de spin nuclear para facilitar visualización


from orbitales_atomicos import autoestado_SO,autoestado_HF

from matplotlib.animation import FuncAnimation


# Creamos la figura y los ejes en 3D
fig = plt.figure(figsize=(14,9) )
ax  = fig.add_subplot(1,1,1,projection='3d')  


# Parámetros para mallas
clim   = 15
N      = 40                      # la grilla tendrá 50³ puntos
umbral = 0.1                     # umbral para el cálculo de superficies: límite 10% de probabilidad


X,Y,Z       = mgrid[-clim:clim:N*1j,-clim:clim:N*1j,-clim:clim:N*1j]
r,phi,theta = sqrt( X**2 + Y**2 + Z**2 ) , arctan2(Y,X)  ,  arctan2( sqrt(X**2+Y**2) , Z  )

psi_fun_g      = autoestado_HF('5S1/2',F=1,mf=0,I=3/2) 
psi_fun_e      = autoestado_HF('5P3/2',F=1,mf=1,I=3/2)

WT = linspace(0,pi)
umbral_abs = 8e-5


def update(jj):
    ax.cla()
    print(jj)
    wt = WT[jj]
    
    psi = psi_fun_g*cos(wt) + 1j*psi_fun_e*sin(wt)
    
    # Armamos listas donde vamos a acumular las caras, vértives y colores de las
    # superficies que vamos a calcular
    vertices = []
    caras    = []
    colores  = []
    id_color = []
    last_index = 0
    
    WF = abs(psi(r,phi,theta))**2
    wf = sum(WF,0)
    
    verts_UP,faces_UP,verts_DW, faces_DW = array([]),array([]), array([]),array([])
    
    # Si tiene componente SPIN UP
    try:
        verts_UP, faces_UP,_,_ = measure.marching_cubes_lewiner(wf[0], umbral_abs , allow_degenerate=False  )
        UP=True
    except:
        UP=False
        #print(ii,'up false')
    # Si tiene componente SPIN DOWN
    try:
        verts_DW, faces_DW,_,_ = measure.marching_cubes_lewiner(wf[1], umbral_abs , allow_degenerate=False  )
        DW=True
    except:
        DW=False
        #print(ii,'dw false')
    # Convertimos indices a coordenadas 
    verts_UP = verts_UP/N*clim*2-clim   if UP else array([])
    verts_DW = verts_DW/N*clim*2-clim   if DW else array([])
    
    # apilamos superficies a graficar
    verts    = array(  verts_UP.tolist() + verts_DW.tolist()                          )
    faces    = array(  faces_UP.tolist() + (faces_DW+verts_UP.shape[0]).tolist()      )
    
    
    # Guardamos los vértices y las caras de los triángulos en las estructuras que definimos
    vertices     += verts.tolist()
    caras        += (faces + last_index).tolist()
    id_color     += [0]* faces_UP.shape[0] + [1]* faces_DW.shape[0]
    last_index   += verts.shape[0]
        
    
    vertices = array(vertices, dtype=float32)
    caras    = array(caras   , dtype=int32)
    id_color = array(id_color)
    
    
    # Creamos un colormap con los colores acumulados
    cmap = mpl.colors.ListedColormap([ 'C0'    , 'C1'     ])
    
    
    # Graficamos la superficie
    sup = ax.plot_trisurf(vertices[:, 0], vertices[:,1], caras, vertices[:, 2],
                          cmap=cmap, 
                          lw=0.5 , alpha=0.2)
    
    
    # Asignamos los valores de identificación de color a cada triángulo
    sup.set_array( id_color )
    
    # Re-escalamos el colormap para que coincida con los valores asignados
    #sup.autoscale()
    sup.set_clim(0,1)

    # sup.set_edgecolor([ f'C{ii}' for ii in id_color ] )
    
    ax.set_xlim(-5,5)
    ax.set_ylim(-5,5)
    ax.set_zlim(-5,5)
    
    ax.set_xlabel('x [Å]')
    ax.set_ylabel('y [Å]')
    ax.set_zlabel('z [Å]')
    
    
    #ax.set_title('Estados:\n' + '\n'.join([ str(p) for p in estados ]) )



update(0)


anim = FuncAnimation(fig, update, frames=range(len(WT)), interval=300, repeat=True)

anim.save(f'transicion4.gif', dpi=80, writer='imagemagick')



