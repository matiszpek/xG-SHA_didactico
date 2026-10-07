# 02 · Variables aleatorias, esperanza y varianza

> **La idea en una frase:** una variable aleatoria es un número que depende del azar. La **esperanza** es su promedio a la larga, y es **lineal**: por eso sumar los xG da los goles esperados. La **varianza** dice cuánto se aleja de ese promedio.

**Lectura:** [Seeing Theory](https://seeing-theory.brown.edu/), cap. 3 (*Probability Distributions*).

---

## 1. Variables aleatorias

Una **variable aleatoria** (VA) X asigna un número a cada resultado: los goles de un partido, la velocidad de un jugador, la altura de una caja.

| | Discreta | Continua |
|---|---|---|
| Valores | contables: 0, 1, 2, … | un intervalo: [0, 40] km/h |
| Se describe con | **función de probabilidad** `P(X = k)` | **densidad** `f(x)` |
| Probabilidades | `P(X = k)` directo | `P(a ≤ X ≤ b) = ∫ₐᵇ f(x) dx`, el **área** bajo f |

**Una densidad no es una probabilidad** (diagnóstico, bloque 2, pregunta 6). `f(x)` puede valer más que 1: la uniforme en [0, 0,5] vale 2 en todo el intervalo, y el área igual da 1. Lo que no puede pasar de 1 es el área. En una continua, la probabilidad de un valor **exacto** es 0.

**Función de distribución acumulada (CDF):** `F(x) = P(X ≤ x)`. Va de 0 a 1 y nunca baja. La usaste para ecualizar histogramas en U2.

## 2. Esperanza

$$E[X] = \sum_k k\,P(X = k) \qquad\text{o}\qquad E[X] = \int x\,f(x)\,dx$$

Es el promedio ponderado por la probabilidad: el "centro de masa" de la distribución. El dado: E[X] = (1 + 2 + … + 6)/6 = 3,5, un valor que nunca sale.

### Linealidad: la propiedad más útil de toda la probabilidad

$$E[aX + b] = a\,E[X] + b \qquad E[X + Y] = E[X] + E[Y]$$

**Siempre**, aunque X e Y dependan una de la otra.

**El xG es esto.** Cada tiro es una VA de Bernoulli: vale 1 si es gol (con probabilidad p) y 0 si no, y su esperanza es p. Los goles del partido son la suma de esas VA. Por linealidad, **la esperanza de goles es la suma de los xG**. Ni siquiera hace falta suponer que los tiros son independientes.

E[2X + 1] con un dado da 2·3,5 + 1 = 8.

## 3. Varianza y desvío

$$\operatorname{Var}(X) = E\big[(X - E[X])^2\big] = E[X^2] - E[X]^2 \qquad \sigma = \sqrt{\operatorname{Var}(X)}$$

Es el promedio de las distancias **al cuadrado** a la media. El desvío σ está en las mismas unidades que X.

- `Var(aX + b) = a² Var(X)`: sumar una constante no dispersa nada, y escalar por a dispersa por a².
- Si X e Y son **independientes**: `Var(X + Y) = Var(X) + Var(Y)`. Esto **sí** necesita independencia.

Para los datos (de la pregunta 5 del diagnóstico): media 5, varianza 4, desvío 2.

## 4. Las distribuciones que vamos a usar

| Distribución | Qué modela | E | Var |
|---|---|---|---|
| **Bernoulli(p)** | un tiro: gol o no | p | p(1 − p) |
| **Binomial(n, p)** | goles en n tiros **iguales** | np | np(1 − p) |
| **"Poisson-binomial"** | goles en tiros con **distintos** xG | Σ pᵢ | Σ pᵢ(1 − pᵢ) |

Para tres tiros de xG 0,1, 0,3 y 0,5: E = 0,9 goles y Var = 0,09 + 0,21 + 0,25 = 0,55, o sea σ ≈ 0,74. Un xG de 0,9 con σ = 0,74 te dice que 0, 1 y 2 goles son todos perfectamente esperables.

### La distribución exacta de los goles: es una convolución

¿P(exactamente k goles)? Agregá los tiros de a uno. Si antes tenías la distribución `d` (d[k] = P(k goles)) y agregás un tiro de probabilidad p:

$$d_{\text{nueva}}[k] = d[k]\,(1 - p) + d[k-1]\,p$$

(Para tener k goles, o ya tenías k y erraste, o tenías k − 1 y la metiste.) Eso es exactamente **convolucionar d con [1 − p, p]**, la operación de U2 en 1D. `np.convolve` lo hace. Es `distribucion_goles` del TP3.

## 5. Monte Carlo: cuando la cuenta es difícil, simulá

Para estimar una probabilidad o una esperanza, **simulá muchas veces** y contá. Por la **ley de los grandes números**, el promedio de las simulaciones converge al valor real.

El **error** de estimar una probabilidad p con n simulaciones tiene un desvío de `√(p(1 − p)/n)`. Para reducir el error a la mitad hacen falta **4 veces** más simulaciones: el error baja como 1/√n.

Monte Carlo es la red de seguridad: si tu cuenta exacta y la simulación no coinciden, una de las dos está mal. En el TP3 verificás `distribucion_goles` contra `simular_goles`.

## 6. Media, mediana, moda, percentiles

- **Media:** la esperanza. Sensible a los valores extremos.
- **Mediana:** el valor que deja la mitad de cada lado. **Robusta.**
- **Moda:** el valor más probable.
- **Percentil q:** el valor que deja el q % por debajo. La mediana es el percentil 50.

Una velocidad con un error de tracking de 800 km/h destruye la media y el máximo, y casi no mueve la mediana ni el percentil 95 (U0).

## 7. Correlación

$$\operatorname{Cov}(X, Y) = E[(X - \mu_X)(Y - \mu_Y)] \qquad \rho = \frac{\operatorname{Cov}(X, Y)}{\sigma_X\,\sigma_Y} \in [-1, 1]$$

- ρ mide relación **lineal**. **ρ = 0 no implica independencia.** Con X uniforme en {−1, 0, 1} e Y = X², la covarianza es E[X³] − E[X]E[X²] = 0 − 0 = 0, pero Y está **totalmente determinada** por X.
- **Correlación no implica causalidad:** variables de confusión, causalidad inversa, casualidad.
- Si son independientes, ρ = 0 (al revés no vale).

---

## Resumen para volver

- **Densidad ≠ probabilidad:** puede valer > 1. La probabilidad es el área.
- **E es lineal, siempre:** goles esperados = Σ xG. E[2X + 1] = 2E[X] + 1.
- **Var:** promedio de las distancias al cuadrado. `Var(aX + b) = a²Var(X)`. Suma de varianzas **solo con independencia**.
- Bernoulli: p y p(1 − p). Goles de varios tiros: E = Σ pᵢ y Var = Σ pᵢ(1 − pᵢ).
- **Distribución exacta de goles = convolución** de las Bernoulli.
- **Monte Carlo:** el error baja como 1/√n.
- Mediana y percentiles: robustos. ρ = 0 no es independencia.
