# U4 — Geometría de la cámara

**Sesiones:** 5 (~10 h, más el TP) · **TP:** TP4 → `mv/camara.py`

## Por qué esta unidad

Una posición en píxeles no significa nada: 300 px cerca de la cámara son unos pocos metros, y en la lateral lejana pueden ser treinta. Para medir en **metros** (distancias, velocidades, mapas de calor, la ubicación de un tiro para el xG) hay que traducir la imagen al plano de la cancha. Esa traducción es una **homografía**: una matriz de 3×3 que se estima a partir de puntos conocidos.

Es donde todo U1 rinde:
- coordenadas homogéneas y la división por W (tu `aplicar` ya la hace);
- cuadrados mínimos homogéneos con SVD (el DLT es exactamente eso);
- condicionamiento (la normalización de Hartley).

Y la probabilidad de U3 entra para diseñar RANSAC.

Además, es la unidad donde el proyecto anterior más se golpeó: homografías con 4 puntos que "daban error 0" y diferían en 20 metros (D24), y una cobertura real de calibración de ~0 %. Al terminar vas a entender por qué.

## Objetivos

Al terminar U4 puedo, sin buscar:
1. Explicar el modelo ***pinhole***: por qué se divide por la profundidad, qué son los **intrínsecos** (K) y los **extrínsecos** (R, t), y armar `P = K [R | t]`.
2. Deducir por qué un plano del mundo y la imagen se relacionan con una **homografía** `H = [p₁ p₂ p₄]`, con 8 grados de libertad, y qué conserva y qué no.
3. Derivar el **DLT** (`A h = 0`) y resolverlo con la SVD; aplicar la **normalización de Hartley** y explicar qué mejora y qué no (medido).
4. Distinguir error algebraico, geométrico y **de reproyección**, y explicar por qué con **4 puntos** el error de reproyección da 0 y **no valida nada**.
5. Implementar **RANSAC** adaptativo y calcular cuántas iteraciones hacen falta.
6. Calibrar un **frame real** del club y mostrar la cancha reproyectada y la vista cenital, diciendo cuánto error tiene en metros.

## Plan

| Sesión | Videos y lectura | Apunte | Práctica |
|---|---|---|---|
| **1** | Stachniss, Photogrammetry I, clases 15–16 · Szeliski 2.1 | [01 · El modelo *pinhole*](apuntes/01-pinhole.md) | Guía A + TP4 (`modelo_cancha`, `matriz_camara`, `proyectar`) |
| **2** | First Principles of CV: *Image Stitching* · Hartley & Zisserman, cap. 2 (2.1–2.4) | [02 · La homografía](apuntes/02-homografia.md) | Guía B + TP4 (`homografia_desde_camara`) |
| **3** | Stachniss, clase 17 · Hartley & Zisserman 4.1–4.4 | [03 · DLT](apuntes/03-dlt.md) | Guía C + TP4 (`normalizar_puntos`, `matriz_dlt`, `dlt_homografia`) |
| **4** | Hartley & Zisserman 4.2 (y 5.1 por encima) | [04 · Errores y estabilidad](apuntes/04-errores-estabilidad.md) | Guía D + TP4 (`error_reproyeccion`) + secciones 2–3 del informe |
| **5** | First Principles of CV: *Image Stitching* (RANSAC) · Hartley & Zisserman 4.7 | [05 · RANSAC](apuntes/05-ransac.md) | Guía E + TP4 (`iteraciones_ransac`, `ransac_homografia`) + frame real |

## Qué necesitás de antes

- `mv/geometria.py` del TP1 andando: `aplicar` (para aplicar homografías) y `warp` (para la vista cenital).
- Un frame real del club en `datos/frames/` (`python herramientas/bajar_frames.py --help`), preferentemente uno donde se vea **mucha cancha**: el área y la línea de medio a la vez, si existe.
- No hay dependencias nuevas.

## Guía y TP

- [Guía de ejercicios](guia.md): bloques A–E con respuestas.
- [TP4 — De píxeles a metros](tp4/enunciado.md).

## Conexión con el producto

Es la pieza que convierte píxeles en metros. Y explica con números por qué la **cámara** es la decisión central del producto: con una **cámara fija** alcanza con una homografía para todo el partido (calibrada una vez, con todos los puntos que quieras); con una que **panea**, hace falta una por frame y propagarla (U5), que es justo donde se trabó el proyecto anterior.
