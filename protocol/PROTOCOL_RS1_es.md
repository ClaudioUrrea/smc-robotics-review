# PROTOCOLO_RS1.md — Revisión narrativa estructurada (enfoque A) · 2026-11-11
Paper R2 · *Sliding Mode Control in Robotics: A Fifty-Year Review and Tutorial Since Utkin* (título de trabajo) · Mathematics (MDPI), tipo Review · plazo 18-nov-2026.

## 1. Decisiones fijadas
- Enfoque A (decisión del autor, 11-nov): panorama histórico 1977–2026 + taxonomía variante × plataforma + matriz de decisión + tutorial ilustrativo.
- Tipo de revisión: narrativa estructurada con búsqueda documentada y reproducible. No PRISMA-ScR completo. Guía de calidad: SANRA (Baethge et al., 2019; por verificar en REFERENCE_CHECK).
- Fuentes: WoS Core Collection + Scopus (decisión del autor, 11-nov), mismas cadenas adaptadas a cada sintaxis. Duplicados entre bases: se eliminan por DOI y, sin DOI, por título normalizado; se conserva el registro WoS.
- Perfiles de autor (solo control de solapamiento y autocitas): WoS AI=KWU-1600-2024; Scopus AU-ID 24078008600.
- Consulta a la oficina editorial sobre el ejemplo tutorial: sí (CORREO_EDITORIAL.md).

## 2. Preguntas de la revisión
- P1. ¿Cómo evolucionó el SMC desde Utkin (1977) hasta 2026 y qué problema resolvió cada variante?
- P2. ¿Qué variantes se usan en cada plataforma robótica y con qué tipo de validación?
- P3. ¿Qué criterios prácticos guían la elección de una variante (modelo requerido, chattering, convergencia, carga de cálculo, número de parámetros de ajuste)?
- P4. ¿Cómo se diseña e implementa paso a paso un SMC en un robot de referencia?

## 3. Estratos del corpus
| Estrato | Contenido | Cómo se identifica |
|---|---|---|
| E-F Fundacional | Obras clásicas (1950s–2015): Utkin 1977, Slotine–Sastry 1983, Young–Utkin–Özgüner 1999, Levant 2003, etc. | Selección experta + citas hacia atrás de las anclas y de las revisiones incluidas. Se declara así en el texto |
| E-R Revisiones | Revisiones y tutoriales 2010–2026 | WoS: Q05, Q06, Q07, Q09b (ya exportados, 290 registros). Scopus: SR05, SR06 |
| E-V Variantes | Artículos 2016–2026 por variante (más citados) | Exportaciones X01–X09 |
| E-P Plataformas | Artículos 2016–2026 por plataforma (más citados) | Exportaciones X10–X14 |
| E-N Recientes | Artículos 2025–2026 (más citados) | Exportación X15 |

## 4. Exportaciones que debe hacer el autor (para RS2)
**Copie las cadenas desde CADENAS_WOS.txt y CADENAS_SCOPUS.txt (texto plano).** Las cadenas de esta tabla van entre comillas invertidas de formato y dan error si se copian con ellas. Scopus: 15 espejos S01–S15 más SR05 y SR06 (revisiones, todos los registros). Si falta tiempo, mínimo en Scopus: SR05, SR06 y S15.
Procedimiento para cada fila: Búsqueda avanzada → pegar la cadena COMPLETA → Buscar → ordenar «Citas: mayor número primero» → Exportar → BibTeX → «Rango de registros» 1 a N → «Registro completo» → guardar con el nombre indicado.

Bloque común (ya incluido en cada cadena): términos de modo deslizante y DT=(Article OR Review).

