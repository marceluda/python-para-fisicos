---
title: Toolkit para realizar ajustes no lineales
description: Toolkit para realizar ajustes no lineales
layout: page
mathjax: true
---


<div class="alert alert-danger" role="alert" >
  <strong>Aviso:</strong> La página está en construcción.
</div>

Aquí se presenta un sript ya armado para facilitar la realización de ajustes no lineales
con múltiples parámetros, con una interfaz gráfica para definir los parámetros iniciales.

Está diseñado para usarse en [Spyder](https://www.spyder-ide.org/), que viene como parte del sistema de paquetes [Anaconda](https://www.anaconda.com/products/distribution#Downloads).

<div class="alert alert-info" role="info" >
  <strong>Referencia:</strong>
    <ul>
        <li><a href="{{ site.baseurl }}/tuto/labo2/03_ajustes">Ajustes no lineales</a></li>
    </ul>
</div>

<center>
<p> <a href="https://github.com/marceluda/python-para-fisicos/blob/gh-pages/tuto/labo2/toolkit_ajustes/ajuste_no_lineal.py" class="btn btn-primary btn-lg" role="button">
Código Fuente del toolkit para ajustes
</a> </p>
</center>


-------

## Configuración de Spyder

Para usar herramientas interactivas en Spyder hay que configurar el IPython para graficar de modo automático.

Eso se puede hacer desde las preferencias:

![grafico](spyder_pref.png "grafico")

Y luego ir a IPython, Gráficos, Automático

![grafico](spyder_auto.png "grafico")

Una vez realizado reiniciar el Spyder.


------

## Modo de uso

1) Primero hacer una copia del script

2) Modificar el modelo a ajustar por uno propio. Notar que los parámetros están todos en orden dentro de una lista o un array llamado `params`.

```python
def modelo(x,params):
    """
    Modelo que se va a usar para ajustar los datos
        x: valores del eje x
        params: lista o vector de parámetros
    devuelve:
        valores del eje y
        """
    m,y0,A,x0,w0,x1,w1 = params

    if not type(x)==ndarray:
        x = array(x)

    y = m*x+y0
    y+= A/( 1+ ( (x-x0)/w0  )**2 )
    y+= A/( 1+ ( (x-x1)/w1  )**2 )

    return y
```

3) Según el modelo definido hay que configurar los parámetros a usar.

- En la lista `nombres` van los nombres de cada parámetro (es para visualizar los resultados)
- En `parametros_iniciales` van los valores iniciales para empezar el proceso de ajuste
- En `limites` se colocan los límites inferior y superior de cada parámetro. Esto es necesario para definir los `Slider` que se utilizarán para hacer un primer ajuste a mano.

```python
# Acá ponemos la info de los parámetros
nombres              = "m,y0,A,x0,w0,x1,w1".split(',')
parametros_iniciales = [      0 ,        0 ,    10 ,    30 ,   10 ,    70 ,   10 ]
limites              = [[-10,10],[-100,100],[0,100],[0,100],[0,40],[0,100],[0,40]]
```

4) Definir opciones de ajuste:

```python
# Opciones de ajuste
GRAFICAR_PASO_A_PASO = True   # Ver en cada paso del algoritmo el gráfico
AJUSTAR_CON_LIMITES  = True   # Utilizar límites para el ajuste de parámetros. NO SE RECOMIENDA
AJUSTAR_CON_ESCALAS  = True   # Usar escalas de parámetros en los ajustes. NO SE RECOMIENDA
```

- `GRAFICAR_PASO_A_PASO` permite visualizar el resultado de cada paso del ajuste. Hace más lento el proceso, pero se entiende mejor qué está haciendo el algoritmo.
- `AJUSTAR_CON_LIMITES` toma los límites fijados en `limites` como límites estrictos de los parámetros. Se lo puede usar cuando se quiere restringir un parámetro a un subconjunto particular.
- `AJUSTAR_CON_ESCALAS` define la escala de los cambios aplicados a cada parámetro a partir del ancho del intervalo definido en `limites`.

5) Definir los datos a ajustar. Con `USAR_DATOS_FICTICIOS=True` se generan datos random para probar. Si se lo establece en `False` se pueden usar las líneas post `else` para definir los datos a ajustar.

