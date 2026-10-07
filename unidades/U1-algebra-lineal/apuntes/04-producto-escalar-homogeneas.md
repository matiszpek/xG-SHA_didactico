# 04 · Producto escalar, cambio de base y coordenadas homogéneas

> **La idea en una frase:** el producto escalar mide **cuánto de un vector apunta en la dirección de otro**. Las coordenadas homogéneas agregan un 1 a cada punto para que **trasladar** (y más adelante proyectar en perspectiva) también sea multiplicar por una matriz.

**Videos:**
- 3Blue1Brown, caps. 9 (*Dot products and duality*) y 13 (*Change of basis*). Opcional: cap. 10 (*Cross products*).
- Stachniss, Photogrammetry I, clase 15 (*Homogeneous Coordinates*), los primeros ~30 minutos.

---

## 1. Producto escalar

$$v \cdot w = v_1 w_1 + v_2 w_2 = \|v\|\,\|w\|\cos\theta$$

**Geométricamente:** proyectá w sobre la recta de v. El producto escalar es (largo de esa sombra) × (largo de v).
- **> 0:** apuntan "para el mismo lado" (ángulo < 90°).
- **= 0:** son **perpendiculares** (ortogonales).
- **< 0:** apuntan para lados opuestos.

**Pregunta 1 del diagnóstico:** v = (3, 4), w = (1, 0).
- ‖v‖ = √(9 + 16) = 5.
- v·w = 3.
- cos θ = 3 / (5 · 1) = 0,6, así que θ ≈ 53,1°.

### Proyección

La componente de v en la dirección de un vector unitario u (‖u‖ = 1) es `(v·u) u`. Lo que queda, `v − (v·u) u`, es **perpendicular** a u.

Esa descomposición, "lo que está en la dirección más lo que es perpendicular", es la idea central de **cuadrados mínimos** (apunte 06).

### Distancia de un punto a una recta

Una recta se puede escribir como `a x + b y + c = 0`, con (a, b) **normal** (perpendicular) a la recta. Si normalizamos para que a² + b² = 1:

$$\text{distancia}(p, \text{recta}) = |a\,p_x + b\,p_y + c|$$

Es un producto escalar con la normal, más un corrimiento. Lo vas a implementar en el TP1.

### Dualidad (lo de 3Blue1Brown)

Hacer el producto escalar con un vector fijo w es una transformación lineal de 2D a 1D: una matriz de 1×2, `wᵀ`. "Vector" y "función lineal que devuelve un número" son dos caras de lo mismo. Va a volver en U6: cada neurona calcula `w·x + b`.

### Similitud coseno

`cos θ = v·w / (‖v‖‖w‖)` mide cuánto se parecen dos vectores en **dirección**, ignorando el largo. En U8 se usa para comparar *embeddings* de jugadores: dos recortes del mismo jugador deberían tener *embeddings* con coseno cercano a 1.

## 2. Cambio de base

Si tenés una base nueva {b₁, b₂} (escrita en coordenadas viejas) y la ponés como columnas de B:
- un vector con coordenadas **nuevas** x' está en coordenadas viejas en `x = B x'`;
- y al revés, `x' = B⁻¹ x`.

Una transformación M (escrita en la base vieja), expresada en la base nueva, es:

$$M' = B^{-1} M B$$

Se lee de derecha a izquierda: traducir a lo viejo, transformar, volver a lo nuevo. Este "sándwich" va a volver en los autovectores (apunte 05) y en la rotación alrededor de un punto (abajo).

## 3. El problema de la traslación

Trasladar (mover todo un vector t) **no es lineal**: mueve el origen, y una transformación lineal deja el origen fijo. No hay ninguna matriz de 2×2 que sume (tx, ty).

**El truco:** agregar una tercera coordenada que valga siempre 1.

$$(x, y) \;\longrightarrow\; \begin{bmatrix}x\\y\\1\end{bmatrix}
\qquad
\begin{bmatrix}1 & 0 & t_x\\0 & 1 & t_y\\0 & 0 & 1\end{bmatrix}\begin{bmatrix}x\\y\\1\end{bmatrix} = \begin{bmatrix}x + t_x\\y + t_y\\1\end{bmatrix}$$

La traslación ahora **es** una multiplicación. Y cualquier transformación lineal M de 2×2 se mete en la esquina:

