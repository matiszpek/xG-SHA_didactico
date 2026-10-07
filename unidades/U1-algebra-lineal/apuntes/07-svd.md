# 07 · Descomposición en valores singulares (SVD)

> **La idea en una frase:** **toda** matriz, cuadrada o no, se descompone en *rotar → estirar a lo largo de los ejes → rotar*. La SVD dice cuáles son esas rotaciones y esos estiramientos. Y la dirección que **menos** se estira es la solución de los problemas de "ajuste homogéneo", que es como se calcula la homografía.

**Videos:**
- MIT 18.06 (Strang), clase 29 (*Singular Value Decomposition*);
- o Steve Brunton, serie *Singular Value Decomposition*: *Overview* y *Mathematical Overview*.

---

## 1. La descomposición

$$A = U\,\Sigma\,V^\top$$

Para A de m×n:
- **Vᵀ** (n×n) es una rotación (o reflexión) en el espacio de **entrada**.
- **Σ** (m×n) es diagonal, con números σ₁ ≥ σ₂ ≥ … ≥ 0: los **valores singulares**. Estira cada eje por σᵢ.
- **U** (m×m) es una rotación (o reflexión) en el espacio de **salida**.

Se lee de derecha a izquierda, como siempre: rotar, estirar y rotar.

### La imagen que hay que tener en la cabeza

Tomá la **circunferencia unitaria** y aplicale A. Sale una **elipse**:
- los **semiejes** de la elipse miden σ₁ y σ₂;
- apuntan en las direcciones **u₁, u₂** (columnas de U);
- los vectores de la circunferencia que caen sobre esos semiejes son **v₁, v₂** (columnas de V): `A vᵢ = σᵢ uᵢ`.

Lo vas a graficar en el TP1.

## 2. Relación con los autovectores

$$A^\top A = V\,\Sigma^2\,V^\top$$

- Las columnas de V son los **autovectores** de AᵀA (que es simétrica: apunte 05).
- Los σᵢ² son sus **autovalores**.

A diferencia de los autovectores, la SVD **existe siempre**, para cualquier matriz, y sus rotaciones son siempre perpendiculares.

## 3. Qué te dicen los valores singulares

- **Rango** = cantidad de σᵢ distintos de cero.
- Si el último σ es **casi cero**, la matriz casi aplasta una dirección: está mal condicionada.
- **Número de condición** = σ₁ / σₙ (es lo que calcula `np.linalg.cond`).
- `|det(A)| = σ₁ · σ₂ · … · σₙ` (para cuadradas): el factor de área, de nuevo.

## 4. Aproximación de rango bajo

$$A = \sum_i \sigma_i\, u_i\, v_i^\top$$

Toda matriz es una **suma de "capas"** de rango 1, ordenadas por importancia. Quedarse con las k primeras da **la mejor aproximación de rango k** que existe (teorema de Eckart–Young).

Una imagen en grises es una matriz. Con k = 20 capas de 720, ya se reconoce el frame. Es una forma de compresión, y lo vas a probar en el TP1.

## 5. El truco que vamos a usar en U4: `min ‖Ax‖` con `‖x‖ = 1`

Hay problemas donde la ecuación es **homogénea**: `A x = 0`. Por ejemplo:
- todas las rectas `a x + b y + c = 0` que pasan por un conjunto de puntos;
- la homografía en el DLT.

`x = 0` siempre es solución, y no sirve. Con ruido, no hay otra solución exacta. Se busca:

$$\hat{\mathbf x} = \arg\min_{\|\mathbf x\| = 1} \|A\mathbf x\|$$

**Respuesta:** `x̂` es **la última columna de V**, el vector singular derecho del **valor singular más chico**. Es la dirección de entrada que A "menos estira", lo más cerca que hay de un vector del espacio nulo. El valor del mínimo es justamente σ_min.

¿Por qué? Escribí `x = V y`, que tiene el mismo largo porque V es una rotación. Entonces `‖Ax‖ = ‖U Σ Vᵀ V y‖ = ‖Σ y‖`, que con ‖y‖ = 1 es mínimo poniendo todo el peso en el último eje.

```python
U, S, Vt = np.linalg.svd(A)
x = Vt[-1]          # ¡ojo! NumPy devuelve Vᵀ: la última FILA de Vt es la última columna de V
```

## 6. Cuadrados mínimos totales: ajustar una recta "de verdad"

Recordá el problema del apunte 06: cuadrados mínimos ordinarios miden el error en **vertical** y fallan con rectas casi verticales.

Los **cuadrados mínimos totales** minimizan la **distancia perpendicular** de cada punto a la recta. La receta:

1. **Centrar** los puntos: restar la media `p̄`. La recta óptima pasa por el centroide.
2. Armar la matriz M de N×2 con los puntos centrados.
3. SVD de M:
   - **v₁** (la dirección de mayor dispersión) es la **dirección de la recta**;
   - **v₂** (la de menor dispersión) es la **normal** `(a, b)`.
4. `c = −(a, b) · p̄`.

Es exactamente el **apunte 05 aplicado a la covarianza**: `MᵀM` es (N veces) la matriz de covarianza de los puntos. La recta va en la dirección de mayor varianza, y eso es **PCA**.

Trata a x e y **por igual**, así que funciona para cualquier inclinación, vertical incluida. Lo implementás en el TP1 y comparás contra los ordinarios con una recta casi vertical.

## 7. Pseudo-inversa

Para cuadrados mínimos ordinarios, la SVD también da la solución más estable:

$$\hat{\mathbf x} = A^+ b, \qquad A^+ = V\,\Sigma^{+}\,U^\top$$

donde Σ⁺ invierte los σᵢ no nulos. Es lo que hace `np.linalg.lstsq` por dentro, y `np.linalg.pinv` la calcula.

---

## Resumen para volver

- `A = U Σ Vᵀ`: rotar, estirar (σ₁ ≥ σ₂ ≥ … ≥ 0) y rotar. Existe **siempre**.
- La circunferencia unitaria va a una elipse de semiejes σᵢ en las direcciones uᵢ, con `A vᵢ = σᵢ uᵢ`.
- V tiene los autovectores de AᵀA, y σᵢ² son sus autovalores.
- Rango = cantidad de σ > 0. Condición = σ₁/σₙ.
- Rango k: quedarse con las k primeras capas `σᵢ uᵢ vᵢᵀ`.
- **`min ‖Ax‖` con `‖x‖ = 1` → última columna de V** (`Vt[-1]` en NumPy). Es el corazón del DLT (U4).
- **Recta por cuadrados mínimos totales:** centrar y hacer la SVD; la normal es el último vector singular. Es PCA.
