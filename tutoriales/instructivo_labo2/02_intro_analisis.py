#%% linea 36
from numpy import *
import matplotlib.pyplot as plt

# Generador de aleatoriedad
random.seed(1024)

# Preparamos datos simulados
datos = ( random.randn(850)*100-150   ).astype(int).tolist()
datos+= ( random.randn(150)*30 +10   ).astype(int).tolist()
datos = array(datos)
datos = datos[ random.permutation( len(datos) ) ]

x = datos.copy()



#%% linea 53
sum(x)/len(x)
# -126.417

mean(x)
# -126.417



#%% linea 63
plt.plot(                   x , arange(len(x)), '.' , label='datos')
plt.plot( ones(len(x))*mean(x), arange(len(x)), '-' , label='media', linewidth=5 , alpha=0.7)
plt.yticks([])
plt.legend()
plt.xlabel('x')
# plt.savefig('02_01_media.png')



#%% linea 81
varA = sum(  (x - mean(x))**2  )/len(x)
varA = var(x)
# 12250.093111

devA = sqrt(varA)
devA = std(x)
# 110.68013873771572


plt.plot(                   x , arange(len(x)), '.' , label='datos')
plt.plot( ones(len(x))*mean(x), arange(len(x)), '-' , label='media', linewidth=5 , alpha=0.7)
plt.fill_between( [ mean(x)-std(x), mean(x)+std(x) ]  , [0,0] , [len(x)]*2 , label='std', alpha=0.5 , zorder=1)

plt.yticks([])
plt.legend()
plt.xlabel('x')
# plt.savefig('02_02_std.png')



#%% linea 111
plt.subplot(211)
plt.plot(                   x , arange(len(x)), '.' , label='datos')
plt.plot( ones(len(x))*mean(x), arange(len(x)), '-' , label='media', linewidth=5 , alpha=0.7)
plt.fill_between( [ mean(x)-std(x), mean(x)+std(x) ]  , [0,0] , [len(x)]*2 , label='std', alpha=0.5 , zorder=1)

plt.yticks([])
plt.legend()
plt.xlabel('x')
plt.grid(b=True)

plt.subplot(212)
plt.hist(x,30)
plt.ylabel('Conteo')
plt.xlabel('valores x')
plt.grid(b=True)

plt.tight_layout()
# plt.savefig('02_03_hist.png')



#%% linea 140
x1 = random.randn(100)*10
y1 = (random.rand(100)-0.5)*10+8

plt.subplot(2,2,1)
plt.plot(x1,y1,'.')
plt.ylabel('y1')
plt.xlabel('x1')

plt.subplot(2,2,2)
plt.plot(x1,'.', label='x1')
plt.plot(y1,'.', label='y1')
plt.ylabel('valor')
plt.xlabel('posicion')
plt.legend()


plt.subplot(2,2,3)
plt.hist(x1,20)
plt.yticks([])
plt.xlabel('x1')

plt.subplot(2,2,4)
plt.hist(y,20)
plt.yticks([])
plt.xlabel('y1')

plt.tight_layout()
# plt.savefig('02_04_cov.png')



#%% linea 176
random.seed(1024)
t = linspace(0,5*pi,100)
x2 = (sin(t)+1)+t/2 + random.randn(100)/2
y2 = ((sin(t)+1)+t/2)*2.1+3 + random.randn(100)/2

plt.subplot(2,2,1)
plt.plot(x2,y2,'.')
plt.ylabel('y2')
plt.xlabel('x2')

plt.subplot(2,2,2)
plt.plot(x2,'.', label='x2')
plt.plot(y2,'.', label='y2')
plt.ylabel('valor')
plt.xlabel('posicion')
plt.legend()


plt.subplot(2,2,3)
plt.hist(x2,20)
plt.yticks([])
plt.xlabel('x2')

plt.subplot(2,2,4)
plt.hist(y2,20)
plt.yticks([])
plt.xlabel('y2')

plt.tight_layout()
# plt.savefig('02_05_cov.png')



#%% linea 220
cov_xy2 = sum( ( x2-mean(x2) )*( y2-mean(y2) )  ) / ( len(x2)-1 )
# 11.986200769263622

cov(x2,y2)

# array([[  6.01124359,  11.98620077],
#        [ 11.98620077,  25.33765995]])

cov_xy2 = cov(x2,y2)[0,1]
# 11.986200769263622

cov_xy1 = cov(x1,y1)[0,1]
# 8.823807524442465



#%% linea 247
corrcoef(x1,y1)
# array([[ 1.        ,  0.29015905],
#        [ 0.29015905,  1.        ]])

corrcoef(x2,y2)
# array([[ 1.        ,  0.97121668],
#        [ 0.97121668,  1.        ]])

cor1 = cov_xy1/( std(x1,ddof=1) * std(y1,ddof=1) )
cor1 = corrcoef(x1,y1)[0,1]
# 0.29015904574546342

cor2 = cov_xy2/( std(x2,ddof=1) * std(y2,ddof=1) )
cor2 = corrcoef(x2,y2)[0,1]
# 0.97121668087762869



#%% linea 334
#%%  Ejemplo de ajuste lineal simple

param = polyfit(x2,y2,1)

print('A*x+B')
print('A:',param[0] , '   B:',param[1])

# A*x+B
# A: 1.99396357831    B: 3.39185944525

mod = polyval(param,x2)

#plt.plot(x2, y2   ,'.', label='datos')
plt.errorbar(x2, y2, yerr=0.5, fmt='.', label='datos')
plt.plot(x2, mod  ,'-', label='modelo')

plt.xlabel('x2')
plt.ylabel('y2')
plt.legend()
plt.grid(b=True)

plt.tight_layout()
# plt.savefig('02_07_ajuste_lineal.png')

chi2 = sum( (y2 - mod)**2 )
# 142.3236051732523
R    = corrcoef(x2,y2)[0,1]
# 0.97121668087762869

R2   = R**2
# 0.9432618412149576



#%% linea 372
# Ejemplo de ajuste lineal simple

from scipy.optimize import curve_fit

def modelo(x, A, B):
    return x*A+B

# Parámetros iniciales con los que vamos a iniciar el proceso de fiteo
parametros_iniciales=[1,0]

# Hacemos el ajuste con curve_fit
popt, pcov = curve_fit(modelo, x2, y2, p0=parametros_iniciales)

# curve_fit devuelve dos resultados. El primero (popt) son los
# parámetros óptimos hallados. El segundo (pcov) es la matriz de
# covarianza de los parámetros hallados.

x_modelo  = linspace(0, 10, 1000)

plt.figure()
plt.plot( x2,                 y2,  'o', label='datos')
plt.plot(x_modelo, modelo(x_modelo, *popt), 'r-', label='modelo ajustado')
plt.legend(loc='best')
plt.xlabel('x2')
plt.ylabel('y2')

plt.tight_layout()
# plt.savefig('02_08_ajuste_lineal.png')


print(popt)
# [ 1.99396358  3.39185943]

# De la matris de covarinza podemos obtener los valores de desviacion estandar
# de los parametros hallados
pstd = sqrt(diag(pcov))

nombres_de_param=['A','B']
print('Parámetros hallados:')
for i,param in enumerate(popt):
    print('{:s} = {:5.3f} ± {:5.3f}'.format( nombres_de_param[i] , param , pstd[i]) )
#
# Parámetros hallados:
#
# A = 1.994 ± 0.049
# B = 3.392 ± 0.280

# plt.savefig('02_08_ajuste_lineal.png')
