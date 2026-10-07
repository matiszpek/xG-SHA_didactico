"""Tests del TP1 — mv/geometria.py

    pytest tests/test_u1_geometria.py -v -k "parte_a"     # solo la parte A
    pytest tests/test_u1_geometria.py -v -k "parte_b"     # solo la parte B
"""

import time

import numpy as np
import pytest

from mv import geometria as g

PI = np.pi


# ===================================================================== Parte A

class TestParteA_Matrices:
    def test_parte_a_rotacion_90(self):
        R = g.rotacion(PI / 2)
        assert R.shape == (2, 2)
        np.testing.assert_allclose(R @ [1, 0], [0, 1], atol=1e-12, err_msg="R(90°) tiene que llevar î a ĵ")
        np.testing.assert_allclose(R @ [0, 1], [-1, 0], atol=1e-12)

    def test_parte_a_rotacion_es_ortogonal(self):
        R = g.rotacion(0.7)
        np.testing.assert_allclose(R.T @ R, np.eye(2), atol=1e-12, err_msg="una rotación cumple RᵀR = I")
        assert np.linalg.det(R) == pytest.approx(1.0), "una rotación tiene determinante 1"

    def test_parte_a_escala_y_cizalla(self):
        np.testing.assert_allclose(g.escala(2, 3) @ [1, 1], [2, 3])
        np.testing.assert_allclose(g.cizalla(kx=0.5) @ [0, 1], [0.5, 1], err_msg="con kx, ĵ va a (kx, 1)")
        np.testing.assert_allclose(g.cizalla(ky=2) @ [1, 0], [1, 2])
        assert np.linalg.det(g.cizalla(kx=3)) == pytest.approx(1.0), "la cizalla no cambia áreas"

    def test_parte_a_a_homogenea(self):
        T = g.a_homogenea(np.array([[1, 2], [3, 4]]), (5, 6))
        np.testing.assert_allclose(T, [[1, 2, 5], [3, 4, 6], [0, 0, 1]])

    def test_parte_a_traslacion(self):
        np.testing.assert_allclose(g.traslacion(5, -2), [[1, 0, 5], [0, 1, -2], [0, 0, 1]])


class TestParteA_Aplicar:
    def test_parte_a_aplicar_traslacion(self):
        P = np.array([[0, 0], [1, 2], [-3, 4]], dtype=float)
        Q = g.aplicar(g.traslacion(10, 20), P)
        assert Q.shape == (3, 2), f"aplicar tiene que devolver (N, 2); devolvió {Q.shape}"
        np.testing.assert_allclose(Q, P + [10, 20])

    def test_parte_a_aplicar_rotacion(self):
        P = np.array([[1, 0], [0, 1], [2, 2]], dtype=float)
        Q = g.aplicar(g.a_homogenea(g.rotacion(PI / 2)), P)
        np.testing.assert_allclose(Q, [[0, 1], [-1, 0], [-2, 2]], atol=1e-12,
                                   err_msg="¿multiplicaste por T o por Tᵀ? Revisá B4 de la guía")

    def test_parte_a_aplicar_divide_por_w(self):
        T = g.a_homogenea(g.rotacion(0.3), (4, -1))
        P = np.random.default_rng(0).normal(size=(10, 2))
        np.testing.assert_allclose(g.aplicar(5 * T, P), g.aplicar(T, P), atol=1e-12,
                                   err_msg="multiplicar T por un escalar no cambia la transformación "
                                           "(si dividís por W)")

    def test_parte_a_aplicar_perspectiva(self):
        H = np.array([[1, 0, 0], [0, 1, 0], [0.01, 0, 1]], dtype=float)  # W = 1 + 0.01·x
        Q = g.aplicar(H, np.array([[100, 50]], dtype=float))
        np.testing.assert_allclose(Q, [[50, 25]], err_msg="W = 2 en ese punto: hay que dividir x e y por W")

    def test_parte_a_rotacion_alrededor_deja_fijo_el_centro(self):
        T = g.rotacion_alrededor(PI / 2, (100, 50))
        np.testing.assert_allclose(g.aplicar(T, np.array([[100, 50]])), [[100, 50]], atol=1e-9)
        np.testing.assert_allclose(g.aplicar(T, np.array([[101, 50]])), [[100, 51]], atol=1e-9,
                                   err_msg="el punto a la derecha del centro tiene que ir 'abajo' "
                                           "(y + 1) con θ = 90°")

    def test_parte_a_composicion_orden(self):
        R = g.a_homogenea(g.rotacion(PI / 2))
        S = g.a_homogenea(g.escala(2, 1))
        p = np.array([[1.0, 0.0]])
        np.testing.assert_allclose(g.aplicar(R @ S, p), [[0, 2]], atol=1e-12)
        np.testing.assert_allclose(g.aplicar(S @ R, p), [[0, 1]], atol=1e-12)


