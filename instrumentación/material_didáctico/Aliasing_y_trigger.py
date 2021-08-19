#!/home/lolo/anaconda3/bin/python3
"""
Simulasiones para explicar funcionamiento de osciloscopio
"""

from numpy import *
import matplotlib.pyplot as plt


import matplotlib as mpl

mpl.rcParams['figure.figsize'] = [8.0, 6.0]
mpl.rcParams['figure.dpi'] = 80
mpl.rcParams['savefig.dpi'] = 100

mpl.rcParams['font.size'] = 20
mpl.rcParams['legend.fontsize'] = 'large'
mpl.rcParams['figure.titlesize'] = 'medium'


import os


from matplotlib.animation import FuncAnimation



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Aliasing con animación (sin interactividad)
ii = 0

barrido = [33 , 61 , 80 , 100]

xx = linspace(-0,10,2000)
yy = sin(2*pi*xx)


fig, ax = plt.subplots(1,1, figsize=(15,9))

pp, = ax.plot( xx, yy , linewidth=4 )


ax.set_xlabel('tiempo [s]')
ax.set_ylabel('señal [V]')

fig.tight_layout(h_pad=0.1, w_pad=0.1)
fig.subplots_adjust(hspace=0.05, wspace=0.05)


txt =  ax.text( 0 ,-0.7 , f'Tasa de muestreo: {ii}\nΔT:{ii}',
                horizontalalignment='left', bbox={'facecolor':'white', 'alpha': 0.65, 'edgecolor': None},
                verticalalignment='center',
                fontsize=20 , alpha=1, zorder=250 , color='black' )

x1 = arange(0,10,1.15)
y1 = sin(2*pi*x1 )

p1, = ax.plot( x1, y1  , '.-' , color='C1', markersize=10 , linewidth=2.5  )

ax.set_yticks( [-1,0,1])

ax.set_xticks( x1 , minor=True)
ax.grid(b=True,linestyle='-',color='gray', axis='x', which='minor')


def update(ii):
    step = interp(ii, [0,100] , [1.15,0.1] )
    x1 = arange(0,10, step  )
    y1 = sin(2*pi*x1 )
    ax.set_xticks( x1 , minor=True)
    txt.set_text(f'Tasa de muestreo:  {round(1/step,2)} Hz\nΔT:  {round(step,2)} s')
    
    
    p1.set_xdata( x1 )
    p1.set_ydata( y1 )
    p1.set_markersize( interp(ii, [0,100] , [20,5] )  )
    
fot = ( sin( linspace(0,pi,400) )**2*100 ).astype(int)

update(0)

for ii in barrido:
    update(ii)
    guardar(ii)
    

#%

anim = FuncAnimation(fig, update, frames=fot, interval=25, repeat=True)



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#  Aliasing con gadgets

from matplotlib.widgets import Slider, Button, RadioButtons


ii = 0

xx = linspace(-0,10,2000)
yy = sin(2*pi*xx)


gs_kw = dict(width_ratios=[1], height_ratios=[0.9,0.1])
#fig, axx = plt.subplots(1,4,figsize=(14,7) , gridspec_kw=gs_kw)

fig,axx = plt.subplots(2,1,figsize=(15,9), gridspec_kw=gs_kw )

ax = axx[0]

pp, = ax.plot( xx, yy , linewidth=4 , alpha=0.5 )


ax.set_xlabel('tiempo [ms]')
ax.set_ylabel('señal [V]')

fig.tight_layout(h_pad=0.1, w_pad=0.1)
#fig.subplots_adjust(hspace=0.05, wspace=0.05)


x1 = arange(0,10,1.15)
y1 = sin(2*pi*x1 )

p1, = ax.plot( x1, y1  , '.-' , color='C3', markersize=10 , linewidth=2.5  )

ax.set_yticks( [-1,0,1])

ax.set_xticks( x1 , minor=True)
ax.grid(b=True,linestyle='-',color='gray', axis='x', which='minor')

txt =  ax.text( 0 ,-0.7 , f'Tasa de muestreo: {ii}\nΔT:{ii}',
                horizontalalignment='left', bbox={'facecolor':'white', 'alpha': 0.65, 'edgecolor': None},
                verticalalignment='center',
                fontsize=20 , alpha=1, zorder=250 , color='black' )

def update(ii):
    step = interp(ii, [0,100] , [1.15,0.1] )
    x1 = arange(0,10, step  )
    y1 = sin(2*pi*x1 )
    ax.set_xticks( x1 , minor=True)
    txt.set_text(f'Tasa de muestreo:  {round(1/step,2)} Hz\nΔT:  {round(step,2)} s')
    
    
    p1.set_xdata( x1 )
    p1.set_ydata( y1 )
    p1.set_markersize( interp(ii, [0,100] , [20,5] )  )
    fig.canvas.draw_idle()
    
fot = ( sin( linspace(0,pi,400) )**2*100 ).astype(int)

update(100)

sl = Slider( axx[1] , '' , 0, 100 , valinit=100  , color='C3' )
sl.on_changed(update)


