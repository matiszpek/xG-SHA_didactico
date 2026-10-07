# 04 · Canny y la transformada de Hough

> **La idea en una frase:** Canny convierte la magnitud del gradiente en **bordes finos y continuos**: suaviza, deriva, se queda con los máximos y une con histéresis. Hough convierte esos píxeles sueltos en **rectas**: cada píxel "vota" por todas las rectas que pasan por él, y gana la más votada.

**Videos:**
- First Principles of CV, Módulo 2: *Edge Detection* (la parte de Canny) y *Boundary Detection* (Hough).

**Lectura:** Szeliski, 7.2.1 (Canny) y 7.4.2 (Hough).

---

## 1. Canny: qué se le pide a un detector de bordes

John Canny (1986) formuló tres criterios:
1. **Buena detección:** encontrar los bordes reales y no inventar bordes en el ruido.
2. **Buena localización:** el borde detectado tiene que estar donde está el borde real.
3. **Una sola respuesta por borde:** no una franja de 5 píxeles de ancho.

Los cinco pasos de abajo atacan esos tres criterios.

### Paso 1 — Suavizar (gaussiano, σ)
Contra el ruido (criterio 1). σ chico deja más detalle y más ruido; σ grande deja bordes más limpios pero mal localizados, y se pierden los bordes chicos (criterio 2).

### Paso 2 — Gradiente (Sobel)
Magnitud y orientación (apunte 03).

### Paso 3 — Supresión de no máximos (NMS)
La magnitud del gradiente alrededor de un borde forma una "loma" de varios píxeles de ancho. Para afinarla (criterio 3), un píxel **sobrevive solo si es mayor o igual que sus dos vecinos en la dirección del gradiente**, o sea, en la dirección *perpendicular* al borde.

¿Por qué en esa dirección? Porque a lo largo del borde la magnitud es parecida (es el mismo borde) y la que hay que adelgazar es la loma *transversal*.

Con una grilla de píxeles, la dirección se **cuantiza** en 4 opciones:

| θ (mod 180°) | El gradiente apunta… | Vecinos a comparar |
|---|---|---|
| ~0° | horizontal | izquierda y derecha |
| ~45° | abajo a la derecha (¡y hacia abajo!) | (y+1, x+1) y (y−1, x−1) |
| ~90° | vertical | arriba y abajo |
| ~135° | abajo a la izquierda | (y+1, x−1) y (y−1, x+1) |

El error clásico es pensar la diagonal con la y hacia arriba: queda "la otra diagonal", y los bordes diagonales quedan gruesos. El test `test_s4_nms_diagonal` lo atrapa.

### Paso 4 — Doble umbral
- **Fuertes:** magnitud > `alto`. Seguro son bordes.
- **Débiles:** `bajo` < magnitud ≤ `alto`. Dudosos.
- El resto se descarta.

### Paso 5 — Histéresis
Un débil se conserva **solo si está conectado a un fuerte** (con 8 vecinos, directamente o a través de otros débiles).

**Por qué funciona:** el ruido produce respuestas débiles **aisladas**, mientras que los bordes reales son **continuos**: un borde real que se debilita un tramo (una sombra, la pierna de un jugador encima de la línea) sigue conectado a sus tramos fuertes.

**Implementación sin recorrer píxeles:** partir de la máscara de fuertes y repetir *dilatar* (cada píxel pasa a True si algún vecino es True), recortar con la máscara de débiles, hasta que no cambie nada. Cada iteración "avanza" un píxel por los caminos débiles.

### Umbrales relativos
`bajo` y `alto` como **fracción del máximo** (por ejemplo, 0,1 y 0,25) hacen que no dependan del contraste de cada frame. Una relación típica es alto ≈ 2–3 × bajo.

## 2. Hough: de píxeles a rectas

**El problema:** Canny devuelve miles de píxeles de borde. De la cancha, los jugadores, la tribuna y el ruido. Algunas rectas están cortadas (un jugador parado encima). ¿Cuáles píxeles forman rectas, y qué rectas?

Ajustar por cuadrados mínimos (TP1) no sirve directamente: no sabés **qué** puntos van con **qué** recta, y un solo *outlier* arruina el ajuste.

### La idea: votar

Por cada píxel de borde pasan infinitas rectas. Cada píxel **vota por todas ellas**. Una recta real con 300 píxeles va a recibir 300 votos; las rectas "casuales" reciben pocos.

