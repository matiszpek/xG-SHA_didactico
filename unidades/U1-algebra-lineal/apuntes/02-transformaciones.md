# 02 · Matrices como transformaciones

> **La idea en una frase:** una matriz es una función que deforma el plano dejando las líneas rectas y el origen fijo, y **sus columnas dicen a dónde van a parar los vectores base**.

**Videos:** 3Blue1Brown, caps. 3 y 4 (el 5, en 3D, es opcional pero lindo).

---

## 1. Transformación lineal

Una transformación T del plano es **lineal** si:
- las rectas siguen siendo rectas (no se curvan), y
- el origen queda fijo.

Dicho en fórmulas: `T(v + w) = T(v) + T(w)` y `T(c·v) = c·T(v)`.

**La consecuencia que lo es todo.** Como cualquier v se escribe `v = x·î + y·ĵ`, por linealidad:

$$T(v) = x\,T(\hat\imath) + y\,T(\hat\jmath)$$

Así que alcanza con saber **a dónde van î y ĵ** para saber a dónde va *cualquier* vector. Esos dos vectores destino se escriben como columnas, y eso es la matriz:

$$A = \begin{bmatrix} | & | \\ T(\hat\imath) & T(\hat\jmath) \\ | & | \end{bmatrix}
\qquad
A\begin{bmatrix}x\\y\end{bmatrix} = x \cdot \text{(columna 1)} + y \cdot \text{(columna 2)}$$

**Multiplicar una matriz por un vector es hacer una combinación lineal de sus columnas.** Es la misma receta de la sección anterior, pero con ingredientes nuevos.

## 2. Leer una matriz sin hacer cuentas

Volvamos a la pregunta 2 del diagnóstico.

**A = [[0, −1], [1, 0]]**
- Columna 1: î = (1, 0) va a (0, 1).
- Columna 2: ĵ = (0, 1) va a (−1, 0).

î pasa a apuntar hacia arriba y ĵ hacia la izquierda: es una **rotación de 90° antihoraria**.

**B = [[2, 0], [0, 1]]**
- î va a (2, 0) y ĵ se queda en (0, 1).

**Estira el eje x al doble** y deja el eje y igual.

Catálogo de las que más vamos a usar:

| Nombre | Matriz | Qué hace |
|---|---|---|
| Rotación θ | `[[cos θ, −sin θ], [sin θ, cos θ]]` | gira θ antihorario (con la y hacia arriba, ver nota) |
| Escala | `[[sx, 0], [0, sy]]` | estira cada eje por separado |
| Cizalla (*shear*) | `[[1, k], [0, 1]]` | "inclina" las verticales: ĵ va a (k, 1) |
| Reflexión en x | `[[1, 0], [0, −1]]` | espeja (da vuelta arriba con abajo) |
| Proyección sobre x | `[[1, 0], [0, 0]]` | aplasta todo sobre el eje x |

**Nota sobre la y en las imágenes.** En una imagen la y crece **hacia abajo**, así que una rotación "antihoraria" en la matemática se ve **horaria** en la pantalla. No cambia nada de la cuenta, solo cómo se ve. Pasa todo el tiempo y no es un bug.

## 3. Composición = producto (de derecha a izquierda)

Aplicar primero B y después A es aplicar la matriz `A·B`:

$$A(B\,v) = (AB)\,v$$

**Se lee de derecha a izquierda**, como la composición de funciones `f(g(x))`. La matriz que está más cerca del vector es la que se aplica primero.

¿Cómo se calcula AB sin la regla de memoria? Las columnas de AB son a dónde van î y ĵ después de aplicar B y después A. O sea: **cada columna de AB es A por la columna correspondiente de B**.

### `AB ≠ BA`, visto

Rotar 90° (R) y después estirar x al doble (S):
- `S·R`: primero rotás î hacia arriba, después estirás el eje x, pero î ya no está ahí. î termina en (0, 1).
- `R·S`: primero estirás î a (2, 0), después rotás. î termina en (0, 2).

Distinto resultado: el orden importa porque son operaciones geométricas distintas, no por una regla algebraica arbitraria.

### La pregunta 3 del diagnóstico, mirada de nuevo

`[[1, 2], [3, 4]] · [[0, 1], [1, 0]]`. La segunda matriz manda î a ĵ y ĵ a î: **intercambia los vectores base**.

Por la regla de las columnas, la columna 1 del producto es A·(0, 1), que es la columna 2 de A, y la columna 2 del producto es A·(1, 0), que es la columna 1 de A. **El producto es A con las columnas intercambiadas**: `[[2, 1], [4, 3]]`.

Multiplicar a la derecha mezcla columnas; multiplicar a la izquierda mezcla filas.

## 4. Por qué importa en visión

- **Transformar una imagen** (rotarla, escalarla, deformarla) es aplicar una matriz a las coordenadas de sus píxeles. Es el TP1.
- **Encadenar transformaciones** (cámara → imagen → recorte → red neuronal) es multiplicar matrices, y el orden importa.
- **Una red neuronal sin activaciones** es un producto de matrices, o sea **una sola matriz**: por más capas que tenga, es una única transformación lineal. Es la pregunta 6 del bloque 4 del diagnóstico, ahora con fundamento.

## 5. En NumPy

```python
import numpy as np
th = np.pi / 2
R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
S = np.array([[2, 0], [0, 1]])
R @ np.array([1, 0])         # ≈ [0, 1]
(S @ R)[:, 0], (R @ S)[:, 0] # ≈ [0, 1] y [0, 2]: la primera columna es a dónde va î

# Aplicar una matriz a MUCHOS puntos a la vez: puntos como filas (N, 2)
P = np.random.rand(100, 2)
P_rot = P @ R.T              # (N,2) @ (2,2): fila a fila es (R @ p)ᵀ = pᵀ Rᵀ
```

Ese `P @ R.T` merece un minuto: queremos `R @ p` para cada punto p (columna), pero tenemos los puntos como **filas**. Como `(R p)ᵀ = pᵀ Rᵀ`, multiplicar la matriz de filas por `Rᵀ` hace todo de una.

---

## Resumen para volver

- Transformación lineal: las rectas siguen rectas y el origen queda fijo.
- **Las columnas de la matriz son las imágenes de î y ĵ.** Con eso se "lee" cualquier matriz.
- `A v` = combinación lineal de las columnas de A con los coeficientes de v.
- `AB` = primero B y después A (de derecha a izquierda). En general `AB ≠ BA`.
- Multiplicar a la derecha mezcla columnas; a la izquierda, filas.
- Para muchos puntos como filas: `P @ M.T`.
