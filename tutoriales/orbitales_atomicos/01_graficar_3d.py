#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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


# Funcion para hallar la máxima extensión en r de un estado
def coordenada_maxima(psi):
    """
    Función para hallar la máxima extensión en r de un estado, cortando al 1% del máximo.
    """
    
    # Buscamos el estado de mayor extensión en r
    if type(psi) == Ψ:
        Ψmax = psi
    else:
        Ψmax = [ pp for pp in sorted(psi.psi_vec, key=lambda x: x.n*100 + x.l ) ][-1]
    maxima_raiz = (Ψmax.n+Ψmax.l + (Ψmax.n-Ψmax.l-2)* sqrt(Ψmax.n+Ψmax.l))*Ψmax.n*0.5/2
    
    # Obtenemos el valor en que se vuelve menos al 1% del máximo
    x0          = linspace(0,maxima_raiz*10,10000)
    y0          = Ψmax.R(x0)**2 / (Ψmax.R(x0).max()**2)
    r_max_001   = x0[nonzero(y0>0.01)[0][-1]]
    
    return    r_max_001*1.1



graficar_curvas_de_nivel = True

#%% Graficar un esatdo en 3D y en su corte transversal en 3 planos

# Primero definimos el estado a graficar

psi = Ψ(5,2,1) - Ψ(5,2,-1)/1j



# Creamos 4 conjuntos de ejes... el primero que sea 3D
fig, axx = plt.subplots(2,2, figsize=(14,9) )
axx[0,0].remove()
axx[0,0]=fig.add_subplot(2,2,1,projection='3d')


    
# Parámetros para mallas
clim   = coordenada_maxima(psi)  # Maxima extensión de ejes
N      = 50                      # la grilla tendrá 50³ puntos
umbral = 0.1                     # umbral para el cálculo de superficies: límite 10% de probabilidad


# Selecciono Eje 3D
ax = axx[0,0] #################################################################

# Definimos una grilla de coordenadas cartesianas 
# desde -clim hasta +clim con N pts, para cada coordenada
X,Y,Z       = mgrid[-clim:clim:N*1j,-clim:clim:N*1j,-clim:clim:N*1j]

# Transformamos a coordenadas esféricas
r,phi,theta = sqrt( X**2 + Y**2 + Z**2 ) , arctan2(Y,X)  ,  arctan2( sqrt(X**2+Y**2) , Z  )

# Calculamos la probabilidad, como el módulo de la función de ona al cuadrado
WF = abs(psi(r,phi,theta))**2

# Buscamos superficies de contorno. 
# Son superficies que encierran el volumen en el que la probabilidad es mayor a umbral*MaximaProbabilidad
vertices, caras,_,_ = measure.marching_cubes_lewiner(WF, WF.max()*umbral , allow_degenerate=False  )

# La función devuelde los índices de vértices de la grilla y las caras de los triángulos
# las caras de los triángulos son tripletes de índices que indican cuales vértices de "vertices" conforman el triángulo


# Convertimos los índices de los vértices hallados en las coordenadas cartecianas correspondientes
vertices = vertices/N*clim*2-clim

# graficamos la superfice como conjuntos de triangulos en 3D
sup = ax.plot_trisurf(vertices[:, 0], vertices[:,1], caras, vertices[:, 2],
                      cmap=cmap_fase, 
                      lw=1 , alpha=0.5)

# Para colorear la fase, buscamos la posición media de cada triángulo obteniso
x_tri, y_tri, z_tri = array([  mean([ vertices[i] for i in cara ],0) for cara in caras ]).T

# Pasamos esas posiciones a polares
r_tri,phi_tri,theta_tri = sqrt( x_tri**2 + y_tri**2 + z_tri**2 ) , arctan2(y_tri,x_tri)  ,  arctan2( sqrt(x_tri**2+y_tri**2) , z_tri  )

# Y obtenemos la fase de complejos para la función de onda en esos puntos
fase = angle( psi(r_tri,phi_tri,theta_tri) )

# Asignamos el valor de fase a la superficie graficada
sup.set_array( fase )

# Establecemos los límites de la escala de color
sup.set_clim( -pi , pi )


ax.set_xlabel('x [Å]')
ax.set_ylabel('y [Å]')
ax.set_zlabel('z [Å]')



# Cortes en planos transversales 
ax = axx[0,1] #  Plano XY ################################################################

