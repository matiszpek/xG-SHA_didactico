# U1 — Guía de ejercicios

Un bloque por sesión.
- **Lápiz primero.** Los ejercicios de "sin cuentas" se responden **dibujando**: hacé el dibujo de î y ĵ antes y después.
- Después verificás con NumPy, si aplica, y recién al final mirás la respuesta.

---

## A — Vectores y bases (sesión 1)

**A1.** Escribí (5, 1) como combinación lineal de b₁ = (1, 1) y b₂ = (1, −1). ¿Cuáles son las coordenadas de (5, 1) en la base {b₁, b₂}?

**A2.** ¿Son base del plano?
- (a) (1, 2) y (2, 4)
- (b) (1, 2) y (2, 3)
- (c) (1, 0), (0, 1) y (1, 1)

Justificá cada una con una frase.

**A3.** ¿Cuál es el span de (1, 0, 0), (0, 1, 0) y (1, 1, 0) en el espacio? ¿Son independientes?

**A4.** Dos píxeles valen (100, 20, 20) y (200, 40, 40) en RGB. ¿Qué relación tienen como vectores? ¿Qué significa eso en términos de color? ¿Por qué eso sugiere que, para separar equipos por camiseta, conviene mirar la **dirección** del vector color más que su largo?

## B — Matrices como transformaciones (sesión 2)

**B1.** Sin cuentas, decí qué hace cada matriz (dibujá a dónde van î y ĵ):
- (a) `[[1, 0], [0, -1]]`
- (b) `[[0, 1], [1, 0]]`
- (c) `[[1, 0.5], [0, 1]]`
- (d) `[[0.5, 0], [0, 0.5]]`
- (e) `[[-1, 0], [0, -1]]`

**B2.**
- (a) Escribí la matriz que rota 30° antihorario, con números.
- (b) Escribí la matriz que **primero** estira x al doble y **después** rota 90° antihorario. ¿En qué orden se multiplican?

**B3.** Con R = rotación de 90° y C = `[[1, 1], [0, 1]]` (cizalla), calculá RC y CR. Describí en palabras qué hace cada una y explicá por qué son distintas.

**B4.** Tenés N puntos como **filas** en P de shape (N, 2) y una matriz M de 2×2. ¿Por qué para transformarlos se hace `P @ M.T` y no `P @ M`? Probalo con M = rotación de 90° y P = `[[1, 0]]`.

## C — Determinante, inversa y espacios (sesión 3)

**C1.** Calculá e interpretá geométricamente el determinante de:
- (a) `[[3, 0], [0, 2]]`
- (b) `[[1, 2], [2, 4]]`
- (c) `[[0, 1], [1, 0]]`
- (d) una rotación cualquiera
- (e) `[[1, 5], [0, 1]]`

**C2.** El cuadrado [0, 1] × [0, 1] se transforma con `[[2, 1], [1, 3]]`. ¿Qué área tiene la figura resultante? ¿Qué figura es?

**C3.** Con A = `[[1, 2], [2, 4]]`:
- (a) Describí su espacio columna y su espacio nulo.
- (b) ¿Tiene solución `Ax = (1, 3)`? ¿Y `Ax = (2, 4)`? Si tiene, escribí **todas** las soluciones.

**C4.** Calculá la inversa de `[[2, 1], [1, 1]]` con la fórmula de 2×2 y verificá que `A A⁻¹ = I`.

**C5.** Un amigo marca 4 puntos de la cancha para calcular una homografía y tres de ellos caen casi sobre la misma línea lateral. Con lo que viste de determinante y rango, explicá en dos líneas por qué eso es una mala idea.

## D — Producto escalar y homogéneas (sesión 4)

**D1.**
- (a) Ángulo entre (1, 1) y (1, 0).
- (b) Proyección de (2, 3) sobre la dirección de (1, 1).
- (c) ¿Cuánto vale el producto escalar entre un vector y uno perpendicular?

**D2.** Distancia del punto (3, 4) a la recta 3x + 4y − 10 = 0. (Normalizá primero.)

