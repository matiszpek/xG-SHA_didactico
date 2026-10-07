"""Probabilidad aplicada — TP3, parte A (Unidad 3).

Lo que el diagnóstico mostró flojo, convertido en funciones que se usan en el resto de la materia:
complemento, distribución de una suma de tiros, Monte Carlo, Bayes, gaussianas (1D y multivariada)
y log-verosimilitud.

REGLA DEL TP: vectorizado (salvo donde el docstring permite un loop corto). Se puede usar np.linalg
(solve, det, eigh). NO se puede usar scipy.stats para resolver (sí para comparar).
"""

from __future__ import annotations

import numpy as np


def prob_al_menos_uno(ps) -> float:
    """P(al menos un éxito) con eventos INDEPENDIENTES de probabilidades ps. Pista: el complemento."""
    raise NotImplementedError("TP3 — prob_al_menos_uno")


def distribucion_goles(xgs) -> np.ndarray:
    """Distribución EXACTA de la cantidad de goles, dados los xG de cada tiro (independientes).

    Devuelve un array de largo len(xgs) + 1: salida[k] = P(exactamente k goles).

    Idea: con un solo tiro de prob p, la distribución es [1−p, p]. Agregar un tiro nuevo es
    "convolucionar" la distribución que tenías con [1−p, p] (¿por qué? → apunte 02). Se permite un loop
    sobre los tiros (np.convolve de a uno).
    """
    raise NotImplementedError("TP3 — distribucion_goles")


def simular_goles(xgs, n_sim: int, rng: np.random.Generator | None = None) -> np.ndarray:
    """Monte Carlo: simula n_sim partidos con esos tiros y devuelve la cantidad de goles de cada uno, shape (n_sim,).

    Sin loops: una matriz (n_sim, n_tiros) de uniformes comparada contra los xG.
    """
    raise NotImplementedError("TP3 — simular_goles")


def bayes(p_a: float, p_b_dado_a: float, p_b_dado_no_a: float) -> float:
    """P(A | B) por el teorema de Bayes, con P(B) por probabilidad total."""
    raise NotImplementedError("TP3 — bayes")


def densidad_normal(x, mu: float = 0.0, sigma: float = 1.0) -> np.ndarray:
    """Densidad de la normal N(mu, sigma²) evaluada en x (escalar o array)."""
    raise NotImplementedError("TP3 — densidad_normal")


def densidad_normal_multivariada(X: np.ndarray, mu, Sigma) -> np.ndarray:
    """Densidad de la normal multivariada N(mu, Sigma) en cada fila de X (N, d). Devuelve (N,).

        p(x) = exp(−½ (x−μ)ᵀ Σ⁻¹ (x−μ)) / sqrt((2π)^d · det Σ)

    No inviertas Σ: usá np.linalg.solve (U1). Para el término cuadrático de todas las filas a la vez,
    np.einsum o un producto elemento a elemento + sum sobre el eje correcto.
    """
    raise NotImplementedError("TP3 — densidad_normal_multivariada")


def mahalanobis(X: np.ndarray, mu, Sigma) -> np.ndarray:
    """Distancia de Mahalanobis de cada fila de X a mu: sqrt((x−μ)ᵀ Σ⁻¹ (x−μ)). Devuelve (N,).

    Es "cuántos desvíos" estás del centro, teniendo en cuenta la forma (elipse) de la distribución.
    """
    raise NotImplementedError("TP3 — mahalanobis")


def elipse_confianza(mu, Sigma, k: float = 2.0, n: int = 100) -> np.ndarray:
    """n puntos (n, 2) de la elipse de los puntos a distancia de Mahalanobis k de mu.

    Receta (U1, apunte 05): autovalores λ y autovectores V de Σ (np.linalg.eigh). La elipse es la
    circunferencia unitaria, estirada por k·sqrt(λᵢ) en cada eje, rotada por V y trasladada a mu.
    """
    raise NotImplementedError("TP3 — elipse_confianza")


def log_verosimilitud_bernoulli(y, p, eps: float = 1e-12) -> float:
    """Σ [ y·log p + (1−y)·log(1−p) ] — la log-verosimilitud de resultados 0/1 dadas probabilidades p.

    Recortá p a [eps, 1−eps] antes del log, para que p = 0 o 1 no dé −∞.
    """
    raise NotImplementedError("TP3 — log_verosimilitud_bernoulli")
