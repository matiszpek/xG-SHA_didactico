# TP4 — De píxeles a metros

**Unidad:** U4 · **Entrega:** una sola, al terminar la sesión 5 · **Tiempo estimado:** 6–8 h en total

## Objetivo

1. Implementar desde cero la cadena que convierte una imagen de la cámara del club en un mapa de la cancha en metros: modelo de cámara, homografía por **DLT normalizado** y **RANSAC**.
2. **Medir** cuánto se puede confiar en esa homografía: con cuántos puntos, dónde, con cuánto ruido. Es la medición que faltó en el proyecto anterior.
3. Calibrar un **frame real** de Hebraica y decir, con números, cuántos metros de error tiene y en qué zona.

## Código — `mv/camara.py`

Funciones, en el orden de las sesiones:

| Sesión | Funciones |
|---|---|
| 1 | `modelo_cancha`, `matriz_camara`, `proyectar` |
| 2 | `homografia_desde_camara` |
| 3 | `normalizar_puntos`, `matriz_dlt`, `dlt_homografia` |
| 4 | `error_reproyeccion` |
| 5 | `iteraciones_ransac`, `ransac_homografia` |

```bash
pytest tests/test_u4_camara.py -v      # 15 tests (necesita mv/geometria.py del TP1)
```

**Reglas** (también en el docstring del módulo):
- sin loops sobre puntos para armar matrices: `matriz_dlt` se arma con operaciones vectorizadas. El loop de RANSAC sobre iteraciones sí está permitido;
- `np.linalg` (svd, inv, solve) se puede usar;
- `cv2.findHomography` y `cv2.getPerspectiveTransform` **solo para comparar**, nunca para resolver;
- reusá `mv.geometria.aplicar`, no la reescribas.

## Informe (`tp4.ipynb`)

El notebook ya trae la cámara sintética, una función para dibujar las líneas de la cancha y las celdas de carga. Lo que dice **TODO** es tuyo.

| Sección | Qué se hace | Pregunta central |
|---|---|---|
| 1 | Cámara sintética: la cancha proyectada, el punto de fuga de las laterales y la altura en píxeles de un jugador según dónde esté | ¿Se parece a lo que se ve en el stream? ¿El rango de alturas coincide con los 30–230 px medidos? |
| 2 | DLT contra `cv2.findHomography` y el efecto de normalizar (condicionamiento y error) | ¿Qué mejora la normalización, y qué **no**? |
| 3 | **Estabilidad:** error en **metros** sobre la cancha en función de la cantidad de puntos (4, 5, 6, 8, 12) y de dónde están (repartidos contra amontonados en un área) | ¿Cuántos puntos hacen falta para menos de 1 m de error? ¿En qué zona de la cancha es peor? |
| 4 | **RANSAC:** con 3 outliers, DLT contra RANSAC; iteraciones teóricas contra lo observado (en cuántas corridas falla con N iteraciones) | ¿La fórmula predice bien la tasa de fallas? |
| 5 | **Frame real:** marcar **6 o más** puntos notables, estimar H, residuos por punto, validación dejando uno afuera (*leave-one-out*) en metros, cancha reproyectada sobre la imagen | ¿Cuánto error tiene, en metros, y dónde? ¿Las líneas caen sobre la cal? |
| 6 | **Vista cenital** con tu `warp` y posiciones de 5–10 jugadores (clickeando sus **pies**) en metros | ¿Las posiciones son creíbles? ¿Qué pasaría si clickearas la cabeza? |
| 7 | Conclusión | Con lo medido: ¿se puede calcular la distancia recorrida de un jugador con esta calibración? ¿Con qué error? |

### Cómo marcar los puntos del frame real (sección 5)

1. Bajá un frame donde se vean **muchas marcas de la cancha** (área grande y chica, punto penal, línea de medio).
2. Abrilo en cualquier programa que muestre la coordenada del cursor (GIMP, Paint, o `%matplotlib widget` en el notebook) y anotá el píxel de cada punto que reconozcas **con seguridad**.
3. Cargalos en el diccionario `clicks` del notebook con los **nombres de `modelo_cancha`**: por ejemplo, `"area_grande_izq_lejana_frente": (812, 274)`.
4. Ojo con el lado: si la cámara mira el arco izquierdo, los puntos son `_izq_`. Lo "lejano" es lo que está **arriba** en la imagen.
5. Las intersecciones de líneas son mucho más precisas que el punto penal o el borde del círculo: preferilas. Anotá en el informe cuáles te dejaron dudas.

Si en un mismo frame no encontrás 6 puntos seguros, **decilo** y mostrá el resultado con los que tengas, explicando qué implica (apunte 04). Eso también es un resultado: es exactamente lo que le pasó al proyecto anterior.

## Para el coloquio

- Derivá en el pizarrón las dos filas de `A` para una correspondencia. ¿Qué "truco" las hace lineales?
- ¿Por qué la solución es `Vt[-1]` y no resolver `A h = 0` con `np.linalg.solve`?
- Tu homografía con 4 puntos tiene error de reproyección 0. ¿Está bien? ¿Cómo lo sabés?
- ¿Qué mediste que mejora la normalización, y qué mediste que **no** mejora?
- Con 40 % de outliers, ¿cuántas iteraciones de RANSAC necesitás? ¿Y si el modelo fuera una recta?
- RANSAC te da 95 % de inliers. ¿Eso prueba que la homografía es buena? Dá un caso en que no.
- ¿Por qué el borde **inferior** de la caja de un jugador, y no el centro?
- Con tu calibración real: un jugador en la lateral lejana se mueve 1 píxel. ¿Cuántos metros son?

## Criterios

Los de [`meta/metodo.md`](../../../meta/metodo.md). En este TP pesan mucho las secciones **3 y 5**: el error **en metros**, medido con puntos que no se usaron para ajustar, es lo que separa una calibración que sirve de una que solo "se ve bien".
