"""Modelo de Expected Goals desde cero — TP3, parte B (Unidad 3).

Regresión logística entrenada por máxima verosimilitud con descenso por gradiente, más las
herramientas para evaluarla honestamente.

Coordenadas: las de StatsBomb (en yardas). Cancha de 120 × 80, el que patea ataca hacia x = 120,
el arco está en x = 120 entre los palos y = 36 e y = 44 (8 yardas de ancho), centro en (120, 40).

REGLA DEL TP: sin loops sobre tiros (el loop sobre las iteraciones del descenso por gradiente sí).
NO se puede usar sklearn para resolver (sí para comparar en el notebook y en los tests).
"""

from __future__ import annotations

import numpy as np

ARCO_X = 120.0
PALO_IZQ_Y, PALO_DER_Y = 36.0, 44.0


def distancia_y_angulo(x, y) -> tuple[np.ndarray, np.ndarray]:
    """Distancia al CENTRO del arco (yardas) y ángulo de visión del arco (radianes) desde cada (x, y).

    El ángulo de visión es el ángulo entre los vectores tirador→palo izquierdo y tirador→palo derecho.
    Calculalo con arctan2(|producto vectorial|, producto escalar) (U1, apunte 04): es estable incluso
    pegado al arco, donde la fórmula con arctan "simple" se rompe.
    """
    raise NotImplementedError("TP3 — distancia_y_angulo")


def estandarizar(X: np.ndarray, media=None, desvio=None) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(X − media) / desvio por columna. Devuelve (X_estandarizada, media, desvio).

    - Si media y desvio son None, se calculan de X (esto se hace con el TRAIN).
    - Si vienen dados, se usan esos (esto se hace con el TEST: nunca se recalculan con el test → leakage).
    - Si una columna tiene desvío 0, usar 1 (no dividir por cero).
    """
    raise NotImplementedError("TP3 — estandarizar")


def sigmoide(z) -> np.ndarray:
    """σ(z) = 1 / (1 + e^(−z)), NUMÉRICAMENTE ESTABLE.

    Con z = −1000, e^(−z) da overflow. Truco: para z < 0 usar la forma equivalente e^z / (1 + e^z).
    """
    raise NotImplementedError("TP3 — sigmoide")


def predecir_proba(X: np.ndarray, w, b: float) -> np.ndarray:
    """P(gol) = σ(X·w + b) para cada fila de X. Devuelve (N,)."""
    raise NotImplementedError("TP3 — predecir_proba")


def log_loss(y, p, eps: float = 1e-12) -> float:
    """Log loss (= cross-entropy binaria) PROMEDIO: −mean[ y·log p + (1−y)·log(1−p) ]. Recortá p con eps."""
    raise NotImplementedError("TP3 — log_loss")


def gradiente_log_loss(X: np.ndarray, y, w, b: float, l2: float = 0.0) -> tuple[np.ndarray, float]:
    """Gradiente de la log loss promedio respecto de (w, b). Devuelve (dw (k,), db float).

    Derivalo vos (apunte 05). El resultado es sorprendentemente simple: con e = p − y,
        dw = Xᵀ e / N        db = mean(e)
    Si l2 > 0, se suma l2·w a dw (regularización; no a b).
    """
    raise NotImplementedError("TP3 — gradiente_log_loss")


def entrenar_logistica(X: np.ndarray, y, lr: float = 0.1, n_iter: int = 2000,
                       l2: float = 0.0) -> tuple[np.ndarray, float, np.ndarray]:
    """Descenso por gradiente desde w = 0, b = 0. Devuelve (w, b, historia) con historia[i] = log loss
    DESPUÉS del paso i (largo n_iter).
    """
    raise NotImplementedError("TP3 — entrenar_logistica")


def auc(y, p) -> float:
    """Área bajo la curva ROC = P(un gol elegido al azar tiene p mayor que un no-gol elegido al azar).

    Se calcula con RANGOS (estadístico de Mann-Whitney), sin armar la curva:
        AUC = (suma de los rangos de los positivos − n_pos·(n_pos+1)/2) / (n_pos · n_neg)
    donde los rangos son 1..N según p, y los EMPATES reciben el rango promedio.
    """
    raise NotImplementedError("TP3 — auc")


def curva_calibracion(y, p, n_bins: int = 10) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Agrupa las predicciones en n_bins intervalos iguales de [0, 1] y devuelve, por intervalo:
    (p media predicha, frecuencia real de goles, cantidad de tiros). Intervalos vacíos → NaN (sin warnings).

    Un modelo bien calibrado: "de los tiros con p ≈ 0,3, entra el 30 %".
    """
    raise NotImplementedError("TP3 — curva_calibracion")


def split_por_partido(match_ids, frac_test: float = 0.2, rng: np.random.Generator | None = None) -> np.ndarray:
    """Máscara booleana: True para los tiros que van a TEST. Se eligen PARTIDOS al azar
    (round(frac_test · n_partidos) de ellos), y todos los tiros de esos partidos van a test.
    """
    raise NotImplementedError("TP3 — split_por_partido")
