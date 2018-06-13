# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 11:28:00 2018

@author: lolo
"""

from numpy import *
import matplotlib.pyplot as plt



#%%

# Primero creamos los datos a graficar

xx = linspace(0,4*pi,1e3)
x2 = linspace(0,4*pi,20)

y1 = ( cos(xx*2*pi*3) * 2 + 3 ) * exp(-xx)
y2 = exp(xx*3)*0.5


y3 = cos(xx*2)
y4 = cos(x2*2)+ random.randn( len(x2) )/10


#%% Al estilo Matlab

plt.figure( figsize=(8,5) ) # Dimenciones en pulgadas

plt.subplot(2,2,1)
plt.plot(xx,y1,label='cos')
plt.plot(xx,y2,label='exp')
plt.xlabel('Eje X lineal [unidades]')
plt.ylabel('Eje Y lineal [unidades]')
plt.ylim(-1,6)
plt.title('subplot 1')
plt.grid(b=True)


plt.subplot(2,2,2)
plt.plot(xx,y1,'-',label='cos')
plt.plot(xx,y2,'-.',label='exp')
plt.semilogx()
plt.xlabel('Eje X log [unidades]')
plt.ylabel('Eje Y lineal [unidades]')
plt.grid(b=True,axis='x')
plt.legend(loc='best')


plt.title('subplot 2')
plt.subplot(2,2,3)
plt.plot(xx,y1,'-',label='cos')
plt.plot(xx,y2,'--',label='exp')
plt.semilogy()
plt.xlabel('Eje X lineal [unidades]')
plt.ylabel('Eje Y log [unidades]')
plt.title('subplot 3')
plt.grid(b=True,axis='y')
plt.legend(loc='best')


plt.subplot(2,2,4)
plt.plot(xx,y1,label='cos')
plt.plot(xx,y2,label='exp')
plt.semilogx()
plt.semilogy()
plt.xlabel('Eje X log [unidades]')
plt.ylabel('Eje Y log [unidades]')
plt.title('subplot 4')
plt.grid(b=True,which='major',color='gray')
plt.grid(b=True,which='minor',color='lightgray')

# Este comando es para adaptar los graficos al espacio de la ventana
plt.tight_layout()

# Este comando exporta la figura actual. 
# Se puede guardar en formato de imagen plana (como .png, .jpg, .gif)
# o en formatos vectoriales (como .eps, .pdf o .svg)

plt.savefig('mutil_plot_matlab_style.png')




#%% Al estilo Matplotlib. Nos da mayor margen de acción

plt.figure( figsize=(12,7) ) # Dimenciones en pulgadas


ax1 = plt.subplot2grid((3,4), (0, 0), colspan=3 )
ax2 = plt.subplot2grid((3,4), (1, 0), colspan=3, sharex=ax1)
ax3 = plt.subplot2grid((3,4), (2, 0) )
ax4 = plt.subplot2grid((3,4), (2, 1), colspan=2 )
ax5 = plt.subplot2grid((3,4), (0, 3), rowspan=3 )


ax1.plot(xx,y1,'-')
ax1.grid(b=True,axis='x')
ax1.set_ylabel('Eje Y')
ax1.set_title('ax1')

ax2.plot(xx,y2*y1,'-' ,label='y2*y1')
ax2.plot(xx,y2   ,'-.',label='y2')
ax2.plot(xx,y1   ,'--',label='y1')
ax2.semilogy()
ax2.grid(b=True,axis='x')
ax2.set_xlabel('Eje X')
ax2.set_ylabel('Eje Y')
ax2.set_title('ax2')
ax2.legend(loc='best')


ax3.plot(xx,y1,'-')
ax3.semilogy()
ax3.semilogx()
ax3.grid(b=True,which='major',color='gray')
ax3.grid(b=True,which='minor',color='gray',linestyle=':')
ax3.set_xlabel('Eje X')
ax3.set_ylabel('Eje Y')
ax3.set_title('ax3')


ax4.plot(xx,y3,'-')
ax4.plot(x2,y4,'o')
ax4.set_xlabel('Eje X')
ax4.set_ylabel('Eje Y (sin ticks)')
ax4.set_title('ax4')
ax4.set_yticks([])
ax4.set_xticks( arange(0,max(xx),pi/2) )
ax4.set_xticklabels( [ str(int(y))+r' $\frac{\pi}{2}$' for y in arange(0,max(xx),pi/2)/(pi/2)  ] )
ax4.grid(b=True,which='major',color='gray')


ax5.plot(y1,xx)
ax5.semilogy()
ax5.invert_yaxis()
ax5.set_xlabel('Eje Y')
ax5.set_ylabel('Eje X (invertido + log)',rotation=-90)
ax5.set_title('ax5')

plt.tight_layout()




# Este comando exporta la figura actual. 
# Se puede guardar en formato de imagen plana (como .png, .jpg, .gif)
# o en formatos vectoriales (como .eps, .pdf o .svg)

plt.savefig('mutil_plot_matplotlib_style.png')