| Archivo | N | Cadena completa |
|---|---|---|
| X01_integral.bib | 30 | `TS=("integral sliding mode*" OR "integral sliding-mode*") AND TS=(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND DT=(Article OR Review) AND PY=(2016-2026)` |
| X02_terminal.bib | 30 | `TS=("terminal sliding" OR "nonsingular terminal" OR "fast terminal") AND TS=(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND DT=(Article OR Review) AND PY=(2016-2026)` |
| X03_orden_superior.bib | 30 | `TS=("higher-order sliding" OR "high-order sliding" OR "second-order sliding" OR "super-twisting") AND TS=(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND DT=(Article OR Review) AND PY=(2016-2026)` |
| X04_adaptativo.bib | 30 | `TS=("adaptive sliding mode*" OR "adaptive sliding-mode*") AND TS=(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND DT=(Article OR Review) AND PY=(2016-2026)` |
| X05_inteligente.bib | 30 | `TS=("sliding mode*" OR "sliding-mode*") AND TS=(fuzzy OR "neural network*" OR "reinforcement learning") AND TS=(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND DT=(Article OR Review) AND PY=(2016-2026)` |
| X06_fraccionario.bib | 30 | `TS=("fractional-order" OR "fractional order") AND TS=("sliding mode*" OR "sliding-mode*") AND TS=(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND DT=(Article OR Review) AND PY=(2016-2026)` |
| X07_observadores.bib | 30 | `TS=("sliding mode observer*" OR "sliding-mode observer*" OR "sliding mode differentiator*" OR "robust exact differentiator*") AND TS=(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND DT=(Article OR Review) AND PY=(2016-2026)` |
| X08_tiempo.bib | 30 | `TS=("sliding mode*" OR "sliding-mode*") AND TS=("fixed-time" OR "prescribed-time" OR "predefined-time" OR "event-triggered") AND TS=(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND DT=(Article OR Review) AND PY=(2016-2026)` |
| X09_implementacion.bib | 30 | `TS=("sliding mode*" OR "sliding-mode*") AND TS=(chattering) AND TS=("discrete-time" OR discretization OR discretisation OR "sampled-data" OR implicit) AND TS=(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND DT=(Article OR Review) AND PY=(2016-2026)` |
| X10_manipuladores.bib | 30 | `TS=("sliding mode*" OR "sliding-mode*" OR "super-twisting" OR "terminal sliding") AND TS=(manipulator* OR "robot arm*" OR "robotic arm*") AND DT=(Article OR Review) AND PY=(2016-2026)` |
| X11_moviles.bib | 30 | `TS=("sliding mode*" OR "sliding-mode*" OR "super-twisting" OR "terminal sliding") AND TS=("mobile robot*" OR "wheeled robot*" OR nonholonomic OR "legged robot*") AND DT=(Article OR Review) AND PY=(2016-2026)` |
| X12_aereos.bib | 30 | `TS=("sliding mode*" OR "sliding-mode*" OR "super-twisting" OR "terminal sliding") AND TS=(quadrotor* OR quadcopter* OR multirotor* OR UAV* OR "unmanned aerial") AND DT=(Article OR Review) AND PY=(2016-2026)` |
| X13_submarinos.bib | 30 | `TS=("sliding mode*" OR "sliding-mode*" OR "super-twisting" OR "terminal sliding") AND TS=("underwater vehicle*" OR AUV* OR ROV* OR "underwater robot*") AND DT=(Article OR Review) AND PY=(2016-2026)` |
| X14_exoesqueletos.bib | 30 | `TS=("sliding mode*" OR "sliding-mode*" OR "super-twisting" OR "terminal sliding") AND TS=(exoskeleton* OR "rehabilitation robot*" OR "wearable robot*") AND DT=(Article OR Review) AND PY=(2016-2026)` |
| X15_recientes.bib | 60 | `TS=("sliding mode*" OR "sliding-mode*" OR "super-twisting" OR "terminal sliding") AND TS=(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND DT=(Article OR Review) AND PY=(2025-2026)` |

Total máximo: 480 registros WoS + 480 Scopus + SR05/SR06 antes de eliminar duplicados (se espera un solapamiento alto entre bases). Registrar en BRECHA_WOS.md el conteo total que muestre WoS para cada cadena (lo hago yo al recibir los archivos si el autor anota el número en el nombre o en el chat).

## 5. Criterios de selección (RS2: título y resumen; RS3: texto completo o resumen extendido)
Inclusión
- I1. El SMC (cualquier variante) o un observador por modo deslizante es el método principal, no solo una comparación.
- I2. Plataforma robótica de las cinco clases (manipulador, móvil terrestre, aéreo, submarino, exoesqueleto/rehabilitación), o revisión/tutorial de SMC general con aplicación robótica.
- I3. Artículo o revisión revisado por pares, en inglés.
- I4. Para E-V, E-P y E-N: 2016–2026. E-F sin límite de año.

