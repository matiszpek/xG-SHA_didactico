# U3 — Probabilidad + primer modelo (xG)

**Sesiones:** 5 (~10 h, más el TP) · **TP:** TP3 → `mv/prob.py`, `mv/xg.py`

## Por qué esta unidad

Es el área más floja del diagnóstico (casi desde cero) y la que más se usa por debajo de todo lo demás:
- **evaluar detectores** es probabilidad condicional (U7);
- el **filtro de Kalman** es Bayes + gaussianas (U8);
- **RANSAC** se diseña con probabilidad (U4);
- **entrenar cualquier modelo** es máxima verosimilitud (U6).

Y el primer modelo que vas a entrenar desde cero es el que da nombre al proyecto: **el xG**.

Lo que ya traés: sumar los xG de los tiros da los goles esperados. Es la linealidad de la esperanza, y la usaste sin saberlo.

## Objetivos

Al terminar U3 puedo, sin buscar:
1. Calcular "al menos uno" por complemento, distinguir independientes de excluyentes y aplicar **Bayes** con la tasa base.
2. Explicar densidad contra probabilidad, esperanza (y su **linealidad**), varianza, y calcular la distribución exacta de goles (como **convolución**) y verificarla con Monte Carlo.
3. Interpretar una **gaussiana multivariada**: la matriz de covarianza como elipse (autovectores de U1) y la distancia de Mahalanobis.
4. Derivar la **regresión logística** desde la máxima verosimilitud: *cross-entropy* y su gradiente **a mano**.
5. Entrenarla con descenso por gradiente, estandarizando bien.
6. Evaluarla honestamente: línea de base, AUC, **calibración**, split **por partido**, y cuántos datos hacen falta para creerse un número.

## Plan

| Sesión | Videos y lectura | Apunte | Práctica |
|---|---|---|---|
| **1** | Seeing Theory, caps. 1–2 · 3Blue1Brown: *Bayes theorem, the geometry of changing beliefs* | [01 · Probabilidad y Bayes](apuntes/01-probabilidad-basica.md) | Guía A + TP3 A (`prob_al_menos_uno`, `bayes`) |
| **2** | Seeing Theory, cap. 3 | [02 · Variables aleatorias](apuntes/02-variables-aleatorias.md) | Guía B + TP3 A (`distribucion_goles`, `simular_goles`) |
| **3** | StatQuest: *The Normal Distribution* · repaso de U1, apunte 05 | [03 · La normal](apuntes/03-normal-multivariada.md) | Guía C + TP3 A (el resto de `prob.py`) |
| **4** | StatQuest: *Maximum Likelihood*, serie *Logistic Regression* · *xG Philosophy* | [04 · MLE y logística](apuntes/04-maxima-verosimilitud-logistica.md) | Guía D + TP3 B (el modelo) |
| **5** | — | [05 · Evaluación](apuntes/05-evaluacion.md) | Guía E + TP3 B (evaluación) + informe |

## Datos

```bash
python herramientas/bajar_tiros_statsbomb.py       # ~260 partidos de selecciones, ~6400 tiros, ~1 minuto
```

Genera `datos/statsbomb/tiros.csv`. Los datos son [StatsBomb Open Data](https://github.com/statsbomb/open-data): uso **no comercial** y con atribución.

Además vas a marcar a mano **tiros de Hebraica** en `tp3/tiros_hebraica.csv` (instrucciones en el enunciado).

Dependencias nuevas: `pandas` y `scikit-learn` (sklearn solo para **comparar**). Ya están en `requirements.txt`.

## Guía y TP

- [Guía de ejercicios](guia.md): bloques A–E con respuestas.
- [TP3 — xG desde cero](tp3/enunciado.md).
