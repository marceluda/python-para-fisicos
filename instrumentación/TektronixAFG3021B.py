#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de funciones Tektronix AFG 3021B
Manual U (web): https://github.com/hgrecco/labosdf-bin/raw/master/manuals/TektronixAFG3000.pdf
Manual P (web): https://github.com/hgrecco/labosdf-bin/raw/master/manuals/TektronixAFG3000_p.pdf
Manual U (local): \\Srvlabos\manuales\Tektronix\AFG3012B (M Usuario).pdf
Manual P (local): \\Srvlabos\manuales\Tektronix\AFG3012B (Prog Manual).pdf

Para intro teórica, ver:
https://marceluda.github.io/python-para-fisicos/tuto/labo2/05_instrumentacion/
"""




from __future__ import division, unicode_literals, print_function, absolute_import

import time

import numpy as np
import visa

print(__doc__)


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Configuración e identificación del dispositivo

# Este string determina el intrumento que van a usar.
# Lo tienen que cambiar de acuerdo a lo que tengan conectado.
resource_name = 'USB0::0x0699::0x0346::C033250::INSTR'

rm = visa.ResourceManager()

# Abre la sesion VISA de comunicacion
fungen = rm.open_resource(resource_name)

print(fungen.query('*IDN?'))








#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Ejemplo de barrido de frecuencia y amplitud

# Rampa logaritmica de frequencias 
# Vean la ayuda de "np.logspace?" en la consola
# Ejemplo de barrido logarítmico de de 10^1 Hz hasta 10^3 Hz en 20 pasos
for freq in np.logspace(1, 3, 20):
    fungen.write(f'FREQ {freq}' )
    time.sleep(0.1)




# Rampa lineal de amplitudes
# Barrido de 0 a 1 Volt en 10 pasos
for amplitude in np.linspace(0, 1, 10):
    fungen.write('VOLT {amplitude}' )
    time.sleep(0.1)

    
# Rampa lineal de offset
for offset in np.linspace(0, 1, 10):
    fungen.write('VOLT:OFFS {offset}'  )
    time.sleep(0.1)




# Al terminar cerramos:
fungen.close()





