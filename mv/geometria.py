"""Geometría 2D y álgebra lineal aplicada — TP1 (Unidad 1).

Convenciones (además de las de mv/imagen.py):

- Los puntos se pasan como FILAS: un array (N, 2) con columnas (x, y) en píxeles.
- Las transformaciones afines y proyectivas son matrices (3, 3) en coordenadas homogéneas que
  llevan un punto (x, y, 1) de la imagen de ENTRADA a la de SALIDA.
- Las rotaciones usan la matriz "de libro": [[cos θ, −sin θ], [sin θ, cos θ]]. Como en las imágenes
  la y crece hacia abajo, un θ positivo se VE como un giro horario en pantalla. No es un error.
- Una recta a·x + b·y + c = 0 se representa con el array (a, b, c), NORMALIZADO para que a² + b² = 1.

REGLA DEL TP: sin `for` sobre píxeles ni sobre puntos. Se puede usar np.linalg.solve, np.linalg.svd,
np.cross y np.linalg.inv (para invertir la matriz de 3×3 de la transformación). NO se puede usar
cv2.warpAffine / cv2.remap / np.polyfit / np.linalg.lstsq para resolver: son para comparar en el notebook.
"""

from __future__ import annotations

import numpy as np

# =====================================================================================
# Parte A — Transformaciones (después de la sesión 4)
# =====================================================================================


def rotacion(theta: float) -> np.ndarray:
    """Matriz (2, 2) de rotación por `theta` radianes."""
    raise NotImplementedError("TP1 — rotacion")


def escala(sx: float, sy: float) -> np.ndarray:
    """Matriz (2, 2) que estira el eje x por `sx` y el eje y por `sy`."""
    raise NotImplementedError("TP1 — escala")


def cizalla(kx: float = 0.0, ky: float = 0.0) -> np.ndarray:
    """Matriz (2, 2) de cizalla: [[1, kx], [ky, 1]].

    Con kx ≠ 0, ĵ = (0, 1) va a (kx, 1): las verticales se inclinan.
    """
    raise NotImplementedError("TP1 — cizalla")


def a_homogenea(M: np.ndarray, t: tuple[float, float] = (0.0, 0.0)) -> np.ndarray:
    """Arma la matriz afín (3, 3) a partir de una lineal M (2, 2) y una traslación t = (tx, ty).

    Resultado: [[M, t], [0, 0, 1]]  →  (x, y) ↦ M·(x, y) + t
    """
    raise NotImplementedError("TP1 — a_homogenea")


def traslacion(tx: float, ty: float) -> np.ndarray:
    """Matriz (3, 3) que traslada por (tx, ty)."""
    raise NotImplementedError("TP1 — traslacion")


def aplicar(T: np.ndarray, puntos: np.ndarray) -> np.ndarray:
    """Aplica la matriz homogénea T (3, 3) a puntos (N, 2) y devuelve (N, 2).

    Pasos: agregar la columna de unos → multiplicar → DIVIDIR por la tercera coordenada.
    La división tiene que estar aunque con matrices afines no haga nada: en U4 esta misma
    función aplica homografías, y ahí la división por W es la perspectiva.
    Consecuencia que el test verifica: aplicar(T, p) == aplicar(5 * T, p).
    """
    raise NotImplementedError("TP1 — aplicar")


def rotacion_alrededor(theta: float, centro: tuple[float, float]) -> np.ndarray:
    """Matriz (3, 3) que rota `theta` alrededor de `centro` (no del origen).

    Pista: el "sándwich" del apunte 04. Componé con @ las funciones de arriba.
    """
    raise NotImplementedError("TP1 — rotacion_alrededor")


