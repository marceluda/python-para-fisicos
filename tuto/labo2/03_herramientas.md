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

```python
#%%
random.seed(1024)

f0 = 10 # Hz

t  = linspace(0,60,100000)
y1 = 2* cos(2*pi*f0*t + (random.rand(len(t))-0.5)/3 ) + random.randn(len(t))/3

y1 += 2* cos(2*pi*f0*t*3.3 + (random.rand(len(t))-0.5)/30 ) + random.randn(len(t))/30

plt.figure()
plt.plot(t,y1)

#%%
t_step = mean(diff(t))

N      = len(y1)
ii     = arange(N)
Norma  = sinc(ii/N) * exp(-1j*ii*pi/N)  * 2/N
Y1     = fft.rfft( y1 )[0:N//2] * Norma[0:N//2]
ff     = fft.fftfreq( N , d=t_step  )[0:N//2]


plt.figure()
plt.plot( ff , abs(Y1)    )
plt.semilogy()
plt.ylabel('Amplitud')

#plt.plot( ff , angle(Y1)*180/pi , *argv, **kwargs )
#plt.set_yticks([-180, -135, -90, -45, 0, 45, 90, 135, 180])
#plt.set_ylabel('fase [grad]')

plt.semilogx()
plt.xlabel('Frecuencia [Hz]')
plt.grid(b=True,linestyle='--',color='lightgray')
plt.tight_layout()

```

## Filtros


## Análisis gráfico


## Adquisición remota



{% include page_navbar.html up=1 %}
