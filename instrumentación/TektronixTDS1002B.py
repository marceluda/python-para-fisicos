#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Osciloscopio Tektronix TDS1002B
Manual U (web): https://github.com/hgrecco/labosdf-bin/raw/master/manuals/TDS1002 Manual.pdf
Manual P (web): https://github.com/hgrecco/labosdf-bin/raw/master/manuals/TDS 100-1000-2000_prog.pdf
Manual U (local): \\Srvlabos\manuales\Tektronix\TDS1002 Manual.pdf
Manual P (local): \\Srvlabos\manuales\Tektronix\TDS 200-1000-2000_prog.pdf

Para intro teórica, ver:
https://marceluda.github.io/python-para-fisicos/tuto/labo2/05_instrumentacion/
"""

import time

from matplotlib import pyplot as plt
import numpy as np
import visa

print(__doc__)


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Configuración e identificación del dispositivo


# Este string determina el intrumento que van a usar.
# Lo tienen que cambiar de acuerdo a lo que tengan conectado.
resource_name = 'USB0::0x0699::0x0363::C065089::INSTR'

# Creamos ol objeto "osci" que nos permite comunicarnos con el instrumento
rm            = visa.ResourceManager()
osci          = rm.open_resource(resource_name)

# Pedimos la identificación del equipo
print(  osci.query('*IDN?')   )




# Activo modo de transmision: Binario
osci.write('DAT:ENC RPB')
osci.write('DAT:WID 1')



# Adquiero parámetros necesarios para convertir datos digitales a las 
# magnitudes físicas originales (segundos y Volts)
xze, xin, yze, ymu, yoff = osci.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', separator=';')


##########################
# ATENCIÓN!              #
##########################

# cáda vez que cambien las escalas del osciloscopio van a tener que volver 
# a levantar xze, xin, yze, ymu, yoff  !!!




#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Ejemplo de adquisición

canal   = 1

# Selecciono el canal
# Las strings"f" (notar la f antes del ' ) permiten incluir variables del
# entorno que seran convertidas a texto
osci.write(f'DATA:SOU {canal}')

# Adquiere los datos del canal 1 y los devuelve en un array de numpy
datos_y = osci.query_binary_values('CURV?', datatype='B', container=np.array)

volts   = (datos_y-yoff)*ymu+yze;
tiempo  = xze + np.arange(len(datos_y)) * xin

plt.plot(  tiempo, data )
plt.xlabel('Tiempo [s]' )
plt.ylabel('Voltaje [V]')







# Al finalizar la serie de mediciones ser debe cerrar el instrumento:
# osci.close()



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Elegir canal 

canal   = 1
osci.write(f'DATA:SOU {canal}')


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Escalas de tiempo

# Para escala de tiempos por división:
#    HORizontal:MAIn:SCAle <escala>	
# donde <escala> está en segundos 
# <escala> puede ser: 1  ,  2.5  , 5    con un exponente
# Ej: 2.5E-3 son 2.5 ms
#       5E-6 son   5 us

escala = 2.5e-3 
osci.write(f'HORizontal:MAIn:SCAle {escala:3.1E}')

# Con esto puedo ver la escala actual:
escala_actual = osci.query('HORizontal:MAIn:SCAle?')
print(f'La escala horizontal actual es: {escala_actual}  seg')



# Para posicion del tiempo
#    HORizontal:MAIn:POSition <NR3>

# Ej: que el trigger se dispare 10 ms antes de llegar al centro de la pantalla
diff_tiempo = 10e-3
osci.write(f'HORizontal:MAIn:POS {diff_tiempo}')



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Escalas de voltaje por canal

# Para escala de voltaje por división del canal <x>:
#    CH<x>:SCAle <escala>
# Escala varía entre 2 mV y 5 V, con valores en secuencia 1,2,5 
# Ejemplo: pner en el canal 1 una escala de 100 mV por división:

canal  = 1
escala = 100e-3
osci.write(f'CH{canal}:SCAle {escala:3.1E}')


# Para posicion de voltaje del canal <x>:
#    CH<x>:POSition <NR3>

# La posición te dice cuantas divisiones hacia abajo o hacia arriba está corriedo
# el centro de la escala

canal  = 2
div    = 1.5
osci.write(f'CH{canal}:POS {div}')


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Mediciones de parámetros de una señal


# Se puede pedir al osciloscopio que nos mida parámetros como frecuencia, periodo
# maximo, promedio, etc de una señal. Las magnitudes medibles son:
#
#    For TBS1000B/EDU models.
#        MEASUrement:IMMed:TYPe { CRMs | FALL | FREQuency | MAXImum |
#        MEAN | MINImum | NONe | NWIdth | PERIod | PK2pk | PWIdth |
#        RISe | RMS | CURSORRms | PDUTy | PHAse | DELAYRR | DELAYRF |
#        DELAYFR | DELAYFF | AMplitude | CMEAN | High | LOW | NDUty |
#        POVERshoot | NOVERshoot | CURSORMean | BURSTWIDth | AREA |
#        CAREA | PPULSECount | NPULSECount | REDGECount | FEDGECount

# Comandos:
# Fuente
#    MEASUrement:IMMed:SOUrce  CH<x>
# Typo
#   MEASUrement:IMMed:TYPe
# obtenr valor 
#    MEASUrement:IMMed:VALue?
# obtener unidad
#    MEASUrement:IMMed:UNIts?




# ejemplo:
# Medimos Frecuencua, periodo, promedio, mínimo, máximo, RMS y amplitud
# para el canal 1

canal = 1
osci.write(f'MEASUrement:IMMed:SOUrce CH{canal}')

for parametro in 'FREQ PERI MEAN MINI MAXI RMS AM':
    # digo que tipo de medicion es
    osci.write(f'MEASUrement:IMMed:TYPe {parametro}')
    
    # obtengo valor
    par_valor  = osci.query('MEASUrement:IMMed:VALue?')
    
    # obtengo unidad
    par_unidad = osci.query('MEASUrement:IMMed:UNIts?')

    # imprimo:
    print(f'{parametro} : {par_valor} {par_unidad}')



