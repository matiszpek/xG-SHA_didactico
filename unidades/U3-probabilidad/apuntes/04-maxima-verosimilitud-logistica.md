# 04 · Máxima verosimilitud y regresión logística

> **La idea en una frase:** para elegir los parámetros de un modelo, elegí los que hacen **más probables los datos que observaste**. Para la regresión logística, eso es minimizar la *cross-entropy*, y como no hay fórmula cerrada, se baja por el gradiente. Así se entrena un modelo de xG y, en el fondo, también una red neuronal.

**Videos:** StatQuest, *Maximum Likelihood, clearly explained* y la serie *Logistic Regression* (partes 1–3). **Lectura:** *xG Philosophy* (Tippett), los capítulos sobre cómo se construye el modelo.

---

## 1. Verosimilitud

Tenés un modelo con parámetros θ y datos observados. La **verosimilitud** es la probabilidad de esos datos **como función de θ**:

$$L(\theta) = P(\text{datos} \mid \theta)$$

Es la misma fórmula que la probabilidad, pero mirada al revés: los datos están fijos y lo que se mueve es θ. El estimador de **máxima verosimilitud** (MLE) es el θ que la maximiza.

**Ejemplo: una moneda.** 7 caras en 10 tiros. Con probabilidad de cara p:

$$L(p) = p^7 (1-p)^3 \qquad \log L(p) = 7\log p + 3\log(1-p)$$

Derivando e igualando a 0: `7/p − 3/(1 − p) = 0`, así que **p̂ = 0,7**. La intuición ("la fracción observada") sale formalmente.

### ¿Por qué el log?
- Convierte productos en sumas: con datos independientes, `L = Π pᵢ` y `log L = Σ log pᵢ`.
- Con miles de datos, el producto de probabilidades es ~10⁻³⁰⁰ y la computadora lo redondea a 0. La suma de logs no tiene ese problema.
- El log es creciente: maximizar log L es lo mismo que maximizar L.

**Para la normal**, la MLE de μ es la media muestral y la de σ² es el promedio de los desvíos al cuadrado (dividiendo por N; con N − 1 sale el estimador "insesgado", una sutileza que no importa acá).

## 2. El modelo de xG: regresión logística

Queremos `P(gol | características del tiro)`. Las características (*features*) son, por ejemplo, distancia, ángulo y si fue de cabeza: un vector x.

**Primer intento:** `p = w·x + b`. No sirve: da valores fuera de [0, 1].

**La logística:** modelar lineal el **log-odds**:

$$\log\frac{p}{1-p} = \mathbf w \cdot \mathbf x + b \quad\Longleftrightarrow\quad p = \sigma(\mathbf w \cdot \mathbf x + b), \qquad \sigma(z) = \frac{1}{1 + e^{-z}}$$

- `p/(1 − p)` son los **odds** ("chances"): con p = 0,2, los odds son 1 a 4 (0,25).
- La **sigmoide** σ "aplasta" cualquier número real a (0, 1): σ(0) = 0,5, σ(+∞) → 1 y σ(−∞) → 0.
- **Interpretación de un peso:** si la feature j sube 1 unidad, el log-odds sube wⱼ, o sea que los **odds se multiplican por e^{wⱼ}**.

**Derivada de la sigmoide** (la vas a necesitar):

$$\sigma'(z) = \sigma(z)\,(1 - \sigma(z))$$

## 3. La verosimilitud de la logística es la *cross-entropy*

Cada tiro i es una Bernoulli con probabilidad pᵢ = σ(w·xᵢ + b). La probabilidad de su resultado yᵢ ∈ {0, 1} se escribe en una sola fórmula:

$$P(y_i) = p_i^{\,y_i}(1 - p_i)^{1 - y_i}$$

(Si yᵢ = 1 da pᵢ; si yᵢ = 0 da 1 − pᵢ.) La log-verosimilitud de todos los tiros:

$$\log L = \sum_i \big[y_i \log p_i + (1 - y_i)\log(1 - p_i)\big]$$

Maximizarla es **minimizar** su negativo promedio, la ***log loss*** o ***cross-entropy*** binaria:

$$\mathcal L(\mathbf w, b) = -\frac1N \sum_i \big[y_i \log p_i + (1 - y_i)\log(1 - p_i)\big]$$

La *cross-entropy* que no recordabas en el diagnóstico (bloque 4, pregunta 5) **es** la log-verosimilitud negativa. No es una "pérdida inventada": sale de pedir que el modelo haga probables los datos.

