

# Cosas que tenemos y que podemos tener
( hace replace de esto
[y](/usr/share/atom/resources/app.asar/node_modules) por esto  [x](https://raw.githubusercontent.com/june29/dotfiles/master/.atom/packages/autocomplete-emojis/node_modules) )

### De la Dokuwiki tenemos registradas estas

  1. [2017-Abril Mediciones para caracterizar lockeo RP](http://localhost/dokuwiki/lolo:2017-abril_mediciones_para_caracterizar_lockeo_rp)
    - de `20170428 - Nuevas med` extrajiste los datos para el armado de un poster para la AFA.
    - Datos para la AFA: `/home/lolo/Dropbox/Doctorado/datos_labo/2017-04-28`
    - Las caracterizaciones del diodo V usado para estas mediciones de Rb están en esta página.
  2. [2017-Septiembre Mediciones para scope+lock a FP](http://localhost/dokuwiki/lolo:2017-septiembre_mediciones_para_scope_lock_a_fp)
    - Algunas mediciones iniciales de lockeo a FP. Hay una de la señal de error que es "de manual"
      `data_20170806_154619.py`
    - Arranque de lockeo, normalito.
    - Carpeta de datos: `/home/lolo/Dropbox/Doctorado/datos_labo/2017-09-07`
    - Incluye video de barrido de modos. El último video tiene barido y lockeo. Los modos son de "tipo trilobite"
    - Cuentas de jorge para justificar que la salida de los PIDs da cuenta de las desviaciones que
      hubiese tenido el laser a lazo abierto, pero para las frecuencia bajas (tiempos largos
      comparados con el pasabajos)
  3. [2017-Noviembre: Caracterizar scope+lock para publicar](http://localhost/dokuwiki/lolo:2017-noviembre_scope_lock)
    - Medición de latencia (quedó viejo??).
      - Carpeta: `/home/lolo/Dropbox/Doctorado/datos_labo/2017-11-01_caracterizacion_RP`
    - Más mediciones de lockeo a FP
    - En `dia_20171107` hiciste medición comparando CTRL con Error y señalando el margen
      a partir del cual tiene sentido analizar esa diferencia.
    - `dia_20171109` medición larga con gráficos muy bonitos
    - En la carpeta `/home/lolo/Dropbox/Doctorado/datos_labo/20171102` hay otras mediciones largas con
      videos de modos TEM02
      - La larga es: `20171102_140828.bin`
      - Gráficos bonitos
    - En `/home/lolo/Dropbox/Doctorado/datos_labo/20171109` hay una medición larga (`20171109_184719.bin`) de
      la que hiciste gráficos bonitos

### Cosas que se podrían reportar

  1. **Capacidades del sistema diseñado**
    - Toolkit de lockeo con control web y control remoto :o:
    - Interfase gráfica amigable para configurar un lockeo "out of the box" :o:
      - Tal vez sería útil tener mejores capturas de ese proceso para reportar en el manual o en el artículo :x:
    - PIDs que cubren multiples órdenes de magnitud sin recompilar la capa FPGA :o:
      - Describir pormenorizadamente :x:
      - Caracterizar :x:
    - Lock-in para democulación y para medición :o: :heavy_exclamation_mark:
      - Lento armónico y rápido cuadrado :o:
      - Describir promenorizadamente :x:
      - Caracterizar :x:
    - Sistema de control de lock: :heavy_exclamation_mark:
      - Por posición de barrido :o:
      - Por thredshold de una señal determinada :x:
    - Sistema de relock :o:
    - Facilidades para relevar rta del sistema
      - Son fáciles de implementar :o:
      - Habría que probarlas :x:
  2. **Cuestiones de diseño**
    - Funcionamiento en capas:
      1. Frontend: Web / navegador
      2. Procesameinto
        - Interfase C, fácil de reprogramar, entendible para todos.
        - Control remoto por Matlab / Python
        - Linea de comandos de Linux
      3. FPGA / circuito: Funcionamiento en tiempo real
    - Mantener alcance de bajo nivel (usamos int para configurar, swiches para FPGA, y cosas así)
      - Mas que nada para poder operar el dispositivo en los límites de resolución
  3. **Puesta a Prueba**
    - Capacidades de medición
      - Caracterización de resolución, ruidos eléctricos, sensibilidad, etc.
      - Esto por ahí va mas para la web, no?
    - Lockeo a espectro del Rb :o:
      - Prestaciones logradas
      - Excusa para presentar lock-in lento armónico
        - Mediciones 1n 1f, 2f, 3f :o:
        - Cuidados tenidos en cuenta para el armado de las funciones
        - Distorción armónica y ... (?)
      - Excusa para presentar caracterización de la rta del Sistema :x:
    - PDH :heavy_exclamation_mark: :heavy_exclamation_mark:
      - Prestaciones del lockeo
      - Excusa para presentar lock-in cuadrado :o:
        - Particularidades de la implementación (cuadrada digital, distorcion armónica, límite de rendimiento)
      - Excusa para presentar sistema de re-lock?? (Esta idea fue sacada del paper del NIST, no se cuanto tiene de sentido extenderse en esto)
      - Algo sobre tuneo de PIDs? Creo que no...



### Referencias:

| Símbolo                  | significado                 |
|--------------------------|-----------------------------|
| :o:                      | lo tenemos                  |
| :x:                      | nos falta                   |
| :heavy_exclamation_mark: | Es (relativamente) original |




# Idea de estructura del Documento




# Pendientes
## Lista de pendientes para publicar artículo

  1. Definir secciones y estructuras
  2. Caracterizar prestaciones
  3. etc

## Lista de pendientes para publicar código

  1. Repaso general de comentarios, nombres de variables, etc.
  2. Documentar funciones in-situ
  3. <del>Makefile que genere directamente los paquetes</del> (creo que esto ya está).
  4. `Readme.md` y `changelog.md`
  5. Lista de TODO
    - Subir al market
    - Ver como meter mejor el control remoto
    - Pasar control remoto a Paramiko
    - Instalador multiplataforma
    - Re-habilitar las funciones de texto para los controles (como poner "Z seg" o "W Hz" como entradas)
  6. Lista de bugs
    - Algunas salidas de PWM están deshabilitadas
    - Señales de oscilo no centradas en Cero cuando no es in1 o in2
    - Testear inicio de lock por trigger de amplitud y combinado


## Lista de pendientes para publicar Manual
  1. Instructivos para procedimientos comunes
    - Lockear en un barrido
    - Cómo caracterizar rta del sistema
    - Cómo optimizar PIDs
  2. Videos explicativos de procedimientos comunes
  3. Documentar control remoto
  4. Mejorar instructivo de instalación.
  5. Hacer referencia al papper de tutorial de teo de control