**D3.** Escribí la matriz homogénea de 3×3 que rota 90° antihorario **alrededor del punto (100, 50)**. Verificá que (100, 50) queda fijo.

**D4.** Con coordenadas homogéneas y producto vectorial:
- (a) intersección de x + y − 4 = 0 y x − y = 0;
- (b) intersección de x + y − 4 = 0 y x + y − 6 = 0. ¿Qué significa el resultado?
- (c) la recta que pasa por (0, 0) y (2, 1).

**D5.** Aplicale la traslación T(5, 2) en homogéneas a `(1, 0, 1)` y a `(1, 0, 0)`. ¿Por qué el segundo no se mueve? ¿Qué representa?

## E — Autovectores (sesión 5)

**E1.** Autovalores y autovectores de `[[2, 1], [1, 2]]`. Verificá que los autovectores son perpendiculares. ¿Por qué tenía que pasar?

**E2.** Autovalores (con el truco de la media y el producto) y autovectores de `[[4, 1], [2, 3]]`.

**E3.** Sin cuentas, decí los autovectores y los autovalores de:
- (a) la reflexión `[[-1, 0], [0, 1]]`;
- (b) una rotación de 30°;
- (c) `[[3, 0], [0, 3]]`.

**E4.** Tenés las posiciones de los clicks que hiciste sobre la línea lateral de la cancha (una nube alargada en diagonal). Calculás la matriz de covarianza de esos puntos y sus autovectores. ¿Qué representa el autovector del autovalor más grande? ¿Y el del más chico? ¿Qué tendría que valer el autovalor chico si tus clicks fueran perfectos?

## F — Cuadrados mínimos (sesión 6)

**F1.** Ajustá y = m x + c a los puntos (0, 1), (1, 3), (2, 4) y (3, 4) **a mano**, con las ecuaciones normales.

**F2.** Con la recta de F1, calculá los residuos y verificá que el vector de residuos es perpendicular a las dos columnas de A. ¿Qué tiene que ver eso con la geometría de la proyección?

**F3.** Los puntos (5, 0), (5, 1), (5, 2) y (5, 3) están sobre una recta vertical. Armá AᵀA para ajustar y = m x + c y calculá su determinante. ¿Qué pasa y por qué?

**F4.** Uno de tus clicks quedó 50 px lejos de la línea, porque clickeaste un jugador. ¿Cuánto pesa en la suma de cuadrados comparado con un click a 2 px? ¿Qué te dice eso sobre los cuadrados mínimos y los datos sucios?

## G — SVD (sesión 7)

**G1.** Para A = `[[0, -2], [1, 0]]`, calculá AᵀA, sus autovalores y, de ahí, los valores singulares de A. ¿A qué elipse manda A a la circunferencia unitaria?

**G2.** Puntos (0, 0), (1, 1), (2, 2,1) y (3, 2,9).
- (a) Calculá el centroide.
- (b) Sin hacer la SVD, ¿qué dirección aproximada esperás para v₁ y para v₂?
- (c) Escribí la recta `a x + b y + c = 0` aproximada.
- (d) Verificá con `np.linalg.svd`.

**G3.** En el problema `min ‖Ax‖` con `‖x‖ = 1`:
- (a) ¿Por qué hace falta la condición ‖x‖ = 1?
- (b) Si el valor singular más chico de A es exactamente 0, ¿qué significa?

**G4.** Una imagen en grises de 720×1280 tiene 921.600 números. Si la aproximás con rango k = 20, ¿cuántos números tenés que guardar (U, Σ y V truncadas)? ¿Qué porcentaje del original es?

---

## Respuestas

<details><summary>A</summary>

**A1.** a + b = 5 y a − b = 1, así que a = 3 y b = 2: (5, 1) = 3b₁ + 2b₂. Coordenadas en la nueva base: (3, 2).

**A2.**
- (a) No: son paralelos (el segundo es el doble del primero) y su span es una recta.
- (b) Sí: no son paralelos.
- (c) No: generan el plano, pero son 3 y el tercero es redundante.

**A3.** El plano z = 0. Son dependientes: (1, 1, 0) = (1, 0, 0) + (0, 1, 0).