Exclusión
- X1. SMC solo como línea base de comparación.
- X2. Sin plataforma robótica (motores, convertidores, redes eléctricas), salvo E-F o revisiones metodológicas citadas por su aporte teórico.
- X3. Sin resumen o retractado.
- X4. Duplicado (se conserva el registro con DOI).

Reglas de decisión: en caso de duda en RS2 se incluye y se resuelve en RS3. Cada exclusión registra su código (X1–X4).

## 6. Formulario de extracción (RS3)
`id, doi, anio, estrato, plataforma, variante(s), objetivo (seguimiento/estabilización/fuerza/formación), mitigacion_chattering, incertidumbre_perturbacion, observador, convergencia (asintótica/finita/fija/prescrita), validacion (simulación/experimento/HIL), gdl, implementacion_discreta (sí/no), codigo_disponible (sí/no), citas_wos`

## 7. Síntesis prevista (RS4)
- Línea de tiempo 1977–2026 con hitos fundacionales y la aparición de cada variante.
- Matriz de conteos variante × plataforma, con el tipo de validación dominante.
- Matriz de decisión con criterios cualitativos: modelo requerido, chattering, tipo de convergencia, complejidad de implementación, carga de cálculo y número de parámetros.
- Retos abiertos: discretización, tiempo real, aprendizaje con garantías, validación experimental.
- Diagrama de flujo de la búsqueda con conteos por etapa: identificados, sin duplicados, cribados y finalmente incluidos.

## 8. Tutorial ilustrativo (sujeto a la respuesta editorial)
- Modelo: manipulador plano de 2 GDL con parámetros de libro de texto (fuente publicada, citada). No se usan el modelo SCARA ni el FOSMC propios.
- Controladores: SMC clásico con capa límite, super-twisting y terminal no singular. Misma referencia, misma perturbación, mismo paso de integración.
- Resultados presentados como demostración didáctica y reproducible; código Python en repositorio público (enlace en Data Availability y Supplementary Materials).
- Si la oficina editorial lo objeta: se reduce a pseudocódigo y pasos de diseño, sin figuras de simulación.

## 9. Limitaciones que se declararán
Dos bases (WoS y Scopus), sin IEEE Xplore ni Google Scholar; muestreo de los más citados por estrato (sesgo hacia trabajos antiguos, compensado por X15); revisión narrativa, no sistemática; selección del estrato fundacional por criterio experto.

## 10. Calendario
| Fecha | Etapa |
|---|---|
| 11-nov | RS1 (este protocolo) · autor exporta X01–X15 y envía el correo |
| 12-nov | RS2 cribado |
| 13–14-nov | RS3 extracción |
| 14-nov | RS4 síntesis · E3 plan y REFERENCE_CHECK |
| 15–16-nov | Redacción y tutorial |
| 17-nov | Auditoría (RS6/E8) |
| 18-nov | Paquete y envío |

## Enmiendas 11-nov-2026 (decisión del autor)
- Categoría CONTEXTO (nueva): revisiones/tutoriales de SMC en capítulo de libro o ponencia, y revisiones de SMC en dominios no robóticos. No son evidencia primaria; sirven para introducción, historia y comprobación de brecha.
- Cadena genérica SR07 (Scopus) añadida para reducir la dependencia de los términos de plataforma; validada con AU-ID (7/7). Los registros fuera de las cinco clases de plataforma se marcan «DUDA I2» y se deciden en RS3.

