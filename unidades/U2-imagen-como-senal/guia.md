# U2 — Guía de ejercicios

Un bloque por sesión. Lápiz primero, NumPy para verificar y recién al final las respuestas.

---

## A — Color e histogramas (sesión 1)

**A1.** Pasá a HSV, a mano, el píxel de pasto (60, 140, 55). Dejá H en grados y S y V en [0, 1].

**A2.** El mismo pasto a la sombra, con 40 % de la luz: (24, 56, 22). Calculá su HSV. ¿Qué cambió y qué no? ¿Por qué?

**A3.** Una camiseta blanca (230, 230, 225) y una negra (30, 30, 35).
- (a) Calculá H y S de las dos.
- (b) ¿Sirve el tono para separarlas? ¿Qué usarías en su lugar?
- (c) ¿Por qué ese "algo" es peligroso con sol y sombra?

**A4.** Dos tonos rojos: H = 355° y H = 5°.
- (a) ¿Cuánto da `|a − b|`? ¿Cuánto es la distancia real?
- (b) Escribí la fórmula de distancia circular, vectorizada para arrays.

**A5.** Ecualizá a mano la imagen 1×8 `[50, 50, 50, 50, 100, 100, 200, 200]` con la fórmula del apunte.

**A6.** ¿Por qué `lut[img]` aplica la tabla a todos los píxeles de una vez? ¿Qué shape tiene el resultado si `img` es (720, 1280)?

## B — Convolución (sesión 2)

**B1.** Con f = `[0, 0, 1, 2, 3, 0, 0]` y k = `[1, 0, −1]` (índices −1, 0, 1), y relleno con ceros, calculá a mano:
- (a) la correlación;
- (b) la convolución.

¿Qué relación hay entre los dos resultados? ¿Por qué?

**B2.** Convolucionás una imagen negra con un único píxel blanco en el medio, usando un kernel cualquiera de 3×3. ¿Qué ves en la salida? ¿Y con correlación?

**B3.** ¿Son separables?
- (a) `[[1, 2, 1], [2, 4, 2], [1, 2, 1]] / 16`
- (b) `[[0, 1, 0], [1, −4, 1], [0, 1, 0]]` (el Laplaciano)

Justificá con el rango. Si es separable, escribí los dos vectores.

**B4.** Un frame 1080p con un kernel gaussiano de 31×31. ¿Cuántas multiplicaciones hacés en total con el kernel 2D? ¿Y separable?

**B5.** Desenfocás con un kernel de promedio de 21×21 usando relleno con ceros. ¿Qué le pasa al borde de la imagen? ¿Qué modo usarías?

**B6.** Con σ = 2:
- (a) ¿cuántos coeficientes tiene el kernel con radio ceil(3σ)?
- (b) ¿por qué 3σ y no 2σ ni 5σ?
- (c) ¿por qué hay que normalizarlo para que sume 1?

**B7.** Una ventana de 3×3 con valores `[10, 10, 10, 255, 10, 10, 10, 10, 10]` (un píxel "sal"). ¿Cuánto da la media? ¿Y la mediana? ¿Qué filtro conviene y por qué?

## C — Gradiente (sesión 3)

**C1.** Con f(x, y) = x² + 3xy:
- (a) las derivadas parciales;
- (b) el gradiente en (1, 2);
- (c) la derivada en la dirección (0, 1) y en la dirección (1, 1)/√2;
- (d) ¿en qué dirección crece más rápido f en (1, 2), y cuánto?

**C2.** Con L(w, b) = (w·x + b − y)²:
- (a) calculá ∂L/∂w y ∂L/∂b;
- (b) con x = 2, y = 5, w = 1 y b = 0, ¿hacia dónde hay que mover (w, b) para bajar L?

**C3.** Aplicás Sobel Sx a la imagen I(x, y) = 3x (una rampa).
- (a) ¿Cuánto da gx en el interior? ¿Por qué no da 3?
- (b) ¿Cuánto da gy?

**C4.** Dos píxeles vecinos tienen ruido independiente con desvío 5. ¿Qué desvío tiene su diferencia? Si el "escalón" real entre ellos es de 6 niveles, ¿se distingue del ruido?

