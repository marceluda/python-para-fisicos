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

estados = autoestado_HF('5P3/2',F=1,mf=1,I=3/2) 

#estados = autoestado_HF('5S1/2',F=1,mf=0,I=3/2) 




mis  = [ ee[0] for ee in estados ] 
psis = [ ee[1] for ee in estados ] 


# Creamos la figura y los ejes en 3D
fig = plt.figure(figsize=(14,9) )

ax = fig.add_subplot(1,1,1,projection='3d')  


# Parámetros para mallas
clim   = max([ coordenada_maxima(estado[1],umbral=0.08) for estado in estados ])  # Maxima extensión de ejes
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


# Recorremos los estados
for mi,psi,ii in zip(mis,psis,range(len(mis))):
    print(ii)
    # Calculamos densidad de probabilidad
    WF = abs(psi(r,phi,theta))**2
    
    verts_UP,faces_UP,verts_DW, faces_DW = array([]),array([]), array([]),array([])
    
    # Si tiene componente SPIN UP
    if WF[0].max()>0:
        verts_UP, faces_UP,_,_ = measure.marching_cubes_lewiner(WF[0], WF.max()*umbral , allow_degenerate=False  )
    
    # Si tiene componente SPIN DOWN
    if WF[1].max()>0:
        verts_DW, faces_DW,_,_ = measure.marching_cubes_lewiner(WF[1], WF.max()*umbral , allow_degenerate=False  )
    
    # Convertimos indices a coordenadas 
    verts_UP = verts_UP/N*clim*2-clim   if WF[0].max()>0 else array([])
    verts_DW = verts_DW/N*clim*2-clim   if WF[1].max()>0 else array([])
    
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



# Armamos 4 estados diferentes para graficar

estados = autoestado_HF('5P3/2',F=1,mf=1,I=3/2) 

#estados = autoestado_HF('5S1/2',F=1,mf=0,I=3/2) 


mis_valores = [1.5,0.5,-0.5,-1.5]
mis         = [ ee[0] for ee in estados ] 
psis        = [ ee[1] for ee in estados ] 


# Creamos la figura y los ejes en 3D
fig = plt.figure(figsize=(14,9) )

ax = fig.add_subplot(1,1,1,projection='3d')  


# Parámetros para mallas
clim   = max([ coordenada_maxima(estado[1],umbral=0.08) for estado in estados ])  # Maxima extensión de ejes
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


# Recorremos los estados
for mi,psi,ii in zip(mis,psis,range(len(mis))):
    print(ii)
    # Calculamos densidad de probabilidad
    WF = abs(psi(r,phi,theta))**2
    
    verts_UP,faces_UP,verts_DW, faces_DW = array([]),array([]), array([]),array([])
    
    # Si tiene componente SPIN UP
    if WF[0].max()>0:
        verts_UP, faces_UP,_,_ = measure.marching_cubes_lewiner(WF[0], WF.max()*umbral , allow_degenerate=False  )
    
    # Si tiene componente SPIN DOWN
    if WF[1].max()>0:
        verts_DW, faces_DW,_,_ = measure.marching_cubes_lewiner(WF[1], WF.max()*umbral , allow_degenerate=False  )
    
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


#ax.set_title('Estados:\n' + '\n'.join([ str(p) for p in estados ]) )






#%% Estados Hiperfinos sumando estados

from orbitales_atomicos import autoestado_SO,autoestado_HF


from matplotlib.animation import FuncAnimation


def hf(WF,mi=3/2,I=3/2):    
    mis_valores = arange(I,-I-1,-1)
    return array( [ WF if mi==MI else WF*0  for MI in mis_valores ] )


# Armamos 4 estados diferentes para graficar

estados = autoestado_HF('5P3/2',F=1,mf=1,I=3/2) 

#estados = autoestado_HF('5S1/2',F=1,mf=0,I=3/2) 


mis_valores = [1.5,0.5,-0.5,-1.5]
mis         = [ ee[0] for ee in estados ] 
psis        = [ ee[1] for ee in estados ] 



# Creamos la figura y los ejes en 3D
fig = plt.figure(figsize=(14,9) )

ax = fig.add_subplot(1,1,1,projection='3d')  


# Parámetros para mallas
#clim   = max([ coordenada_maxima(estado[1],umbral=0.08) for estado in estados ])  # Maxima extensión de ejes
clim   = 15
N      = 30                      # la grilla tendrá 50³ puntos
umbral = 0.1                     # umbral para el cálculo de superficies: límite 10% de probabilidad

# Definimos una grilla de coordenadas cartesianas 
# desde -clim hasta +clim con N pts, para cada coordenada
X,Y,Z       = mgrid[-clim:clim:N*1j,-clim:clim:N*1j,-clim:clim:N*1j]

# Transformamos a coordenadas esféricas
r,phi,theta = sqrt( X**2 + Y**2 + Z**2 ) , arctan2(Y,X)  ,  arctan2( sqrt(X**2+Y**2) , Z  )





psi_fun_g      = sum([  hf(ee[1](r,phi,theta),ee[0])   for ee in autoestado_HF('5S1/2',F=1,mf=0,I=3/2)  ],0)
psi_fun_e      = sum([  hf(ee[1](r,phi,theta),ee[0])   for ee in autoestado_HF('5P3/2',F=1,mf=1,I=3/2)  ],0)



WT = linspace(0,pi)

umbral_abs = 8e-5


#%
def update(jj):
    ax.cla()
    print(jj)
    wt = WT[jj]
    
    psi_fun = psi_fun_g*cos(wt) + 1j*psi_fun_e*sin(wt)
    
    # Armamos listas donde vamos a acumular las caras, vértives y colores de las
    # superficies que vamos a calcular
    vertices = []
    caras    = []
    colores  = []
    id_color = []
    last_index = 0
    
    for mi,psi,ii in zip(mis,psi_fun,range(len(mis))):
        #print(ii)
        # Calculamos densidad de probabilidad
        WF = abs(psi)**2
        
        
        
        
        verts_UP,faces_UP,verts_DW, faces_DW = array([]),array([]), array([]),array([])
        
        # Si tiene componente SPIN UP
        try:
            verts_UP, faces_UP,_,_ = measure.marching_cubes_lewiner(WF[0], umbral_abs , allow_degenerate=False  )
            UP=True
        except:
            UP=False
        # Si tiene componente SPIN DOWN
        try:
            verts_DW, faces_DW,_,_ = measure.marching_cubes_lewiner(WF[1], umbral_abs , allow_degenerate=False  )
            DW=True
        except:
            DW=False
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

#%%
anim = FuncAnimation(fig, update, frames=range(len(WT)), interval=300, repeat=True)

anim.save(f'transicion2.gif', dpi=80, writer='imagemagick')

