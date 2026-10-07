# U3 — Probabilidad + primer modelo (xG)

**Sesiones:** 5 · **TP:** TP3 → `mv/prob.py`, `mv/xg.py` · **Estado:** 📋 ficha

## Por qué
El diagnóstico mostró que esta es el área más floja (casi desde cero) y es la que más se usa por debajo de todo lo demás:
- **evaluar detectores** es probabilidad condicional;
- el **filtro de Kalman** del tracking es Bayes + gaussianas;
- **RANSAC** se diseña con probabilidad;
- **entrenar cualquier modelo** es máxima verosimilitud.

Y el primer modelo que vamos a entrenar es el que da nombre al proyecto: **el xG**.

Lo que ya traés bien: sumar los xG de los tiros da los goles esperados. Es la linealidad de la esperanza, y la usaste sin saberlo.

## Objetivos
1. Probabilidad condicional, independencia, regla del producto, complemento ("al menos uno"), **Bayes**.
2. Variables aleatorias discretas y continuas, densidad, esperanza, varianza, **linealidad de la esperanza**.
3. Bernoulli, binomial, normal. **Gaussiana multivariada** y matriz de covarianza (con autovectores de U1).
4. **Máxima verosimilitud**: por qué *cross-entropy* es la log-verosimilitud negativa de una Bernoulli.
5. Regresión logística como modelo probabilístico, entrenada por **descenso por gradiente** (el gradiente se deriva a mano).
6. Evaluación: *log loss*, AUC, **calibración**. *Data leakage* y por qué separar por partido.

## Contenidos y recursos por sesión

| Sesión | Contenido | Recursos |
|---|---|---|
| 1 | Probabilidad básica, condicional, independencia, complemento, Bayes (con el detector de pelota del diagnóstico) | Seeing Theory, caps. 1–2 · 3Blue1Brown: *Bayes theorem, the geometry of changing beliefs* |
| 2 | Variables aleatorias, esperanza, varianza, linealidad. Bernoulli y binomial. Simulación con NumPy | Seeing Theory, cap. 3 |
| 3 | Normal, normal multivariada, covarianza, elipses de confianza (autovectores de la covarianza) | StatQuest: *The Normal Distribution* · repaso del apunte 05 de U1 |
| 4 | Máxima verosimilitud. Regresión logística. *Cross-entropy*. Descenso por gradiente | StatQuest: *Maximum Likelihood*, serie *Logistic Regression* · *xG Philosophy* (Tippett) |
| 5 | Evaluación: *log loss*, ROC/AUC, calibración, splits por partido. Aplicación a tiros de Hebraica | StatsBomb Open Data |

## TP3 (borrador)
- `mv/prob.py`: simulaciones de Monte Carlo para verificar resultados analíticos (por ejemplo, la probabilidad de 0 goles dados los xG), y la densidad gaussiana multivariada.
- `mv/xg.py`:
  - *features* geométricas del tiro (distancia y **ángulo** al arco);
  - `sigmoide`;
  - `log_verosimilitud`;
  - `gradiente`, **derivado a mano**;
  - `entrenar`, con descenso por gradiente;
  - `predecir`;
  - `log_loss`, `auc`, `curva_calibracion`.

Notebook:
- datos de StatsBomb;
- split **por partido**;
- comparar contra `sklearn.LogisticRegression` (que tiene que dar casi lo mismo) y contra el xG de StatsBomb;
- aplicar el modelo a ~20 tiros de Hebraica marcados a mano sobre un croquis de la cancha;
- discutir si un modelo entrenado con fútbol profesional sirve para Sub-21 amateur.

## Conexión con el producto
El xG es una de las métricas del producto. Además, *log loss*, calibración y split por partido son la forma correcta de evaluar **cualquier** modelo del producto.
