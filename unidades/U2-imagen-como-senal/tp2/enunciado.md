# TP2 — Bordes y líneas de la cancha

**Unidad:** U2 · **Entrega:** por sesión o todo junto · **Tiempo estimado:** 6–8 h en total

## Objetivo

Construir desde cero la caja de herramientas clásica de procesamiento de imágenes y usarla para un problema real del proyecto: **encontrar automáticamente las líneas de la cancha** en un frame de Hebraica. Ese es el insumo de la homografía de U4.

Todo va a `mv/filtros.py`. Leé el docstring del módulo antes de arrancar: tiene las convenciones (modos de borde, kernels impares) y la lista de lo que **no** se puede usar.

## Parte por sesión

| Sesión | Funciones | Tests |
|---|---|---|
| S1 · Color | `rgb_a_hsv`, `mascara_pasto_hsv`, `ecualizar_histograma` | `pytest tests/test_u2_filtros.py -v -k s1` |
| S2 · Convolución | `correlacionar`, `convolucionar`, `kernel_gaussiano`, `filtrar_separable`, `desenfocar_gaussiano`, `filtro_mediana` | `-k s2` |
| S3 · Gradiente | `gradiente_sobel`, `magnitud_orientacion` | `-k s3` |
| S4 · Canny y Hough | `supresion_no_maximos`, `histeresis`, `canny`, `hough_rectas`, `picos_hough`, `recta_desde_hough` | `-k s4` |

Son 31 tests en total. Varios comparan contra OpenCV, SciPy o scikit-image: esas librerías **verifican** tu implementación, no la reemplazan.

## Informe (`tp2.ipynb`)

| Sección | Experimento | Pregunta central |
|---|---|---|
| S1.a | Canales H, S y V de un frame | ¿Qué "ve" cada canal? |
| S1.b | Máscara RGB (TP0) contra HSV con una sombra simulada (y real, si tu frame tiene) | ¿Cuál resiste y por qué? |
| S1.c | Ecualizar un frame oscuro | ¿Qué gana y qué empeora? |
| S2.a | Tu convolución contra SciPy: diferencia y tiempo | — |
| S2.b | Modos de borde con un desenfoque grande | ¿Qué artefacto deja cada modo? |
| S2.c | Kernel "desplazamiento": correlación contra convolución | ¿Para qué lado se mueve la imagen con cada una? |
| S2.d | σ = 1, 2, 4, 8 sobre un recorte con la pelota | ¿Desde qué σ desaparece la pelota? |
| S2.e | Separable contra 2D, con k = 31 | ¿La aceleración coincide con k/2? |
| S2.f | Gaussiano contra mediana con sal y pimienta | ¿Cuál gana y por qué? |
| S3.a | gx, gy, magnitud y orientación de un frame | ¿Qué bordes detecta cada uno? |
| S3.b | Perfil 1D a través de una línea de cal, derivado con y sin suavizar | Ver el ruido amplificado y los "dos bordes" |
| S4.a | Canny paso a paso, y contra `cv2.Canny` | ¿Qué hace cada paso? |
| S4.b | Barrido de umbrales | ¿Qué se gana y qué se pierde? |
| **S4.c** | **Pipeline de líneas de la cancha:** pasto HSV → cal → Canny → Hough → refinar con cuadrados mínimos totales → intersecciones | ¿Hasta dónde llega lo automático en **tus** frames? |

La S4.c es el corazón del TP. Si tu frame solo muestra las laterales, documentalo: es un resultado válido y explica por qué la calibración del proyecto anterior terminó siendo asistida.

## Para el coloquio

- En tu `convolucionar`: ¿qué shape tiene la vista de `sliding_window_view` y por qué no ocupa memoria nueva?
- Mostrame en tu código dónde se da vuelta el kernel. ¿Qué pasaría con Sobel si confundieras correlación con convolución?
- ¿Por qué tu máscara HSV resiste la sombra? Hacé la cuenta con un píxel.
- En tu supresión de no máximos: ¿qué vecinos comparás cuando θ = 45°, y por qué esos y no los otros dos?
- ¿Cuántas iteraciones hace tu histéresis en el peor caso? ¿De qué depende?
- ¿Por qué Hough encuentra a veces dos rectas por línea de cal? ¿Cómo lo manejaste?

## Criterios

Los de [`meta/metodo.md`](../../../meta/metodo.md). En este TP pesa mucho la **S4.c**: que el pipeline funcione en tus frames y, sobre todo, que el informe diga **honestamente** dónde falla y por qué.
