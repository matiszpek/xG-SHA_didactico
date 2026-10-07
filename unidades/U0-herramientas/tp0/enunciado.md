# TP0 — Anatomía de un frame

**Unidad:** U0 · **Entrega:** commit + push y avisar "entrego el TP0" · **Tiempo estimado:** 2–4 h

## Objetivo

Poner en práctica todo U0 sobre material real: implementar las primeras funciones de la librería `mv/` y usarlas para "diseccionar" un frame de un partido y la trayectoria de un jugador.

## Parte A — `mv/imagen.py`

Implementar las 10 funciones. Cada una tiene en su docstring el **contrato exacto**: qué recibe, qué devuelve y los casos borde.

| Función | Concepto de U0 que pone en juego |
|---|---|
| `a_float`, `a_uint8` | dtypes, clip, redondeo |
| `bgr_a_rgb` | slicing con paso negativo sobre el último eje |
| `a_gris` | producto escalar sobre el último eje (`@`) |
| `recortar` | orden (y, x), recorte a los bordes, vista contra copia |
| `histograma` | contar sin loops (`np.bincount`) |
| `ajustar_brillo_contraste` | overflow, saturación |
| `mascara_pasto` | máscaras booleanas + la trampa de `uint8` |
| `color_medio` | máscara + reducción sobre el eje correcto |
| `mosaico` | shapes; bonus: `reshape` + `transpose` |

**Regla:** nada de `for` sobre píxeles.

## Parte B — `mv/cinematica.py`

Implementar las 7 funciones: posición media, distancias, distancia total, velocidades, filtro de tramos imposibles, distancia filtrada y velocidad tope robusta.

Es el ejercicio 7 del diagnóstico, bien hecho y con datos sucios.

## Verificación automática

```bash
pytest tests/test_u0_imagen.py tests/test_u0_cinematica.py -v
```

Tienen que pasar los 35. Si un test falla, **leé el mensaje antes que nada**: está escrito para decirte qué concepto está fallando.

## Parte C — Informe (`tp0.ipynb`)

El notebook ya tiene la estructura armada. Completás el código que falta y **respondés las preguntas en las celdas de texto**: respuestas cortas, pero con tus palabras y justificadas con lo que ves.

1. **Anatomía:** shape, dtype y peso del frame; los canales por separado; el gris.
2. **Histogramas:** qué dicen del frame. ¿Qué canal domina en el pasto?
3. **Overflow:** sumarle brillo bien y mal, y mirar la diferencia.
4. **Pasto:** máscara, fracción de pasto según el `margen` y el color medio del pasto.
5. **Jugadores:** 6 recortes elegidos a mano, el mosaico y el color medio de cada torso. ¿Se separan los equipos?
6. **Vista contra copia:** romper la imagen a propósito y explicar por qué pasó.
7. **Trayectoria:** distancia cruda contra filtrada, velocidad tope, histograma de velocidades y el efecto del ruido según la frecuencia de muestreo.

Con un frame real es mucho más interesante: corré antes `herramientas/bajar_frames.py`. Si no, el notebook usa un frame sintético.

## Para el coloquio

Después de la corrección te voy a hacer preguntas sobre **tu** código. Prepará poder responder, sin mirar:
- ¿Por qué tu `recortar` devuelve una copia? ¿En qué caso sería mejor una vista?
- ¿Qué pasaría en tu `mascara_pasto` si sacaras la conversión de dtype? Dame un píxel concreto que falle.
- ¿Por qué `a_gris` funciona con `@`? ¿Qué shapes entran y cuál sale?
- ¿Por qué la distancia cruda de la trayectoria es mayor que la real aun **sin** saltos?
- ¿Por qué el percentil y no el máximo? ¿Cuándo el percentil 95 también fallaría?

## Criterios

Ver [`meta/metodo.md`](../../../meta/metodo.md): correctitud (tests), comprensión (coloquio), código y honestidad del informe.

**Bonus (opcional):** `mosaico` sin ningún loop (`reshape` + `transpose`), y explicar en el notebook por qué el `transpose` es necesario.