# Definimos coordenadas y las pasamos a esféricas. La coordenada Z está fijada en 0
X,Y,Z       = mgrid[-clim:clim:N*1j,-clim:clim:N*1j,0:1]
r,phi,theta = sqrt( X**2 + Y**2 + Z**2 ) , arctan2(Y,X)  ,  arctan2( sqrt(X**2+Y**2) , Z  )

# Calculamos la probabilidad
WF         = abs(  psi(r,phi,theta))**2    # Probabilidad
fase       = angle(psi(r,phi,theta))       # Fase
xx, yy, zz = X[:,0,0], Y[0,:,0], Z[0,0,:]  # Ejes de coordenadas


# Calculamos imagen coloreada en función de la fase del estado
img        =  cmap_fase(  mpl.colors.Normalize(vmin=-pi,vmax=pi)( fase[:,:,0].T ) )

# En la capa 3 (transparencial de los pixels), modulamos la transparencia con la amplitud de probabilidad
img[:,:,3] = mpl.colors.Normalize(vmin=WF.min(),vmax=WF.max())( WF[:,:,0].T )

# graficamos
ax.imshow( img ,  interpolation='bilinear', origin='lower' , aspect='auto', 
          extent=(xx.min(),xx.max(),yy.min(),yy.max())
          )

if graficar_curvas_de_nivel:
    niveles = linspace(0,WF.max(),8)[:-1]
    CS = ax.contour(WF[:,:,0].T , niveles , origin='lower',
                                  linewidths=1, colors='gray', alpha=0.5,
                                  extent=(xx.min(),xx.max(),yy.min(),yy.max()) )
    
    # ax.clabel(CS, inline=1, fmt={ l: f'{int(l/WF.max()*100)}' for l in niveles }, fontsize=10)

ax.set_xlabel('x [Å]')
ax.set_ylabel('y [Å]')


ax = axx[1,0] #  Plano YZ ################################################################

X,Y,Z       = mgrid[0:1,-clim:clim:N*1j,-clim:clim:N*1j]
r,phi,theta = sqrt( X**2 + Y**2 + Z**2 ) , arctan2(Y,X)  ,  arctan2( sqrt(X**2+Y**2) , Z  )

WF         = abs(  psi(r,phi,theta))**2
fase       = angle(psi(r,phi,theta))
xx, yy, zz = X[:,0,0], Y[0,:,0], Z[0,0,:]

img        =  cmap_fase(  mpl.colors.Normalize(vmin=-pi,vmax=pi)( fase[0,:,:].T ) )
img[:,:,3] = mpl.colors.Normalize(vmin=WF.min(),vmax=WF.max())( WF[0,:,:].T )

ax.imshow( img ,  interpolation='bilinear', origin='lower' , aspect='auto', 
          extent=(yy.min(),yy.max(),zz.min(),zz.max())
          )
if graficar_curvas_de_nivel:
    niveles = linspace(0,WF.max(),8)[:-1]
    CS = ax.contour(WF[0,:,:].T , niveles , origin='lower',
                                  linewidths=1, colors='gray', alpha=0.5,
                                  extent=(yy.min(),yy.max(),zz.min(),zz.max()) )
    
    # ax.clabel(CS, inline=1, fmt={ l: f'{int(l/WF.max()*100)}' for l in niveles }, fontsize=10)

ax.set_xlabel('y [Å]')
ax.set_ylabel('z [Å]')


ax = axx[1,1] #  Plano XZ ################################################################

X,Y,Z       = mgrid[-clim:clim:N*1j,0:1,-clim:clim:N*1j]
r,phi,theta = sqrt( X**2 + Y**2 + Z**2 ) , arctan2(Y,X)  ,  arctan2( sqrt(X**2+Y**2) , Z  )

WF         = abs(  psi(r,phi,theta))**2
fase       = angle(psi(r,phi,theta))
xx, yy, zz = X[:,0,0], Y[0,:,0], Z[0,0,:]

img        =  cmap_fase(  mpl.colors.Normalize(vmin=-pi,vmax=pi)( fase[:,0,:].T ) )
img[:,:,3] =  mpl.colors.Normalize(vmin=WF.min(),vmax=WF.max())( WF[:,0,:].T )

ax.imshow( img ,  interpolation='bilinear', origin='lower' , aspect='auto', 
          extent=(xx.min(),xx.max(),zz.min(),zz.max())
          )

if graficar_curvas_de_nivel:
    niveles = linspace(0,WF.max(),8)[:-1]
    CS = ax.contour(WF[:,0,:].T , niveles , origin='lower',
                                  linewidths=1, colors='gray', alpha=0.5,
                                  extent=(xx.min(),xx.max(),zz.min(),zz.max()) )
    
    # ax.clabel(CS, inline=1, fmt={ l: f'{int(l/WF.max()*100)}' for l in niveles }, fontsize=10)

