# U4 — Guía de ejercicios

Un bloque por sesión. En geometría, **hacé un dibujo antes de hacer la cuenta**: la mitad de los errores son de signo o de orientación (¿Z hacia dónde?, ¿lejano es arriba o abajo?).

---

## A — El modelo *pinhole* (sesión 1)

**A1.** Con f = 1400 px, un jugador de 1,75 m:
- (a) ¿cuántos píxeles mide a 30 m de la cámara?
- (b) ¿a qué distancia está si mide 230 px? ¿Y si mide 30 px?

**A2.** Con K = [[1000, 0, 320], [0, 1000, 240], [0, 0, 1]], R = I y t = 0, proyectá los puntos (2, 1, 10) y (4, 2, 20). ¿Qué tienen en común, y qué significa?

**A3.** Una cámara con R = I está en C = (1, 2, 3). ¿Cuánto vale t? ¿Por qué t no es simplemente C?

**A4.** Con la misma K y R = I:
- (a) calculá el punto de fuga de las rectas con dirección d = (0, 0, 1);
- (b) ¿y el de d = (1, 0, 0)? ¿Qué significa el resultado?

**A5.** En una imagen ves la pelota en el píxel (900, 400). Explicá con la geometría de la proyección por qué no podés saber, solo con eso, si está en el piso a 40 m o en el aire a 25 m.

## B — La homografía (sesión 2)

**B1.** P = [[1, 0, 0, 2], [0, 1, 0, 3], [0, 0, 1, 1]]. ¿Cuál es la homografía del plano Z = 0? ¿Qué transformación es?

**B2.** Completá: para estimar una traslación hacen falta ___ puntos; una similitud, ___; una afín, ___; una homografía, ___. Justificá con los grados de libertad.

**B3.** H = [[1, 0, 0], [0, 1, 0], [0, 1, 1]]. Llevá a la imagen los puntos (0, 0), (0, 2) y su punto medio (0, 1).
- (a) ¿El punto medio de las imágenes es la imagen del punto medio?
- (b) ¿Qué conclusión sacás para "medir distancias en píxeles"?

**B4.** La cámara está a 9 m de altura. Un jugador de 1,75 m está a 30 m (en horizontal) de la cámara. Si usás H⁻¹ con el píxel de su **cabeza** (en vez de sus pies), ¿dónde lo ubica sobre el césped? ¿Cuántos metros de error? (Pista: triángulos semejantes; la homografía supone que todo está en el piso.)

**B5.** La cámara del club panea 1° entre dos frames (solo rota, alrededor de un eje vertical). Con f = 1400, ¿cuántos píxeles se desplaza más o menos el centro de la imagen? ¿Qué te dice sobre usar **una sola** H para varios frames?

## C — DLT (sesión 3)

**C1.** Escribí las dos filas de A para la correspondencia (x, y) = (1, 2) → (u, v) = (3, 5).

**C2.**
- (a) ¿Por qué se impone ‖h‖ = 1 en vez de, por ejemplo, h₉ = 1? (Pensá qué pasa si la H verdadera tiene h₉ = 0.)
- (b) Con 4 correspondencias en posición general, A es de 8×9. ¿Cuál es la dimensión de su espacio nulo?
- (c) ¿Y si 3 de los 4 puntos están alineados?

**C3.** Calculá la T de Hartley para:
- (a) (0, 0), (2, 0), (0, 2), (2, 2);
- (b) (0, 0), (10, 0), (0, 10), (10, 10).

**C4.** En una correspondencia típica de la cancha, x ≈ 80 m y u ≈ 1500 px. ¿Cuánto vale la entrada `u·x` de A, y cuánto la `−1`? ¿Qué tiene que ver con el apunte 03 de U1?

**C5.** Si Ĥ lleva puntos normalizados a puntos normalizados, ¿por qué H = Td⁻¹ Ĥ Ts y no Ts⁻¹ Ĥ Td? Leelo de derecha a izquierda.

## D — Errores y estabilidad (sesión 4)