axx[1].set_xticks(      [14.28, 61.9, 90.5, 100])
axx[1].set_xticklabels( ['1 Hz', '2 Hz' , '5 Hz', '10 Hz' ])
axx[1].set_xlabel('Tasa de muestreo [Hz]')


fig.tight_layout(h_pad=0.1, w_pad=0.1)


#   1   -- 14.28
#   0.5 -- 61.9
#   0.2 -- 90.5
















#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Memoria de lectura y Trigger

gs_kw = dict(width_ratios=[1], height_ratios=[0.9,0.1])
fig,axx = plt.subplots(2,1,figsize=(15,9), gridspec_kw=gs_kw, constrained_layout=True, sharex=True )


ax1,ax2 = axx


ax1.set_ylim(-32,32)
ax2.set_xlim(0,30)
ax2.set_xticks( arange(0,31) )
ax2.set_xticklabels( [] )
ax2.set_yticklabels( [] )

for ax in axx:
    ax.grid(b=True,linestyle='-',color='lightgray')


def iterador():
    jj = 0
    while True:
        jj += 1
        
        if jj >1e6:
            break
        yield jj


xx = arange(30)+0.5
yy = zeros(30)

txt = []
for jj in arange(30):
    txt.append( ax.text(jj+0.5, 0.5, '0' , 
                        horizontalalignment='center',verticalalignment='center',
                        fontsize=14 ) )


pos_wr1  = ax1.axvline(5, color='red' , lw=8, alpha=0.2 )
pos_wr2  = ax2.axvline(5, color='red' , lw=8, alpha=0.2 )

pos_tr1  = ax1.axvline(0, color='C2' , lw=8, alpha=0.2 )
pos_tr2  = ax2.axvline(0, color='C2' , lw=8, alpha=0.2 )

for pos_tr in [pos_tr1,pos_tr2]:
    pos_tr.set_visible(False)


trigger = 9

ax1.axhline( trigger , color='C2', lw=2 , alpha=0.5)

pl1, = ax1.plot(xx,yy, 'o-' )



#%
jj = 0

last_y = 0

for x in iterador():
    yy[jj] = round(cos( x/10)*31)
    
    txt[jj].set_text(f'{int(yy[jj])}')
    
    if last_y < trigger and yy[jj]>=trigger:
        pos_tr1.set_xdata([jj+0.5,jj+0.5])
        pos_tr2.set_xdata([jj+0.5,jj+0.5])
    
    last_y = yy[jj]
    
    jj +=1
    jj %= 30
    
    pl1.set_ydata(yy)
    pos_wr1.set_xdata([jj+0.5,jj+0.5])
    pos_wr2.set_xdata([jj+0.5,jj+0.5])
    
    plt.pause(0.1)
    
    



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Memoria de lectura y Trigger que se detiene

gs_kw = dict(width_ratios=[1], height_ratios=[0.9,0.1])
fig,axx = plt.subplots(2,1,figsize=(15,9), gridspec_kw=gs_kw, constrained_layout=True, sharex=True )


ax1,ax2 = axx


ax1.set_ylim(-32,32)
ax2.set_xlim(0,30)
ax2.set_xticks( arange(0,31) )
ax2.set_xticklabels( [] )
ax2.set_yticklabels( [] )

for ax in axx:
    ax.grid(b=True,linestyle='-',color='lightgray')


def iterador():
    jj = 0
    while True:
        jj += 1
        
        if jj >1e6:
            break
        yield jj


xx = arange(30)+0.5
yy = zeros(30)

txt = []
for jj in arange(30):
    txt.append( ax.text(jj+0.5, 0.5, '0' , 
                        horizontalalignment='center',verticalalignment='center',
                        fontsize=14 ) )


pos_wr1  = ax1.axvline(5, color='red' , lw=8, alpha=0.2 )
pos_wr2  = ax2.axvline(5, color='red' , lw=8, alpha=0.2 )

pos_tr1  = ax1.axvline(0, color='C2' , lw=8, alpha=0.2 )
pos_tr2  = ax2.axvline(0, color='C2' , lw=8, alpha=0.2 )




trigger = 9

ax1.axhline( trigger , color='C2', lw=2 , alpha=0.5)

pl1, = ax1.plot(xx,yy, 'o-' )




jj = 0

last_y   = 0
detenete = False
det_cont = 0
for x in iterador():
    yy[jj] = round(-cos( (x-3)/10)*31)
    
    txt[jj].set_text(f'{int(yy[jj])}')
    
    if last_y < trigger and yy[jj]>=trigger:
        for pos_tr in [pos_tr1,pos_tr2]:
            pos_tr.set_visible(True)
            pos_tr.set_xdata([jj+0.5,jj+0.5])
        detenete = True
    
    if detenete:
        det_cont+=1
    
    if det_cont==15:
        break
    
    last_y = yy[jj]
    
    jj +=1
    jj %= 30
    
    pl1.set_ydata(yy)
    pos_wr1.set_xdata([jj+0.5,jj+0.5])
    pos_wr2.set_xdata([jj+0.5,jj+0.5])
    
    plt.pause(0.2)
    
  
for ax in axx:
    ax.axvline(jj, color='black' , lw=3)