$$T = \begin{bmatrix} M & t \\ 0\;\;0 & 1\end{bmatrix} \quad\text{(transformación afín: lineal + traslación)}$$

**¿Por qué funciona?** Geométricamente, el plano de la imagen pasa a ser el plano z = 1 dentro del espacio 3D. Una traslación de ese plano *es* una cizalla del espacio 3D, que sí es lineal (y deja fijo el origen 3D).

**Ventaja enorme:** todo se compone multiplicando matrices de 3×3. Rotar, trasladar, escalar y volver a trasladar es un solo producto.

### Rotar alrededor de un punto c (no del origen)

Es el sándwich: llevar c al origen, rotar, volver.

$$T = T(c)\; R(\theta)\; T(-c)$$

(De derecha a izquierda: primero `T(−c)`.) Lo implementás en el TP1.

## 4. Puntos y direcciones; la división por w

En coordenadas homogéneas:
- `(x, y, 1)` es un **punto**;
- `(x, y, 0)` es una **dirección** (un "punto en el infinito"): la traslación no la afecta (probalo).
- `(2x, 2y, 2)` representa **el mismo punto** que `(x, y, 1)`: para volver a 2D se divide por la tercera coordenada.

$$(X, Y, W) \;\longrightarrow\; (X/W,\; Y/W)$$

Con las afines, W siempre queda en 1 y la división no hace nada. Pero en U4, la homografía tiene la última fila `(h₇, h₈, h₉)` en vez de `(0, 0, 1)`, entonces **W cambia según el punto**. Esa división por W es **la perspectiva**: lo lejano se achica. Por eso tu función `aplicar` del TP1 tiene que dividir por W desde ya.

## 5. Rectas en homogéneas (bonus que vamos a usar)

La recta `a x + b y + c = 0` se representa con el vector `l = (a, b, c)`. Un punto `p = (x, y, 1)` está sobre la recta si y solo si:

$$l \cdot p = 0$$

Y como el **producto vectorial** `l₁ × l₂` da un vector perpendicular a los dos:
- **Intersección de dos rectas:** `p = l₁ × l₂`, y después se divide por la tercera coordenada.
- **Recta que pasa por dos puntos:** `l = p₁ × p₂`.

Si las rectas son paralelas, la intersección da W = 0: un punto en el infinito. Las líneas laterales de la cancha son paralelas en la realidad, pero en la imagen se cruzan en un punto finito: el **punto de fuga** (diagnóstico, bloque 5, pregunta 4). Lo vas a calcular en el TP1.

Producto vectorial en 3D (o `np.cross`):
$$a \times b = (a_2 b_3 - a_3 b_2,\; a_3 b_1 - a_1 b_3,\; a_1 b_2 - a_2 b_1)$$

## 6. En NumPy

```python
import numpy as np
P = np.array([[0, 0], [1, 0], [0, 1]], dtype=float)          # N puntos como filas
Ph = np.hstack([P, np.ones((len(P), 1))])                     # (N, 3) homogéneas
T = np.array([[1, 0, 5], [0, 1, 2], [0, 0, 1]], dtype=float)  # trasladar (5, 2)
Q = Ph @ T.T                                                  # (N, 3)
Q[:, :2] / Q[:, 2:3]                                          # volver a 2D dividiendo por W

l1 = np.array([1, 0, -2])   # x = 2
l2 = np.array([0, 1, -3])   # y = 3
p = np.cross(l1, l2); p[:2] / p[2]                            # → (2, 3)
```

---

## Resumen para volver

- `v·w = ‖v‖‖w‖cos θ`: el largo de la sombra × el largo. Si da 0, son perpendiculares.
- Distancia de un punto a la recta `ax + by + c = 0` (con a² + b² = 1): `|a x + b y + c|`.
- Cambio de base: `M' = B⁻¹ M B` (traducir, aplicar, volver).
- Homogéneas: `(x, y) → (x, y, 1)`. La traslación pasa a ser una matriz de 3×3. Todo se compone multiplicando.
- Rotar alrededor de c: `T(c) R T(−c)`.
- Para volver a 2D: **dividir por W**. En U4, esa división es la perspectiva.
- Rectas como vectores (a, b, c): intersección `l₁ × l₂`, recta por dos puntos `p₁ × p₂`. Paralelas: W = 0.
