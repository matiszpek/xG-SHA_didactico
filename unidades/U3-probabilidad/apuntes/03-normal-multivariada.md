# 03 · La normal, en una y en varias dimensiones

> **La idea en una frase:** la normal aparece cuando muchos efectos chicos se suman. En varias dimensiones, su forma es una **elipse** cuyos ejes son los **autovectores** de la matriz de covarianza. Es el lenguaje con el que el filtro de Kalman (U8) describe "dónde creo que está el jugador".

**Videos:** StatQuest, *The Normal Distribution*, y repasar el apunte 05 de U1 (autovectores de matrices simétricas).

---

## 1. La normal en 1D

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}}\,e^{-\frac{(x-\mu)^2}{2\sigma^2}}$$

- **μ:** el centro (media = mediana = moda).
- **σ:** el ancho (desvío).

La regla del **68–95–99,7**: dentro de μ ± σ cae el 68 % de la probabilidad; dentro de μ ± 2σ, el 95 %; dentro de μ ± 3σ, el 99,7 %. Es la regla que justificó el radio de 3σ del kernel gaussiano en U2.

**Estandarizar:** `z = (x − μ)/σ` dice "a cuántos desvíos está x". Si un Sub-21 corre en promedio a 22 km/h en piques, con σ = 4, un pique de 30 km/h está en z = 2: es raro (~2,3 % por encima) pero normal. Uno de 50 km/h está en z = 7: no es un pique, es un error de tracking.

### ¿Por qué aparece tanto? El teorema central del límite

La **suma** (o el promedio) de muchas VA independientes, cualquiera sea su distribución, se parece a una normal. El ruido de un sensor es la suma de muchos efectos chicos, y por eso es aproximadamente gaussiano. Los goles de un equipo en una temporada (suma de muchos tiros) también se aproximan con una normal.

## 2. Varias dimensiones: vector de medias y matriz de covarianza

La posición (x, y) de un jugador con error de medición es un **vector aleatorio**. Se describe con:
- **μ = (μₓ, μᵧ):** el centro;
- **Σ, la matriz de covarianza:**

$$\Sigma = \begin{bmatrix} \operatorname{Var}(x) & \operatorname{Cov}(x,y) \\ \operatorname{Cov}(x,y) & \operatorname{Var}(y)\end{bmatrix}$$

Σ es **simétrica**, y además **semidefinida positiva**: ninguna varianza puede ser negativa en ninguna dirección.

Con datos (N, 2), centrados como D = X − media:

$$\hat\Sigma = \frac{1}{N} D^\top D$$

Es la misma `MᵀM` de cuadrados mínimos totales (U1, apunte 07). No es casualidad.

## 3. La normal multivariada

$$f(\mathbf x) = \frac{1}{\sqrt{(2\pi)^d \det\Sigma}}\; \exp\!\Big(-\tfrac12 (\mathbf x - \boldsymbol\mu)^\top \Sigma^{-1} (\mathbf x - \boldsymbol\mu)\Big)$$

Hay dos piezas:
- **El exponente** es menos un medio por la **distancia de Mahalanobis** al cuadrado:

$$d_M(\mathbf x)^2 = (\mathbf x - \boldsymbol\mu)^\top \Sigma^{-1} (\mathbf x - \boldsymbol\mu)$$

  Es "cuántos desvíos" estás del centro, **teniendo en cuenta la forma**: alejarte en la dirección en que los datos se dispersan mucho cuesta poco, y en la dirección en que se dispersan poco cuesta mucho.
- **El `det Σ`** normaliza para que el volumen bajo la curva dé 1. Es el factor de área de U1: si Σ estira el espacio, la densidad se reparte en más área.

Para calcular `Σ⁻¹ v`, **no se invierte**: `np.linalg.solve(Σ, v)` (U1, apunte 03).

## 4. La geometría: elipses y autovectores

Los puntos con la misma densidad (`d_M = k`) forman una **elipse**. ¿Cuál?

Por U1 (apunte 05), como Σ es simétrica: `Σ = V Λ Vᵀ`, con V una rotación y Λ diagonal. Entonces:
- los **ejes** de la elipse apuntan en las direcciones de los **autovectores** de Σ;
- los **semiejes** miden `k·√λᵢ`: la raíz del autovalor es el **desvío en esa dirección**.

Para dibujar la elipse de "k desvíos":
1. tomar la circunferencia unitaria;
2. estirarla por `k√λᵢ` en cada eje;
3. rotarla con V;
4. trasladarla a μ.

Es `elipse_confianza` del TP3, y es exactamente la "circunferencia que va a una elipse" de la SVD.

**Ejemplo.** Con `Σ = [[2, 1], [1, 2]]`, los autovalores son 3 y 1, con autovectores (1, 1) y (1, −1). La elipse es alargada en la diagonal, con desvíos √3 ≈ 1,73 y 1 en las dos direcciones. Esa forma dice que x e y están **positivamente correlacionadas**.

**Si det Σ = 0**, la elipse se aplasta en un segmento: los datos están sobre una recta, una variable es función lineal de la otra. Σ no es invertible y la densidad no existe. Es lo que pasa si calculás la covarianza de puntos alineados (guía C3).

## 5. Dónde la vas a usar

- **Kalman (U8).** El estado de un jugador (posición, velocidad) es una gaussiana multivariada. La **predicción** agranda la elipse (cuanto más tiempo pasa, menos seguro estás) y la **medición** la achica. La asociación detección↔track usa la distancia de **Mahalanobis**: una detección "lejos" en la dirección en que el filtro tiene mucha incertidumbre puede igual ser compatible.
- **Dispersión de tiros, mapas de calor:** una gaussiana es la forma más simple de resumir una nube de posiciones.
- **K-means y equipos (U8):** K-means asume nubes "redondas". Si no lo son, estandarizar (o usar Mahalanobis) cambia el resultado. Es la lección de Lab del proyecto anterior.

---

## Resumen para volver

- Normal 1D: μ y σ. 68–95–99,7. z = (x − μ)/σ es "cuántos desvíos".
- **TCL:** las sumas de muchos efectos chicos son ≈ normales.
- Covarianza: `Σ̂ = DᵀD / N`, simétrica y semidefinida positiva.
- **Mahalanobis:** `√((x − μ)ᵀ Σ⁻¹ (x − μ))`. Se calcula con `solve`, no con `inv`.
- **Elipse:** ejes = autovectores de Σ, semiejes = k·√λ. det Σ = 0 es una elipse aplastada.
- La vas a usar en Kalman (U8), en la asociación por Mahalanobis y en el *clustering* de equipos.
