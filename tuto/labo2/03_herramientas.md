---
title: Herramientas útiles para análisis
description: Herramientas de análisis
layout: page
mathjax: true
navbar: labo2
---


{% include page_navbar.html %}

<div class="alert alert-danger" role="alert" >
  <strong>Aviso:</strong> La página está en construcción.
</div>




## Transformada de Fourier

Ejemplo de datos frabricados:

```python
random.seed(1024)

# Simulamos una frecuencia base de 10 Hz
f0 = 10 # Hz

# durante un tiempo de 60 segundos, con 100000 muestras equi-espaciadas
t  = linspace(0,60,100000)

# Incluimos ruido de fase y ruido de amplitud
y1 = 2* cos(2*pi*f0*t + (random.rand(len(t))-0.5)/3 ) + random.randn(len(t))/3

# Y agregamos otra componente de 3.3 veces la frecuencia f0
y1 += ( 2* cos(2*pi*f0*t*3.3 + (random.rand(len(t))-0.5)/3 ) + random.randn(len(t))/3 ) /100


plt.figure(1)
plt.plot(t,y1)
plt.xlabel('tiempo [s]')
plt.ylabel('señal')
plt.title('Muestra en el dominio temporal de la señal')
# plt.savefig('03_01_simulacion_frecuencia.png')
```

![grafico](03_01_simulacion_frecuencia.png "grafico")


```python
# Para poder construir el eje de frecuencias de la tranformada de Fourier hace
# falta:
#  - Tener los datos en tiempos equiespaciados
#  - Saber el tiempo de separacion entre los datos, que llamaremos t_step

t_step = mean(diff(t))

# Nos sirve asber el largo del vector temporal
N      = len(y1)
ii     = arange(N)

# Este factor de normalización corrige artificios de cálculo, debido a que
# la FFT no es un implementación completa de la Tranformada de Fourier.
Norma  = sinc(ii/N) * exp(-1j*ii*pi/N)  * 2/N

# Calculamos la transformada
Y1     = fft.rfft( y1 )[0:N//2] * Norma[0:N//2]
ff     = fft.fftfreq( N , d=t_step  )[0:N//2]

# Graficamos el valor absoluto en escala lograritmica

plt.figure(2)
plt.plot( ff , abs(Y1)  , '.-' , alpha=0.5 )
plt.semilogy()
plt.ylabel('Amplitud')

#plt.plot( ff , angle(Y1)*180/pi , *argv, **kwargs )
#plt.set_yticks([-180, -135, -90, -45, 0, 45, 90, 135, 180])
#plt.set_ylabel('fase [grad]')

plt.semilogx()
plt.xlabel('Frecuencia [Hz]')
plt.grid(b=True,linestyle='--',color='lightgray')
plt.tight_layout()
# plt.savefig('03_02_fft.png')
```

![grafico](03_02_fft.png "grafico")


## Filtros


## Análisis gráfico


## Adquisición remota



{% include page_navbar.html up=1 %}