**A4.** El segundo es el doble del primero: misma dirección, distinto largo. Es el mismo color (mismo tono) con más brillo. Al sol y a la sombra, la misma camiseta cambia sobre todo el **largo** del vector, no la dirección. Por eso la dirección es más estable: es la idea detrás del tono en HSV y de la "cromaticidad".
</details>

<details><summary>B</summary>

**B1.**
- (a) Reflexión sobre el eje x (invierte y).
- (b) Reflexión sobre la recta y = x: intercambia los ejes.
- (c) Cizalla horizontal: ĵ va a (0,5, 1) y las verticales se inclinan.
- (d) Achica todo a la mitad.
- (e) Rotación de 180° (o reflexión respecto del origen).

**B2.**
- (a) `[[cos30, −sin30], [sin30, cos30]] ≈ [[0.866, −0.5], [0.5, 0.866]]`.
- (b) R·S = `[[0, −1], [1, 0]] · [[2, 0], [0, 1]] = [[0, −1], [2, 0]]`. S va a la **derecha** porque se aplica primero.

**B3.**
- RC = `[[0, −1], [1, 1]]`: primero inclina y después rota.
- CR = `[[1, −1], [1, 0]]`: primero rota y después inclina.

Son distintas porque la cizalla "sabe" cuál es el eje horizontal: si rotás antes, inclinás en otra dirección.

**B4.** Queremos `M p` para cada punto p (columna). Con filas: `(M p)ᵀ = pᵀ Mᵀ`. `[[1, 0]] @ R.T = [[0, 1]]` (correcto: î rotado 90°). `[[1, 0]] @ R = [[0, −1]]` (rotó −90°: aplicó Mᵀ, que para una rotación es la inversa).
</details>

<details><summary>C</summary>

**C1.**
- (a) 6: las áreas se multiplican por 6.
- (b) 0: aplasta el plano a la recta y = 2x.
- (c) −1: conserva el área pero da vuelta la orientación (es una reflexión).
- (d) 1: las rotaciones no cambian áreas ni orientación.
- (e) 1: la cizalla inclina sin cambiar el área. Es el "mazo de cartas" que se corre.

**C2.** Área = |det| = 2·3 − 1·1 = 5. Es un paralelogramo con lados (2, 1) y (1, 3).

**C3.**
- (a) Espacio columna: la recta de dirección (1, 2), o sea y = 2x. Núcleo: la dirección (2, −1), porque A(2, −1) = (0, 0).
- (b) (1, 3) no está sobre y = 2x, así que no tiene solución. (2, 4) sí: hay infinitas, x = (2, 0) + t(2, −1) para todo t real.

**C4.** det = 1, así que A⁻¹ = `[[1, −1], [−1, 2]]`.

**C5.** Si los puntos están casi alineados, no "abren" el plano: la información que dan es casi de una recta. El sistema del DLT queda casi singular (algún valor singular ≈ 0 y número de condición enorme), y un error chico en un click se convierte en una homografía muy distinta. Es lo que pasó en el proyecto anterior con cuadriláteros muy achatados.
</details>

<details><summary>D</summary>

**D1.**
- (a) cos θ = 1/√2, así que θ = 45°.
- (b) u = (1, 1)/√2; (v·u) u = (5/√2)(1, 1)/√2 = (2,5, 2,5).
- (c) 0.

**D2.** Normalizar dividiendo por √(9 + 16) = 5: 0,6x + 0,8y − 2 = 0. Distancia = |0,6·3 + 0,8·4 − 2| = |1,8 + 3,2 − 2| = **3**.

**D3.** T(c) R T(−c) = `[[0, −1, 150], [1, 0, −50], [0, 0, 1]]`. Para (100, 50): x' = −50 + 150 = 100 e y' = 100 − 50 = 50. ✓

**D4.**
- (a) (1, 1, −4) × (1, −1, 0) = (−4, −4, −2), así que (2, 2).
- (b) (1, 1, −4) × (1, 1, −6) = (−2, 2, 0): W = 0, un punto en el infinito en la dirección (−1, 1), que es justamente la dirección de las dos rectas. Las paralelas "se cortan en el infinito".
- (c) (0, 0, 1) × (2, 1, 1) = (−1, 2, 0): la recta −x + 2y = 0, o sea y = x/2. ✓
</details>