### ¿Cómo se parametriza una recta?

No con `y = m x + b`: m se va a infinito para las verticales. Es el mismo problema que los cuadrados mínimos ordinarios en el TP1. Se usa la **forma normal**:

$$x\cos\theta + y\sin\theta = \rho$$

- (cos θ, sin θ) es el vector **normal** a la recta y ρ es la **distancia (con signo)** desde el origen. Es la misma recta `(a, b, c) = (cos θ, sin θ, −ρ)` del TP1, ya normalizada.
- θ ∈ [0, π) y ρ ∈ [−D, D], con D = la diagonal de la imagen. Todo acotado y sin infinitos.

### El espacio de parámetros

Para un píxel fijo (x₀, y₀), las rectas que pasan por él cumplen `ρ(θ) = x₀ cos θ + y₀ sin θ`: una **sinusoide** en el plano (θ, ρ).

Píxeles **alineados** dan sinusoides que se **cruzan en un mismo punto** (θ*, ρ*): esa es la recta que los une.

Discretizando (θ, ρ) en una grilla, el **acumulador**:
1. Para cada θ (180 valores, por ejemplo) y para todos los píxeles a la vez: `ρ = x cos θ + y sin θ`, redondeado a la celda.
2. Contar votos por celda: `np.bincount`.
3. Los **picos** del acumulador son las rectas.

**Elegir picos** es otra supresión de no máximos: después de tomar el pico más alto, se borran sus vecinos (si no, el segundo "pico" es la misma recta corrida 1 píxel).

### Resolución y costo
- Celdas más finas en θ y ρ dan rectas más precisas, pero los votos se reparten: los picos se achatan y el ruido pesa más.
- Costo: O(N píxeles × n_θ). Una mejora clásica: cada píxel vota solo por los θ **cercanos a la orientación de su gradiente**. Es más rápido y más limpio.

### Hough inicializa y cuadrados mínimos refinan
Hough da una recta **robusta pero gruesa**, del ancho de una celda. Para precisión:
1. tomar los píxeles de borde cercanos a esa recta (`distancia_a_recta` del TP1, menos de ~2 px);
2. ajustarlos con **cuadrados mínimos totales** (TP1).

Esta dupla, "método robusto para encontrar candidatos + ajuste fino con los *inliers*", es exactamente la estructura de **RANSAC** en U4.

## 3. Pipeline para las líneas de la cancha

1. **Máscara de pasto** en HSV. **Erosionarla** unos píxeles: si no, el borde entre la cancha y la tribuna es el borde más fuerte del frame. Lección real del proyecto anterior: Hough encontraba prolijamente el contorno de la cancha contra la tribuna en vez de las líneas de cal.
2. **Candidatos a cal:** dentro del pasto, píxeles con **V alto y S bajo** (blanco).
3. **Canny** (o directamente la máscara de cal, adelgazada).
4. **Hough** → picos → **refinar** con cuadrados mínimos totales.
5. **Intersecciones** con `interseccion` (TP1): esquinas del área y cruces con la línea de medio. Son los puntos que necesita la homografía de U4.

**Lo que hay que saber de antemano:** con la cámara del club, muchos frames muestran **solo las laterales**, que son casi paralelas entre sí y no dan intersecciones útiles. Por eso el proyecto anterior terminó con una calibración **asistida** (detección automática como ayuda + clicks a mano). En el TP2 vas a ver hasta dónde llega lo automático en tus frames.

---

## Resumen para volver

- **Canny:** suavizar → gradiente → **NMS en la dirección del gradiente** (4 direcciones; ojo con la y hacia abajo) → doble umbral → **histéresis** (débiles conectados a fuertes, con 8 vecinos).
- Umbrales relativos al máximo; alto ≈ 2–3 × bajo.
- **Hough:** forma normal `x cos θ + y sin θ = ρ`, sin infinitos. Cada píxel es una sinusoide en (θ, ρ); los alineados se cruzan en un punto.
- Acumulador con `bincount` por θ. Picos con supresión de la vecindad.
- Hough encuentra candidatos y cuadrados mínimos totales refinan (la idea de RANSAC).
- En la cancha: erosionar la máscara de pasto, buscar cal (V alto, S bajo), Hough, refinar, intersecciones.
