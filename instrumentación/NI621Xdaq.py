#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NI-DAQmx Python Documentation: https://nidaqmx-python.readthedocs.io/en/latest/index.html
NI USB-621x User Manual: https://www.ni.com/pdf/manuals/371931f.pdf

Basado en:
https://github.com/diegoshalom/labosdf/blob/master/software/python/Labo5%202021/daq.py
"""

import matplotlib.pyplot as plt
import numpy as np
import nidaqmx
import time


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Para saber el ID de la placa conectada (DevX)
system = nidaqmx.system.System.local()
for device in system.devices:
    print(device)

# Dejamos definido el dispositivo y puerto para el resto del script

DSIP = 1
PORT = 1

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Configuración y armado de función de adquisición


# Para setear (y preguntar) el modo y rango de un canal analógico
with nidaqmx.Task() as task:
    # Configuramos rango de adquisición para el puerto en cuestión
    ai_channel = task.ai_channels.add_ai_voltage_chan(f"Dev{DISP}/ai{PORT}",max_val=10,min_val=-10)
    
    # Imprimimos la información
    print(ai_channel.ai_term_cfg)    
    print(ai_channel.ai_max)
    print(ai_channel.ai_min)	
	

## Medicion por tiempo/samples de una sola vez
def medir(duracion, fs):
    cant_puntos = duracion*fs    
    with nidaqmx.Task() as task:
        modo= nidaqmx.constants.TerminalConfiguration.DIFFERENTIAL
        task.ai_channels.add_ai_voltage_chan(f"Dev{DISP}/ai{PORT}", terminal_config = modo)
               
        task.timing.cfg_samp_clk_timing(fs,samps_per_chan = cant_puntos,
                                        sample_mode = nidaqmx.constants.AcquisitionType.FINITE)
        
        datos = task.read(number_of_samples_per_channel=nidaqmx.constants.READ_ALL_AVAILABLE)           
    datos = np.asarray(datos)    
    return datos


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Adquisición UNA vez

duracion = 1       # segundos
fs       = 250000  # Frecuencia de muestreo

y        = medir(duracion, fs)


plt.plot(y)
plt.grid()
plt.show()


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Medicion continua

fs    = 250000 # Frecuencia de muestreo
task  = nidaqmx.Task()
modo  = nidaqmx.constants.TerminalConfiguration.DIFFERENTIAL
task.ai_channels.add_ai_voltage_chan(f"Dev{DISP}/ai{PORT}", terminal_config = modo)
task.timing.cfg_samp_clk_timing(fs, sample_mode = nidaqmx.constants.AcquisitionType.CONTINUOUS)
task.start()
t0    = time.time()
total = 0


for i in range(10):
    time.sleep(0.1)
    datos = task.read(number_of_samples_per_channel=nidaqmx.constants.READ_ALL_AVAILABLE)           
    total = total + len(datos)
    t1    = time.time()
    print("{t1-t0:2.3f} s {len(datos):d} {total:d} {total/(t1-t0):2.3f}" )    
    
task.stop()
task.close()



