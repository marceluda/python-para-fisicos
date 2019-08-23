---
title: Instrumentación y adquisición remota
description: Control remoto de instrumentos de laboratorio
layout: page
mathjax: true
navbar: labo2
---


{% include page_navbar.html %}

<div class="alert alert-danger" role="alert" >
  <strong>Aviso:</strong> La página está en construcción.
</div>

A continuación se presentan los conceptos básicos necesarios para poder
realizar control remoto de un instrumento y adquisición programada.


Un instrumento de medición permite convertir una magnitud física que se desea medir
en otra magnitud que pueda ser registrada o percibida por nuestros sentidos.
Los instrumentos fueron variando a lo largo de la historia en la medida que avanza
la tecnología.

  - Un ejemplo antiguo y analógico puede ser una balanza: transforma una fuerza (el peso)
    en un desplazamiento espacial que puede ser medido mediante una regla.
  - Con el advenimiento de la electrónica, se pasó a un esquema en el que la mayoría de los
    instrumentos transforman la magnitud medida a una señal eléctrica (una corriente o tensión), que luego es medida y registrada por otro instrumento (multímetro, osciloscopio, etc) y
    presentada en un pantalla.
    - _magnitud a medir_ → _señal de corriente / tensión_ → _pantalla o registro en papel_
  - En la actualidad, con la tecnología digital, cada vez es más habitual que los instrumentos
    entreguen directamente en forma digital (por un canal de comunicación de datos)
    el resultado de una medición.
    - _magnitud a medir_ → _señal de corriente / tensión_ → _pantalla_
    - _magnitud a medir_ → _señal de corriente / tensión_ → _canal digital de datos_ → _computadora_
    - _magnitud a medir_ → _canal digital de datos_ → _computadora_

Por ello, hoy en día se necesita conocer cómo es el proceso de **digitalización** y
el de **transmisión de datos** para poder realizar una adquisición por computadora.
La incorporación de la computadora al laboratorio permite entonces automatizar
(programación mediante) el registro de datos o la realización de (algunas partes de) un experimento.

![grafico](digitalizacion.png "digitalizacion")


## Instrumentación

