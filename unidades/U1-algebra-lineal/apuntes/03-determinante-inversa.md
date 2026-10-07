# 03 · Determinante, inversa, rango y los espacios de una matriz

> **La idea en una frase:** el determinante dice **por cuánto se multiplican las áreas**. Si da 0, la transformación aplasta el plano a una recta o un punto, y eso **no se puede deshacer**.

**Videos:** 3Blue1Brown, caps. 6, 7 y 8.

---

## 1. El determinante como factor de área

Tomá el cuadradito de lado 1 que forman î y ĵ. La transformación A lo convierte en un paralelogramo, formado por las dos columnas de A. El **determinante** es el área (con signo) de ese paralelogramo.

Como todo se transforma "igual" en todos lados, **cualquier** región multiplica su área por det(A).

$$\det\begin{bmatrix}a & b\\ c & d\end{bmatrix} = ad - bc$$

Interpretación del signo y del valor:

| det(A) | Significado |
|---|---|
| 3 | las áreas se triplican |
| 0,5 | las áreas se reducen a la mitad |
| −1 | las áreas se conservan, pero el plano **se da vuelta** (como mirarlo en un espejo) |
| **0** | **todo se aplasta** a una recta (o a un punto): el área pasa a ser 0 |

**Pregunta 5 del diagnóstico:** `[[2, 1], [4, 2]]` da det = 2·2 − 1·4 = 0. Las dos columnas, (2, 4) y (1, 2), son paralelas: todo el plano cae sobre la recta que generan. **El área se pierde.**

Propiedad importante, y obvia con la geometría:

$$\det(AB) = \det(A)\,\det(B)$$

Si B multiplica las áreas por 2 y A por 3, hacer las dos cosas las multiplica por 6.

En 3D, el determinante es el factor de **volumen**.

## 2. Inversa: deshacer

La inversa A⁻¹ es la transformación que **deshace** lo que hizo A: `A⁻¹ A = I` (la identidad, que no mueve nada).

¿Cuándo existe? Cuando A **no aplastó** nada. Si A llevó el plano a una recta, muchos puntos distintos cayeron sobre el mismo punto de la recta, y no hay forma de saber de cuál vino cada uno.

$$A \text{ es invertible} \iff \det(A) \neq 0$$

Tu respuesta del diagnóstico (det ≠ 0 y Gauss-Jordan con `[A | I] → [I | A⁻¹]`) estaba bien: era la parte de la cuenta. Esta es la parte de *por qué*.

Para 2×2:
$$\begin{bmatrix}a & b\\ c & d\end{bmatrix}^{-1} = \frac{1}{ad-bc}\begin{bmatrix}d & -b\\ -c & a\end{bmatrix}$$

(Fijate cómo aparece el determinante dividiendo: si es 0, explota.)

**Regla de oro numérica:** casi nunca hay que *calcular* la inversa. Para resolver `Ax = b`, se usa `np.linalg.solve(A, b)`, que es más rápido y más preciso que `np.linalg.inv(A) @ b`.

## 3. Rango, espacio columna y espacio nulo

**Espacio columna** de A: el span de sus columnas. Son todos los resultados posibles `A x`, o sea, *a dónde puede llegar* la transformación.

**Rango** de A: la dimensión del espacio columna.
- Rango 2 en el plano: no aplasta nada (invertible).
- Rango 1: aplasta a una recta.
- Rango 0: todo al origen.

**Espacio nulo** (o núcleo) de A: todos los x con `A x = 0`. Son los vectores que la transformación **manda al origen**, los que "se pierden".
- Si A es invertible, el único es x = 0.
- Si det = 0, hay toda una recta (o más) de vectores que caen en el 0.

### Todo junto: el teorema que conecta todo

Para una matriz cuadrada A de n×n, estas afirmaciones son **todas equivalentes**:

- det(A) ≠ 0
- A es invertible
- las columnas de A son linealmente independientes
- el rango de A es n
- el espacio nulo es solo {0}
- `A x = b` tiene solución única para todo b

Si una falla, fallan todas. Esto es lo que más vas a usar.

### `Ax = b`, geométricamente

Resolver `A x = b` es preguntar: **¿qué vector x, al transformarlo, cae en b?**
- Si A es invertible: hay exactamente uno, `x = A⁻¹ b`.
- Si A aplasta y b está **sobre** la recta de llegada (en el espacio columna): hay infinitas soluciones. Cualquier solución más cualquier cosa del espacio nulo también es solución.
- Si A aplasta y b está **fuera** del espacio columna: **no hay solución**. ← Este es el caso de cuadrados mínimos (apunte 06).

## 4. Matrices no cuadradas

Una matriz de m×n lleva vectores de n dimensiones a m dimensiones.
- **3×2:** del plano al espacio. Las 2 columnas son a dónde van î y ĵ, ahora como vectores 3D: el plano queda "metido" dentro del espacio.
- **2×3:** del espacio al plano. Es una **proyección**: inevitablemente se pierde una dimensión.

**Esto es una cámara.** Una cámara proyecta el mundo 3D en una imagen 2D, y por eso es imposible saber la profundidad de un punto a partir de una sola imagen.
- Es la ambigüedad de altura de la pelota que viste en el diagnóstico (bloque 5, pregunta 10).
- La homografía de U4 la evita con un truco: si sabemos que el punto está **sobre el plano de la cancha**, el problema vuelve a ser de plano a plano, y ahí sí es invertible.

## 5. En visión

- **Homografía degenerada:** si los 4 puntos que marcaste están casi alineados, la matriz que sale tiene det ≈ 0 y no sirve.
- **DLT** (U4): la homografía es el vector del **espacio nulo** de un sistema de ecuaciones. Encontrar el espacio nulo (o, con ruido, lo más cercano a uno) es el corazón del método.
- `np.linalg.cond(A)`: el **número de condición** mide qué tan cerca está A de aplastar algo. Un número enorme significa que pequeños errores en los datos dan errores enormes en la solución.

```python
import numpy as np
A = np.array([[2, 1], [4, 2]])
np.linalg.det(A)            # 0.0
np.linalg.matrix_rank(A)    # 1
B = np.array([[2, 1], [4, 2.001]])
np.linalg.cond(B)           # ~ 12.500: casi singular
```

---

## Resumen para volver

- det = factor de área (con signo). det < 0: da vuelta el plano. det = 0: aplasta.
- `det(AB) = det(A) det(B)`.
- Invertible ⟺ det ≠ 0 ⟺ columnas independientes ⟺ rango completo ⟺ núcleo = {0}.
- Espacio columna: a dónde se puede llegar. Espacio nulo: lo que se pierde.
- `Ax = b`: una, infinitas o ninguna solución, según esos espacios.
- m×n: de n a m dimensiones. Una cámara es una proyección 3D → 2D: se pierde la profundidad.
- Usar `np.linalg.solve`, no `inv`.
