#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LOCKIN Tektronix SR830
Manual (web): http://www.thinksrs.com/downloads/PDFs/Manuals/SR830m.pdf
Manual (local): \\Srvlabos\manuales\Standford\SR830m.pdf
"""


import visa

print(__doc__)


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Identificación del dispositivo

# Este string determina el intrumento que van a usar.
# Lo tienen que cambiar de acuerdo a lo que tengan conectado.
resource_name = 'GPIB0::8::INSTR'

rm            = visa.ResourceManager()
lockin        = rm.open_resource(resource_name)

# Pide indentificacion
print(lockin.query('*IDN?'))



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Leer componentes demoduladas de a una

# Lee las salidas una a la vez
# X=1, Y=2, R=3, T=4
x = lockin.query_ascii_values('OUTP ?1')
y = lockin.query_ascii_values('OUTP ?2')
r = lockin.query_ascii_values('OUTP ?3')
t = lockin.query_ascii_values('OUTP ?4')

print(x, y, r, t)


# Al terminar cerramos el intrumento
# lockin.close()


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Leer componentes demoduladas todas juntas

# O bien todas juntas
x,y,r,t = lockin.query_ascii_values('SNAP ? 1,2,3,4')

print(x,y,r,t)



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Cambia el voltaje en la salida auxiliar
# El primer numero es la salida y el segundo es el voltaje

SALIDA = 0
valor  = 4.32
lockin.write(f'AUXV {SALIDA}, {valor}')

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Serie de configuraciones útiles

# Acá los códigos desde el manual:

#    FMOD (?) {i}  |  Set (Query) the Reference Source to External (0) or Internal (1).
#    FREQ (?) {f}  |  Set (Query) the Reference Frequency to f Hz.Set only in Internal reference mode.
#    SLVL (?) {x}  |  Set (Query) the Sine Output Amplitude to x Vrms. 0.004 ≤ x ≤5.000
#    HARM (?) {i}  |  Set (Query) the Detection Harmonic to 1 ≤ i ≤ 19999 and i•f ≤ 102 kHz
#    
#    ISRC (?) {i}  |  Set (Query) the Input Configuration to A (0), A-B (1) , I (1 MΩ) (2) or I (100 MΩ) (3).
#    
#    ILIN (?) {i}  |  Set (Query) the Line Notch Filters to Out (0), Line In (1) , 2xLine In (2), or Both In (3).
#    
#    SENS (?) {i}  |  Set (Query) the Sensitivity to 2 nV (0) through 1 V (26) rms full scale.
#    
#    OFLT (?) {i}  |  Set (Query) the Time Constant to 10 μs (0) through 30 ks (19).
#    
#    OFSL (?) {i}  |  Set (Query) the Low Pass Filter Slope to 6 (0), 12 (1), 18 (2) or 24 (3) dB/oct.

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Uso de referencia interna del lock-in para modular

frecuencia  = 1025 # Hz
AmpRMS      = 0.5  # Amplitud en Volts RMS

lockin.write(f'FMOD 1')              # referencia interna
lockin.write(f'FREQ {frecuencia}')   # frecuencia
lockin.write(f'SLVL {AmpRMS}')       # amplitud


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Configuración de la entrada

lockin.write(f'ISRC 0')              # canal A
lockin.write(f'ISRC 1')              # canal A-B
lockin.write(f'ISRC 2')              # canal A modo corriente 1 MΩ
lockin.write(f'ISRC 3')              # canal A modo corriente 100 MΩ

lockin.write(f'ILIN 0')              # Sin filtros
lockin.write(f'ILIN 1')              # Notch a 50 Hz
lockin.write(f'ILIN 2')              # Notch a 100 Hz
lockin.write(f'ILIN 3')              # Notch a 50 Hz y 100 Hz


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Configuración demodulación

# Valores de sensibilidad posibles: (ver manual, sec 5-6)

#    i    sensitivity        i    sensitivity
#    0        2 nV/fA        13      50 μV/pA
#    1        5 nV/fA        14     100 μV/pA
#    2       10 nV/fA        15     200 μV/pA
#    3       20 nV/fA        16     500 μV/pA
#    4       50 nV/fA        17       1 mV/nA
#    5      100 nV/fA        18       2 mV/nA
#    6      200 nV/fA        19       5 mV/nA
#    7      500 nV/fA        20      10 mV/nA
#    8        1 μV/pA        21      20 mV/nA
#    9        2 μV/pA        22      50 mV/nA
#    10       5 μV/pA        23     100 mV/nA
#    11      10 μV/pA        24     200 mV/nA
#    12      20 μV/pA        25     500 mV/nA
#                            26        1 V/μA

sens = 12   # 20 μV
lockin.write(f'SENS {sens}')

# Valores de tiempo de integración posible: (ver manual, sec 5-6)

#    i    time constant        i    time constant
#    0            10 μs        10            1 s
#    1            30 μs        11            3 s
#    2           100 μs        12           10 s
#    3           300 μs        13           30 s
#    4             1 ms        14          100 s
#    5             3 ms        15          300 s
#    6            10 ms        16            1 ks
#    7            30 ms        17            3 ks
#    8           100 ms        18           10 ks
#    9           300 ms        19           30 ks

# Orden
# 6 dB/oct (i=0), 12 dB/oct (i=1), 18 dB/oct (i=2) or  24 dB/oct (i=3)

t_int  = 8  # 100 ms
orden  = 3  # Orden 4, 24 dB/oct

lockin.write(f'OFLT {t_int}')

lockin.write(f'OFSL {orden}')