<details><summary>D5 · E</summary>

**D5.** (1, 0, 1) → (6, 2, 1): el punto se trasladó. (1, 0, 0) → (1, 0, 0): con W = 0, la columna de traslación se multiplica por 0. Representa una **dirección**, y las direcciones no se trasladan.

**E1.** m = 2 y p = 3, así que λ = 2 ± 1 = **3 y 1**. Autovectores (1, 1) y (1, −1), que son perpendiculares porque la matriz es simétrica (teorema espectral).

**E2.** m = 3,5 y p = 10, así que λ = 3,5 ± √(12,25 − 10) = 3,5 ± 1,5 = **5 y 2**. Para λ = 5, (1, 1); para λ = 2, (1, −2).

**E3.**
- (a) (1, 0) con λ = −1 (se da vuelta) y (0, 1) con λ = 1 (queda igual).
- (b) No tiene autovectores reales.
- (c) Todos los vectores son autovectores, con λ = 3.

**E4.** El autovector del autovalor grande es la dirección de la línea: la de mayor dispersión. El del chico es la normal a la línea. El autovalor chico es la varianza de los clicks *perpendicular* a la línea. Si los clicks fueran perfectos, valdría **0**. Es exactamente cuadrados mínimos totales (apunte 07).
</details>

<details><summary>F</summary>

**F1.** AᵀA = `[[Σx², Σx], [Σx, N]] = [[14, 6], [6, 4]]` y Aᵀy = `[Σxy, Σy] = [23, 12]`. Resolviendo: **m = 1** y **c = 1,5**, o sea y = x + 1,5.

**F2.** Residuos y − ŷ = (−0,5, 0,5, 0,5, −0,5).
- Contra la columna de x: 0·(−0,5) + 1·0,5 + 2·0,5 + 3·(−0,5) = 0.
- Contra la columna de unos: la suma da 0.

Es la condición `Aᵀe = 0`: el error es perpendicular al espacio columna, porque ŷ es la proyección de y.

**F3.** AᵀA = `[[100, 20], [20, 4]]`, con det = 400 − 400 = **0**. Las columnas de A (x = 5 siempre, y la de unos) son paralelas: la recta vertical x = 5 no se puede escribir como y = mx + c. Hacen falta cuadrados mínimos totales.

**F4.** 50² = 2500 contra 2² = 4: **625 veces más**. Un solo outlier tironea la recta como si fueran cientos de puntos buenos. Cuadrados mínimos no es robusto, y por eso existe RANSAC (U4).
</details>

<details><summary>G</summary>

**G1.** AᵀA = `[[1, 0], [0, 4]]`, con autovalores 1 y 4, así que **σ = 2 y 1**. La circunferencia va a una elipse de semiejes 2 y 1. Concretamente, A manda (0, 1) a (−2, 0) y (1, 0) a (0, 1): la elipse tiene el eje largo horizontal (largo 2) y el corto vertical (largo 1).

**G2.**
- (a) Centroide = (1,5, 1,5).
- (b) Los puntos están casi sobre y = x: v₁ ≈ (1, 1)/√2 y v₂ ≈ (1, −1)/√2.
- (c) Aproximadamente 0,71x − 0,71y + 0 = 0, o sea y ≈ x.
- (d) NumPy da v₁ ≈ (0,714, 0,701).

**G3.**
- (a) Sin la condición, x = 0 siempre da ‖Ax‖ = 0, y no sirve. Con la condición ‖x‖ = 1 se pide "la mejor dirección", no el vector cero.
- (b) Que existe una solución exacta de Ax = 0 distinta de cero. A tiene un espacio nulo no trivial, y los datos son perfectamente consistentes, sin ruido.

**G4.** U truncada: 720·20. Σ: 20. V truncada: 1280·20. Total: 14.400 + 20 + 25.600 = **40.020** números, ~4,3 % del original.
</details>