class TestParteA_Interpolacion:
    def test_parte_a_bilineal_enteros_exactos(self):
        img = np.arange(20, dtype=float).reshape(4, 5)
        ys, xs = np.indices(img.shape)
        np.testing.assert_allclose(g.interpolar_bilineal(img, xs, ys), img,
                                   err_msg="en coordenadas enteras hay que devolver el píxel exacto")

    def test_parte_a_bilineal_punto_medio(self):
        img = np.array([[0, 10], [20, 30]], dtype=float)
        v = g.interpolar_bilineal(img, np.array([0.5]), np.array([0.5]))
        assert v.shape == (1,)
        assert v[0] == pytest.approx(15.0), "el centro de 4 píxeles es su promedio"
        v = g.interpolar_bilineal(img, np.array([0.25]), np.array([0.0]))
        assert v[0] == pytest.approx(2.5), "un cuarto del camino entre 0 y 10 es 2,5"

    def test_parte_a_bilineal_es_exacta_en_planos(self):
        ys, xs = np.indices((30, 40))
        img = 3.0 * xs - 2.0 * ys + 7.0                     # una "rampa": función lineal
        rng = np.random.default_rng(0)
        px, py = rng.uniform(0, 39, 200), rng.uniform(0, 29, 200)
        np.testing.assert_allclose(g.interpolar_bilineal(img, px, py), 3 * px - 2 * py + 7, atol=1e-9,
                                   err_msg="la interpolación bilineal reproduce exacto cualquier función lineal")

    def test_parte_a_bilineal_afuera_es_cero(self):
        img = np.ones((10, 10))
        v = g.interpolar_bilineal(img, np.array([-0.5, 3, 9.5, 3]), np.array([3, -1, 3, 12]))
        np.testing.assert_allclose(v, 0, err_msg="fuera de la imagen hay que devolver 0")

    def test_parte_a_bilineal_borde_derecho_no_explota(self):
        img = np.arange(12, dtype=float).reshape(3, 4)
        v = g.interpolar_bilineal(img, np.array([3.0, 3.0]), np.array([2.0, 0.0]))
        np.testing.assert_allclose(v, [11.0, 3.0], err_msg="el último píxel (x = W−1) es válido")

    def test_parte_a_bilineal_color_y_shapes(self):
        img = np.random.default_rng(1).integers(0, 255, size=(20, 30, 3)).astype(np.uint8)
        xs = np.full((4, 5), 3.0)
        ys = np.full((4, 5), 7.0)
        v = g.interpolar_bilineal(img, xs, ys)
        assert v.shape == (4, 5, 3), f"para imagen color y coords (4, 5) hay que devolver (4, 5, 3); {v.shape}"
        np.testing.assert_allclose(v[0, 0], img[7, 3], err_msg="ojo: img[y, x], no img[x, y]")


class TestParteA_Warp:
    @pytest.fixture
    def img(self):
        ys, xs = np.indices((120, 160))
        base = (127 + 60 * np.sin(xs / 9.0) + 60 * np.cos(ys / 7.0)).astype(np.uint8)
        return np.stack([base, base[::-1], 255 - base], axis=-1)

    def test_parte_a_warp_identidad(self, img):
        out = g.warp(img, np.eye(3), img.shape[:2])
        assert out.dtype == np.uint8, "si entra uint8 tiene que salir uint8"
        np.testing.assert_array_equal(out, img)

    def test_parte_a_warp_traslacion_entera(self, img):
        out = g.warp(img, g.traslacion(10, 5), img.shape[:2])
        np.testing.assert_array_equal(out[5:, 10:], img[:-5, :-10],
                                      err_msg="trasladar (10, 5) mueve la imagen 10 a la derecha y 5 abajo")
        assert out[:5].max() == 0 and out[:, :10].max() == 0, "lo que queda sin imagen tiene que valer 0"

    def test_parte_a_warp_shape_de_salida(self, img):
        out = g.warp(img, g.a_homogenea(g.escala(0.5, 0.5)), (60, 80))
        assert out.shape == (60, 80, 3)

    def test_parte_a_warp_como_opencv(self, img):
        cv2 = pytest.importorskip("cv2")
        T = g.rotacion_alrededor(0.4, (80, 60)) @ g.a_homogenea(g.escala(1.1, 0.9))
        mio = g.warp(img, T, img.shape[:2]).astype(float)
        ref = cv2.warpAffine(img, T[:2].astype(np.float64), (160, 120), flags=cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_CONSTANT, borderValue=0).astype(float)
        # comparamos lejos de los bordes de la imagen fuente (OpenCV y nosotros los tratamos distinto)
        ys, xs = np.indices((120, 160))
        src = g.aplicar(np.linalg.inv(T), np.stack([xs.ravel(), ys.ravel()], 1))
        interior = ((src[:, 0] > 1) & (src[:, 0] < 158) & (src[:, 1] > 1) & (src[:, 1] < 118)).reshape(120, 160)
        dif = np.abs(mio - ref)[interior]
        assert dif.mean() < 1.0 and dif.max() <= 3, (f"diferencia con OpenCV: media {dif.mean():.2f}, "
                                                     f"máx {dif.max():.0f} (esperado: media < 1)")

    def test_parte_a_warp_vectorizado(self):
        img = np.random.default_rng(2).integers(0, 255, size=(720, 1280, 3)).astype(np.uint8)
        t0 = time.perf_counter()
        g.warp(img, g.rotacion_alrededor(0.2, (640, 360)), (720, 1280))
        dt = time.perf_counter() - t0
        assert dt < 5.0, f"warp de un frame 720p tardó {dt:.1f} s; vectorizado tarda < 1 s"


