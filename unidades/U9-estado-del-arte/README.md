# U9 — Estado del arte + trabajo final

**Sesiones:** 3 (+ el trabajo final) · **Estado:** 📋 ficha

## Por qué
Cerrar la materia mirando hacia adelante:
- qué cambió con los *transformers* y los modelos fundacionales;
- cómo se ve el estado del arte en análisis de fútbol;
- y demostrar todo lo aprendido en un pipeline propio.

## Objetivos
1. *Attention* y *transformers* aplicados a imágenes (ViT): qué tienen distinto de una CNN.
2. Modelos fundacionales: **CLIP** (imagen + texto), **DINOv2** (*features* autosupervisadas, útiles para re-ID), **SAM** (segmentar cualquier cosa).
3. SoccerNet: los desafíos, los datasets y *Game State Reconstruction* (el problema completo: detectar, trackear, identificar y ubicar en la cancha).
4. Leer un paper con el método de las tres pasadas, y reproducir una figura.

## Contenidos y recursos por sesión

| Sesión | Contenido | Recursos |
|---|---|---|
| 1 | *Attention*, *transformers*, ViT | 3Blue1Brown, *Attention in transformers* · paper de ViT |
| 2 | CLIP, DINOv2, SAM: qué hace cada uno y cómo se usa sin entrenar | Papers de CLIP, DINOv2 y SAM |
| 3 | SoccerNet GSR: lectura guiada del paper | SoccerNet GSR (arXiv:2404.11335) · Keshav, *How to Read a Paper* |

## Trabajo final
Un pipeline didáctico sobre **un clip real de 1 minuto** de un partido de Hebraica, usando la librería `mv/`:
1. detección (YOLO *fine-tuneado* en U7, evaluado);
2. tracking (tu SORT de U8) con equipos;
3. homografía (tu DLT + RANSAC de U4), con propagación si la cámara panea (U5);
4. salida: mapa de calor por equipo y distancia recorrida por jugador (U0, filtrada).

El informe tiene que decir **honestamente** qué anda, qué no y con qué datos se midió cada cosa. No es el producto: es la demostración de que entendés cada pieza.

Al terminar: **repetir el diagnóstico inicial** (`meta/diagnostico.md`) y comparar.