**D1.** Calibrás con exactamente 4 puntos y el error de reproyección te da 0,0 px. ¿Qué podés concluir? ¿Qué harías para saber si la H sirve?

**D2.** Tenés 7 clicks. Describí la validación *leave-one-out*: ¿cuántas homografías ajustás, con cuántos puntos cada una, y qué medís?

**D3.** El tracking da la posición de un jugador **quieto** 10 veces por segundo, cada una con un error gaussiano independiente de 0,3 m en cada eje.
- (a) ¿Cuánto mide en promedio el "paso" entre dos posiciones consecutivas?
- (b) ¿Cuántos kilómetros "recorre" en 90 minutos sin moverse?
- (c) ¿Y si el error no es independiente entre frames sino **sistemático** (la misma H un poco mal en todo el partido)?

**D4.** Con la cámara sintética del TP, ¿cuántos metros representa 1 píxel cerca de la cámara (punto (50, 60): la lateral cercana queda justo afuera del cuadro), en el centro (50, 34) y en la lateral lejana (50, 0)? Hacelo por separado para 1 px horizontal y 1 px vertical. (Mové 1 px el píxel de cada punto y llevalo a la cancha con H⁻¹.) ¿Qué zona y qué dirección son las más delicadas?

## E — RANSAC (sesión 5)

**E1.** ¿Cuántas iteraciones (confianza 0,99) hacen falta para una homografía con 60 % de inliers? ¿Y con 10 %?

**E2.** Con 50 % de inliers, ¿cuántas iteraciones haría falta si en vez de muestras de 4 usaras muestras de 8 ("para que el DLT ya promedie el ruido")? ¿Conviene?

**E3.** Tenés 30 correspondencias, 3 de ellas malas. La probabilidad de que una muestra de 4 sea limpia, ¿es exactamente w⁴ = 0,9⁴? Calculala exacta (sin reposición) y compará.

**E4.** Los clicks buenos tienen error gaussiano de 1,5 px en cada eje. ¿Qué fracción de los buenos queda **afuera** con umbral 3 px? ¿Y con 5 px? (Pista: la distancia de un error gaussiano 2D tiene P(r > k·σ) = e^(−k²/2).)

**E5.** En el proyecto anterior, RANSAC daba 90 % de inliers justo en los frames donde la estimación era peor (apunte 05). Explicá cómo puede pasar y proponé una verificación independiente.

---

# Respuestas

## A

**A1.**
- (a) 1400 · 1,75 / 30 ≈ **82 px**.
- (b) Z = f · 1,75 / h: con 230 px, 2450 / 230 ≈ **10,7 m**; con 30 px, ≈ **82 m**. El rango de 30–230 px medido en el club corresponde a jugadores entre ~11 y ~80 m de la cámara, si su focal fuera ~1400 (no la medimos: es una suposición).

**A2.** (2, 1, 10) → (1000 · 0,2 + 320, 1000 · 0,1 + 240) = **(520, 340)**. (4, 2, 20) → **(520, 340)**, el mismo píxel. Son dos puntos sobre el **mismo rayo** que sale de la cámara (el segundo es el doble del primero): la proyección no distingue la profundidad.

**A3.** t = −R·C = **(−1, −2, −3)**. t no es "dónde está la cámara": es dónde queda el **origen del mundo** visto en coordenadas de la cámara. Como `X_cam = R X + t`, para que la cámara (X = C) quede en el origen de sus propias coordenadas hace falta R C + t = 0.

**A4.**
- (a) K R d = K (0, 0, 1) = (320, 240, 1) → **(320, 240)**, el punto principal. Las rectas paralelas al eje óptico fugan al centro de la imagen (como las vías del tren mirando hacia adelante).
- (b) K (1, 0, 0) = (1000, 0, **0**): W = 0, un punto **en el infinito**. Las rectas paralelas al plano de la imagen se ven **paralelas**.

