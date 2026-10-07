# U2 — La imagen como señal

**Sesiones:** 4 (~8 h, más el TP) · **TP:** TP2 → `mv/filtros.py`

## Por qué esta unidad

Hasta acá una imagen fue un array. En esta unidad pasa a ser una **señal**: algo que varía en el espacio, con ruido, bordes y texturas. La operación central es la **convolución**: casi todo lo clásico (desenfocar, derivar, detectar bordes) y casi todo lo moderno (las CNN de U6) es convolucionar.

Del diagnóstico salen tres cosas que esta unidad corrige con fundamento:
- los bordes están donde la derivada es **grande**;
- **derivar amplifica el ruido**, y por eso se desenfoca antes;
- **el tono de HSV resiste la sombra**.

También acá se aprende el **cálculo multivariable** que falta para U3 y U6.

## Objetivos

Al terminar U2 puedo, sin buscar:
1. Explicar por qué HSV separa "qué color" de "cuánta luz", y cuándo el tono no sirve.
2. Implementar la convolución 2D vectorizada, explicar la diferencia con la correlación y elegir el modo de borde.
3. Explicar el gaussiano (σ, radio 3σ, normalización) y por qué es **separable** (rango 1).
4. Calcular derivadas parciales, gradientes y la regla de la cadena en varias variables.
5. Calcular e interpretar el gradiente de una imagen (Sobel): magnitud, orientación y signos con la y hacia abajo.
6. Implementar Canny paso a paso, y explicar qué criterio ataca cada paso.
7. Detectar rectas con Hough, y refinarlas con los cuadrados mínimos totales del TP1.

## Plan

| Sesión | Videos y lectura | Apunte | Práctica |
|---|---|---|---|
| **1** | First Principles of CV: *Image Formation*, *Image Sensing* · Stachniss, clase 4 | [01 · Color e histogramas](apuntes/01-color-histogramas.md) | Guía A + **TP2 S1** |
| **2** | First Principles of CV: *Image Processing I* · 3Blue1Brown: *But what is a convolution?* · Szeliski 3.2–3.3 | [02 · Convolución](apuntes/02-convolucion.md) | Guía B + **TP2 S2** |
| **3** | Khan Academy: *partial derivatives*, *gradient* · First Principles of CV: *Edge Detection* · Stachniss, clase 12 | [03 · Gradiente y bordes](apuntes/03-gradiente-bordes.md) | Guía C + **TP2 S3** |
| **4** | First Principles of CV: *Boundary Detection* · Szeliski 7.2.1 y 7.4.2 | [04 · Canny y Hough](apuntes/04-canny-hough.md) | Guía D + **TP2 S4** |

En esta unidad el TP va **en paralelo** con las sesiones: cada sesión implementa su parte de `mv/filtros.py` (los tests están separados por sesión: `-k s1`, `-k s2`, etc.).

## Guía y TP

- [Guía de ejercicios](guia.md): bloques A–D con respuestas.
- [TP2 — Bordes y líneas de la cancha](tp2/enunciado.md).

**Requisito:** TP1 aprobado. El TP2 usa `mv.geometria` (cuadrados mínimos totales, intersecciones) para refinar las rectas de Hough.
