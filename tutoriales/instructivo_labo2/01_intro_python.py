#%% linea 75
a = 11
b = 2
print(a+b)
# imprime: 13
print(a*b)
# imprime: 22
print(b**a)
# imprime 2 elevado a la 11, osea: 2048
a = a + 5
print(a)
# Se reemplaza el valor de a por el de "a+5". Al imprimir a se ve: 16



#%% linea 118
numero_entero  =  3    # Ejemplo de número entero
num1           =  3.8  # Ejemplo de número real
num2           = -2.0  # Otro número real
num3           = 5.2e9 # Otro número real: 5.2 x 10^9
texto          = 'esto es un texto'
lista          = [1,2,3,4,5,6]  # Esto es una lista... un conjunto
                                # ordenado de valores, en este caso
                                # de tipo int



#%% linea 133
lista   = [-20,50,3,-91,8]
max_val = max(lista)
print('De la lista:', lista )
print('El valor máximo es:', max_val)



#%% linea 147
import numpy

vector_a = numpy.array( [ 1.2, 3.4, -1.0] )
vector_b = numpy.array( [10.0,   0,  2.0] )
print('vector_a:',vector_a)
print('vector_b:',vector_b)
print('vector_a*vector_b:',  vector_a*vector_b  )



#%% linea 159
import numpy as np

a = np.array( [ 1.2, 3.4, -1.0] )
b = np.array( [10.0,   0,  2.0] )
print('a:',a)
print('b:',b)
print('a*b:',  a*b  )



#%% linea 170
from numpy import array,sin,cos,pi

a = array( [ 0 , pi/2 , pi] )
b = cos( a )
c = sin( a )

print('a:', a )
print('b:', b )
print('c:', c )



#%% linea 189
from numpy import *

a = array( [ 0 , pi/2 , pi] )
b = cos( a )
c = sin( a )



#%% linea 243
from numpy import *

a = array( [ 1 , 0 , 1] )
b = array( [ 2 , 1 , 3] )
c = array( [[ -1 , 2 , 0]] ).T

A = array( [[1,1,1],[2,2,2],[3,3,3]] )
A = array([[1, 1, 1],
           [2, 2, 2],
           [3, 3, 3]])



#%% linea 303
a*b

a*c

a+b

a/b

A**2

b**b



#%% linea 358
a.dot(b)

a.dot(c)

cross(a,b)

a.dot(A)

A.dot(c)

c.T.dot(A**2).dot(c)



#%% linea 382
n = arange(10)   # Lista de los primeros 10 enteros
# array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

n = arange(10)   # Lista de los primeros 10 enteros
# array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

n2 = n**2 - 9    # realizamos cálculo con esos enteros
# array([-9, -8, -5,  0,  7, 16, 27, 40, 55, 72])

x = linspace(0,2*pi,9)   # Generamos 9 numeros entre 0 y pi para el array x
# array([ 0.        ,  0.78539816,  1.57079633,  2.35619449,  3.14159265,
#         3.92699082,  4.71238898,  5.49778714,  6.28318531])

y = 3*sin(x)             # Calculamos el seno de x por 3
y.round(5)               # Con esto nos devuelve los numeros redondeados al decimal 5
# array([ 0.     ,  2.12132,  3.     ,  2.12132,  0.     , -2.12132,
#        -3.     , -2.12132, -0.     ])

sin(x**2)/x              # Ojo con dividir por cero!
# __main__:1: RuntimeWarning: invalid value encountered in true_divide
# array([        nan,  0.73652934,  0.39742005, -0.28351271, -0.13696913,
#         0.07201305, -0.04536937, -0.16888007,  0.15570773])



#%% linea 415
from numpy import *
import matplotlib.pyplot as plt