El primer paso es conocer los instrumentos que se van a utilizar.
Imaginemos que contamos con un osciloscopio y un generador de funciones.
Debemos ir a buscar la información relevante de estos equipos.

  - Osciloscopio: `Tektronix TBS1052b-edu`
    - Página web del producto: [https://www.tek.com/oscilloscope/tbs1052b-edu](https://www.tek.com/oscilloscope/tbs1052b-edu)
    - [Página de documentos del producto](https://www.tek.com/product-support?model=TBS1052B-EDU)
      - [Manual de operación](TBS1000B-User-Manual-077088602-RevA.pdf) ([web](https://download.tek.com/manual/TBS1000B-User-Manual-077088602-RevA.pdf))
      - [Manual de programación](TBS1000-B-EDU-TDS2000-B-C-TDS1000-B-C-EDU-TDS200-TPS2000-Programmer_EN-US-RevA.pdf) ([web](https://download.tek.com/manual/TBS1000-B-EDU-TDS2000-B-C-TDS1000-B-C-EDU-TDS200-TPS2000-Programmer_EN-US-RevA.pdf))
  - Generador de funciones: `Tektronix AFG1022`
    - Página web del producto: [https://www.tek.com/arbitrary-function-generator/afg1000-arbitrary-function-generator](https://www.tek.com/arbitrary-function-generator/afg1000-arbitrary-function-generator)
    - Documentos del producto:
      - [Manual de operación](AFG1022-Quick-Start-User-Manual-EN.pdf) ([web](https://download.tek.com/manual/AFG1022-Quick-Start-User-Manual-EN.pdf))
      - [Manual de programación](AFG1000-Programmer-Manual-EN-077112901-RevA.pdf) ([web](https://download.tek.com/manual/AFG1000-Programmer-Manual-EN-077112901(20160719)-RevA.pdf))

En los manuales están los detalles técnicos de cada instrumento. Esto incluye detalles de la conversión
Analógico/Digital de los equipos. Por ejemplo, en el manual del osciloscopio (pág 115):

![grafico](TBS1052b_manual.png "TBS1052b_manual")

Nos especifica:
  - Datos de la digitalización
    - Resolución "vertical" (de Voltaje): `8 bits` → $2^8 = 256$ pasos de digitalización
    - Sample Rate: `1 GS/s`, 1 Giga Sample son 1000 millones de datos por segundo (maximo)
    - Record Length: `2500` puntos, 2500 datos de 8 bits pueden ser registrados en el tiempo.
  - Datos de electrónica relevantes:
    - "Bandwidth" / Ancho de banda: `50 MHz` , frecuencia de corte a partir de la cual se pierden armónicos. Es una limitación eléctrica (la limitación de digitalización es el SampleRate/2 , mucho mayor al BandWidth que reportan acá).
    - Impedancia de entrada: `1 MΩ`

En el manual del generador de funciones (pag 11)

![grafico](AFG1022_manual_00.png "AFG1022_manual_00")

(pag 22)

![grafico](AFG1022_manual_01.png "AFG1022_manual_01")

Nos especifica:
  - Datos de la conversión A/D
    - "Waveform" / Forma de la Onda: hasta `8192` puntos (para definir la forma de onda) de `14 bits` de resolución ($2^{14} = 16384$ pasos de digitalización)
    - Sample Rate: `125 MS/s`, Hasta 125 Mega Samples por segundo son 125 millones de puntos por segundo (máximo)
    - Amplitud: los `14 bits` se distribuyen en un rango desde `2 mVpp` (mili Volts de pico a pico) hasta `20 Vpp` para una carga "alta" (mucho mayor a `50 Ω` ).
  - Datos de electrónica relevantes:
    - Impedancia de salida: `50 Ω`

<div class="alert alert-info" role="alert" >
  <strong>Importante:</strong> Tener conocimiento de los detalles técnicos de
  conversión A/D y de las características eléctricas del instrumental es fundamental
  para poder diseñar un experimento. Pero además es necesario para poder interpretar
  los datos adquiridos por un instrumento determinado y transformarlos luego en
  las magnitudes que representan lo que estamos tratando de medir.
</div>

Luego, debemos conocer cuales son los canales de comunicación con ese instrumental.
Existe una API estándar en la industria llamada [VISA](https://en.wikipedia.org/wiki/Virtual_instrument_software_architecture)
(Virtual instrument software architecture), que permite unificar en una sola
interfaz las diferentes tecnologías de comunicación.

![grafico](visa.png "VISA")

Cada sistema operativo y software o lenguaje de programación tiene alguna
implementación propia de VISA (a veces debe ser instalada). En el caso de
`python` hay que instalar `pyvisa`.

La mayoría de los instrumentos soporta comandos por
[SCPI](https://en.wikipedia.org/wiki/Standard_Commands_for_Programmable_Instruments),
que es una sintaxis estándar para escribir instrucciones para instrumentos.
Las instrucciones consisten en palabras y valores escritos en texto plano, cada
una asociada a los diferentes valores que puede medir un instrumento o parámetros de
configuración necesarios para su operación.

<div class="alert alert-info" role="alert" >
  <strong>Importante:</strong> Cada instrumento tiene su propio conjunto de
  instrucciones. Para saber cómo operarlo debemos leer el Manual de Programación
  específico de cada uno.
</div>

Por ejemplo, para adquirir el vector de números que representan el voltaje medido por
el canal 1 de un osciloscopio se usan estos dos comandos:

Seleccionar el canal 1:

  `'DATA:SOURCE CH1'`

leer los datos

  `CURV?`

Para establecer la frecuencia de la función de onda de un generador de funciones
en `50 Hz` usamos este comando:

  `FREQ 50`

Así, en nuestro lenguaje de programación, deberemos crear textos con estas
instrucciones y enviarlas a cada instrumento mediante la API de VISA.

## Control remoto en Python

Hay varios ejemplos de adquisición remota y control ya armados.
Algunos están en repositorios compartidos, como los del profesor
[Hernan Grecco en GitHub](https://github.com/hgrecco/labosdf/tree/master/software/python/instrumentos).


Veamos dos ejemplos...

### Osciloscopio

Importaremos la librería `visa` y usaremos el Resource Manager de la librería que nos permite
conectarnos al equipo informándole la dirección. Luego, los métodos `query()` y `write()`
nos permitirán enviar las instrucciones al equipo y traer la respuesta (en el caso de `query()`).

Vamos a usar las siguientes **instrucciones extraídas del manual**.
Lo que está entre corchetes `[]` o en minúscula es opcional ponerlo.

| Referencia  | Comando (ej) | Función |
|-------------|--------------|---------|
| `DATa:SOUrce <wfm>`  | `DATA:SOU 1` | Selecciona el canal del osciloscopio |
| `CURV?`                         | `CURV?`     | Pide los datos medidos del canal actual |
| `HORizontal:MAIn:SCAle <escala>`                           | `HOR:MAIN:SCA 5E-3`      | Fija la escala temporal del osciloscopio (en segundos) |
| `WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;` | `WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;` | Adquiere los datos de la escala de la pantalla del osciloscopio |

El último comando son en realidad varios anidados. Permiten obtener la información necesaria para transformar los
2500 números enteros de 8 bits que adquirimos con `CURV?` en Volts con el espaciado en segundos que corresponda.


```python
from matplotlib import pyplot as plt
from numpy import *
import visa

print(__doc__)

# Cargamos el Resource Manager. El manejador de recursos VISA
rm = visa.ResourceManager()

# Informamos la dirección de acceso al osciloscopio (en este caso, por USB)
osci = rm.open_resource('USB0::0x0699::0x0363::C065089::INSTR')

# Con el método 'query()' podemos enviar instrucciones QUE TIENEN RESPUESTA
# Por ejemplo, la instrucción que nos informa el nombre del instrumento
# al que nos conectamos
respuesta = osci.query('*IDN?')

# La instruccion '*IDN?' nos permite conocer a que instrumento nos conectamos
print(respuesta)


# Le pido algunos parametros de la pantalla, para poder escalear adecuadamente
xze, xin, yze, ymu, yoff = osci.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', separator=';')

# Con el método 'write' enviamos instrucciones QUE NO TIENEN RESPUESTA
# Modo de transmisión: Binario
osci.write('DAT:ENC RPB')
osci.write('DAT:WID 1')

# Adquiere los datos del canal 1 y los devuelve en un array de numpy
data = osci.query_binary_values('CURV?', datatype='B', container=np.array)

voltaje =(data-yoff)*ymu+yze;
tiempo = xze + np.arange(len(data)) * xin

plt.plot(tiempo, voltaje )
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [V]')
```

### Generador de funciones

Vamos a usar las siguientes **instrucciones extraídas del manual**.
Lo que está entre corchetes `[]` o en minúscula es opcional ponerlo.

| Referencia  | Comando (ej) | Función |
|------------------------------
| `[SOURce[1|2]]:VOLTage <amplitude>`                           | `VOLT 0.5`      | Cambiar la amplitud pico a pico (en Volts) |
| `[SOURce[1|2]]:FREQuency <frequency>`                         | `FREQ 2000`     | Cambiar la frecuencia (en Hz) |
| `[SOURce[1|2]]:VOLTage[:LEVel][:IMMediate]:OFFSet <voltage>`  | `VOLT:OFFS 0.3` | Cambiar la tensión del centro de la funcion de onda. |



```python
import time

from numpy import *
import visa

# Cargamos el Resource Manager. El manejador de recursos VISA
rm = visa.ResourceManager()

# Informamos la dirección de acceso al osciloscopio (en este caso, por USB)
fungen = rm.open_resource('USB0::0x0699::0x0346::C033250::INSTR')

# Con el método 'query()' podemos enviar instrucciones QUE TIENEN RESPUESTA
# Por ejemplo, la instrucción que nos informa el nombre del instrumento
# al que nos conectamos
print(fungen.query('*IDN?'))

# Para enviar instrucciones que no entregan una respuesta se usa
# el método 'write()'

# Vamos a generar valores de frecuencias con una separación logarítmica
# vamos de 10^1 a 10^3 , con 20 pasos
for freq in logspace(1, 3, 20):
    fungen.write('FREQ {:f}'.format(freq) )
    print('Comando enviado: ' + 'FREQ {:f}'.format(freq)  )
    time.sleep(0.1)  # tiempo de espera de 0.1 segundos

# Rampa lineal de amplitudes
# Vamos a tener 10 pasos que van de 0 V a 1 V
for amplitude in np.linspace(0, 1, 10):
    fungen.write('VOLT {:f}'.format(amplitude) )
    print('Comando enviado: ' + 'VOLT {:f}'.format(amplitude)  )
    time.sleep(0.1)  # tiempo de espera de 0.1 segundos


# Rampa lineal de offset
# Vamos a tener 10 pasos que van de 0 V a 1 V
for offset in np.linspace(0, 1, 10):
    fungen.write('VOLT:OFFS {:f}'.format(offset)  )
    print('Comando enviado: ' + 'VOLT:OFFS {:f}'.format(offset)   )
    time.sleep(0.1)  # tiempo de espera de 0.1 segundos


# Cuando dejamos de usar el generador de funciones, lo cerramos
fungen.close()

```




{% include page_navbar.html up=1 %}
