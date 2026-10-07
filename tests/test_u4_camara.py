"""Tests del TP4 — mv/camara.py   (necesita mv/geometria.py del TP1 andando: usa `aplicar`)

    pytest tests/test_u4_camara.py -v
"""

import numpy as np
import pytest

from mv import camara as cam
from mv import geometria as g


def _camara_club():
    """Cámara sintética parecida a la del club: al costado de la cancha, 9 m de alto, mirando el centro.
    Mundo: X a lo largo (0 → 100), Y a lo ancho (0 = lateral lejana, 68 = cercana), Z hacia ABAJO
    (así el sistema es de mano derecha y "derecha en la imagen" = +X)."""
    K = np.array([[1400, 0, 960], [0, 1400, 540], [0, 0, 1.0]])
    C = np.array([50.0, 80.0, -9.0])
    zc = np.array([50.0, 34.0, 0.0]) - C
    zc /= np.linalg.norm(zc)
    abajo = np.array([0, 0, 1.0])
    yc = abajo - (abajo @ zc) * zc
    yc /= np.linalg.norm(yc)
    xc = np.cross(yc, zc)
    R = np.vstack([xc, yc, zc])
    return K, R, -R @ C


def _misma_homografia(H1, H2, atol=1e-6):
    return np.allclose(H1 / H1[2, 2], H2 / H2[2, 2], atol=atol)


# --------------------------------------------------------------------- modelo de cancha y cámara

def test_modelo_cancha():
    p = cam.modelo_cancha()
    assert len(p) == 27, f"hay 27 puntos notables (ver docstring); hay {len(p)}"
    np.testing.assert_allclose(p["centro"], [50, 34])
    np.testing.assert_allclose(p["penal_izq"], [11, 34], err_msg="el penal está a 11 m de la línea de fondo")
    ancho_area = p["area_grande_izq_cercana_fondo"][1] - p["area_grande_izq_lejana_fondo"][1]
    assert ancho_area == pytest.approx(40.32), "el área grande mide 40,32 m de ancho"
    assert p["area_grande_der_lejana_frente"][0] == pytest.approx(100 - 16.5)
    assert p["area_chica_izq_lejana_frente"][0] == pytest.approx(5.5)
    p2 = cam.modelo_cancha(105, 68)
    assert p2["penal_der"][0] == pytest.approx(94), "con largo 105, el penal derecho está en 105 − 11"


def test_matriz_camara_y_proyectar():
    K = np.array([[1000, 0, 320], [0, 1000, 240], [0, 0, 1.0]])
    P = cam.matriz_camara(K, np.eye(3), [0, 0, 5])
    assert P.shape == (3, 4)
    x = cam.proyectar(P, np.array([[1.0, 0, 0], [0, 0, 0], [0, 2.0, 5.0]]))
    np.testing.assert_allclose(x, [[1000 / 5 + 320, 240], [320, 240], [320, 240 + 1000 * 2 / 10]],
                               err_msg="x = f·X/Z + cx: lo que está más lejos (Z más grande) se ve más chico")


def test_homografia_desde_camara():
    K, R, t = _camara_club()
    P = cam.matriz_camara(K, R, t)
    H = cam.homografia_desde_camara(P)
    assert H.shape == (3, 3) and H[2, 2] == pytest.approx(1.0)
    XY = np.random.default_rng(0).uniform([0, 0], [100, 68], (20, 2))
    X3 = np.column_stack([XY, np.zeros(20)])
    np.testing.assert_allclose(g.aplicar(H, XY), cam.proyectar(P, X3), atol=1e-8,
                               err_msg="para puntos con Z = 0, la cámara ES una homografía: las columnas 1, 2 y 4 de P")


# --------------------------------------------------------------------- DLT

def test_normalizar_puntos():
    pts = np.random.default_rng(1).uniform([300, 200], [1700, 900], (15, 2))
    pn, T = cam.normalizar_puntos(pts)
    assert T.shape == (3, 3)
    np.testing.assert_allclose(pn.mean(axis=0), 0, atol=1e-10, err_msg="el centroide tiene que quedar en el origen")
    assert np.linalg.norm(pn, axis=1).mean() == pytest.approx(np.sqrt(2)), "la distancia media al origen tiene que ser √2"
    np.testing.assert_allclose(g.aplicar(T, pts), pn, atol=1e-10, err_msg="T tiene que llevar los puntos originales a los normalizados")


def test_matriz_dlt_anula_a_h():
    K, R, t = _camara_club()
    H = cam.homografia_desde_camara(cam.matriz_camara(K, R, t))
    src = np.random.default_rng(2).uniform([20, 0], [80, 68], (6, 2))
    dst = g.aplicar(H, src)
    A = cam.matriz_dlt(src, dst)
    assert A.shape == (12, 9), "2 ecuaciones por correspondencia, 9 incógnitas"
    np.testing.assert_allclose(A @ H.ravel(), 0, atol=1e-6, err_msg="con correspondencias exactas, A·h = 0")


