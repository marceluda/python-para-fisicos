# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 10:44:31 2018

@author: lolo
"""

from numpy import *
import matplotlib.pyplot as plt


#%% Funciones útiles


def smooth(x, window_len=11, window='hanning'):
    s=r_[2*x[0]-array(x[window_len:1:-1]), x, 2*x[-1]-array(x[-1:-window_len:-1])]
    w = ones(window_len,'d')
    y = convolve(w/w.sum(), s, mode='same')
    return y[window_len-1:-window_len+1]

def findpeaks(x,minh=0,mind=1):
    nn=len(x)
    z=nonzero(
        logical_and(
            logical_and( 
                diff(x)[0:nn-2]*diff(x)[1:nn-1]<=0 ,
                diff(x)[0:nn-2]>0
                ),
            x[0:nn-2]>minh
            )
        )[0]+1
    z=z.tolist()
    while(len(nonzero(diff(z)<mind)[0])>0):
        z.pop( nonzero(diff(z)<mind)[0][0]+1 )
    return z

