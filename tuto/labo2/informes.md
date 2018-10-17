---
title: Informes para Labo 2
description: Consejos básicos para auto-corregirse los informes
layout: page
mathjax: true
---

<div class="alert alert-danger" role="alert" >
  <strong>Aviso:</strong> Esta página no pertenece realmente al proyecto <strong>Python para Física</strong> y sólo está acá por comodidad para la cursada.
</div>


## Estructura de los informes

Veamos primero cual debe ser la estructura de los informes:

  1. **Título:** En una sola frase, de qué se trata el trabajo o qué tiene de innovador
  2. **Autores:** Incluir filiación (ej: Laboratorio Tal de Tal Universidad ó Materia del de tal carrera, tal Univ) y contacto (al menos un mail).
  3. **Resumen:** (un párrafo) Qué se hizo, qué se quiere mostrar, qué resultado se obtuvo.
  4. **Introducción**
    - Texto introductorio que nos pone en tema.
    - Motivación del trabajo. Puede ser histórica (este tema viene de X e Y y acá se continua aportando Tal cosa) o práctica (queremos lograr hacer tal cosa que ya se hace, pero mas rápido y mas chiquito (?) ) o varias...
    -  **Marco teórico**.
      - Introducir / mencionar la **teoría que sirve de base** para entender los fenómenos que se van a ver.
      - Acá suele haber uno o varias citas a textos que hablen de esa teoría (algún libro de las referencias).
      - Introducir **fórmulas relevantes**. Relevantes son: Las que son útiles para entender el fenómeno, las que se necesitan para poder procesar o interpretar los datos y las que se necesitan para deducir estas ultimas.
    - Antecedentes. Cosas que ya se saben sobre el fenómeno a estudiar. Alguna cita a trabajos anteriores.
    - Anticipar estructura del resto del documento: "En las sección 2 se presentará el diseño del armado experimental, haciendo incapié en X cosa importante. En la sección 3 se explicará el desarrollo de la experiencia y el proceso de medición. Finalmente, en la sección 4 se presentan los resultados y análisis" ... o similar...
    - **No tiene por que estar TODO esto** si o si en la introducción, pero el marco teórico SI es indispensable.
  5. Cuerpo
    - Descripción del armado experimental y de los experimentos.
    - Mediciones, procedimiento experimental. Cuidados y consideraciones relevantes sobre qué se hizo o cómo se lo hizo.
    - El objetivo de esas dos partes es que le puedan contar a un colega de otra universidad, con su mismo nivel de formación, qué hicieron, con información suficiente para que ese colega lo pueda reproducir. Tiene sentido mencionar instrumental usado, durante el texto, no como lista de ingredientes.
    - Presentación de resultados. Se prefieren gráficos por sobre tablas. En lo posible, gráficos trabajados. No olvidar intervalos de incerteza y propagar errores cuando se deba.
    - **Análsis de datos**. **Comparación con las ecuaciones relevantes del marco teórico**. Determinación de variables calculadas, parámetros de ajustes, etc.
    - No tiene que ser ordenado de esa forma. Resultados y análisis pueden ir juntos. Sin son varias experiencias, hay varias formas de ordenar posibles. Tiene que ser entendible y coherente.
  6. **Conclusiones:** Conclusiones globales, cierre de discusiones relevantes, perspectivas futuras, problemas abiertos.
  7. **Referencias:** Deben estar numeradas. Lo estándar es con corchetes tipo [1]  [2]  ... una por línea. Las referencias deben haber sido usadas en el texto y citadas donde corresponda.
  8. **Apéndices:** Información importante o útil que escapa un poco al relato central del texto.
    - Puede ser un procedimiento de análisis usado, que se menciona en el texto y se explica detalladamente acá.
    - Pueden ser gráficos auxiliares generados para obtener información que no es central en el análisis, pero es necesario para poder hacer ese análisis.
    - Pueden ser deducciones de fórmulas, tablas de información auxiliar, etc
    - Solo tiene sentido ponerlo si aporta algo, no tiene sentido ponerlo "para agregar info"


## Consejos para las figuras

  - **Los epígrafes**
    - **Deben contener la información necesaria para entender el gráfico** que se presenta. Descripción de lo que se ve y no es evidente, o requiere información textual además de la gráfica.
    - Se espera también **que sirva para un "lectura diagonal del texto"**. Esto es: si alguien lee el texto por arriba, entre el resumen, los epígrafes y las figuras debería entenderse masomenos qué se hizo en el trabajo. Por ende, a veces se agrega en las figura UNA oración sobre la figura contando cómo es el experimento (si es un armado experimental) o cómo se la analiza/que resultados brinda (si es un gráfico de resultados). UNA oración.
  - **Los gráficos de datos**
    - Generalmente, pocos datos se grafican con items discretos, con sus barras de error.
    - Si se compara con un modelo, el modeo se lo suele graficar con lineas continuas.
    - Evaluar si tiene sentido que algún eje use escala logarítmica. Recordar que con esta escala no se ve ni el cero ni los números negativos
    - Es util poner una grilla de fondo, como referencia.
    - Si hay varias curvas, poner cuadro de leyendes / referencias.
    - Siempre preguntarse: **¿Para que muetro este gráfcio? ¿que quiero transmitir?**
      - ¿Quiero remarcar que hay un pico a X frecuencia? ... entones lo resalto, hago una flechan una linea vertical, algo que remarque eso
      - ¿Quiero comparar los datos con un modelo?. Entonces incluyo el ajuste, la comparación o algo que me permita evaluarlo. Si hago ajuste, reporto el parámetro relevante que quería encontrar (con su intervalo de incerteza!).
      - ¿Quiero mostrar que sigue una tendencia ... lineal, cuadrataica, logarítmica, etc?. Evaluar si vale la pena linealizar. Si uno quiere reportar "que algo se parece a una recta", reportar estimadores de bondad de ajuste que hablen de eso, como el $R ^2$
    - Elegir bien las escalas. Si algo está en "segundos", dependiendo del orden de magnitud, pueden ser s, ms, $\mu$s , ns ... etc.
    - Siempre poner etiqueta a los ejes. No olvidar las unidades
  - **Graficos de armado experimental **
    - Los apartos usados no tiene por que tener mucho diseño. Hasta pueden ser cajas, con sus entradas y salidas relevantes.
    - Sí deben tener nombre o alugna identificación que se referencie en el epígrafe.
    - Deben estar señaladas las variable importantes. ¿Hay distancias que midieron que son importantes para analizar los resultados?. Márquenlas con una recta, ponganle nombre. Resáltenlas. Señalen las variables y parametros relevantes que se controlan o se miden.
    - **¿Para que muestran esa figura?**
      - Si es para dar una idea de dimensiones, de dificultad del armado experimental, de lo delicado de determiado montaje... Tal vez les conviene una FOTO.
      - Si es para dar idea de la disposicion de elementos, donde la geometría de la disposición es clave... Tal vez conviene un grafico tipo PLANO, respetando dimensiones relevantes, con un buen diseño. (pocas veces es necesario esto)
      - Si es para transmitir la **lógica detrás de un armado experimental**, para que se entienda que algo geenra una señal, eso se transmite a otro lado, actua sobre otra cosa y es medido con otro aparato... entonces un gráfico con bloques puede llegar a ser suficiente, sin detalles gráficos, pero si remarcando las variables relevantes.
      - Puede ser cosas medio mixtas. Está permitido usar la imaginación. Pero sean atentos al objetivo de fondo: ¿Sirve la figura para transmitir lo que quiero transmitir?
  - Las figuras deben ser numeradas y referenciadas en el texto.
  
