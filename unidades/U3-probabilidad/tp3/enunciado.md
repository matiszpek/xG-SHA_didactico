# TP3 — xG desde cero

**Unidad:** U3 · **Entrega:** parte A (sesiones 1–3) y parte B (sesiones 4–5) · **Tiempo estimado:** 6–8 h en total

## Objetivo

1. Convertir lo que el diagnóstico mostró flojo en **herramientas que funcionan**: complemento, distribución de goles, Monte Carlo, Bayes y gaussianas.
2. Construir el **primer modelo del proyecto**, un modelo de Expected Goals: regresión logística entrenada por máxima verosimilitud con tu propio descenso por gradiente, evaluada como se debe.
3. Aplicarlo a **tiros reales de Hebraica**, diciendo con honestidad qué se puede concluir y qué no.

## Parte A — `mv/prob.py` (sesiones 1–3)

Funciones:
- `prob_al_menos_uno`
- `distribucion_goles` (es una convolución: apunte 02)
- `simular_goles`
- `bayes`
- `densidad_normal`
- `densidad_normal_multivariada`
- `mahalanobis`
- `elipse_confianza`
- `log_verosimilitud_bernoulli`

```bash
pytest tests/test_u3_prob_xg.py -v -k prob     # 10 tests
```

## Parte B — `mv/xg.py` (sesiones 4–5)

Funciones:
- `distancia_y_angulo`
- `estandarizar`
- `sigmoide` (estable)
- `predecir_proba`
- `log_loss`
- `gradiente_log_loss` (**derivado a mano**: el test lo compara con diferencias finitas)
- `entrenar_logistica`
- `auc` (con rangos)
- `curva_calibracion`
- `split_por_partido`

```bash
pytest tests/test_u3_prob_xg.py -v -k xg       # 13 tests
```

## Datos

```bash
python herramientas/bajar_tiros_statsbomb.py   # → datos/statsbomb/tiros.csv (~6400 tiros)
```

### Tiros de Hebraica (`tp3/tiros_hebraica.csv`)

Elegí **un partido** del canal y marcá **todos los tiros** de los dos equipos: una fila por tiro.

| Columna | Qué poner |
|---|---|
| `partido` | por ejemplo, `cissab` |
| `minuto` | minuto del partido |
| `equipo` | `hebraica` o `rival` |
| `dist_linea_m` | distancia en **metros** desde la línea de fondo hasta el tirador |
| `lateral_m` | distancia en **metros** del tirador a la línea imaginaria que sale del centro del arco: positiva hacia un lado y negativa hacia el otro (el signo no importa para el xG) |
| `parte_cuerpo` | `pie`, `cabeza` u `otro` |
| `tipo` | `Open Play`, `Free Kick` o `Penalty` |
| `gol` | 0 o 1 |
| `nota` | lo que quieras: "rebote", "dudoso"… |

**Para estimar las distancias**, usá las marcas reglamentarias como regla:
- área chica: 5,5 m de profundidad y 18,3 m de ancho;
- punto penal: a 11 m;
- área grande: 16,5 m de profundidad y 40,3 m de ancho.

Un tiro "en el borde del área, a la altura del palo derecho" es más o menos `dist_linea_m = 16,5` y `lateral_m = 3,7`. No hace falta precisión de centímetros. Anotá en `nota` los que te dejen dudas.

## Informe (`tp3.ipynb`)

| Sección | Qué se hace | Pregunta central |
|---|---|---|
| A1 | Distribución exacta de goles contra Monte Carlo | ¿Coinciden? ¿Cuántas simulaciones hacen falta? |
| A2 | Bayes: P(real \| detecta) en función de la tasa base | ¿Desde qué tasa base el detector deja de servir? |
| A3 | Gaussiana de las posiciones de tiro, elipses y Mahalanobis | ¿Una gaussiana describe bien dónde se tira? |
| B1 | Features y split por partido | — |
| B2 | Modelo solo con distancia y curvas de pérdida con varios η | ¿Qué pasa con η grande? |
| B3 | Distancia + ángulo + cabeza, contra sklearn, e interpretación de los pesos (odds) | ¿Qué te dice cada peso? |
| B4 | Evaluación: línea de base, log loss, AUC, calibración, y el xG de StatsBomb como referencia | ¿Cuánto te falta para llegar a StatsBomb, y por qué? |
| B5 | Mapa de xG sobre media cancha | ¿Tiene la forma que esperabas? |
| B6 | *Leakage*: split por tiro contra por partido | ¿Cambia algo? ¿Por qué tan poco (o tanto)? |
| B7 | (Opcional) Agregar rivales en el triángulo y la posición del arquero | ¿Mejora? ¿Cuánto, y con qué incertidumbre? |
| **B8** | **Hebraica:** xG por tiro, xG del partido por equipo, distribución de goles contra goles reales | ¿Qué podés concluir y qué **no**? |

## Para el coloquio

- Derivá en el pizarrón el gradiente de la log loss para un tiro. ¿Dónde aparece la regla de la cadena?
- ¿Por qué tu `sigmoide` tiene dos ramas? ¿Qué pasaba con z = −1000 sin eso?
- ¿Por qué `distribucion_goles` es una convolución? ¿Qué tiene que ver con el filtro de U2?
- ¿Con qué datos estandarizaste el test? ¿Qué pasaría si lo hicieras con los suyos propios?
- Tu modelo tiene AUC 0,78 y el de StatsBomb 0,83. ¿Qué información tiene StatsBomb que el tuyo no?
- Con tus tiros de Hebraica: ¿qué afirmación concreta podés hacer, y cuál no, sobre si el modelo sirve en Sub-21?

## Criterios

Los de [`meta/metodo.md`](../../../meta/metodo.md). En este TP pesa mucho la **B8**: aplicar el modelo es fácil; decir con honestidad cuánto vale el resultado es lo que importa.
