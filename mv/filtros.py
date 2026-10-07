"""La imagen como señal: color, convolución, gradiente, bordes y rectas — TP2 (Unidad 2).

Convenciones (además de las de mv/imagen.py):

- Salvo que se diga otra cosa, las funciones de filtrado trabajan sobre imágenes en GRISES (H, W)
  y devuelven float64 de la MISMA shape (la salida no se achica: se rellena el borde).
- Modos de borde (`modo`), cómo se rellena afuera de la imagen antes de filtrar:
      "cero"      → 0 0 | a b c d | 0 0          (np.pad mode="constant")
      "replicar"  → a a | a b c d | d d          (np.pad mode="edge")
      "espejo"    → c b | a b c d | c b          (np.pad mode="reflect")  ← el default
- Los kernels 2D tienen tamaño IMPAR en cada eje (el centro es un píxel).
- Ángulos en radianes salvo en HSV, donde H va en grados [0, 360).

REGLA DEL TP: nada de `for` sobre píxeles. Se permiten loops cortos sobre cosas que NO son píxeles:
los elementos de un kernel chico, los 180 ángulos de Hough, las iteraciones de la histéresis o los canales.
Pista para la convolución: np.lib.stride_tricks.sliding_window_view + np.einsum (o un loop sobre el kernel).

NO se puede usar (para resolver): cv2.filter2D, cv2.Sobel, cv2.Canny, cv2.cvtColor, scipy.ndimage.*,
scipy.signal.*, skimage.*. Sí para comparar en el notebook y en los tests.
"""

from __future__ import annotations

import numpy as np

# =====================================================================================
# Sesión 1 — Color e histogramas
# =====================================================================================


def rgb_a_hsv(img: np.ndarray) -> np.ndarray:
    """Convierte RGB → HSV. Entrada (H, W, 3) uint8 (en [0, 255]) o float (en [0, 1]).

    Devuelve float64 (H, W, 3) con:
      H (tono) en grados, [0, 360);  S (saturación) en [0, 1];  V (valor/brillo) en [0, 1].

    Fórmulas (con R, G, B en [0, 1], M = max, m = min, C = M − m):
      V = M
      S = C / M   (y S = 0 si M = 0)
      H = 60° · ( (G−B)/C mod 6 )   si M == R
          60° · ( (B−R)/C + 2 )     si M == G
          60° · ( (R−G)/C + 4 )     si M == B
          0                         si C == 0   (gris: el tono no está definido)
    Sin NaN ni warnings (cuidado con las divisiones por cero: np.where antes de dividir).
    """
    raise NotImplementedError("TP2 — rgb_a_hsv")


def mascara_pasto_hsv(img: np.ndarray, h_min: float = 70.0, h_max: float = 170.0,
                      s_min: float = 0.2, v_min: float = 0.08) -> np.ndarray:
    """Máscara booleana (H, W) de pasto: tono entre h_min y h_max, saturación ≥ s_min y brillo ≥ v_min.

    A diferencia de la regla RGB del TP0, oscurecer la imagen (sombra) casi no cambia H ni S.
    """
    raise NotImplementedError("TP2 — mascara_pasto_hsv")


def ecualizar_histograma(gris: np.ndarray) -> np.ndarray:
    """Ecualización de histograma de una imagen uint8 (H, W). Devuelve uint8.

    Con hist = histograma, cdf = suma acumulada, N = cantidad de píxeles y cdf_min = cdf en el
    primer valor que aparece:
        lut[v] = round( (cdf[v] − cdf_min) / (N − cdf_min) · 255 )
        salida = lut[gris]          (indexar un array con otro: la "tabla" se aplica de una)
    Si la imagen es constante (N == cdf_min), devolverla igual.
    """
    raise NotImplementedError("TP2 — ecualizar_histograma")


# =====================================================================================
# Sesión 2 — Convolución y filtros
# =====================================================================================


def correlacionar(img: np.ndarray, kernel: np.ndarray, modo: str = "espejo") -> np.ndarray:
    """Correlación 2D: salida[y, x] = Σ_{i,j} kernel[i, j] · img_rellena[y + i, x + j].

    (Con el kernel centrado: i y j recorren el kernel y la imagen se rellena r píxeles por lado.)
    img: (H, W); kernel: (kh, kw) impares. Devuelve float64 (H, W).
    """
    raise NotImplementedError("TP2 — correlacionar")


def convolucionar(img: np.ndarray, kernel: np.ndarray, modo: str = "espejo") -> np.ndarray:
    """Convolución 2D = correlación con el kernel DADO VUELTA en los dos ejes. Una línea."""
    raise NotImplementedError("TP2 — convolucionar")


def kernel_gaussiano(sigma: float, radio: int | None = None) -> np.ndarray:
    """Kernel gaussiano 1D, normalizado para que sume 1.

    - Posiciones x = −r, …, 0, …, r con r = `radio` o, si es None, r = ceil(3·sigma).
    - Valores ∝ exp(−x² / (2σ²)). Largo 2r + 1.
    """
    raise NotImplementedError("TP2 — kernel_gaussiano")


def filtrar_separable(img: np.ndarray, k1d: np.ndarray, modo: str = "espejo") -> np.ndarray:
    """Convoluciona con k1d a lo largo de las filas y después a lo largo de las columnas.

    Da lo mismo que convolucionar con el kernel 2D np.outer(k1d, k1d), pero con 2·k operaciones
    por píxel en vez de k². (¿Por qué funciona? → apunte 02 y la SVD de U1.)
    """
    raise NotImplementedError("TP2 — filtrar_separable")