## Enmiendas 11-nov-2026 (b) — refuerzo de exhaustividad previo a RS3
1. **Cribado completo de cadenas genéricas.** SR07 (Scopus, 4.839) y W01 (WoS, top 1.000 de 5.932 por citas) se criban en su totalidad con las mismas reglas (antes, solo los 300 más citados). Ajustes de reglas: (a) revisiones de control de una plataforma sin SMC como tema principal → CONTEXTO (posicionamiento/brecha); (b) «Euler-Lagrange» y «mechanical system» → DUDA I2.
2. **Bola de nieve por citas (backward/forward).** Fuente: OpenCitations Index v2 + metadatos Crossref. Hacia atrás: referencias de 19 revisiones semilla (SMC y control de plataformas). Hacia adelante: citantes de 6 clásicos de SMC en robótica (Slotine 1984/1985, Slotine-Sastry 1983, Young 1978, Man-Paplinski-Wu 1994, Feng-Yu-Man 2002; este último parcial, 1.048 citantes recuperados por corte del servidor). Filtro por título (SMC ∧ plataforma), 2016–2026, artículo de revista; pre-2016 con ≥150 citas → CANDIDATO CANÓNICO (decisión experta). Limitación: OpenCitations no cubre todas las editoriales; OpenAlex/Semantic Scholar no disponibles por cuota el 11-nov.
3. **Diseño en dos niveles.** *Corpus de mapeo*: todos los INCLUIR (codificación automática provisional de variante, plataforma y validación experimental; validación en RS3 sobre muestra aleatoria de 100 registros, con kappa de Cohen para plataforma y concordancia por etiqueta de variante; si kappa < 0,7 se recodifica). Sustenta matriz variante × plataforma, series temporales y tasa de validación experimental. *Corpus de síntesis*: subconjunto curado (≈250–300 referencias citadas) seleccionado en RS3/RS4 por celda de la matriz (más citados, más recientes, experimentales, y revisiones cercanas).
4. **Canon fundacional (E-F).** 42 obras: 39 con DOI verificado en Crossref, 3 libros sin DOI (Slotine-Li 1991, Emelyanov 1967, Itkis 1976). Se corrigió una entrada inexistente (Shtessel-Fridman-Plestan 2016 → «Adaptive sliding mode control and observation», IJC 2016). Se añaden como candidatos los 28 clásicos de robótica SMC surgidos de la bola de nieve.

## Enmiendas 11-nov-2026 (c) — cierre de la búsqueda
1. Cadena SR08 en Scopus (complemento de plataforma sin la palabra «robot») y W12 en WoS (W01 ∪ W02), ambas exportadas completas. Motivo: la estimación de recall con muestra independiente era del 70 %.
2. Bola de nieve hacia adelante con Semantic Scholar (paginación completa) y hacia atrás con la unión OpenCitations + Semantic Scholar + referencias en texto libre de Crossref resueltas.
3. Regla de exclusión X2 por dominio no robótico (automoción y energía: suspensión, frenado, vehículo eléctrico, PMSM, convertidores, etc.) cuando el título no menciona ninguna plataforma robótica. «Vehicle» solo cuenta como DUDA I2 si va calificado (autonomous/unmanned/underwater/aerial/surface/ground).
4. Recall estimado = 96,0 % (IC 95 % 94,2–97,8 %). Detalle en BUSQUEDA_RECALL_LIMITACIONES.md.


## Enmiendas 11-nov-2026 (d) — mitigación de limitaciones residuales
1. **Análisis de sensibilidad:** se reportan los artículos no ingleses (767) y las ponencias o capítulos en inglés (5.075), sin incorporarlos al corpus.
2. **Codificación automática:** se usan solo las palabras clave del autor (sin Keywords Plus ni palabras indexadas) y se amplía el patrón HOSM. Prevalidación con un segundo codificador ciego (κ ≥ 0,74); la validación humana sigue en RS3.
3. **Calibración del indicador experimental:** se calibró contra texto completo (VPP 0,87; prevalencia corregida 32 %).

