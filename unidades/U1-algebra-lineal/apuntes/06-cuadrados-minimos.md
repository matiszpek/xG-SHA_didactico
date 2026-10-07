# 06 · Cuadrados mínimos

> **La idea en una frase:** cuando `Ax = b` no tiene solución (más ecuaciones que incógnitas, y con ruido), la "mejor" x es la que hace que `Ax` caiga en la **proyección** de b sobre el espacio columna de A. Eso da las **ecuaciones normales** `AᵀA x = Aᵀb`.

**Videos:** MIT 18.06 (Gilbert Strang), clases 15 (*Projections onto Subspaces*) y 16 (*Projection Matrices and Least Squares*).

---

## 1. El problema

Querés ajustar la recta `y = m x + c` a los N puntos que marcaste sobre la línea lateral de la cancha. Cada punto da una ecuación:

$$\begin{bmatrix} x_1 & 1\\ x_2 & 1\\ \vdots & \vdots \\ x_N & 1\end{bmatrix}\begin{bmatrix} m\\ c\end{bmatrix} = \begin{bmatrix} y_1\\ y_2\\ \vdots\\ y_N\end{bmatrix}
\qquad\Longleftrightarrow\qquad A\,\mathbf{x} = b$$

Son N ecuaciones con 2 incógnitas. Con ruido (tu click nunca cae exacto sobre la línea), **no hay ninguna recta que pase por todos**: b no está en el espacio columna de A. Es la pregunta 7 del diagnóstico: "¿es un sistema incompatible?" Sí. ¿Y entonces qué?

## 2. La mejor solución posible

Si no podemos lograr `Ax = b`, buscamos que `Ax` quede **lo más cerca posible** de b:

$$\hat{\mathbf x} = \arg\min_{\mathbf x} \|A\mathbf x - b\|^2 = \arg\min \sum_i (m x_i + c - y_i)^2$$

Es la suma de los cuadrados de los **residuos verticales**: la distancia vertical de cada punto a la recta. De ahí el nombre.

## 3. La geometría: proyectar

`A x` recorre el espacio columna de A (todas las combinaciones de sus columnas): un plano dentro del espacio de N dimensiones. b está fuera de ese plano.

**¿Cuál es el punto del plano más cercano a b?** Su **proyección ortogonal**: la "sombra" de b sobre el plano. En ese punto, el error `e = b − A x̂` es **perpendicular** al plano, o sea, perpendicular a cada columna de A:

$$A^\top (b - A\hat{\mathbf x}) = 0 \quad\Longrightarrow\quad \boxed{A^\top A\, \hat{\mathbf x} = A^\top b}$$

Esas son las **ecuaciones normales**. "Normal" de perpendicular, no de común. No hizo falta cálculo: salió de la geometría del apunte 04.

`AᵀA` es una matriz chica (2×2 en la recta) y **simétrica** (apunte 05). Si las columnas de A son independientes, es invertible y la solución es única.

### Con cálculo, para U3 y U6

Lo mismo sale de derivar `‖Ax − b‖²` respecto de x e igualar a cero: el gradiente es `2Aᵀ(Ax − b)`. Cuando en U3 entrenemos el modelo de xG, no va a haber una fórmula cerrada como esta, y vamos a **bajar por ese gradiente** de a pasos. Ese es el descenso por gradiente del diagnóstico.

## 4. Cómo se resuelve en la práctica

```python
import numpy as np
x = np.array([100., 300., 500., 700., 900.])       # clicks sobre una línea de la cancha
y = np.array([412., 431., 449., 472., 488.])
A = np.column_stack([x, np.ones_like(x)])           # (N, 2)
m, c = np.linalg.solve(A.T @ A, A.T @ y)            # ecuaciones normales

# Lo que se usa en la vida real (más estable numéricamente):
(m2, c2), *_ = np.linalg.lstsq(A, y, rcond=None)
```

En el TP1 implementás las ecuaciones normales a mano (con `solve`, que está permitido), y comparás contra `np.polyfit` o `lstsq`.

## 5. Lo que cuadrados mínimos supone (y dónde falla)

**1. Mide el error en vertical.** Supone que las x son exactas y que el error está solo en y. Para una recta **casi vertical** eso es un desastre:
- la pendiente m tiende a infinito;
- los residuos verticales no tienen sentido;
- y la recta x = 5 directamente no se puede escribir como y = mx + c.

En la imagen, las líneas de la cancha tienen **cualquier** inclinación. → La solución son los **cuadrados mínimos totales** (apunte 07): medir la distancia **perpendicular** a la recta, que trata a x e y por igual.

**2. Un solo punto malo arruina todo.** Al elevar al cuadrado, un punto lejos (un *outlier*: un click en el lugar equivocado, un jugador parado sobre la línea) pesa muchísimo. → La solución es **RANSAC** (U4): ajustar con subconjuntos chicos al azar y quedarse con el que más puntos "convence".

**3. Mal condicionamiento.** Si los x están todos amontonados o son valores muy grandes (píxeles del orden de 1000, mezclados con el 1 de la columna de unos), `AᵀA` queda casi singular y la solución es inestable. → La solución es **normalizar** los datos antes (centrar y escalar). Es exactamente la "normalización de Hartley" del DLT en U4.

## 6. Dónde aparece en visión

- Ajustar líneas de la cancha a puntos detectados (TP1, U2).
- **Homografía con más de 4 puntos** (U4): el sistema tiene más ecuaciones que incógnitas, así que se resuelve por cuadrados mínimos (en su versión homogénea, con SVD).
- Calibración de cámara.
- **Lucas-Kanade** (U5): el flujo óptico en una ventanita se resuelve con ecuaciones normales de 2×2. ¡La misma `AᵀA`!
- Regresión lineal, que es la base de todo ML.

---

## Resumen para volver

- `Ax = b` sin solución → minimizar `‖Ax − b‖²`.
- Geometría: `A x̂` es la proyección de b sobre el espacio columna, y el error es ⊥ a las columnas.
- **Ecuaciones normales:** `AᵀA x̂ = Aᵀb`. Se resuelven con `solve`, no con `inv`.
- Gradiente de `‖Ax − b‖²`: `2Aᵀ(Ax − b)`. Se usa en U3 y U6.
- Supuestos que fallan: error vertical (se arregla con cuadrados mínimos totales), *outliers* (RANSAC) y escala (normalizar).
