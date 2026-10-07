# U3 — Guía de ejercicios

Un bloque por sesión. En probabilidad, **escribí el evento con palabras antes de calcular**: la mitad de los errores son de planteo.

---

## A — Probabilidad básica y Bayes (sesión 1)

**A1.** P(al menos un 6 en 4 tiradas de un dado). Hacelo por complemento.

**A2.**
- (a) Dá un ejemplo de fútbol de dos eventos excluyentes y otro de dos independientes.
- (b) ¿Pueden dos eventos con probabilidad positiva ser excluyentes **e** independientes a la vez? Justificá.

**A3.** El detector de pelota (90 % de *recall*, 5 % de falsas alarmas):
- (a) P(pelota | detecta) cuando la pelota está en el 20 % de los frames.
- (b) Lo mismo cuando está en el 2 % de los recortes.
- (c) Explicá en una frase por qué cambia tanto.
- (d) Hacé (b) "contando 1000 casos", como 3Blue1Brown.

**A4.** Un detector de jugadores, contra tus etiquetas, da 80 aciertos, 20 detecciones falsas y 40 jugadores no detectados.
- (a) Calculá la precisión y el *recall*.
- (b) Escribí cada una como una probabilidad condicional.

**A5.** Dos tiros, cada uno con xG 0,4 (independientes). Calculá P(0 goles), P(exactamente 1) y P(2 goles). Verificá que suman 1.

## B — Variables aleatorias (sesión 2)

**B1.** Para un dado, calculá E[X], Var(X), E[2X + 1] y Var(2X + 1).

**B2.** Un equipo tira con xG 0,1, 0,3 y 0,5.
- (a) Goles esperados y desvío.
- (b) ¿Es "raro" que haga 0 goles? ¿Y 3?

**B3.** Dá una densidad que valga 2 en algún punto. ¿Cómo es posible, si las probabilidades no pasan de 1?

**B4.** Con X uniforme en {−1, 0, 1} e Y = X², calculá Cov(X, Y). ¿Son independientes?

**B5.** Estimás P(0 goles) por Monte Carlo con 10.000 simulaciones y te da 0,30. ¿Cuál es el error típico de esa estimación? ¿Cuántas simulaciones necesitás para reducirlo a la mitad?

**B6.** Explicá por qué agregar un tiro de prob p a la distribución de goles es convolucionar con [1 − p, p]. Hacelo a mano: empezá con un tiro de 0,4 y agregá otro de 0,4.

## C — La normal (sesión 3)

**C1.** Alturas ~ N(175, 7²) cm. Aproximá con la regla 68–95–99,7:
- (a) P(entre 168 y 182);
- (b) P(> 189).

**C2.** Las velocidades de pique tienen media 22 km/h y desvío 4. Calculá el z de 30 km/h y de 50 km/h. ¿Qué concluís de cada uno?

**C3.** Calculá la matriz de covarianza (dividiendo por N) de los puntos (0, 0), (2, 1) y (4, 2), y su determinante. ¿Qué significa el resultado?

**C4.** Con Σ = diag(4, 1) y μ = 0:
- (a) ¿Cuánto miden los semiejes de la elipse de 2 desvíos?
- (b) ¿Cuál es la distancia de Mahalanobis de (2, 1)? ¿Y la euclídea?

**C5.** Con Σ = [[2, 1], [1, 2]]: autovalores, autovectores y forma de la elipse. ¿Qué dice sobre la relación entre x e y?

## D — Máxima verosimilitud y logística (sesión 4)

**D1.** Con 7 caras en 10 tiradas, escribí log L(p), derivá y encontrá p̂.

**D2.** Demostrá que σ'(z) = σ(z)(1 − σ(z)). ¿Cuánto vale σ'(0)?

**D3.**
- (a) Con p = 0,2, ¿cuánto valen los odds y el log-odds?
- (b) Si w·x + b sube 1, ¿por cuánto se multiplican los odds?
- (c) Si el peso de "cabeza" es −0,8, ¿qué significa?

**D4.** Para **un** tiro, derivá ∂/∂w de [y log p + (1 − y) log(1 − p)], con p = σ(w·x + b), paso por paso con la regla de la cadena.

**D5.** Un paso de descenso por gradiente a mano: X = [[1], [−1]] (ya estandarizada), y = [1, 0], w = 0, b = 0 y η = 1.
- (a) Calculá p, el gradiente y los nuevos w y b.
- (b) ¿Tiene sentido la dirección del cambio?