ax.set_xlabel('x [Å]')
ax.set_ylabel('z [Å]')


# Definiciones finales de formato #############################################

# Lineas de los zeros de los ejes
for ax in axx.flatten()[1:]:
    ax.axvline(0, color='red', lw=0.5 , ls='--' )
    ax.axhline(0, color='red', lw=0.5 , ls='--' )

# Configurar ejes compartidos para facilitar el zoom en la inspección de datos
axx[0,1].get_shared_x_axes().join(axx[0,1], axx[1,1])
axx[1,0].get_shared_y_axes().join(axx[1,0], axx[1,1])

# Correr ticks y etiquetas de ejes a el lugar más comodo
axx[0,1].xaxis.tick_top()
axx[0,1].xaxis.set_label_position('top') 
axx[0,1].yaxis.tick_right()
axx[0,1].yaxis.set_label_position('right')
axx[1,1].yaxis.tick_right()
axx[1,1].yaxis.set_label_position('right')


fig.subplots_adjust(hspace=0.5, wspace=0.5)
fig.tight_layout(h_pad=0.5, w_pad=0.5)





#%% Veriosn Plot.ly 3D

import plotly.io as pio
pio.renderers.default='browser'

import plotly.graph_objects as go
from plotly.tools import FigureFactory as FF


psi = Ψ(5,2,1) - Ψ(5,2,-1)/1j

    
# Parámetros para mallas
clim   = coordenada_maxima(psi)  # Maxima extensión de ejes
N      = 50                      # la grilla tendrá 50³ puntos
umbral = 0.1                     # umbral para el cálculo de superficies: límite 10% de probabilidad


# Selecciono Eje 3D
ax = axx[0,0] #################################################################

# Definimos una grilla de coordenadas cartesianas 
# desde -clim hasta +clim con N pts, para cada coordenada
X,Y,Z       = mgrid[-clim:clim:N*1j,-clim:clim:N*1j,-clim:clim:N*1j]

# Transformamos a coordenadas esféricas
r,phi,theta = sqrt( X**2 + Y**2 + Z**2 ) , arctan2(Y,X)  ,  arctan2( sqrt(X**2+Y**2) , Z  )

# Calculamos la probabilidad, como el módulo de la función de ona al cuadrado
WF = abs(psi(r,phi,theta))**2




# Buscamos superficies de contorno. 
# Son superficies que encierran el volumen en el que la probabilidad es mayor a umbral*MaximaProbabilidad
vertices, caras,_,_ = measure.marching_cubes_lewiner(WF, WF.max()*umbral , allow_degenerate=False  )

# La función devuelde los índices de vértices de la grilla y las caras de los triángulos
# las caras de los triángulos son tripletes de índices que indican cuales vértices de "vertices" conforman el triángulo


# Convertimos los índices de los vértices hallados en las coordenadas cartecianas correspondientes
vertices = vertices/N*clim*2-clim

# Para colorear la fase, buscamos la posición media de cada triángulo obteniso
x_tri, y_tri, z_tri = array([  mean([ vertices[i] for i in cara ],0) for cara in caras ]).T

# Pasamos esas posiciones a polares
r_tri,phi_tri,theta_tri = sqrt( x_tri**2 + y_tri**2 + z_tri**2 ) , arctan2(y_tri,x_tri)  ,  arctan2( sqrt(x_tri**2+y_tri**2) , z_tri  )

# Y obtenemos la fase de complejos para la función de onda en esos puntos
fase = angle( psi(r_tri,phi_tri,theta_tri) )



x,y,z = zip(*vertices)  

colores =  cmap_fase(  mpl.colors.Normalize(vmin=-pi,vmax=pi)( fase ) )

colormap=['rgb(255,105,180)','rgb(255,255,51)','rgb(0,191,255)']
fig = FF.create_trisurf(x=x,
                        y=y, 
                        z=z, 
                        plot_edges  = False,
                        colormap    = colormap,
                        simplices   = caras,
                        color_func  = [ f'rgb({int(c[0]*255)}, {int(c[1]*255)}, {int(c[2]*255)})' for c in colores.tolist() ],
                        title       =repr(psi))

fig['data'][0].update(opacity=0.5)
for eje in 'x y z'.split():
    fig['layout']['scene'][f'{eje}axis']['title']=f'{eje} [Å]'

fig.show()

# fig.write_json('orbitales_02_3D.json')