# cargamos una tira de datos de ejemplo
# Dolar en argentina durante 2018, día por día
dolar = [18.4, 18.45, 18.65, 18.85, 18.85, 18.85, 19.05, 18.95, 18.6, 18.7, 18.7, 18.7,
        18.7, 18.75, 18.9, 18.85, 18.85, 19.0, 19.0, 19.0, 19.1, 19.35, 19.65, 19.55,
        19.55, 19.55, 19.55, 19.55, 19.6, 19.65, 19.4, 19.5, 19.5, 19.5, 19.5, 19.6,
        19.65, 19.95, 20.0, 20.0, 20.0, 20.0, 20.0, 19.9, 19.7, 19.75, 19.75, 19.75,
        19.9, 19.85, 19.9, 19.95, 19.95, 19.95, 19.95, 20.2, 20.2, 20.1, 20.15, 20.25,
        20.25, 20.25, 20.2, 20.35, 20.4, 20.4, 20.25, 20.25, 20.25, 20.2, 20.2, 20.2,
        20.35, 20.2, 20.2, 20.2, 20.2, 20.25, 20.3, 20.25, 20.2, 20.2, 20.2, 20.2,
        20.2, 20.15, 20.15, 20.15, 20.15, 20.15, 20.15, 20.15, 20.2, 20.2, 20.2, 20.2,
        20.2, 20.2, 20.2, 20.15, 20.2, 20.2, 20.2, 20.2, 20.2, 20.2, 20.2, 20.15, 20.2,
        20.2, 20.2, 20.25, 20.25, 20.25, 20.55, 20.55, 20.55, 20.55, 20.55, 20.55,
        21.2, 23.0, 21.8, 21.8, 21.8, 21.9, 22.4, 22.7, 22.7, 23.2, 23.2, 23.2, 24.8,
        24.0, 24.3, 24.3, 24.4, 24.4, 24.4, 24.4, 24.3, 24.4, 24.6, 24.6, 24.6, 24.6,
        24.7, 24.9, 24.9, 24.9, 24.9, 24.9, 24.9, 24.9, 24.9, 24.9, 24.9, 25.3, 25.3,
        25.3, 26.0, 25.8, 26.0, 27.7, 28.3, 28.3, 28.3, 27.6, 27.7, 27.7, 27.5, 27.0,
        27.0, 27.0, 27.0, 27.1, 27.4, 28.1, 28.9, 28.9, 28.9, 28.3, 27.8, 28.1, 28.0,
        27.9, 27.9, 27.9, 27.9, 27.3, 27.4, 27.2, 27.2, 27.2, 27.2, 27.3, 27.5, 27.6,
        27.7, 27.6, 27.6, 27.6, 27.6, 27.5, 27.4, 27.4, 27.4, 27.4, 27.4, 27.3, 27.4,
        27.5, 27.5, 27.3, 27.3, 27.3, 27.4, 27.4, 27.6, 28.1, 29.2, 29.2, 29.2, 30.0,
        29.6, 30.0, 29.8, 29.8, 29.8, 29.8, 29.8, 30.0, 30.2, 30.5, 30.9, 30.9, 30.9,
        30.9, 31.4, 34.0, 37.6, 36.8, 36.8, 36.8, 37.4, 39.0]

dia = arange(2,248)  # días de 1 a 247, aka 4 de septiembre

plt.plot(dia, dolar)
# plt.savefig('01_01_dolar.png')



#%% linea 452
#%% Comparamos el dolar y el real
real  = [5.57, 5.92, 6.02, 6.14, 6.19, 6.1, 5.9, 6.18, 6.63, 6.48, 7.26, 7.01, 7.37, 7.63]
dia_r = [1, 18, 36, 53, 71, 88, 106, 123, 141, 158, 176, 193, 211, 228]

plt.plot(dia  , dolar , '-'  , label='dolar')
plt.plot(dia_r, real  , 'o-' , label='real')
plt.xlabel('Día del año [1 = 1ro de Enero ]')
plt.ylabel('Cotizacion [Pesos Arg]')
plt.title('Evolucion del dolar en 2018')
plt.legend()
plt.grid(b=True)

# plt.savefig('01_02_dolar.png')



#%% linea 470
#%% Ejemplos de manipulación de vectores y mas gráficos

dolar = array(dolar)

plt.subplot(3,1,1)   # figura con 3 filas de graficos, 1 columna, me posiciono en la primera
plt.plot(dia         , dolar        , '-')
plt.plot(dia[0:115]  , dolar[0:115] , '-', color='blue' , linewidth=2)
plt.plot(dia[219:]   , dolar[219:]  , '-', color='red'  , linewidth=2)
#plt.xlabel('Día del año [1 = 1ro de Enero ]')
plt.ylabel('Dolar\n[Pesos Arg]')
plt.grid(b=True)

plt.subplot(3,1,2)   # fme posiciono en la segunda
plt.plot( dia         , dolar/dolar[0] * 100 - 100       , '-')
#plt.xlabel('Día del año [1 = 1ro de Enero ]')
plt.ylabel('Aumento\nanual [%]')
plt.grid(b=True)

plt.subplot(3,1,3)   # fme posiciono en la segunda
plt.plot( dia[1:]         , diff(dolar)/dolar[1:] *100       , '-')
plt.xlabel('Día del año [1 = 1ro de Enero ]')
plt.ylabel('Aumento\ndiario [%]')
plt.grid(b=True)

plt.tight_layout()

# plt.savefig('01_03_dolar.png')



#%% linea 523
savez('datos.npz', varX=varX, varY=varY, texto_mio=texto_mio)



#%% linea 538
datos = load('datos.npz')



#%% linea 548
varX = np.array([10,20,30,70,90,-1])

varY = -3.1415926535897

texto_mio = 'Este texto es una descripción que me recuerda para qué son los valores varX y varY que guardé.'

# Instrucción para guaradar datos en formato NumPy
savez('datos.npz', varX=varX, varY=varY, texto_mio=texto_mio)




#%% linea 562
datos = load('datos.npz')

datos
# Out[2]: <numpy.lib.npyio.NpzFile at 0x7f71fa8f25f8>

# El método keys() del diccionario nos permite saber los nombres con que se guardaron las variables

datos.keys()
# Out[3]: ['varX', 'varY', 'texto_mio']