## Enmiendas 11-nov-2026 (e) — cierre del cribado en RS3
1. I1 e I2 se aplican a todo el corpus de mapeo 2016+ (7.226), no solo a los marcados DUDA, porque el cribado provisional de las cadenas genéricas era laxo.
2. I1: el SMC cuenta como línea base si solo aparece en frases de comparación. I2: la plataforma debe constar en el título o en las palabras clave del autor, o aparecer en el resumen como banco de validación o en la frase inicial. Los dominios no robóticos en el título → X2.
3. Nivel de plataforma: principal o ejemplo de validación. El análisis de sensibilidad usa solo el principal.
4. Validación de las reglas: dos auditorías por lectura (100 de desarrollo + 100 de validación independiente). Precisión del nivel principal 100 % (IC 91–100); exclusiones correctas 85–90 %.
5. Canon: 34 de 37 candidatos aceptados (3 naves espaciales → CONTEXTO); los 3 libros sin DOI se incluyen, verificados por catálogo.
6. κ humano por codificación ciega de 60 registros (CODIFICACION_CIEGA_AUTOR_60.xlsx); sustituye a las columnas «_autor», que no eran ciegas.
7. (v2.1) Normalización de texto antes de aplicar reglas (scripts/rs3_clean.py: título paralelo en chino, puntuación de ancho completo, caracteres CJK, aviso de copyright final). I3 de idioma: se excluyen los registros que Scopus clasifica como no ingleses aunque hayan entrado por WoS o por la bola de nieve (7).
8. (v2.2) Palabras clave: se usan las de autor de WoS si existen; los términos de plataforma del tesauro IEEE solo cuentan si el resumen confirma un robot. Grúas (crane) y vehículos de lanzamiento en el título → X2. La limpieza de texto cubre títulos paralelos en cualquier idioma, entidades y etiquetas HTML y avisos de copyright o licencia.
9. (v2.3) κ humano del autor (60 registros ciegos): tiempo finito/fijo/predefinido (0,62) e ISM (0,56) quedaron bajo 0,7. Las variantes se recodifican con título, palabras clave del autor y resumen (sin frases de comparación), se amplían los patrones (appointed-time, integral fuzzy sliding, actor-critic/ADP) y se quita «model-free» de inteligente. La corrección se verificó en una muestra independiente de 40 registros. El κ oficial que se reporta es el previo a la corrección.

## Enmienda 11-nov-2026 (f) — tutorial (RS4)
Sujeta a la respuesta editorial. El tutorial de 2 GDL incluye cuatro controladores: SMC con capa límite, STA, NTSM y SMC de tiempo fijo (añadido por ser la familia dominante en el corpus). Se evalúan con tres periodos de muestreo (1, 2 y 5 ms) y dos niveles de ruido de medición, con estas métricas: RMSE, tiempo de asentamiento frente a la cota teórica, y chattering (variación total y energía de alta frecuencia de la acción de control). Se presenta como demostración didáctica y reproducible que ilustra las brechas B1–B3 de RS4, no como resultado de investigación. Si la oficina editorial objeta, se aplica el plan original de §8 o se reduce a pseudocódigo.

## Enmienda 12-nov-2026 (g) — revisión de RS5
1. **Parámetros del tutorial:** se mantienen dos eslabones uniformes ideales (1 kg, 1 m, centro de masa a 0,5 m, I = ml²/12), declarados en el texto como elegidos por transparencia y sin reproducir un brazo de laboratorio. Spong et al. (2020) se cita solo por el modelo dinámico. Motivo: ningún libro verificable usa exactamente este conjunto, y atribuir los valores a una fuente que no los contiene sería una cita falsa. Difiere de la consulta editorial («textbook parameters taken from a published source»); si la editorial responde, se aclara en la carta.
2. **PRISMA 2020:** diagrama con la caja de duplicados eliminados (35.478 identificados; 22.803 duplicados; WoS incluye 662 registros de las cadenas específicas). Lista completa (27 ítems) y lista para resúmenes rellenadas sobre las plantillas oficiales (File S2). Los ítems de riesgo de sesgo, sesgo de publicación y certeza se declaran «no evaluados» (revisión narrativa).
3. **Declaraciones en el texto:** registro (no registrado), protocolo y enmiendas (Sección 2.1); un solo revisor con reglas en scripts y asistencia de IA generativa (Sección 2.3 y Agradecimientos); recall global de 93–94 %; corrección de la limitación de «muestreo de los más citados», que ya no aplica al corpus de mapeo.
4. **Material suplementario:** Tablas S1–S4 en inglés (S4 = corpus de mapeo 5.931 + canon 79), File S1 (cadenas) y File S2 (listas PRISMA).
5. **Datos y código:** GitHub (código versionado, release v1.0) y Figshare (DOI del depósito), como pide la guía. Las exportaciones crudas de WoS y Scopus no se redistribuyen por licencia.
