"""Tests del TP0, parte B — mv/cinematica.py

Correr solo estos:   pytest tests/test_u0_cinematica.py -v
"""

import numpy as np
import pytest

from mv import cinematica as cin


@pytest.fixture
def cuadrado():
    # Recorre un cuadrado de 3 m de lado: (0,0) → (3,0) → (3,3) → (0,3) → (0,0)
    return np.array([[0, 0], [3, 0], [3, 3], [0, 3], [0, 0]], dtype=float)


def test_posicion_media(cuadrado):
    m = cin.posicion_media(cuadrado)
    assert np.shape(m) == (2,), f"tiene que devolver shape (2,), devolvió {np.shape(m)}. ¿Usaste el axis correcto?"
    np.testing.assert_allclose(m, [1.2, 1.2])


def test_distancias_por_tramo(cuadrado):
    d = cin.distancias_por_tramo(cuadrado)
    assert d.shape == (4,), f"5 posiciones → 4 tramos; devolviste shape {d.shape}"
    np.testing.assert_allclose(d, [3, 3, 3, 3])


def test_distancias_diagonal():
    P = np.array([[0, 0], [3, 4], [3, 4]], dtype=float)
    np.testing.assert_allclose(cin.distancias_por_tramo(P), [5, 0],
                               err_msg="de (0,0) a (3,4) hay 5 m (Pitágoras); quedarse quieto suma 0")


def test_distancia_total(cuadrado):
    t = cin.distancia_total(cuadrado)
    assert isinstance(t, float), f"tiene que devolver un float de Python, devolvió {type(t)}"
    assert t == pytest.approx(12.0)


def test_distancia_no_es_suma_de_coordenadas():
    P = np.array([[10, 10], [10, 10], [10, 10]], dtype=float)
    assert cin.distancia_total(P) == pytest.approx(0.0), "un jugador quieto recorre 0 m, esté donde esté"


def test_velocidades_kmh():
    P = np.array([[0, 0], [1, 0], [3, 0]], dtype=float)      # tramos de 1 m y 2 m
    v = cin.velocidades_kmh(P, fps=10)                       # cada tramo dura 0,1 s
    np.testing.assert_allclose(v, [36.0, 72.0],
                               err_msg="1 m en 0,1 s = 10 m/s = 36 km/h")


def test_tramos_validos():
    P = np.array([[0, 0], [0.5, 0], [20, 0], [20.5, 0]], dtype=float)
    ok = cin.tramos_validos(P, fps=10, v_max_kmh=40)
    assert ok.dtype == bool, f"tiene que devolver una máscara booleana, devolvió {ok.dtype}"
    # tramos: 0,5 m (18 km/h, válido) · 19,5 m (702 km/h, imposible) · 0,5 m (válido)
    np.testing.assert_array_equal(ok, [True, False, True])


def test_distancia_filtrada_ignora_saltos():
    P = np.array([[0, 0], [0.5, 0], [20, 0], [20.5, 0]], dtype=float)
    assert cin.distancia_total(P) == pytest.approx(20.5)
    assert cin.distancia_total_filtrada(P, fps=10) == pytest.approx(1.0), \
        "el salto de 19,5 m en 0,1 s (702 km/h) no es un jugador corriendo: no se suma"


def test_velocidad_tope_robusta():
    P = np.zeros((101, 2))
    P[:, 0] = np.arange(101) * 0.5          # 0,5 m por tramo a 10 fps = 18 km/h constante
    P[50:, 0] += 30                         # un salto de tracking
    v_max = cin.velocidades_kmh(P, 10).max()
    v_tope = cin.velocidad_tope(P, 10, percentil=95)
    assert isinstance(v_tope, float)
    assert v_max > 1000, "sanity check del test"
    assert v_tope == pytest.approx(18.0), "el percentil 95 no tiene que enterarse de un único salto"


def test_trayectoria_de_ejemplo_plausible():
    from mv.datos import trayectoria_ejemplo
    P, fps = trayectoria_ejemplo(con_saltos=True)
    cruda = cin.distancia_total(P)
    filtrada = cin.distancia_total_filtrada(P, fps)
    assert filtrada < cruda - 50, "filtrar los saltos tiene que bajar bastante la distancia"
    assert 15 < cin.velocidad_tope(P, fps) < 40, "la velocidad tope de un Sub-21 está entre 15 y 40 km/h"
