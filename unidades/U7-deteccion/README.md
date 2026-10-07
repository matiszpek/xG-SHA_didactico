# U7 — Detección

**Sesiones:** 4 · **TP:** TP7 → `mv/deteccion.py` · **Estado:** 📋 ficha

## Por qué
Detectar jugadores y pelota es el primer eslabón de todo el pipeline: si las cajas están mal, todo lo que sigue sale mal multiplicado.

El error más caro del proyecto anterior fue de detección y de evaluación: correr el detector al doble de la resolución con la que fue entrenado, y no tener con qué medirlo. Acá se aprende a **evaluar bien** antes que nada.

## Objetivos
1. Clasificación, detección y segmentación. Representar cajas.
2. **IoU** y **NMS**, implementados.
3. **Precision-recall**, **AP** y **mAP**, implementados y entendidos. Por qué la *accuracy* no sirve (diagnóstico: pelota en el 2 % de los recortes).
4. Cómo funciona un detector de una etapa (YOLO): grilla, *anchors* o *anchor-free*, *heads*, pérdidas.
5. Datasets y anotación. Formato YOLO.
6. ***Fine-tuning*** sobre material propio. Resolución de inferencia contra resolución de entrenamiento. Objetos chicos (la pelota a ~10 px) y fuera de distribución (jugadores muy cercanos).
7. Evaluar por tamaño de objeto y **mirar los errores**, no solo el número.

## Contenidos y recursos por sesión

| Sesión | Contenido | Recursos |
|---|---|---|
| 1 | Cajas, IoU, NMS, precision-recall, AP/mAP | d2l.ai, cap. *Computer Vision* (cajas, *anchors*, NMS) |
| 2 | Detectores: de ventana deslizante a una etapa. YOLO por dentro | Paper de YOLO (Redmon 2016) · CS231n, *Detection and Segmentation* |
| 3 | Anotación, formato, entrenamiento y validación con Ultralytics. Errores típicos | Documentación de Ultralytics |
| 4 | *Fine-tuning* sobre frames del club. Evaluación por tamaño | — |

## TP7 (borrador)
`mv/deteccion.py`:
- `iou` (vectorizado: todas contra todas, con el truco de broadcasting de U0)
- `nms`
- `curva_precision_recall`
- `average_precision`
- `evaluar` (por clase y por rango de tamaño)

Notebook:
- etiquetar ~50–100 frames del club (con una herramienta de anotación);
- evaluar un YOLO preentrenado con **tus** métricas y compararlas con las de Ultralytics;
- el efecto de `imgsz` medido;
- *fine-tuning*;
- la mejora por tamaño de objeto;
- un mosaico de los peores errores.

## Conexión con el producto
Es literalmente la primera etapa del producto, y las métricas de esta unidad son las que van a decidir si el detector está "listo".