**C5.** En un píxel, gx = 0 y gy = 10.
- (a) ¿Hacia dónde apunta el gradiente en la imagen?
- (b) ¿Cómo es el borde: horizontal o vertical?
- (c) ¿Cuánto vale θ?

**C6.** Dibujá el perfil de intensidad, cruzando una línea de cal de 4 px de ancho sobre el pasto, y su derivada. ¿Cuántos máximos de |derivada| hay? ¿Qué te va a devolver Canny?

## D — Canny y Hough (sesión 4)

**D1.** En la supresión de no máximos, ¿qué pasaría si **siempre** compararas con los vecinos izquierdo y derecho, sin mirar θ? Pensá en un borde horizontal.

**D2.** Histéresis en 1D: magnitudes `[0,9, 0,5, 0,5, 0,1, 0,5, 0,95]`, con bajo = 0,3 y alto = 0,8. ¿Qué píxeles sobreviven?

**D3.** Hough:
- (a) Escribí la sinusoide ρ(θ) del punto (3, 4). ¿Cuánto vale en θ = 0 y en θ = 90°? ¿En qué θ es máxima, y cuánto vale ahí?
- (b) ¿Qué (θ, ρ) corresponde a la recta que pasa por (0, 5) y (5, 0)?

**D4.** ¿Por qué Hough no usa la forma y = m x + b? Relacionalo con lo que viste en B2 del TP1.

**D5.** ¿Cuántas celdas tiene el acumulador para una imagen de 1280×720, con 180 valores de θ y paso de ρ de 1 px?

**D6.** En la cancha, Hough te devuelve dos picos con θ casi igual y ρ que difieren en ~4 px. ¿Qué es probablemente? ¿Cómo lo resolverías?

---

## Respuestas

<details><summary>A</summary>

**A1.** R, G, B = 0,235, 0,549, 0,216. M = 0,549 (es G), m = 0,216, C = 0,333.
- V = 0,549.
- S = C/M = 0,607.
- H = 60·((B − R)/C + 2) = 60·(−0,059 + 2) ≈ **116,5°**, un verde amarillento.

**A2.** H ≈ 116,5° y S ≈ 0,607 quedan **iguales**; V baja a 0,22. Al escalar los tres canales por 0,4, los cocientes que definen H y S no cambian.

**A3.**
- (a) Blanca: H = 60° y S = 0,022. Negra: H = 240° y S = 0,14. El tono **existe** numéricamente, pero con S tan baja es ruido: un píxel de compresión cambia H por completo.
- (b) No. Hay que usar V (o L de Lab).
- (c) V cambia con la iluminación: al sol, una camiseta negra puede ser más clara que una blanca en sombra. Solución del proyecto anterior: comparar contra el pasto vecino, que recibe la misma luz.

**A4.**
- (a) 350°. La distancia real es 10°.
- (b) `d = np.abs(a - b); d = np.minimum(d, 360 - d)`.

**A5.** Histograma: 50 → 4, 100 → 2, 200 → 2. CDF: 4, 6, 8. cdf_min = 4 y N = 8.
- lut[50] = 0.
- lut[100] = round(2/4 · 255) = round(127,5) = 128.
- lut[200] = 255.

Resultado: `[0, 0, 0, 0, 128, 128, 255, 255]`.

**A6.** Es indexado avanzado: cada valor de `img` se usa como índice dentro de `lut`. El resultado tiene la shape de `img`, (720, 1280).
</details>

<details><summary>B</summary>

**B1.**
- (a) La correlación es `g[x] = f[x−1] − f[x+1]`, que da `[0, −1, −2, −2, 2, 3, 0]`.
- (b) La convolución es `[0, 1, 2, 2, −2, −3, 0]`.

Una es la opuesta de la otra: dar vuelta `[1, 0, −1]` es `[−1, 0, 1]`, que es el mismo kernel con el signo cambiado.

**B2.** Con convolución aparece **el kernel tal cual** (es la respuesta al impulso). Con correlación aparece dado vuelta.

**B3.**
- (a) Sí: rango 1. Es `[1, 2, 1]ᵀ [1, 2, 1] / 16`.
- (b) No: rango 2. Se puede escribir como la suma de dos separables (la segunda derivada en x más la segunda derivada en y).

