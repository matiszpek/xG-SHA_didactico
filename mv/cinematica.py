"""Cinemática de trayectorias — TP0 (Unidad 0), parte B.

Una trayectoria es un array P de shape (N, 2): la posición (x, y) en METROS de un jugador
en N instantes consecutivos, separados 1/fps segundos.

Son las cuentas que vamos a usar al final de todo el pipeline (distancia recorrida, velocidad),
y que en el diagnóstico salieron mal. Acá se hacen bien, y con cuidado con los datos sucios.

REGLA DEL TP: sin `for`. Todo vectorizado.
"""

from __future__ import annotations

import numpy as np


def posicion_media(P: np.ndarray) -> np.ndarray:
    """Posición promedio: array de shape (2,). Pista: axis."""
    raise NotImplementedError("TP0 — posicion_media")


def distancias_por_tramo(P: np.ndarray) -> np.ndarray:
    """Distancia euclídea entre cada par de posiciones consecutivas.

    Devuelve shape (N-1,): salida[i] = ‖P[i+1] − P[i]‖.
    """
    raise NotImplementedError("TP0 — distancias_por_tramo")


def distancia_total(P: np.ndarray) -> float:
    """Distancia total recorrida (suma de todos los tramos), como float de Python."""
    raise NotImplementedError("TP0 — distancia_total")


def velocidades_kmh(P: np.ndarray, fps: float) -> np.ndarray:
    """Velocidad en cada tramo, en km/h. Shape (N-1,).

    Cada tramo dura 1/fps segundos. Recordá: 1 m/s = 3,6 km/h.
    """
    raise NotImplementedError("TP0 — velocidades_kmh")


def tramos_validos(P: np.ndarray, fps: float, v_max_kmh: float = 40.0) -> np.ndarray:
    """Máscara booleana (N-1,): True en los tramos físicamente posibles (velocidad <= v_max_kmh).

    Ningún jugador Sub-21 corre a más de ~35-38 km/h. Un tramo a 300 km/h no es un pique:
    es el tracker que confundió a un jugador con otro. Esos tramos hay que descartarlos.
    """
    raise NotImplementedError("TP0 — tramos_validos")


def distancia_total_filtrada(P: np.ndarray, fps: float, v_max_kmh: float = 40.0) -> float:
    """Distancia total sumando SOLO los tramos válidos (ver tramos_validos)."""
    raise NotImplementedError("TP0 — distancia_total_filtrada")


def velocidad_tope(P: np.ndarray, fps: float, percentil: float = 95.0) -> float:
    """Velocidad "tope" robusta: el percentil `percentil` de las velocidades (km/h), como float.

    ¿Por qué no el máximo? Porque un solo error de medición manda el máximo a 800 km/h.
    El percentil 95 ignora el 5 % más extremo. (Es la misma idea que preferir la mediana
    a la media cuando hay valores atípicos.)
    """
    raise NotImplementedError("TP0 — velocidad_tope")
