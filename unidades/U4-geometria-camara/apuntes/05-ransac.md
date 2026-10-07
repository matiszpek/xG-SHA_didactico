# 05 · RANSAC: ajustar un modelo cuando hay datos basura

> **La idea en una frase:** en vez de ajustar con todos los datos (y dejar que los *outliers* tironeen), ajustá muchas veces con **muestras mínimas al azar** y quedate con el modelo con el que **más datos están de acuerdo**. La probabilidad dice cuántas veces hay que intentar.

**Videos:** First Principles of CV, *Image Stitching* (la parte de RANSAC). **Lectura:** Hartley & Zisserman, 4.7.

---

## 1. El problema

Cuadrados mínimos (U1) y el DLT suponen que todos los datos son "buenos con un poco de ruido". Un **outlier** los arruina:
- en U1 viste que un click a 50 px pesa 625 veces más que uno a 2 px;
- en el TP4 lo vas a ver: **3 correspondencias malas de 30** destruyen la homografía.

En la práctica los *outliers* son normales:
- una intersección de líneas detectada mal (TP2);
- una correspondencia de *features* equivocada (U5);
- un click en el lugar que no era.

## 2. El algoritmo (Fischler y Bolles, 1981)

Repetir:
1. Elegir al azar una **muestra mínima**: 4 correspondencias para una homografía, 2 puntos para una recta.
2. Ajustar el modelo **solo con esa muestra**.
3. Contar cuántos datos están **de acuerdo**: los ***inliers***, con error < umbral.
4. Si es el mejor conteo hasta ahora, guardarlo.

Al final, **re-ajustar** el modelo con todos los *inliers* del mejor conjunto. Así se usan todos los datos buenos, y no solo los 4 de la muestra.

**Por qué funciona:** basta con que **una** de las muestras sea toda de datos buenos. Ese modelo va a estar de acuerdo con todos los demás datos buenos, mientras que los modelos que salen de muestras con *outliers* están de acuerdo con pocos.

## 3. ¿Cuántas iteraciones? Probabilidad (U3)

Sea w la fracción de *inliers* y n el tamaño de la muestra:
- P(una muestra es toda de *inliers*) = wⁿ, si los datos son muchos y se eligen independientes;
- P(una muestra tiene al menos un *outlier*) = 1 − wⁿ;
- P(**ninguna** de N muestras es limpia) = (1 − wⁿ)ᴺ.

Queremos que esa probabilidad sea menor que 1 − p, con p la confianza (por ejemplo, 0,99):

$$N = \left\lceil \frac{\log(1 - p)}{\log(1 - w^n)} \right\rceil$$

Es el complemento de "al menos uno" de U3, otra vez.

| *Inliers* (w) | Homografía (n = 4) | Recta (n = 2) |
|---|---|---|
| 90 % | 5 | 3 |
| 70 % | 17 | 7 |
| 50 % | 72 | 17 |
| 30 % | 567 | 49 |

El tamaño de la muestra pesa muchísimo (wⁿ). Por eso siempre se usa la muestra **mínima**.

**RANSAC adaptativo:** no se sabe w de antemano. Se arranca con "muchas" iteraciones y, cada vez que se encuentra un conjunto de *inliers* más grande, se recalcula N con la fracción observada. Es lo que pide `ransac_homografia`.

## 4. El umbral

- Es la distancia máxima (en píxeles) para considerar que un dato "está de acuerdo".
- Va unas pocas veces por encima del ruido esperado: con clicks de ~1–2 px, entre 3 y 5 px.
- **Muy chico:** los buenos con un poco de ruido quedan afuera.
- **Muy grande:** entran *outliers* "cercanos".

## 5. Cuándo RANSAC falla (y miente)

- **Muestras degeneradas:** 4 puntos con 3 alineados dan una H basura que puede, por casualidad, juntar *inliers*. Las implementaciones serias descartan las muestras degeneradas.
- **Demasiados *outliers*:** con w = 0,1 y n = 4 hacen falta ~46.000 iteraciones.
- **Un modelo equivocado pero consistente:** RANSAC encuentra **lo que es consistente, no lo que es correcto**.

  En el proyecto anterior (D29), el flujo óptico sobre césped hacía que los únicos puntos que "sobrevivían" fueran los que no se movían. RANSAC los declaraba *inliers* del modelo "la cámara no se movió", con un **90 % de inliers**, justo en los casos donde la estimación era peor. Un número alto de *inliers* no prueba nada si los datos mismos están sesgados. Hay que **verificar con un método independiente** (allá: la correlación de fase).

---

## Resumen para volver

- **RANSAC:** muestras mínimas al azar → ajuste → contar *inliers* → quedarse con el mejor → **re-ajustar con todos los inliers**.
- Iteraciones: **N = log(1 − p) / log(1 − wⁿ)**. Con 50 % de inliers y n = 4, son 72. Siempre la muestra mínima.
- Adaptativo: recalcular N cuando mejora el conjunto de inliers.
- Umbral: unas pocas veces el ruido esperado.
- Encuentra lo **consistente**, no necesariamente lo **correcto**: verificar con otro método.
