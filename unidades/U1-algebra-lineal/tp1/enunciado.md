# TP1 — Geometría de la imagen

**Unidad:** U1 · **Entrega:** en dos partes, o todo junto · **Tiempo estimado:** 4–6 h en total

## Objetivo

Implementar desde cero las herramientas geométricas que se usan en toda la visión por computadora:
- **transformar imágenes** con matrices (rotar, escalar, deformar), resolviendo bien la interpolación;
- **ajustar rectas** a puntos ruidosos de la cancha, entendiendo qué minimiza cada método y dónde falla.

Todo va a `mv/geometria.py`. En U4 lo vas a reusar tal cual para la homografía: `aplicar` ya divide por W, y el ajuste por SVD es el mismo truco que el DLT.

---

## Parte A — Transformaciones (después de la sesión 4)

Funciones: `rotacion`, `escala`, `cizalla`, `a_homogenea`, `traslacion`, `aplicar`, `rotacion_alrededor`, `interpolar_bilineal` y `warp`.

```bash
pytest tests/test_u1_geometria.py -v -k parte_a      # 22 tests
```

Lo central de esta parte:
- **`aplicar`** divide por W aunque hoy no haga falta.
- **`interpolar_bilineal`** cuida los bordes (el último píxel es válido y lo de afuera vale 0) y el orden `img[y, x]`.
- **`warp`** usa ***inverse mapping***: recorre los píxeles de la **salida** y pregunta de dónde vienen.

## Parte B — Rectas y SVD (después de la sesión 7)

Funciones: `ajustar_recta_mc`, `ajustar_recta_total`, `distancia_a_recta`, `recta_por_dos_puntos`, `interseccion` y `aproximar_rango`.

```bash
pytest tests/test_u1_geometria.py -v -k parte_b      # 10 tests
```

---

## Informe (`tp1.ipynb`)

| Sección | Qué se hace | Pregunta central |
|---|---|---|
| A1. Ver las matrices | Dibujar î, ĵ y una grilla antes y después de varias matrices | ¿Las columnas predicen lo que ves? |
| A2. Rotar un frame | `warp` contra `cv2.warpAffine`: diferencia y tiempo | ¿Por qué no dan *exactamente* igual? |
| A3. *Forward* contra *inverse* | Ampliar ×2 "empujando" píxeles, y ver los agujeros | ¿Por qué *inverse mapping*? |
| A4. Vecino más cercano contra bilineal | Zoom ×4 a un jugador | ¿Qué se gana y qué se pierde? |
| A5. Enderezar la cancha | Rotar el frame para que la línea lateral lejana quede horizontal | ¿Qué ángulo y alrededor de qué punto? |
| B1. Ajustar la línea lateral | Ordinarios contra totales sobre tus clicks | ¿Dan lo mismo? ¿Por qué? |
| B2. Recta casi vertical | La línea de medio campo | ¿Por qué fallan los ordinarios? |
| B3. Un click malo | Agregar un *outlier* | ¿Cuánto se mueve cada recta? (Motivación para RANSAC.) |
| B4. Intersecciones y punto de fuga | Esquinas y el punto donde se juntan las laterales | ¿Por qué se cortan si en la cancha son paralelas? |
| B5. La elipse de la SVD | La circunferencia unitaria transformada, con σᵢ, uᵢ y vᵢ | ¿Coincide con los autovalores de AᵀA? |
| B6. Comprimir un frame | Rango k = 1, 5, 20, 50 y la curva de valores singulares | ¿Desde qué k se reconoce el partido? |

## Para el coloquio

- Explicá con un dibujo por qué `rotacion_alrededor` es `T(c) R T(−c)` y no `T(−c) R T(c)`.
- ¿Qué pasaría en tu `warp` si usaras T en vez de T⁻¹? Mostralo con un ejemplo de escala.
- En tu `interpolar_bilineal`: ¿qué pasa exactamente en x = W − 1? ¿Y en x = W − 0,5?
- ¿Por qué tu `ajustar_recta_total` centra los puntos? ¿Qué sale si no centrás?
- ¿Por qué el vector normal es la **última** fila de `Vt` y no la primera?
- Si dos rectas son "casi" paralelas, ¿qué le pasa al punto de intersección cuando movés un click 1 píxel?

## Criterios

Los de [`meta/metodo.md`](../../../meta/metodo.md). En este TP pesa mucho la **comprensión geométrica**: en el coloquio te voy a pedir dibujos, no fórmulas.