@pytest.mark.parametrize("n", [4, 8, 20])
def test_dlt_recupera_exacto(n):
    K, R, t = _camara_club()
    H = cam.homografia_desde_camara(cam.matriz_camara(K, R, t))
    src = np.random.default_rng(n).uniform([20, 0], [80, 68], (n, 2))
    dst = g.aplicar(H, src)
    He = cam.dlt_homografia(src, dst)
    assert He[2, 2] == pytest.approx(1.0), "devolvela escalada para que H[2, 2] = 1"
    assert _misma_homografia(He, H, atol=1e-6), f"con {n} puntos exactos hay que recuperar H"


def test_dlt_como_opencv():
    cv2 = pytest.importorskip("cv2")
    K, R, t = _camara_club()
    H = cam.homografia_desde_camara(cam.matriz_camara(K, R, t))
    r = np.random.default_rng(3)
    src = r.uniform([20, 0], [80, 68], (15, 2))
    dst = g.aplicar(H, src) + r.normal(0, 1.5, (15, 2))      # clicks con ~1,5 px de error
    mio = cam.dlt_homografia(src, dst)
    ref, _ = cv2.findHomography(src, dst, 0)                  # OpenCV además refina el error geométrico
    err_mio = cam.error_reproyeccion(mio, src, dst).mean()
    err_ref = cam.error_reproyeccion(ref, src, dst).mean()
    # El DLT minimiza el error ALGEBRAICO; OpenCV después refina el GEOMÉTRICO (apunte 03, sección 5), así que
    # es esperable que OpenCV quede un poco mejor (medido: ~15 %). Mucho peor indica un error.
    assert err_mio <= err_ref * 1.3 + 0.1, f"tu DLT ajusta bastante peor que OpenCV ({err_mio:.2f} vs {err_ref:.2f} px)"


def test_normalizacion_mejora_el_condicionamiento():
    K, R, t = _camara_club()
    H = cam.homografia_desde_camara(cam.matriz_camara(K, R, t))
    src = np.random.default_rng(4).uniform([20, 0], [80, 68], (10, 2))
    dst = g.aplicar(H, src)

    def relacion(A):                       # σ₁ / σ₈: el condicionamiento del problema (σ₉ ≈ 0 es la solución)
        s = np.linalg.svd(A, compute_uv=False)
        return s[0] / s[-2]

    crudo = relacion(cam.matriz_dlt(src, dst))
    norm = relacion(cam.matriz_dlt(cam.normalizar_puntos(src)[0], cam.normalizar_puntos(dst)[0]))
    assert norm < crudo / 100, f"normalizar tiene que mejorar mucho el condicionamiento ({crudo:.0f} → {norm:.1f})"


def test_dlt_sin_normalizar_tambien_funciona():
    K, R, t = _camara_club()
    H = cam.homografia_desde_camara(cam.matriz_camara(K, R, t))
    src = np.random.default_rng(5).uniform([20, 0], [80, 68], (8, 2))
    assert _misma_homografia(cam.dlt_homografia(src, g.aplicar(H, src), normalizar=False), H, atol=1e-5)


def test_error_reproyeccion():
    H = g.traslacion(10, 0)
    src = np.array([[0, 0], [5, 5]], dtype=float)
    e = cam.error_reproyeccion(H, src, np.array([[10, 0], [15, 8]], dtype=float))
    np.testing.assert_allclose(e, [0, 3])


# --------------------------------------------------------------------- RANSAC

def test_iteraciones_ransac():
    assert cam.iteraciones_ransac(0.5, 4, 0.99) == 72, "log(0,01) / log(1 − 0,5⁴) = 71,4 → 72"
    assert cam.iteraciones_ransac(0.9, 4, 0.99) == 5
    assert cam.iteraciones_ransac(1.0, 4, 0.99) == 1
    assert cam.iteraciones_ransac(0.3, 4, 0.99) > 500, "con 30 % de inliers hacen falta muchas"


def test_ransac_descarta_outliers():
    K, R, t = _camara_club()
    H = cam.homografia_desde_camara(cam.matriz_camara(K, R, t))
    r = np.random.default_rng(6)
    src = r.uniform([10, 0], [90, 68], (40, 2))
    dst = g.aplicar(H, src) + r.normal(0, 1.0, (40, 2))
    malos = np.zeros(40, dtype=bool); malos[:12] = True
    dst[malos] += r.uniform(80, 300, (12, 2)) * r.choice([-1, 1], (12, 2))
    He, inl = cam.ransac_homografia(src, dst, umbral=5.0, rng=np.random.default_rng(0))
    assert inl.dtype == bool and inl.shape == (40,)
    np.testing.assert_array_equal(inl, ~malos, err_msg="RANSAC tiene que marcar como inliers exactamente los buenos")
    limpio = g.aplicar(H, src[~malos])
    assert cam.error_reproyeccion(He, src[~malos], limpio).mean() < 1.0, "y la H final ajustada con los inliers"


def test_dlt_sin_ransac_se_rompe_con_outliers():
    K, R, t = _camara_club()
    H = cam.homografia_desde_camara(cam.matriz_camara(K, R, t))
    r = np.random.default_rng(7)
    src = r.uniform([10, 0], [90, 68], (30, 2))
    dst = g.aplicar(H, src)
    dst[:3] += 250.0
    limpio = g.aplicar(H, src[3:])
    assert cam.error_reproyeccion(cam.dlt_homografia(src, dst), src[3:], limpio).mean() > 5, \
        "sanity check: 3 outliers arruinan el DLT común (por eso existe RANSAC)"
