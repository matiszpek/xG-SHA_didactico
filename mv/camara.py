"""Geometría de la cámara: proyección, homografía (DLT normalizado) y RANSAC — TP4 (Unidad 4).

Convenciones:

- Coordenadas de CANCHA en metros: X a lo largo (0 = línea de fondo izquierda → largo), Y a lo ancho
  (0 = lateral LEJANA a la cámara → ancho = lateral cercana). Así la cancha "vista desde arriba" tiene la
  misma orientación que la imagen de la cámara del club (lo lejano arriba).
- Para la cámara 3D (sesión 1) el mundo usa además Z hacia ABAJO (Z = −9 es "9 m de altura"): con X, Y
  así orientados, es la única forma de que el sistema sea de mano derecha.
- Una homografía H (3, 3) lleva puntos de ORIGEN (src) a DESTINO (dst): dst ≃ H · src. Se devuelve
  escalada para que H[2, 2] = 1.
- Se reusa mv.geometria.aplicar (TP1) para aplicar homografías: importala, no la reescribas.

REGLA DEL TP: sin loops sobre puntos para armar matrices (el loop de RANSAC sobre iteraciones sí).
Se puede usar np.linalg (svd, inv, solve). NO se puede usar cv2.findHomography ni cv2.getPerspectiveTransform
para resolver (sí para comparar).
"""

from __future__ import annotations

import numpy as np

from mv.geometria import aplicar  # noqa: F401  (la vas a usar)


def modelo_cancha(largo: float = 100.0, ancho: float = 68.0) -> dict[str, np.ndarray]:
    """Los 27 puntos notables de una cancha, en metros (convenciones del módulo). Medidas del reglamento:
    área grande 16,5 m de profundidad × 40,32 m de ancho; área chica 5,5 × 18,32; penal a 11 m;
    círculo central de radio 9,15 m. El largo y el ancho de Hebraica Pilar se midieron en ~100 × 68.

    Nombres (exactos — los usan los tests y el notebook):
      esquina_{izq,der}_{lejana,cercana}               (4)
      medio_lejano, medio_cercano, centro                (3)  ← la línea de medio y el centro
      circulo_lejano, circulo_cercano                    (2)  ← donde el círculo corta la línea de medio
      penal_izq, penal_der                               (2)
      area_grande_{izq,der}_{lejana,cercana}_{fondo,frente}   (8)  ← "fondo" sobre la línea de fondo
      area_chica_{izq,der}_{lejana,cercana}_{fondo,frente}    (8)
    Devuelve un dict nombre → np.array([X, Y]).
    """
    raise NotImplementedError("TP4 — modelo_cancha")


def matriz_camara(K: np.ndarray, R: np.ndarray, t) -> np.ndarray:
    """P = K · [R | t], de shape (3, 4)."""
    raise NotImplementedError("TP4 — matriz_camara")


def proyectar(P: np.ndarray, X: np.ndarray) -> np.ndarray:
    """Proyecta puntos 3D X (N, 3) con la cámara P (3, 4). Devuelve (N, 2) en píxeles (dividir por W)."""
    raise NotImplementedError("TP4 — proyectar")


def homografia_desde_camara(P: np.ndarray) -> np.ndarray:
    """La homografía cancha → imagen que induce la cámara P sobre el plano Z = 0.

    Si Z = 0, P·(X, Y, 0, 1) solo usa las columnas 1, 2 y 4 de P: esa matriz de 3×3 ES la homografía.
    Devolvela con H[2, 2] = 1.
    """
    raise NotImplementedError("TP4 — homografia_desde_camara")


def normalizar_puntos(pts: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Normalización de Hartley: trasladar el centroide al origen y escalar para que la distancia media
    al origen sea √2. Devuelve (puntos_normalizados (N, 2), T (3, 3)) con puntos_normalizados = aplicar(T, pts).
    """
    raise NotImplementedError("TP4 — normalizar_puntos")


def matriz_dlt(src: np.ndarray, dst: np.ndarray) -> np.ndarray:
    """La matriz A (2N, 9) del DLT: cada correspondencia (x, y) → (u, v) aporta las filas

        [ −x  −y  −1   0   0   0   u·x  u·y  u ]
        [  0   0   0  −x  −y  −1   v·x  v·y  v ]

    de modo que A · h = 0 con h = H.ravel() (H por filas). Derivalas vos (apunte 03) antes de copiarlas.
    Orden de las filas: las dos de la correspondencia 0, las dos de la 1, etc.
    """
    raise NotImplementedError("TP4 — matriz_dlt")


def dlt_homografia(src: np.ndarray, dst: np.ndarray, normalizar: bool = True) -> np.ndarray:
    """Homografía src → dst por DLT con N ≥ 4 correspondencias.

    1. (si normalizar) normalizar src y dst por separado → Ts, Td.
    2. A = matriz_dlt(...) y h = el vector singular derecho del MENOR valor singular (U1, apunte 07).
    3. Des-normalizar: H = Td⁻¹ · Ĥ · Ts.  4. Escalar para que H[2, 2] = 1.
    """
    raise NotImplementedError("TP4 — dlt_homografia")


def error_reproyeccion(H: np.ndarray, src: np.ndarray, dst: np.ndarray) -> np.ndarray:
    """Distancia (en las unidades de dst) entre H·src y dst, por punto. Devuelve (N,)."""
    raise NotImplementedError("TP4 — error_reproyeccion")


def iteraciones_ransac(p_inlier: float, n_muestra: int = 4, confianza: float = 0.99) -> int:
    """Cuántas iteraciones hacen falta para que, con probabilidad `confianza`, al menos UNA muestra de
    n_muestra puntos sea toda de inliers:  N = ceil( log(1 − confianza) / log(1 − p_inlier^n_muestra) ).
    Casos borde: si p_inlier^n_muestra ≥ 1 → 1.
    """
    raise NotImplementedError("TP4 — iteraciones_ransac")


def ransac_homografia(src: np.ndarray, dst: np.ndarray, umbral: float = 3.0, max_iter: int = 2000,
                      confianza: float = 0.99,
                      rng: np.random.Generator | None = None) -> tuple[np.ndarray, np.ndarray]:
    """RANSAC para homografías. Devuelve (H, inliers) con inliers bool (N,).

    Repetir: elegir 4 correspondencias al azar → DLT → contar inliers (error de reproyección < umbral) →
    quedarse con el mejor conjunto. ADAPTATIVO: cada vez que mejora el mejor conjunto, recalcular cuántas
    iteraciones hacen falta con iteraciones_ransac(fracción de inliers actual) (sin pasar max_iter).
    Al final: re-estimar H con TODOS los inliers del mejor conjunto y recalcular los inliers con esa H.
    Si nunca se juntan 4 inliers, levantar RuntimeError.
    """
    raise NotImplementedError("TP4 — ransac_homografia")