# ===================================================================== Parte B

def _misma_recta(r1, r2, atol=1e-6):
    r1 = np.asarray(r1, float) / np.hypot(r1[0], r1[1])
    r2 = np.asarray(r2, float) / np.hypot(r2[0], r2[1])
    return np.allclose(r1, r2, atol=atol) or np.allclose(r1, -r2, atol=atol)


class TestParteB:
    def test_parte_b_mc_exacta(self):
        x = np.linspace(0, 10, 7)
        m, c = g.ajustar_recta_mc(np.column_stack([x, 2 * x - 3]))
        assert m == pytest.approx(2.0) and c == pytest.approx(-3.0)

    def test_parte_b_mc_como_polyfit(self):
        rng = np.random.default_rng(3)
        x = rng.uniform(0, 1000, 50)
        y = 0.1 * x + 400 + rng.normal(0, 3, 50)
        m, c = g.ajustar_recta_mc(np.column_stack([x, y]))
        m_ref, c_ref = np.polyfit(x, y, 1)
        assert isinstance(m, float) and isinstance(c, float), "tiene que devolver floats de Python"
        assert m == pytest.approx(m_ref, rel=1e-6) and c == pytest.approx(c_ref, rel=1e-6)

    def test_parte_b_total_normalizada_y_exacta(self):
        x = np.linspace(0, 10, 9)
        P = np.column_stack([x, 0.5 * x + 1])
        r = g.ajustar_recta_total(P)
        assert np.shape(r) == (3,)
        assert r[0] ** 2 + r[1] ** 2 == pytest.approx(1.0), "la recta tiene que venir normalizada: a² + b² = 1"
        assert _misma_recta(r, [0.5, -1, 1]), f"los puntos están sobre y = 0,5x + 1; devolviste {r}"

    def test_parte_b_total_vertical(self):
        P = np.array([[5, 0], [5, 1], [5, 2], [5, 3]], dtype=float)
        r = g.ajustar_recta_total(P)
        assert _misma_recta(r, [1, 0, -5]), f"la recta vertical x = 5 es (1, 0, −5); devolviste {r}"

    def test_parte_b_total_minimiza_perpendicular(self):
        rng = np.random.default_rng(4)
        t = rng.uniform(-50, 50, 40)
        P = np.column_stack([300 + 0.2 * t, 200 + 5 * t]) + rng.normal(0, 1, (40, 2))   # casi vertical
        r = g.ajustar_recta_total(P)
        m, c = g.ajustar_recta_mc(P)
        d_tls = (g.distancia_a_recta(P, r) ** 2).sum()
        d_ols = (g.distancia_a_recta(P, [m, -1, c]) ** 2).sum()
        assert d_tls <= d_ols + 1e-9, "la recta de cuadrados mínimos totales tiene que tener menor error perpendicular"

    def test_parte_b_distancia(self):
        d = g.distancia_a_recta(np.array([[3, 4], [0, 2.5]]), np.array([3, 4, -10]))
        np.testing.assert_allclose(d, [3, 0], err_msg="(3, 4) está a 3 de 3x + 4y − 10 = 0 (guía D2); "
                                                       "¿normalizaste la recta?")

    def test_parte_b_recta_por_dos_puntos(self):
        r = g.recta_por_dos_puntos(np.array([0, 0]), np.array([2, 1]))
        assert r[0] ** 2 + r[1] ** 2 == pytest.approx(1.0)
        assert _misma_recta(r, [-1, 2, 0])

    def test_parte_b_interseccion(self):
        p = g.interseccion(np.array([1, 1, -4]), np.array([1, -1, 0]))
        np.testing.assert_allclose(p, [2, 2])
        p = g.interseccion(np.array([1, 0, -2]), np.array([0, 1, -3]))
        np.testing.assert_allclose(p, [2, 3])

    def test_parte_b_interseccion_paralelas(self):
        assert g.interseccion(np.array([1, 1, -4]), np.array([1, 1, -6])) is None, \
            "las paralelas no se cortan (W = 0): hay que devolver None"
        assert g.interseccion(np.array([2, 2, -8]), np.array([1, 1, -6])) is None, \
            "paralelas aunque no vengan normalizadas"

    def test_parte_b_aproximar_rango(self):
        rng = np.random.default_rng(5)
        M = rng.normal(size=(30, 20))
        A3 = g.aproximar_rango(M, 3)
        assert A3.shape == M.shape
        assert np.linalg.matrix_rank(A3) == 3
        np.testing.assert_allclose(g.aproximar_rango(M, 20), M, atol=1e-10,
                                   err_msg="con k = rango completo hay que recuperar M")
        s = np.linalg.svd(M, compute_uv=False)
        assert np.linalg.norm(M - A3) == pytest.approx(np.sqrt((s[3:] ** 2).sum())), \
            "el error de la aproximación de rango k es √(σ²ₖ₊₁ + …) (Eckart–Young)"
