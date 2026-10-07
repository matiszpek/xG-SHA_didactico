"""Operaciones básicas sobre imágenes — TP0 (Unidad 0).

Convenciones de toda la librería (leelas, valen para todos los TPs):

- Una imagen color es un array de shape (H, W, 3): **alto primero**, después ancho, después canales.
- Salvo que se diga otra cosa, los canales están en orden **RGB** (mv.datos.cargar_frame ya convierte).
- Un píxel se indexa img[fila, columna] = img[y, x]. El origen (0, 0) es la esquina **superior izquierda**
  y la y crece **hacia abajo**.
- Las cajas se escriben como (x1, y1, x2, y2) en píxeles, con x2 e y2 **excluidos** (como en los slices).
- uint8 = enteros en [0, 255]. float32 = reales; por convención, en [0, 1].

REGLA DEL TP: nada de `for` sobre píxeles. Todo vectorizado con NumPy.
(Un `for` sobre una lista de imágenes, como en `mosaico`, sí está permitido.)
"""

from __future__ import annotations

import numpy as np


def a_float(img: np.ndarray) -> np.ndarray:
    """Convierte una imagen uint8 en [0, 255] a float32 en [0, 1].

    Ejemplo: 255 → 1.0, 0 → 0.0, 51 → 0.2.
    Devuelve un array NUEVO de dtype float32 con la misma shape.
    """
    raise NotImplementedError("TP0 — a_float")


def a_uint8(img: np.ndarray) -> np.ndarray:
    """Convierte una imagen float en [0, 1] a uint8 en [0, 255].

    - Los valores fuera de [0, 1] se recortan (clip) ANTES de convertir: -0.3 → 0, 1.7 → 255.
    - Se redondea al entero más cercano (no se trunca): 0.5/255 de más tiene que sumar 1.
    Devuelve dtype uint8, misma shape.
    """
    raise NotImplementedError("TP0 — a_uint8")


def bgr_a_rgb(img: np.ndarray) -> np.ndarray:
    """Invierte el orden de los canales: BGR → RGB (y también RGB → BGR, es la misma operación).

    Una línea. Pista: el último eje.
    """
    raise NotImplementedError("TP0 — bgr_a_rgb")


def a_gris(img: np.ndarray, pesos: tuple[float, float, float] = (0.299, 0.587, 0.114)) -> np.ndarray:
    """Escala de grises: gris = pesos[0]·R + pesos[1]·G + pesos[2]·B en cada píxel.

    - Entrada: (H, W, 3), uint8 o float, en orden RGB.
    - Salida: (H, W), float32, en la MISMA escala que la entrada (si entra uint8, sale en [0, 255]
      pero como float32; no redondear).
    - Sin loops. Pista: es un producto escalar sobre el último eje.

    Para una imagen BGR, se pasan los pesos invertidos o se convierte antes con bgr_a_rgb.
    """
    raise NotImplementedError("TP0 — a_gris")


def recortar(img: np.ndarray, caja: tuple[int, int, int, int]) -> np.ndarray:
    """Recorta la región caja = (x1, y1, x2, y2) — ojo: x es columna, y es fila.

    - Si la caja se sale de la imagen, se recorta a los bordes (no tira error).
      Ej: en una imagen de 100×200, la caja (-10, 50, 30, 400) devuelve las filas 50:100, columnas 0:30.
    - Devuelve una COPIA: modificar el recorte NO debe modificar la imagen original.
    - Funciona para imágenes (H, W) y (H, W, C).
    """
    raise NotImplementedError("TP0 — recortar")


def histograma(canal: np.ndarray) -> np.ndarray:
    """Histograma de un canal uint8: cuántos píxeles tienen cada valor de 0 a 255.

    - Entrada: array uint8 de cualquier shape (se cuentan todos los elementos).
    - Salida: array de enteros de largo EXACTAMENTE 256; salida[v] = cantidad de píxeles con valor v.
    - Sin loops. Pista: np.bincount (mirá el parámetro minlength).
    """
    raise NotImplementedError("TP0 — histograma")


def ajustar_brillo_contraste(img: np.ndarray, alfa: float = 1.0, beta: float = 0.0) -> np.ndarray:
    """Devuelve alfa·img + beta, SATURANDO en [0, 255]. Entrada y salida uint8.

    - alfa > 1 aumenta el contraste; beta > 0 aclara.
    - Saturar significa: 200 + 100 → 255 (no 44). Redondear al entero más cercano.
    - Ojo con el dtype de las cuentas intermedias.
    """
    raise NotImplementedError("TP0 — ajustar_brillo_contraste")


def mascara_pasto(img: np.ndarray, margen: int = 20) -> np.ndarray:
    """Máscara booleana (H, W) de los píxeles "verdes": G > R + margen  y  G > B + margen.

    - Entrada: RGB uint8 (H, W, 3).
    - Es una regla muy simple (en U2 la mejoramos con HSV), pero tiene una trampa de dtype.
      Pensá qué pasa con R + margen si R = 250 y todo es uint8.
    """
    raise NotImplementedError("TP0 — mascara_pasto")


def color_medio(img: np.ndarray, mascara: np.ndarray) -> np.ndarray:
    """Color promedio de los píxeles donde `mascara` es True.

    - img: (H, W, C); mascara: (H, W) booleana.
    - Devuelve un array (C,) de float64 con el promedio de cada canal.
    - Si la máscara está vacía, devuelve un array (C,) de NaN (sin warnings ni errores).
    """
    raise NotImplementedError("TP0 — color_medio")


def mosaico(imagenes: list[np.ndarray], columnas: int) -> np.ndarray:
    """Arma una grilla con imágenes de IGUAL shape (h, w, C), de izquierda a derecha y de arriba abajo.

    - Resultado: (filas·h, columnas·w, C) con filas = ceil(len(imagenes) / columnas).
    - Los huecos que sobran al final se rellenan con ceros.
    - Mismo dtype que las imágenes de entrada.
    - Acá SÍ podés iterar sobre la lista (son pocas imágenes); lo que no vale es iterar píxeles.
      Bonus (no obligatorio): hacerlo sin loop con reshape + transpose.
    """
    raise NotImplementedError("TP0 — mosaico")