```python
if USAR_DATOS_FICTICIOS:
    random.seed(0)
    parametros_reales = [-0.3, 30, 25, 40,5,47,3]
    datos_x  = linspace(20,80,80)
    datos_y  = modelo(datos_x , parametros_reales )
    datos_y += random.normal(size=len(datos_y))

else:
    datos_x  =  array([0,1])
    datos_y  =  array([0,1])
```

6) Correr el script y ajustar a mano los datos iniciales.

Se verá en pantalla una figura con los gráficos y otra con los `Slider` de cada parámetro.

![grafico](ajuste_params_1.png "grafico")

Luego de variar los parámetros a través de los `Slider` se puede hacercar el modelo a la forma de los datos:

![grafico](ajuste_params_2.png "grafico")

7) Hacer clic en el botón `Ajustar`. El algoritmo tratará de optimizar los parámetros.

8) Interpretar los resultados

Como resultado del ajuste se imprimen los parámetros hallados y otras variables relevantes.

```
N              : 80.00000
P              :  7.00000
SSE            : 60.97525
SST            : 14390.96044
Rsq            :  0.99576
Rsq_adj        :  0.99535


Parámetros con su Error Estandar:
m              :   -0.328 ±    0.008
y0             :   31.767 ±    0.533
A              :   25.680 ±    0.429
x0             :   40.263 ±    0.125
w0             :    4.834 ±    0.214
x1             :   47.117 ±    0.059
w1             :    2.555 ±    0.123

Intervalos de confianza:

Confianza: 95.00%   | alpha=0.050
m              :   -0.328 ±    0.016 [  -0.344 :   -0.312]
y0             :   31.767 ±    1.062 [  30.704 :   32.829]
A              :   25.680 ±    0.855 [  24.825 :   26.534]
x0             :   40.263 ±    0.250 [  40.013 :   40.512]
w0             :    4.834 ±    0.426 [   4.408 :    5.260]
x1             :   47.117 ±    0.118 [  46.999 :   47.236]
w1             :    2.555 ±    0.245 [   2.310 :    2.800]
```

La misma información quedará guardada en el diccionario `resultados`:

```python
resultados
{'parametros': array([-0.32780223, 31.76651197, 25.67959668, 40.26288822,  4.83395351,
        47.11741406,  2.554867  ]),
 'N': 80,
 'P': 7,
 'COV': array([[ 6.27315641e-05, -3.97072958e-03,  2.49777849e-04,
         -2.54910408e-04,  7.39818677e-04, -3.54350877e-05,
         -3.04021149e-05],
        [-3.97072958e-03,  2.84022709e-01, -1.23014686e-02,
          1.85756921e-02, -6.41585523e-02,  1.84396927e-03,
         -1.71162253e-03],
        [ 2.49777849e-04, -1.23014686e-02,  1.83897324e-01,
         -9.44574832e-03, -3.80898529e-02,  3.08814929e-03,
         -1.90515519e-02],
        [-2.54910408e-04,  1.85756921e-02, -9.44574832e-03,
          1.56766530e-02,  4.52454240e-03,  2.32492077e-03,
         -7.60001074e-03],
        [ 7.39818677e-04, -6.41585523e-02, -3.80898529e-02,
          4.52454240e-03,  4.57289377e-02,  1.14937590e-03,
         -6.99136421e-03],
        [-3.54350877e-05,  1.84396927e-03,  3.08814929e-03,
          2.32492077e-03,  1.14937590e-03,  3.51846728e-03,
         -2.39007997e-03],
        [-3.04021149e-05, -1.71162253e-03, -1.90515519e-02,
         -7.60001074e-03, -6.99136421e-03, -2.39007997e-03,
          1.50887203e-02]]),
 'SE': array([0.00792033, 0.53293781, 0.42883251, 0.12520644, 0.21384325,
        0.05931667, 0.12283615]),
 'SSE': 60.975249216786054,
 'SST': 14390.96044355569,
 'Rsq': 0.9957629478966367,
 'Rsq_adj': 0.9953510122754763}
 ```

 También se producen algunos gráficos útiles para interpretar los parámetros y los residuos:

![grafico](resultados_ajuste.png "grafico")