**A5.** Todos los puntos del rayo que sale del centro de la cámara y pasa por (900, 400) caen en ese píxel. El punto en el piso a 40 m y el punto a cierta altura a 25 m pueden estar sobre ese mismo rayo. Sin otra información (otra cámara, el tamaño aparente de la pelota, su sombra, la física de la trayectoria) no hay cómo elegir.

## B

**B1.** Columnas 1, 2 y 4: H = [[1, 0, 2], [0, 1, 3], [0, 0, 1]], una **traslación** en (2, 3).

**B2.** Traslación: **1** (2 grados de libertad). Similitud: **2** (4). Afín: **3** (6). Homografía: **4** (8). Cada punto da 2 ecuaciones, así que hacen falta grados de libertad / 2.

**B3.**
- (0, 0) → (0, 0); (0, 2) → W = 2 + 1 = 3 → **(0, 2/3)**; (0, 1) → W = 2 → **(0, 1/2)**.
- (a) El punto medio de las imágenes es (0, 1/3), pero la imagen del punto medio es (0, 1/2): **no coinciden**. La homografía no conserva razones de distancias.
- (b) La mitad de un segmento en píxeles no es la mitad en metros. Cualquier distancia, velocidad o promedio de posiciones hay que calcularlo **en metros**, después de H⁻¹, nunca en píxeles.

**B4.** El rayo desde la cámara (altura h = 9) que pasa por la cabeza (altura a = 1,75, a 30 m) baja 7,25 m en 30 m. Llega al piso a **30 · 9 / 7,25 ≈ 37,2 m**: lo ubica **~7 m más lejos** de la cámara. En general, D · h / (h − a). Es un error enorme: por eso se usa el **borde inferior** de la caja. Y cuanto más baja es la cámara, peor.

**B5.** f · tan(1°) ≈ 1400 · 0,0175 ≈ **24 px**. Una H calibrada en un frame queda corrida ~24 px al frame siguiente: en la lateral lejana, con ~0,06 m por píxel horizontal (D4), es **~1,4 m** de error después de un solo grado de paneo, y la cámara del club panea todo el tiempo. Con cámara que panea hace falta una H **por frame**.

## C

**C1.**
```
[ -1  -2  -1   0   0   0   3   6   3 ]
[  0   0   0  -1  -2  -1   5  10   5 ]
```

**C2.**
- (a) Fijar h₉ = 1 supone que h₉ ≠ 0. Si la homografía verdadera tiene h₉ = 0 (o muy chico: el origen de la cancha cae cerca de la "recta del infinito" de la imagen), esa normalización falla o se vuelve inestable. ‖h‖ = 1 no excluye ninguna homografía, y además convierte el problema en el de la SVD.
- (b) Si las 8 filas son independientes, rango 8: espacio nulo de **dimensión 1** (una recta: h salvo escala).
- (c) La configuración es degenerada: el rango baja y el espacio nulo tiene dimensión ≥ 2. Hay infinitas "homografías" que cumplen las 4 correspondencias.

**C3.**
- (a) Centroide (1, 1). Las cuatro distancias al centroide valen √2, así que la escala es 1: **T = [[1, 0, −1], [0, 1, −1], [0, 0, 1]]**.
- (b) Centroide (5, 5), distancias 5√2, escala √2 / (5√2) = 0,2: **T = [[0,2, 0, −1], [0, 0,2, −1], [0, 0, 1]]**. Los puntos normalizados son los mismos que en (a) desplazados: la normalización borra las unidades.

**C4.** u·x ≈ 1500 · 80 = **120.000**, contra 1 en la columna de los −1: cinco órdenes de magnitud. Las columnas de escalas muy distintas dan una matriz **mal condicionada**: un número de condición enorme amplifica los errores de redondeo (U1, apunte 03).

**C5.** Leído de derecha a izquierda, H·x tiene que: (1) normalizar el punto de la cancha con **Ts**; (2) aplicar Ĥ (normalizado → normalizado); (3) volver a píxeles con **Td⁻¹**. La otra opción aplicaría primero la normalización del **destino** a un punto del **origen**: no tiene sentido.

## D