datos['varX']
# Out[4]: array([10, 20, 30, 70, 90, -1])

datos['varY']
# Out[5]: array(-3.1415926535897)

datos['texto_mio']
# Out[6]:
# array('Este texto es una descripción que me recuerda para qué son los valores varX y varY que guardé.',
#       dtype='<U94')



#%% linea 589
varX      = datos['varX']
varY      = datos['varY'].tolist()
texto_mio = datos['texto_mio'].tolist()

varX
# Out[8]: array([10, 20, 30, 70, 90, -1])

varY
# Out[9]: -3.1415926535897

texto_mio
# Out[10]: 'Este texto es una descripción que me recuerda para qué son los valores varX y varY que guardé.'



#%% linea 615
import scipy.io as sio    # input / output de SciPy

# Creamos un diccionario
adict = {}
adict['vector1'] = vector_que_queremos_guardar
adict['texto_2'] = 'este es un texto'
adict['nombre_de_matris'] = matris_que_queremos_guardar

sio.savemat('NOMBRE_DEL_ARCHIVO.mat', adict)

# Para recupearar los datos:
bdict = io.loadmat('NOMBRE_DEL_ARCHIVO.mat')



#%% linea 638
datos = array([velocidad,error,aceleracion ])
savetxt('datos.txt', datos.T , delimiter=',', newline='\n', header='', footer='', comments='# ')



#%% linea 661
import os
import requests
if not os.path.isfile('datos.txt'): # Si NO tengo el archivo de datos, lo bajo de ineternet
    res = requests.get('https://marceluda.github.io/python-para-fisicos/tuto/labo2/01_intro_python/datos.txt',{})
    with open( 'datos.txt' ,'w') as output:
        output.write( res.text  )

datos = loadtxt('datos.txt', comments='#', delimiter=',')

velocidad   = datos[0,:]
vel_error   = datos[1,:]
aceleracion = datos[2,:]



#%% linea 682
datos = array([ 4,  0,  4,  2, 19, 15,  4,  8,  2,  9])

print('promedio',            mean(datos)  )
print('suma',                 sum(datos)  )
print('desviacion estandar',  std(datos)  )
print('Num elementos',        len(datos)  )



#%% linea 693
diff(datos)
#  array([ -4,   4,  -2,  17,  -4, -11,   4,  -6,   7])



#%% linea 700
#%%
import os
import requests
if not os.path.isfile('datos.txt'): # Si NO tengo el archivo de datos, lo bajo de ineternet
    res = requests.get('https://marceluda.github.io/python-para-fisicos/tuto/labo2/01_intro_python/datos.txt',{})
    with open( 'datos.txt' ,'w') as output:
        output.write( res.text  )

datos = loadtxt('datos.txt', comments='#', delimiter=',')

tiempo      = datos[:,0]
velocidad   = datos[:,1]
vel_error   = datos[:,2]
aceleracion = datos[:,3]

plt.plot(tiempo  , aceleracion , 'o' , label='datos')
plt.plot( (tiempo[:-1]+tiempo[1:])/2  , diff(velocidad)/diff(tiempo) , '-' , label='calculado' )
plt.xlabel('tiempo [seg]')
plt.ylabel('Aceleracion [m/s2]')
plt.legend()
plt.grid(b=True)

# plt.savefig('01_04_derivada.png')



#%% linea 730
plt.subplot(2,1,1)
plt.fill_between(tiempo  , zeros(len(tiempo)) ,velocidad , alpha=0.5 )
plt.plot(tiempo  , velocidad , 'o-' )
plt.ylabel('velocidad [m/s]')
plt.xlabel('tiempo [seg]')
plt.grid(b=True)

plt.subplot(2,1,2)
plt.plot(tiempo  , cumsum(velocidad * mean(diff(tiempo)) ) , '.-' , label='datos')
plt.xlabel('tiempo [seg]')
plt.ylabel('recorrido [m]')
plt.grid(b=True)

plt.tight_layout()
# plt.savefig('01_05_integral.png')



#%% linea 754
if CONDICION:
    print('se cumplió la condicion')
elif CONDICION2:
    print('se cumplió la condicion 2')
else:
    print('NO se cumplió ninguna')



#%% linea 765
for numero in [5,6,9,7,1,5,6,8]:
    print('El número en esta iteración es: ', numero)
    print('El número al cuadrado es:', numero**2 )



#%% linea 774

numeros_menores_al_anterior = []

for i,numero in enumerate([5,6,9,7,1,5,4,8]):
    if i>0:
        if numero <= numero_anterior:
            numeros_menores_al_anterior.append(  numero  )
    numero_anterior = numero

print( numeros_menores_al_anterior )
# [7, 1, 4]



#%% linea 793

def sinc_cuadrada(x):
    if x!=0:
        rta = sin(x) / x
        rta = rta**2
    else:
        rta = 1
    return rta

sinc_cuadrada(12)
# 0.0019993784467465382

sinc_cuadrada(0)
# 1