**D6.** ¿Por qué hay que estandarizar distancia (yardas) y ángulo (radianes) antes del descenso por gradiente? ¿Qué tiene que ver con el número de condición de U1?

## E — Evaluación (sesión 5)

**E1.** Con el 9,8 % de goles:
- (a) la log loss de predecir siempre 0,098;
- (b) la *accuracy* de decir "nunca gol".

¿Cuál de las dos líneas de base es útil para comparar un modelo de xG?

**E2.** AUC a mano: y = [0, 0, 1, 1] y p = [0,1, 0,4, 0,35, 0,8].

**E3.** Tu modelo le da p ≈ 0,3 a 200 tiros y entraron 45.
- (a) ¿Está bien calibrado en ese intervalo?
- (b) Si un equipo tiene exactamente esos 200 tiros en una temporada, ¿cuántos goles "espera" el modelo y cuántos hizo?

**E4.** Multiplicás todas las predicciones por 0,5. ¿Qué pasa con la AUC? ¿Y con la log loss? ¿Y con la calibración?

**E5.** ¿Por qué separar por partido y no por tiro? Dá un ejemplo concreto de información que "se filtra" si separás por tiro.

**E6.** Marcaste 25 tiros de Hebraica (3 goles) y el modelo les asigna en total 2,1 de xG.
- (a) ¿Podés concluir que el modelo subestima en amateur?
- (b) ¿Qué harías para poder concluirlo?

---

## Respuestas

<details><summary>A</summary>

**A1.** 1 − (5/6)⁴ ≈ **0,518**.

**A2.**
- (a) Excluyentes: "gol" y "atajado" en el mismo tiro. Independientes (en el modelo): gol en el tiro 1 y gol en el tiro 7.
- (b) No. Si son excluyentes, P(A ∩ B) = 0, pero P(A)P(B) > 0. Saber que pasó uno te asegura que el otro no: es la dependencia máxima.

**A3.**
- (a) 0,18/0,22 ≈ **0,82**.
- (b) 0,018/(0,018 + 0,049) ≈ **0,27**.
- (c) Con la pelota en muy pocos casos, las falsas alarmas sobre el 98 % "vacío" superan a las detecciones reales.
- (d) De 1000 recortes, 20 tienen pelota y el detector ve 18. De los 980 vacíos, dice "pelota" en 49. De 67 alarmas, 18 son reales: 27 %.

**A4.**
- (a) Precisión = 80/100 = **0,8**. *Recall* = 80/120 ≈ **0,67**.
- (b) Precisión = P(real | detectado). *Recall* = P(detectado | real).

**A5.**
- P(0) = 0,6² = 0,36.
- P(1) = 2·0,4·0,6 = 0,48.
- P(2) = 0,16.

Suman 1.
</details>

<details><summary>B</summary>

**B1.** E[X] = 3,5 y Var(X) = 35/12 ≈ 2,92. E[2X + 1] = 8 y Var(2X + 1) = 4·35/12 ≈ 11,67 (el +1 no dispersa).

**B2.**
- (a) E = 0,9. Var = 0,09 + 0,21 + 0,25 = 0,55, así que σ ≈ 0,74.
- (b) P(0) = 0,315: no es nada raro. P(3) = 0,015: raro, pero pasa.

**B3.** Una uniforme en [0, 0,5] vale 2 en todo el intervalo. Las probabilidades son **áreas**: 2 · 0,5 = 1.

**B4.** E[X] = 0, E[X³] = 0 y E[X²] = 2/3. Cov = E[X·X²] − E[X]E[X²] = 0 − 0 = **0**. No son independientes: conocer X determina Y.

**B5.** √(0,3·0,7/10.000) ≈ **0,0046**. Para reducir el error a la mitad hacen falta **40.000** simulaciones (4 veces más).

**B6.** Para tener k goles después del tiro nuevo: o tenías k y erraste (d[k]·(1 − p)), o tenías k − 1 y la metiste (d[k − 1]·p). Eso es una convolución.
- Con un tiro: [0,6, 0,4].
- Agregando otro, [0,6, 0,4] * [0,6, 0,4] = [0,36, 0,48, 0,16]. Coincide con A5.
</details>

<details><summary>C</summary>

**C1.**
- (a) μ ± σ, así que ≈ **68 %**.
- (b) Más de 2σ por encima: ≈ 2,5 % (exacto: 2,3 %).

**C2.** z(30) = 2: un pique raro pero real. z(50) = 7: imposible para una normal razonable. Es un error (salto de tracking), no un jugador.