**Por qué castiga tanto equivocarse con confianza.** Si y = 1 y el modelo dice p = 0,01, la pérdida de ese tiro es −log 0,01 ≈ 4,6. Si dice 0,4, es ≈ 0,9. La MSE nunca castiga más de 1.

## 4. El gradiente, derivado a mano

Para un tiro, con z = w·x + b y p = σ(z), por la regla de la cadena (U2, apunte 03):

$$\frac{\partial}{\partial z}\big[y\log p + (1-y)\log(1-p)\big] = \frac{y}{p}\,p(1-p) - \frac{1-y}{1-p}\,p(1-p) = y(1-p) - (1-y)p = y - p$$

Y como `∂z/∂w = x` y `∂z/∂b = 1`, para la pérdida promedio (con el signo menos):

$$\boxed{\;\nabla_{\mathbf w}\mathcal L = \frac1N X^\top(\mathbf p - \mathbf y), \qquad \frac{\partial\mathcal L}{\partial b} = \operatorname{mean}(\mathbf p - \mathbf y)\;}$$

**Error de predicción por feature, promediado.** Es casi la misma fórmula que la del gradiente de cuadrados mínimos (U1, apunte 06). En el TP lo verificás contra **diferencias finitas** (la derivada numérica): es la forma de saber que tu gradiente está bien.

## 5. Descenso por gradiente

No hay fórmula cerrada para el mínimo, así que se baja por la pendiente:

$$\mathbf w \leftarrow \mathbf w - \eta\,\nabla_{\mathbf w}\mathcal L, \qquad b \leftarrow b - \eta\,\frac{\partial\mathcal L}{\partial b}$$

- **η (*learning rate*):** muy grande, oscila o diverge; muy chico, tarda una eternidad (diagnóstico, bloque 4, pregunta 8).
- **¿Mínimos locales?** Acá no: la log loss de la logística es **convexa**, con un único mínimo. Cualquier camino de bajada razonable llega al mismo lugar. (En las redes de U6 eso deja de ser cierto.)

### Estandarizar las features
La distancia va de ~5 a ~40 yardas y el ángulo de 0 a ~1,5 radianes. Con escalas tan distintas, la superficie de la pérdida es un valle muy alargado (mal condicionado, U1), y el descenso hace zigzag: un η que sirve para un peso es enorme para el otro. Estandarizar cada columna (restar la media, dividir por el desvío) hace el valle más "redondo" y el descenso converge mucho más rápido.

**Ojo:** la media y el desvío se calculan con el **train**, y con esos mismos se estandariza el test. Recalcularlos con el test es *leakage* (apunte 05).

### Regularización L2
Sumar `(λ/2)‖w‖²` a la pérdida tira los pesos hacia 0. Sirve cuando hay muchas features o pocos datos (overfitting). En el gradiente se suma `λ w`.

## 6. Features para el xG

- **Distancia** al centro del arco: la más obvia.
- **Ángulo de visión del arco:** el ángulo entre las rectas tirador → palo izquierdo y tirador → palo derecho. Captura lo que la distancia no ve: desde la línea de fondo, pegado al palo, estás cerca **pero casi no ves arco**. Se calcula con `arctan2(|cruz|, punto)` (U1), que es estable.
- **Cabeza o pie:** de cabeza se convierte mucho menos a igual posición.
- Del *freeze frame* de StatsBomb: **rivales en el triángulo** tirador–palos y posición del arquero. Son mejoras posibles.
- **Penales:** se tratan aparte (una constante, ~0,7–0,8).

**Linealidad en el log-odds.** El modelo supone que cada yarda de distancia cambia el log-odds **lo mismo**, tanto a 6 yardas como a 30. Si no es así, se agregan transformaciones (por ejemplo, log de la distancia). Lo probás en el TP.

---

## Resumen para volver

- **MLE:** elegir θ que maximiza P(datos | θ). En la práctica, se maximiza el log. Moneda: p̂ = la fracción observada.
- **Logística:** log-odds lineal, p = σ(w·x + b). Un peso wⱼ multiplica los odds por e^{wⱼ}.
- σ' = σ(1 − σ).
- **−log-verosimilitud promedio = log loss = cross-entropy.**
- **Gradiente:** `Xᵀ(p − y)/N` y `mean(p − y)`. Verificarlo con diferencias finitas.
- Log loss convexa: un solo mínimo. **Estandarizar** con las estadísticas del train.
- Features de xG: distancia, **ángulo**, cabeza. Penales aparte.
