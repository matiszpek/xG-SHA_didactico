# U4 — Geometría de la cámara

**Sesiones:** 5 · **TP:** TP4 → `mv/camara.py` · **Estado:** 📋 ficha

## Por qué
Una posición en píxeles no significa nada: 300 px cerca de la cámara son 3 metros, y lejos son 30. Para medir en **metros** (distancias, velocidades, mapas de calor, xG) hay que traducir la imagen al plano de la cancha. Esa traducción es una **homografía**: una matriz de 3×3 que se estima a partir de puntos conocidos.

Es donde todo U1 rinde:
- coordenadas homogéneas y la división por W (`aplicar` ya lo hace);
- cuadrados mínimos homogéneos con SVD (el DLT);
- condicionamiento y normalización.

Y entra la probabilidad de U3 para diseñar RANSAC.

## Objetivos
1. Modelo *pinhole*: proyección perspectiva, distancia focal, parámetros **intrínsecos** (K) y **extrínsecos** (R, t). La matriz de cámara `P = K [R | t]`.
2. Por qué un plano del mundo y la imagen se relacionan con una **homografía** (8 grados de libertad).
3. **DLT**: armar el sistema `A h = 0` a partir de las correspondencias y resolverlo con la SVD (apunte 07 de U1). **Normalización de Hartley** y por qué es imprescindible.
4. Error algebraico, error geométrico y **error de reproyección**. Por qué con **4 puntos exactos** el error de reproyección da ~0 y **no valida nada**.
5. **RANSAC**: el algoritmo y cuántas iteraciones hacen falta (con la probabilidad de U3).
6. Estabilidad: cómo influyen la cantidad de puntos, su distribución y el ruido de los clicks.

## Contenidos y recursos por sesión

| Sesión | Contenido | Recursos |
|---|---|---|
| 1 | *Pinhole*, proyección, intrínsecos y extrínsecos. Repaso de homogéneas | Stachniss, clases 15–16 · Szeliski 2.1 |
| 2 | Homografía: de dónde sale, qué preserva (rectas) y qué no (paralelismo, ángulos, distancias) | First Principles of CV: *Image Stitching* · Hartley & Zisserman, cap. 2 (lectura parcial) |
| 3 | DLT con SVD y normalización de Hartley | Hartley & Zisserman, cap. 4.1–4.4 · Stachniss, clase 17 |
| 4 | Errores, reproyección, estabilidad. El caso de los 4 puntos | Hartley & Zisserman, cap. 4.2 |
| 5 | RANSAC: algoritmo, cantidad de iteraciones, umbral. Aplicación sobre la cancha | Hartley & Zisserman, cap. 4.7 · First Principles of CV: *Image Stitching* |

## TP4 (borrador)
`mv/camara.py`:
- `normalizar_puntos`
- `dlt_homografia`
- `error_reproyeccion`
- `ransac_homografia`
- `imagen_a_cancha`
- `cancha_a_imagen`
- `modelo_cancha` (las coordenadas de los puntos notables de una cancha de 100 × 68 m, con el área reglamentaria)

Notebook:
- marcar 6–10 puntos de la cancha en un frame real;
- estimar la homografía (tuya contra `cv2.findHomography`);
- **dibujar la cancha reproyectada** sobre la imagen;
- proyectar jugadores a una vista cenital;
- experimento de estabilidad (4 contra 6 contra 10 puntos, con ruido simulado en los clicks);
- RANSAC con un click malo.

## Conexión con el producto
Es la pieza que convierte píxeles en metros. Y explica por qué una **cámara fija** (una sola homografía para todo el partido) simplifica tanto el problema comparada con una que panea.
