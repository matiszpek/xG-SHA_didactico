# 05 · Evaluar un modelo probabilístico (y no engañarse)

> **La idea en una frase:** a un modelo de xG se le piden tres cosas distintas: que **ordene** bien los tiros (AUC), que sus probabilidades **signifiquen** lo que dicen (calibración) y que lo midas con datos que **nunca vio** (split por partido). La *accuracy* no sirve para nada de eso.

---

## 1. La línea de base

Antes de celebrar un número, compará contra el modelo **más tonto posible**: predecir siempre la tasa base. Con ~10 % de goles:
- **Log loss** de predecir siempre p = 0,098: `−(0,098 ln 0,098 + 0,902 ln 0,902) ≈ 0,32`.
- ***Accuracy*** de decir "nunca es gol": **90 %**. Es un número espectacular para un modelo inútil (diagnóstico, bloque 4, pregunta 10).

Tu modelo vale lo que mejora sobre esa base. Una log loss de 0,27 contra 0,32 es una mejora real; un 92 % de *accuracy* contra 90 % no dice casi nada.

## 2. Discriminación: AUC

¿El modelo le da más probabilidad a los goles que a los no-goles?

**AUC** (área bajo la curva ROC) tiene una interpretación probabilística limpia:

$$\text{AUC} = P(\,p_{\text{gol al azar}} > p_{\text{no-gol al azar}}\,)$$

con los empates contando 1/2.
- **0,5:** azar, el modelo no distingue nada.
- **1:** separa perfecto.
- Para xG, ~0,75–0,80 es lo típico; con datos ricos (posición del arquero y de los defensores), ~0,80–0,85.

**Cómo se calcula sin armar la curva:**
1. ordenar todos los tiros por p;
2. asignar rangos 1..N (los empates, con el rango promedio);
3. `AUC = (Σ rangos de los goles − n_pos(n_pos + 1)/2) / (n_pos · n_neg)`.

Es el estadístico de Mann-Whitney. ¿Por qué funciona? La suma de los rangos de los goles cuenta, para cada gol, cuántos tiros tiene por debajo. Restando los pares gol-gol, quedan exactamente los pares gol > no-gol.

**Lo que la AUC NO mide:** si las probabilidades son correctas. Multiplicar todas las p por 0,5 no cambia el orden, así que no cambia la AUC, pero arruina el modelo para sumar xG.

## 3. Calibración: que 0,3 signifique 30 %

Un modelo está **calibrado** si, de todos los tiros a los que les da p ≈ 0,3, entra ~30 %.

**Curva de calibración:**
1. agrupar las predicciones en intervalos (0–0,1, 0,1–0,2, …);
2. en cada intervalo, comparar la **p media predicha** con la **frecuencia real** de goles;
3. bien calibrado = los puntos caen sobre la diagonal.

**Por qué es crucial para el xG:** el xG de un partido es una **suma** de probabilidades (apunte 02). Si el modelo sobreestima un 20 %, cada equipo "genera" 20 % más de lo real. Ordenaría bien (AUC alta) y los totales mentirían.

**Ojo con los intervalos con pocos tiros:** con 6 tiros en el intervalo 0,6–0,7, una frecuencia de 0,17 es casi puro ruido. Mostrá siempre la **cantidad** de tiros por intervalo.

La **log loss** premia las dos cosas a la vez, discriminación y calibración, y por eso es la métrica principal para comparar modelos de xG. (El ***Brier score***, la MSE entre p e y, es otra opción con la misma propiedad.)

## 4. No engañarse: train, validación, test y *leakage*

- **Train:** con estos datos se ajustan los parámetros.
- **Validación:** con estos se eligen las decisiones (qué features, cuánta regularización, η).
- **Test:** se mira **una vez**, al final, para estimar cómo anda con datos nuevos. Si elegís mirando el test, el test deja de ser "nuevo": te sobreajustaste a él.

### *Leakage*: cuando el test no es realmente nuevo

- **Por frame (diagnóstico, bloque 4, pregunta 2):** dos frames consecutivos son casi idénticos. Mezclarlos al azar pone casi-copias en train y en test, y el 98 % es falso.
- **Por tiro:** menos grave, pero existe. Un rebote y el tiro anterior son de la misma jugada; los tiros de un partido comparten equipos, arquero y cancha.
- **La regla:** separar por la unidad que va a ser "nueva" en el uso real. Para el xG de un partido nuevo, **por partido**. Para un detector que va a ver partidos nuevos, **por partido**.
- **Estadísticas del preprocesamiento** (la media y el desvío de la estandarización): se calculan con el train y se **aplican** al test.

## 5. ¿Cuántos datos hacen falta para creerse un número?

Toda métrica tiene ruido. La AUC medida sobre 1200 tiros de test con 120 goles tiene un error típico (un desvío) de ~0,025. Una diferencia de 0,005 entre dos modelos medidos así no significa nada.

Con **25 tiros de Hebraica** (~2–3 goles), **no podés medir la calibración ni la AUC del modelo en tu cancha**: el ruido es mayor que cualquier efecto. Lo honesto es aplicar el modelo y reportar el xG, diciendo explícitamente que **su validez en Sub-21 amateur está "no medida"** hasta tener cientos de tiros etiquetados. Es la regla del proyecto anterior: nada se afirma sin medir, y se dice con cuántos datos.

## 6. Cambio de dominio: profesional → Sub-21

El modelo se entrena con fútbol profesional de elite (mundiales, Euros). En Hebraica cambian:
- los arqueros (posiblemente peores, así que más goles a igual posición);
- la técnica de definición;
- la defensa;
- y las coordenadas: las tuyas salen de marcar a mano sobre un croquis, con error.

**Hipótesis razonable, no medida:** el modelo probablemente **subestima** la conversión en amateur. Para verificarlo hacen falta muchos tiros propios con su resultado. Es uno de los ejemplos de *domain shift* que vuelve en U7, con el detector entrenado en TV y aplicado a la cámara del club.

---

## Resumen para volver

- Siempre contra la **línea de base** (tasa constante). La *accuracy* con 10 % de goles engaña.
- **AUC** = P(p_gol > p_no-gol). Se calcula con rangos. Mide **orden**, no probabilidades.
- **Calibración:** la curva p predicha contra la frecuencia real. **Imprescindible para sumar xG.** Mirá las cantidades por intervalo.
- **Log loss:** premia orden y calibración. Es la métrica principal.
- Train / validación / test. ***Leakage*:** separar **por partido**; estandarizar con las estadísticas del train.
- Con pocos datos, el número es ruido: decirlo. Profesional → amateur es un cambio de dominio **no medido**.
