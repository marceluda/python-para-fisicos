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
from orbitales_atomicos import coordenada_maxima




#%% Armado automático de galería de estados

# Primero definimos el estado a graficar

psi = Ψ(4,3,1)

ii = 0
for n in range(1,6):
    ii = 0
    for l in arange(0,n):
        print(repr(Ψ(n,l,0)),2*l+1 , l , 4*l+1 )
        ii+= 4*l+1
    print(f'{ii}\n')






template0 = """
<script type="text/javascript">
  window.PLOTLYENV=window.PLOTLYENV || {};

  if (document.getElementById("LOLO_ID")) {
      Plotly.d3.json( "LOLO_JSON", function(err, fig) {
        Plotly.plot("LOLO_ID", fig.data, fig.layout);
      });
  };  
</script>
"""



template = """
<div id="LOLO_ID" class="plotly-graph-div" style="height:800px; width:800px;"></div>
"""

template_boton="""
<a href='javascript:Plotly.purge("LOLO_ID");Plotly.d3.json( "LOLO_JSON", function(err, fig) { Plotly.plot("LOLO_ID", fig.data, fig.layout); });' class="btn btn-primary btn-lg" role="button">
LOLO_NOMBRE
</a>
""".strip()

#%%


import plotly.io as pio
pio.renderers.default='browser'

import plotly.graph_objects as go
from plotly.tools import FigureFactory as FF




sub_fig_layout = {1:(1,1),2:(2,3),3:(3,5),4:(5,6),5:(5,9)}


N      = 50                      # la grilla tendrá 50³ puntos
umbral = 0.1                     # umbral para el cálculo de superficies: límite 10% de probabilidad



for n in range(1,6):
    print('\n'*5)
    print(f'## Figuras estados n={n}\n')
          
    print(f'\n![grafico](orb_gal_0{n}.png "grafico")\n')
    
    print(template.replace('LOLO_ID',f'orb_plot_{n}'))
    
    print('<p>')
    
    
    if n<6:
        fig = plt.figure( figsize=(14,9) )
        ax = []
        snx,sny = sub_fig_layout[n]
        for ii in range(sum([ 4*l+1 for l in range(0,n) ])):
            ax +=  [  fig.add_subplot(snx,sny,ii+1,projection='3d')   ]
    
    li=0
    for l in arange(0,n):
        for m in arange(-l,l+1):
            for k in arange( 3 if m>0 else 1 ):
                

                if k==0:
                    psi = Ψ(n,l,m)
                    #pmax = psi.R(clim)**2*clim**2
                elif k==1:
                    psi = ( Ψ(n,l,m) - Ψ(n,l,-m) )/sqrt(2)
                    #pmax = psi.psi_vec[0].R(clim)**2*clim**2
                else:
                    psi = ( Ψ(n,l,m) + Ψ(n,l,-m) )/sqrt(2)/1j
                    #pmax = psi.psi_vec[0].R(clim)**2*clim**2
                
                
                clim   = coordenada_maxima(psi,umbral=umbral )*1.3  # Maxima extensión de ejes
                
                
                # Grilla para el calculo
                X,Y,Z       = mgrid[-clim:clim:N*1j,-clim:clim:N*1j,-clim:clim:N*1j]
                r,phi,theta = sqrt( X**2 + Y**2 + Z**2 ) , arctan2(Y,X)  ,  arctan2( sqrt(X**2+Y**2) , Z  )
                WF          = abs(psi(r,phi,theta))**2
                
                # Vertices
                vertices, caras,_,_ = measure.marching_cubes_lewiner(WF, WF.max()*umbral , allow_degenerate=False  )
                vertices            = vertices/N*clim*2-clim
                
                # graficar
                if n<6:
                    sup                 = ax[li].plot_trisurf(vertices[:, 0], vertices[:,1], caras, vertices[:, 2],
                                                  cmap=cmap_fase, 
                                                  lw=1 , alpha=0.5)
                
                # Calcular fase de los triangulos
                x_tri, y_tri, z_tri     = array([  mean([ vertices[i] for i in cara ],0) for cara in caras ]).T
                r_tri,phi_tri,theta_tri = sqrt( x_tri**2 + y_tri**2 + z_tri**2 ) , arctan2(y_tri,x_tri)  ,  arctan2( sqrt(x_tri**2+y_tri**2) , z_tri  )
                fase                    = angle( psi(r_tri,phi_tri,theta_tri) )
                
                
                
                if k==0:
                    titulo = repr(psi) + ( ' [pz]' if m==0 else ''  )
                else:
                    titulo = f'Ψ({n},{l},±{m})' + f' [{"py" if k==1 else "px"}]' 
                
                # colorear
                if n<6:
                    sup.set_array( fase )
                    sup.set_clim( -pi , pi )
                    
                    
                    ax[li].set_xlabel('x [Å]')
                    ax[li].set_ylabel('y [Å]')
                    ax[li].set_zlabel('z [Å]')
                    
                    ax[li].set_xlim(-clim,clim)
                    ax[li].set_ylim(-clim,clim)
                    ax[li].set_zlim(-clim,clim)
                    
                    ax[li].set_title(titulo, fontsize=10)
                
                
                # Guardo version plotly
                
                x,y,z = zip(*vertices)  
                
                colores =  cmap_fase(  mpl.colors.Normalize(vmin=-pi,vmax=pi)( fase ) )
                
                fig = FF.create_trisurf(x=x,
                                        y=y, 
                                        z=z, 
                                        plot_edges  = False,
                                        simplices   = caras,
                                        color_func  = [ f'rgb({int(c[0]*255)}, {int(c[1]*255)}, {int(c[2]*255)})' for c in colores.tolist() ],
                                        title       = repr(psi)    )
                
                fig['data'][0].update(opacity=0.5)
                for eje in 'x y z'.split():
                    fig['layout']['scene'][f'{eje}axis']['title']=f'{eje} [Å]'
                    fig['layout']['scene'][f'{eje}axis']['range']=[-clim,clim]
                
                
                fig.write_json(f'orbitales_06_{n}{l}{30+m}{k}.json')
                
                
                if li==0:
                    print(template0.replace('LOLO_ID',f'orb_plot_{n}').replace('LOLO_JSON',f'orbitales_06_{n}{l}{30+m}{k}.json')  )
                
                #print('### Estado: ' + repr(psi) )
                #print('\n')
                print(template_boton.replace('LOLO_ID',f'orb_plot_{n}').replace('LOLO_JSON',f'orbitales_06_{n}{l}{30+m}{k}.json').replace('LOLO_NOMBRE',repr(psi).replace('WaveFunction:','').strip())   )
                
                #print('\n'*3)
                
                li+=1
    print('</p>')




print(f'\n![grafico](referencia_colores.png "grafico")\n')

