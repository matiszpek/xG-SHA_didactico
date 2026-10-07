# 05 · Autovalores y autovectores

> **La idea en una frase:** un autovector es una dirección que la transformación **no gira**, solo la estira o la achica. El autovalor es **por cuánto** la estira.

**Videos:** 3Blue1Brown, caps. 14 y 15.

---

## 1. Definición

$$A v = \lambda v \qquad (v \neq 0)$$

Aplicar A a v da lo mismo que multiplicar v por el número λ: v queda **sobre su misma recta**.

- **λ = 2:** se estira al doble.
- **λ = 0,5:** se achica a la mitad.
- **λ = −1:** se da vuelta, pero sigue en la misma recta.
- **λ = 0:** se aplasta al origen. v está en el espacio nulo y det(A) = 0.

Cualquier múltiplo de un autovector también es autovector (con el mismo λ). Lo que importa es la **dirección**, no el largo.

## 2. Cómo se calculan (2×2)

`A v = λ v` equivale a `(A − λI) v = 0`, con v ≠ 0. Una matriz que manda un vector no nulo al cero **aplasta**, así que:

$$\det(A - \lambda I) = 0$$

Para `A = [[a, b], [c, d]]` eso da una cuadrática: `λ² − (a + d) λ + (ad − bc) = 0`.

**El truco rápido de 3Blue1Brown (cap. 15):**
- La suma de los autovalores es la **traza**: `a + d`.
- El producto de los autovalores es el **determinante**: `ad − bc`.
- Con la media `m = (a + d)/2` y el producto `p = ad − bc`:

$$\lambda = m \pm \sqrt{m^2 - p}$$

Después, para cada λ, el autovector sale de resolver `(A − λI) v = 0` (una recta de soluciones).

**Pregunta 6 del diagnóstico:** `[[2, 0], [0, 3]]`. m = 2,5 y p = 6, así que λ = 2,5 ± √(6,25 − 6) = 2,5 ± 0,5, o sea **2 y 3**. Autovectores (1, 0) y (0, 1). Para una matriz **diagonal**, los autovalores están en la diagonal y los autovectores son los ejes.

## 3. Ejemplos para entrenar el ojo

| Matriz | Autovectores | Autovalores | Por qué |
|---|---|---|---|
| `[[3, 1], [0, 2]]` | (1, 0) y (1, −1) | 3 y 2 | î no gira (la columna 1 es múltiplo de î) |
| Rotación 90° | **ninguno real** | ±i | toda dirección gira: no hay recta que quede fija |
| Cizalla `[[1, 1], [0, 1]]` | solo (1, 0) | 1 (doble) | el eje x se queda; todo lo demás se inclina |
| Escala `[[2, 0], [0, 2]]` | **todos** | 2 | estira todo igual |
| Proyección `[[1, 0], [0, 0]]` | (1, 0) y (0, 1) | 1 y 0 | x queda igual; y se aplasta |

## 4. Diagonalizar: elegir la base que simplifica todo

Si A tiene n autovectores independientes, tomarlos como base hace que A sea **diagonal** en esa base: en cada eje solo estira.

$$A = P D P^{-1}$$

P tiene los autovectores como columnas y D los autovalores en la diagonal. Es el sándwich del cambio de base del apunte 04.

**Para qué sirve:** las potencias se vuelven triviales: `Aᵏ = P Dᵏ P⁻¹`, y `Dᵏ` es elevar cada número de la diagonal. Aplicar una transformación 1000 veces deja de ser 1000 multiplicaciones.

## 5. Matrices simétricas: el caso que más vas a ver

Si `A = Aᵀ` (simétrica), entonces (teorema espectral):
- **todos los autovalores son reales**;
- **los autovectores son perpendiculares entre sí**.

Así, `A = Q D Qᵀ`, con Q una **rotación** (o reflexión). Una matriz simétrica es simplemente "**estirar a lo largo de ejes perpendiculares**", posiblemente girados.

¿Por qué importa tanto? Porque las matrices simétricas aparecen en todos lados en visión:
- **Matriz de covarianza** (U3, U8): sus autovectores son las direcciones en que más (y menos) se dispersa una nube de puntos, y sus autovalores son las varianzas en esas direcciones. Es la base de **PCA** y de cómo el filtro de Kalman representa la incertidumbre de la posición de un jugador (una elipse).
- **Tensor de estructura** (U5): el detector de esquinas de Harris mira sus dos autovalores.
  - Dos chicos: zona plana.
  - Uno grande: borde.
  - **Dos grandes: esquina.**
- **`AᵀA`**, que aparece en cuadrados mínimos (apunte 06) y en la SVD (apunte 07), siempre es simétrica.

## 6. En NumPy

```python
import numpy as np
A = np.array([[3, 1], [0, 2]], dtype=float)
lam, V = np.linalg.eig(A)       # V tiene los autovectores (normalizados) como COLUMNAS
lam                             # [3., 2.]
A @ V[:, 1], lam[1] * V[:, 1]   # iguales

S = np.array([[2, 1], [1, 2]], dtype=float)   # simétrica
lam, Q = np.linalg.eigh(S)      # eigh: para simétricas (más estable, autovalores ordenados)
Q.T @ Q                         # ≈ identidad: autovectores perpendiculares
```

---

## Resumen para volver

- `A v = λ v`: v no gira, solo se estira por λ.
- `det(A − λI) = 0`. En 2×2: λ = m ± √(m² − p), con m = traza/2 y p = det.
- Traza = suma de los autovalores. Det = producto de los autovalores.
- Rotaciones: sin autovectores reales. Diagonales: los ejes.
- `A = P D P⁻¹`: en la base de autovectores, A solo estira.
- **Simétrica:** autovalores reales y autovectores perpendiculares. Covarianza, Harris y `AᵀA`.
- `np.linalg.eig` en general; `np.linalg.eigh` para simétricas.