**C3.** La media es (2, 1). Los desvíos son (−2, −1), (0, 0) y (2, 1). Σ = [[8/3, 4/3], [4/3, 2/3]] y det = 16/9 − 16/9 = **0**. Los puntos están **alineados** (y = x/2): la "elipse" es un segmento y Σ no es invertible.

**C4.**
- (a) Los semiejes miden 2·√4 = 4 en x y 2·√1 = 2 en y.
- (b) d_M = √(2²/4 + 1²/1) = √2 ≈ 1,41. La euclídea es √5 ≈ 2,24: en x "cuesta menos" alejarse.

**C5.** λ = 3 con autovector (1, 1) y λ = 1 con autovector (1, −1). La elipse es alargada en la diagonal y = x, con desvíos √3 y 1. x e y están **positivamente correlacionadas** (ρ = 1/2).
</details>

<details><summary>D</summary>

**D1.** log L = 7 log p + 3 log(1 − p). La derivada es 7/p − 3/(1 − p); igualando a 0 sale **p̂ = 0,7**.

**D2.** σ = (1 + e^{−z})⁻¹, así que σ' = e^{−z}/(1 + e^{−z})² = σ · e^{−z}/(1 + e^{−z}) = σ(1 − σ). En z = 0: 0,5·0,5 = **0,25**.

**D3.**
- (a) Odds = 0,2/0,8 = 0,25 y log-odds = ln 0,25 ≈ −1,39.
- (b) Por e ≈ 2,72.
- (c) A igual posición, de cabeza los odds de gol se multiplican por e^{−0,8} ≈ 0,45: menos de la mitad.

**D4.** Con z = w·x + b y p = σ(z):
1. ∂/∂p [y log p + (1 − y) log(1 − p)] = y/p − (1 − y)/(1 − p).
2. ∂p/∂z = p(1 − p).
3. El producto da y(1 − p) − (1 − y)p = y − p.
4. ∂z/∂w = x.

Total: **(y − p)·x**. Para la pérdida (con el signo menos y el promedio): Xᵀ(p − y)/N.

**D5.**
- (a) p = [0,5, 0,5] y e = p − y = [−0,5, 0,5]. dw = (1·(−0,5) + (−1)·0,5)/2 = −0,5 y db = 0. Entonces w = 0 − 1·(−0,5) = **0,5** y b = 0.
- (b) Sí: w > 0 hace que x = 1 (el gol) tenga p > 0,5 y que x = −1 (el no-gol) tenga p < 0,5.

**D6.** Con escalas distintas, la pérdida es un valle muy alargado (mal condicionado): un η que sirve para una dirección es enorme o minúsculo para la otra, y el descenso hace zigzag. Estandarizar lo "redondea". Es el mismo problema que el número de condición grande de U1: la escala de los datos determina qué tan estable es el problema numérico.
</details>

<details><summary>E</summary>

**E1.**
- (a) ≈ **0,32**.
- (b) **90,2 %**.

La log loss constante es una base útil: un buen xG tiene que bajarla clara (por ejemplo, a ~0,27). La *accuracy* de 90 % hace parecer bueno a un modelo inútil.

**E2.** Los 4 pares (gol, no-gol): 0,35 > 0,1 ✓, 0,35 > 0,4 ✗, 0,8 > 0,1 ✓ y 0,8 > 0,4 ✓, así que **AUC = 3/4 = 0,75**.

**E3.**
- (a) Entró el 22,5 % contra un 30 % predicho: el modelo **sobreestima** en ese intervalo, si el intervalo tiene suficientes tiros. Con 200 tiros, el error típico de la frecuencia es ~3 puntos, así que la diferencia es real.
- (b) El modelo espera 60 goles e hizo 45.

**E4.** La AUC **no cambia**: el orden es el mismo. La log loss **empeora**. La calibración se rompe: todo queda subestimado a la mitad.

**E5.** Con split por tiro, el rebote de una jugada puede ir a test y el primer tiro a train. Comparten la posición de los defensores, el arquero y el partido. También quedan en train los tiros del mismo partido, con el mismo arquero y la misma cancha. El test deja de representar "un partido nuevo".

**E6.**
- (a) No. Con 25 tiros, la cantidad de goles tiene un desvío de ~1,3 (√Σp(1 − p)): 3 contra 2,1 está totalmente dentro del ruido.
- (b) Etiquetar **cientos** de tiros, con su resultado, de partidos amateur. Recién ahí comparar la calibración (frecuencia real contra xG por intervalo) con un error chico. Mientras tanto, se reporta como **no medido**.
</details>