**D1.** **Nada**. Con 4 puntos el sistema es exacto: la H pasa por los 4 clicks aunque estén mal. Para validar: más puntos (6 o más) y mirar los residuos; validación con puntos retenidos; y mirar la cancha reproyectada y la vista cenital.

**D2.** Ajustás **7** homografías, cada una con **6** puntos. En cada una, llevás el click que quedó afuera a la cancha con H⁻¹ y medís su distancia (en **metros**) al punto verdadero de `modelo_cancha`. Mirás el error de cada punto y el promedio. Es train/test (U3) con un solo dato de test por vez.

**D3.**
- (a) La diferencia entre dos posiciones tiene error de 0,3·√2 ≈ 0,42 m por eje. La longitud de un vector gaussiano 2D con desvío σ por eje tiene media σ·√(π/2): 0,42 · 1,25 ≈ **0,53 m por paso**.
- (b) 90 · 60 · 10 = 54.000 pasos × 0,53 ≈ **29 km**, sin moverse. Por eso el ruido **no se cancela, se suma** (U0), y por eso hay que suavizar antes de medir distancias (U8).
- (c) Un error **sistemático** (siempre corrido para el mismo lado) no genera "pasos" falsos: el jugador quieto queda quieto. Lo que hace es **deformar** las distancias reales (si la escala está un 5 % mal, los recorridos están un 5 % mal). Son dos errores de naturaleza distinta: el del *jitter* de la detección se acumula; el de la homografía, no.

**D4.** Medido con la cámara del TP (f = 1400, 9 m de altura, 12 m afuera de la lateral):

| Punto | Dónde cae en la imagen | 1 px horizontal | 1 px vertical |
|---|---|---|---|
| (50, 60), cerca | (960, 867) | ~0,015 m | ~0,04 m |
| (50, 34), centro | (960, 540) | ~0,03 m | ~0,17 m |
| (50, 0), lateral lejana | (960, 426) | ~0,06 m | **~0,51 m** |

Dos cosas: lejos, un píxel vale **~15 veces más** que cerca; y en la dirección **vertical** de la imagen (que es la profundidad en la cancha) vale **~9 veces más** que en la horizontal, porque la cancha se ve "aplastada" desde una cámara baja. Un click 2 px más arriba en la lateral lejana es un metro de error. Ahí conviene tener puntos de calibración, clickear con zoom y, sobre todo, **validar**.

## E

**E1.** w⁴ = 0,1296: N = ⌈log 0,01 / log 0,8704⌉ = ⌈33,2⌉ = **34**. Con w = 0,1: w⁴ = 10⁻⁴, **46.050** iteraciones.

**E2.** w⁸ = 1/256: N = **1177**, contra 72 con muestras de 4. Más de 16 veces más iteraciones, y el promedio del ruido igual se consigue al final, re-ajustando con todos los inliers. **No conviene**: siempre la muestra mínima.

**E3.** Sin reposición: C(27, 4) / C(30, 4) = 17.550 / 27.405 ≈ **0,640**, un poco menos que 0,9⁴ ≈ 0,656. Al sacar un bueno, quedan proporcionalmente menos buenos. La fórmula de iteraciones es **optimista** cuando hay pocos datos (por eso en el TP la simulación falla un poco más que la teoría).

**E4.** Con σ = 1,5: umbral 3 px es k = 2 → e^(−2) ≈ **13,5 %** de los buenos afuera. Umbral 5 px es k ≈ 3,3 → e^(−5,6) ≈ **0,4 %**. Con umbral 3 se pierde uno de cada siete clicks buenos: el umbral tiene que estar unas **3 veces por encima del ruido**.

**E5.** RANSAC busca el modelo con **más datos de acuerdo**. Si los datos mismos están sesgados (en el césped uniforme el flujo óptico no encuentra movimiento, así que los puntos "que no se mueven" son mayoría), el modelo "la cámara no se movió" junta muchos inliers y es **consistente, pero falso**. Verificación independiente: otro método que no comparta el sesgo (allá, la correlación de fase sobre toda la imagen), o una validación contra *keyframes* calibrados a mano.
