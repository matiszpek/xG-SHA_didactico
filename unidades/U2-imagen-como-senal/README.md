# U2 — La imagen como señal

**Sesiones:** 4 · **TP:** TP2 → `mv/filtros.py` · **Estado:** 📋 ficha (el material completo se escribe al arrancar U1)

## Por qué
Hasta acá una imagen fue un array. En esta unidad pasa a ser una **señal**: algo que varía en el espacio, que tiene ruido, bordes, texturas y frecuencias. La operación central es la **convolución**: casi todo lo clásico (desenfocar, detectar bordes) y casi todo lo moderno (las CNN) es convolucionar.

Del diagnóstico: los bordes son donde la derivada es **grande**, la derivada amplifica el ruido, por eso se desenfoca antes, y el tono de HSV es estable frente al sol y la sombra.

## Objetivos
1. Implementar la convolución 2D desde cero, vectorizada, y explicar la diferencia con la correlación.
2. Explicar el filtro gaussiano y por qué es separable.
3. **Cálculo multivariable mínimo:** derivadas parciales, gradiente y regla de la cadena en varias variables.
4. Calcular el gradiente de una imagen (Sobel), su magnitud y su orientación.
5. Implementar Canny paso a paso: suavizado, gradiente, supresión de no máximos e histéresis.
6. Usar espacios de color (HSV, Lab) para segmentar el pasto.
7. Entender la idea de la transformada de Hough para detectar rectas.

## Contenidos y recursos por sesión

| Sesión | Contenido | Recursos |
|---|---|---|
| 1 | Formación de imagen (lo mínimo), color (RGB, HSV, Lab), histogramas, operadores puntuales (umbral, ecualización) | First Principles of CV: *Image Formation*, *Image Sensing* · Stachniss, clase 4 |
| 2 | Convolución: definición, *padding*, separabilidad. Filtros de promedio, gaussiano y mediana (no lineal). Ruido | First Principles of CV: *Image Processing I* · 3Blue1Brown: *But what is a convolution?* · Szeliski 3.2–3.3 |
| 3 | Cálculo multivariable: parciales, gradiente, regla de la cadena. Gradiente de imagen, Sobel, derivada de una gaussiana | Khan Academy, *Multivariable calculus* (gradiente) · First Principles of CV: *Edge Detection* · Stachniss, clase 12 |
| 4 | Canny completo. Hough para rectas. Aplicación: líneas de la cancha | First Principles of CV: *Boundary Detection* · Szeliski 7.2, 7.4 |

## TP2 (borrador)
`mv/filtros.py`:
- `convolucionar` (2D, vectorizada, con *padding*)
- `kernel_gaussiano`
- `filtrar_separable`
- `sobel`
- `magnitud_orientacion`
- `supresion_no_maximos`
- `histeresis`
- `canny`
- `rgb_a_hsv`
- `mascara_pasto_hsv`
- `hough_rectas`

Notebook:
- tu convolución contra `scipy.signal.convolve2d` / `cv2.filter2D`;
- el efecto del sigma;
- el ruido de compresión y los bordes falsos;
- la máscara de pasto RGB (TP0) contra HSV, con sol y sombra;
- detectar las líneas de la cancha en un frame real y ajustarlas con lo de TP1.

## Conexión con el producto
La segmentación del pasto (qué es cancha y qué no) y la detección de líneas (asistente de calibración) son piezas directas. Además, entender la convolución es requisito para entender las CNN de U6.