def interpolar_bilineal(img: np.ndarray, xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
    """Valor de la imagen en coordenadas NO enteras (xs, ys), por interpolación bilineal.

    - img: (H, W) o (H, W, C). xs, ys: arrays de la misma shape S (cualquier shape).
    - Devuelve float64 de shape S (grises) o S + (C,) (color).
    - Un punto (x, y) entre los píxeles (x0, y0), (x0+1, y0), (x0, y0+1) y (x0+1, y0+1), con
      x0 = floor(x), y0 = floor(y), dx = x − x0, dy = y − y0, vale:
          (1−dx)(1−dy)·I[y0, x0] + dx(1−dy)·I[y0, x0+1] + (1−dx)dy·I[y0+1, x0] + dx·dy·I[y0+1, x0+1]
    - Los puntos FUERA de la imagen (x < 0, x > W−1, y < 0 o y > H−1) valen 0.
    - En coordenadas enteras devuelve exactamente el píxel.
    - Ojo con los índices x0+1 / y0+1 en el borde derecho e inferior: no se pueden salir del array.
    """
    raise NotImplementedError("TP1 — interpolar_bilineal")


def warp(img: np.ndarray, T: np.ndarray, shape_salida: tuple[int, int]) -> np.ndarray:
    """Transforma la imagen con T (3, 3), que lleva coordenadas de ENTRADA a coordenadas de SALIDA.

    - shape_salida = (H_out, W_out).
    - Método: INVERSE MAPPING. Para cada píxel (x, y) de la salida, buscar de dónde viene:
      (x', y') = T⁻¹·(x, y), e interpolar la entrada ahí.
      (¿Por qué no al revés, "empujando" cada píxel de la entrada a la salida? Es una pregunta
      del informe.)
    - Los píxeles de la salida que caen fuera de la entrada quedan en 0.
    - Mismo dtype que la entrada: si es uint8, se redondea y se recorta a [0, 255].
    - Sin loops. Pista: np.meshgrid (o np.indices) para las coordenadas de todos los píxeles,
      después aplicar e interpolar_bilineal.
    """
    raise NotImplementedError("TP1 — warp")


# =====================================================================================
# Parte B — Ajuste de rectas y SVD (después de la sesión 7)
# =====================================================================================


def ajustar_recta_mc(puntos: np.ndarray) -> tuple[float, float]:
    """Cuadrados mínimos ORDINARIOS: la recta y = m·x + c que minimiza los residuos VERTICALES.

    - puntos: (N, 2), N ≥ 2. Devuelve (m, c) como floats.
    - Con las ecuaciones normales (AᵀA)·[m, c] = Aᵀy, resueltas con np.linalg.solve.
    """
    raise NotImplementedError("TP1 — ajustar_recta_mc")


def ajustar_recta_total(puntos: np.ndarray) -> np.ndarray:
    """Cuadrados mínimos TOTALES: la recta que minimiza las distancias PERPENDICULARES.

    - puntos: (N, 2), N ≥ 2. Devuelve (a, b, c) con a² + b² = 1 (ver la receta en el apunte 07).
    - Funciona con cualquier inclinación, incluida la vertical.
    - El signo de (a, b, c) es arbitrario (−(a, b, c) es la misma recta); los tests lo aceptan.
    """
    raise NotImplementedError("TP1 — ajustar_recta_total")


def distancia_a_recta(puntos: np.ndarray, recta: np.ndarray) -> np.ndarray:
    """Distancia perpendicular (≥ 0) de cada punto (N, 2) a la recta (a, b, c). Devuelve (N,).

    No asumas que la recta viene normalizada: normalizala adentro.
    """
    raise NotImplementedError("TP1 — distancia_a_recta")


def recta_por_dos_puntos(p1: np.ndarray, p2: np.ndarray) -> np.ndarray:
    """Recta (a, b, c) normalizada que pasa por p1 y p2, usando el producto vectorial en homogéneas."""
    raise NotImplementedError("TP1 — recta_por_dos_puntos")


def interseccion(r1: np.ndarray, r2: np.ndarray, eps: float = 1e-9) -> np.ndarray | None:
    """Punto (x, y) donde se cortan dos rectas, usando el producto vectorial en homogéneas.

    - Si las rectas son paralelas (la tercera coordenada del producto es ~0, |W| < eps),
      devuelve None.
    - No asumas que vienen normalizadas: normalizalas adentro. Con las rectas normalizadas,
      |W| = |sen| del ángulo entre ellas, y por eso alcanza con un eps absoluto.
    """
    raise NotImplementedError("TP1 — interseccion")


def aproximar_rango(M: np.ndarray, k: int) -> np.ndarray:
    """Mejor aproximación de rango k de la matriz M (2D), con la SVD: suma de las k primeras capas.

    Devuelve float64 de la misma shape que M.
    """
    raise NotImplementedError("TP1 — aproximar_rango")