def desenfocar_gaussiano(img: np.ndarray, sigma: float, modo: str = "espejo") -> np.ndarray:
    """Desenfoque gaussiano separable. Acepta (H, W) o (H, W, C): en color, cada canal por separado.
    Devuelve float64 con la misma shape.
    """
    raise NotImplementedError("TP2 — desenfocar_gaussiano")


def filtro_mediana(img: np.ndarray, tam: int = 3, modo: str = "espejo") -> np.ndarray:
    """Filtro de mediana de ventana tam × tam (tam impar) sobre (H, W). Devuelve float64.

    No es lineal: no se puede escribir como convolución. Ideal para ruido "sal y pimienta".
    """
    raise NotImplementedError("TP2 — filtro_mediana")


# =====================================================================================
# Sesión 3 — Gradiente
# =====================================================================================


def gradiente_sobel(gris: np.ndarray, modo: str = "espejo") -> tuple[np.ndarray, np.ndarray]:
    """Gradiente con Sobel. Devuelve (gx, gy), float64 (H, W) cada uno.

    - gx > 0 donde la intensidad CRECE HACIA LA DERECHA; gy > 0 donde crece HACIA ABAJO.
    - Kernel (en forma de CORRELACIÓN) para gx:   [[-1, 0, 1],
                                                   [-2, 0, 2],
                                                   [-1, 0, 1]]   y su transpuesta para gy.
    - Sobre una rampa de pendiente 1 por píxel, gx vale 8 (no 1): es una derivada SIN normalizar.
    """
    raise NotImplementedError("TP2 — gradiente_sobel")


def magnitud_orientacion(gx: np.ndarray, gy: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Devuelve (magnitud, orientación): ‖∇I‖ y el ángulo arctan2(gy, gx) en radianes, en (−π, π]."""
    raise NotImplementedError("TP2 — magnitud_orientacion")


# =====================================================================================
# Sesión 4 — Canny y Hough
# =====================================================================================


def supresion_no_maximos(mag: np.ndarray, theta: np.ndarray) -> np.ndarray:
    """Adelgaza los bordes: conserva mag[y, x] solo si es ≥ que sus 2 vecinos EN LA DIRECCIÓN DEL GRADIENTE.

    - Cuantizar el ángulo (en grados, módulo 180) en 4 direcciones:
        [0, 22.5) ∪ [157.5, 180) → vecinos izquierda / derecha
        [22.5, 67.5)             → vecinos (y+1, x+1) y (y−1, x−1)   (ojo: la y va hacia abajo)
        [67.5, 112.5)            → vecinos arriba / abajo
        [112.5, 157.5)           → vecinos (y+1, x−1) y (y−1, x+1)
    - Afuera de la imagen, los vecinos valen 0.
    - Devuelve float64 (H, W): mag donde sobrevive y 0 donde no.
    Sin loops: armá los 8 "vecinos desplazados" con slicing sobre mag rellenada, y elegí con np.select.
    """
    raise NotImplementedError("TP2 — supresion_no_maximos")


def histeresis(mag: np.ndarray, bajo: float, alto: float) -> np.ndarray:
    """Umbral con histéresis. Devuelve bool (H, W).

    - Fuertes: mag > alto. Débiles: mag > bajo.
    - Un débil sobrevive si está conectado a un fuerte (8-vecindad), aunque sea a través de otros débiles.
    - Idea: partir de los fuertes y "dilatar dentro de los débiles" hasta que no cambie nada.
      El loop sobre iteraciones está permitido; dentro de cada iteración, todo vectorizado.
    """
    raise NotImplementedError("TP2 — histeresis")


def canny(gris: np.ndarray, sigma: float = 1.4, bajo: float = 0.1, alto: float = 0.25) -> np.ndarray:
    """Detector de bordes de Canny con TUS funciones: desenfoque gaussiano → Sobel → magnitud/orientación
    → supresión de no máximos → histéresis.

    `bajo` y `alto` son FRACCIONES de la magnitud máxima después de la supresión (así no dependen
    de la escala de la imagen). Devuelve bool (H, W).
    """
    raise NotImplementedError("TP2 — canny")


def hough_rectas(bordes: np.ndarray, n_theta: int = 180,
                 paso_rho: float = 1.0) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Transformada de Hough para rectas en la forma normal  x·cos θ + y·sin θ = ρ.

    - thetas = k·π/n_theta para k = 0, …, n_theta−1   (θ ∈ [0, π)).
    - D = ceil(hypot(H, W));  rhos = np.arange(−D, D + paso_rho, paso_rho).
    - Cada píxel de borde (x, y) vota, para cada θ, en la celda de ρ más cercana: round((ρ + D) / paso_rho).
    - Devuelve (acumulador int (len(rhos), n_theta), thetas, rhos).
    Se permite un loop sobre los θ; no sobre los píxeles (pista: np.bincount).
    """
    raise NotImplementedError("TP2 — hough_rectas")


def picos_hough(acc: np.ndarray, thetas: np.ndarray, rhos: np.ndarray, n: int = 5,
                vecindad: tuple[int, int] = (10, 10)) -> list[tuple[float, float, int]]:
    """Los n picos más votados del acumulador, como lista de (ρ, θ, votos), de más a menos votos.

    Después de tomar un pico, poner en 0 su vecindad (±vecindad[0] celdas de ρ, ±vecindad[1] de θ)
    para no volver a elegir "la misma recta" corrida un poquito. Si se acaban los votos, cortar antes.
    """
    raise NotImplementedError("TP2 — picos_hough")


def recta_desde_hough(rho: float, theta: float) -> np.ndarray:
    """Convierte (ρ, θ) a la recta (a, b, c) de mv.geometria: a·x + b·y + c = 0, ya normalizada."""
    raise NotImplementedError("TP2 — recta_desde_hough")
