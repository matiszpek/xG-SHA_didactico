# U5 — Features y movimiento

**Sesiones:** 3 · **TP:** TP5 → `mv/features.py` · **Estado:** 📋 ficha

## Por qué
La cámara del club **panea** siguiendo la pelota, así que la homografía de U4 cambia en cada frame. Para propagarla hace falta saber **cuánto se movió la cámara** entre un frame y el siguiente. Para eso se usan puntos característicos (*features*) que se siguen de un frame a otro, y el **flujo óptico**.

Es también una lección de método: en el proyecto anterior, el flujo óptico sobre césped convergía a "no se movió" pasados ~12 frames, y RANSAC lo aceptaba como *inlier*. Falló en silencio.

## Objetivos
1. Detector de esquinas de **Harris**: el tensor de estructura y sus **autovalores** (apunte 05 de U1).
2. Descriptores (la idea de SIFT y ORB) y *matching*: distancia, *ratio test*, ambigüedad en texturas repetitivas como el césped.
3. **Flujo óptico** (Lucas-Kanade): la ecuación de restricción de brillo, el problema de apertura, y la solución por cuadrados mínimos con la `AᵀA` de U1.
4. Movimiento de cámara entre frames con RANSAC. Chequeo *forward-backward*.
5. Saber **hasta dónde** es confiable una estimación y medirlo.

## Contenidos y recursos por sesión

| Sesión | Contenido | Recursos |
|---|---|---|
| 1 | Esquinas: Harris, autovalores del tensor de estructura. Descriptores y *matching* | First Principles of CV: *SIFT Detector* · Stachniss, clases 10 y 13 |
| 2 | Flujo óptico: restricción de brillo, problema de apertura, Lucas-Kanade, pirámides | First Principles of CV: *Optical Flow* · Szeliski 9.3 |
| 3 | Movimiento de cámara: *features* → *matching* → RANSAC (de U4) → transformación. *Forward-backward*. Correlación de fase como verificación independiente | Szeliski 8.1, 9.1 |

## TP5 (borrador)
`mv/features.py`:
- `harris`
- `esquinas` (con NMS)
- `lucas_kanade` (en ventanas)
- `movimiento_camara`
- `chequeo_forward_backward`

Notebook:
- estimar el paneo entre frames separados 1, 6, 12, 30 y 60 frames;
- medir dónde deja de ser confiable;
- comparar contra la correlación de fase;
- explicar el modo de falla sobre el césped.

## Conexión con el producto
Es lo que permite propagar la homografía en video con cámara móvil (stream del club, PromesaData) y estabilizar trayectorias.