**B4.** Hay 1920·1080 ≈ 2,07 M píxeles.
- 2D: 961 multiplicaciones por píxel, ≈ 1.990 M en total.
- Separable: 62 por píxel, ≈ 129 M en total, **15 veces menos**.

**B5.** El borde se **oscurece**, porque promediás con el negro de afuera. Conviene `"espejo"` o `"replicar"`.

**B6.**
- (a) 13 coeficientes: radio 6.
- (b) ±3σ junta el 99,7 % del peso. Con 2σ el kernel queda "cortado" (el 5 % del peso se pierde y el filtro deja de ser bien gaussiano); con 5σ solo gastás cómputo en pesos ≈ 0.
- (c) Para no cambiar el brillo medio: una zona constante tiene que seguir igual.

**B7.** La media da 37,2 y la mediana da 10. Conviene la **mediana**: un solo valor extremo no la mueve (es robusta). La media "contagia" el error a toda la ventana.
</details>

<details><summary>C</summary>

**C1.**
- (a) ∂f/∂x = 2x + 3y y ∂f/∂y = 3x.
- (b) ∇f(1, 2) = (8, 3).
- (c) En (0, 1): 3. En (1, 1)/√2: 11/√2 ≈ 7,78.
- (d) En la dirección (8, 3)/‖(8, 3)‖, con pendiente ‖∇f‖ = √73 ≈ 8,54.

**C2.**
- (a) Con e = wx + b − y: ∂L/∂w = 2e·x y ∂L/∂b = 2e.
- (b) e = 2 + 0 − 5 = −3, así que ∇L = (2·(−3)·2, 2·(−3)) = (−12, −6). Para bajar L hay que moverse en **−∇L = (12, 6)**: subir w y b. Tiene sentido, porque la predicción (2) quedó por debajo de y (5).

**C3.**
- (a) gx = 8·3 = **24**. El suavizado [1, 2, 1] suma 4, y la diferencia central abarca 2 píxeles: factor 8.
- (b) gy = 0.

**C4.** 5·√2 ≈ **7,1**. Un escalón de 6 queda **por debajo** del desvío del ruido de la diferencia: es indistinguible píxel a píxel. Hay que suavizar (promediar varios píxeles) para bajar el ruido.

**C5.**
- (a) Apunta hacia **abajo**: la imagen se aclara hacia abajo.
- (b) El borde es **horizontal**.
- (c) θ = 90°.

**C6.** El perfil sube al entrar en la línea, queda alto 4 px y baja al salir. La derivada tiene un pico positivo y uno negativo: **dos máximos** de |derivada|. Canny devuelve **dos bordes paralelos**, uno de cada lado de la línea.
</details>

<details><summary>D</summary>

**D1.** En un borde horizontal, el gradiente es vertical. A izquierda y derecha (a lo largo del borde) la magnitud es parecida, así que casi todos los píxeles de la "loma" sobreviven: el borde queda **grueso**. Además, los bordes horizontales se pueden fragmentar por pequeñas variaciones a lo largo.

**D2.** `[1, 1, 1, 0, 1, 1]`. Los dos 0,5 de la izquierda se conectan con el 0,9 y el 0,5 de la derecha con el 0,95. El 0,1 no pasa ni el umbral bajo.

**D3.**
- (a) ρ(θ) = 3 cos θ + 4 sin θ. En θ = 0 vale 3 y en θ = 90° vale 4. Es máxima en θ = atan2(4, 3) ≈ 53,1°, donde vale **5**: la distancia del punto al origen.
- (b) La recta es x + y = 5. Su normal es (1, 1)/√2, así que θ = 45° y ρ = 5/√2 ≈ 3,54.

**D4.** Para las rectas verticales, m es infinito: no entran en un acumulador finito. Es el mismo problema que los cuadrados mínimos ordinarios con la línea de medio campo (TP1, B2).

**D5.** D = ceil(√(1280² + 720²)) = 1469. Hay 2·1469 + 1 = 2939 valores de ρ, y 2939 × 180 ≈ **529.000 celdas**.

**D6.** Probablemente son **los dos bordes de una misma línea de cal** (C6). Se resuelve:
- promediando las dos rectas;
- o detectando la cal como franja (máscara de blanco adelgazada) en vez de usar bordes;
- o con una vecindad de supresión de picos mayor que el ancho de la línea.
</details>
