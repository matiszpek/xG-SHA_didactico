"""Tests del TP2 — mv/filtros.py

Por sesión:
    pytest tests/test_u2_filtros.py -v -k s1     # color
    pytest tests/test_u2_filtros.py -v -k s2     # convolución y filtros
    pytest tests/test_u2_filtros.py -v -k s3     # gradiente
    pytest tests/test_u2_filtros.py -v -k s4     # Canny y Hough

Comparamos contra OpenCV / SciPy / scikit-image: están para VERIFICAR, no para usar en tu código.
"""

import time

import numpy as np
import pytest

from mv import filtros as f

rng = np.random.default_rng(0)


# ===================================================================== Sesión 1 — color

class TestS1Color:
    def test_s1_hsv_colores_puros(self):
        img = np.array([[[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [128, 128, 128], [0, 0, 0]]],
                       dtype=np.uint8)
        hsv = f.rgb_a_hsv(img)
        assert hsv.shape == (1, 6, 3)
        np.testing.assert_allclose(hsv[0, :4, 0], [0, 120, 240, 60], atol=1e-6,
                                   err_msg="H: rojo 0°, verde 120°, azul 240°, amarillo 60°")
        np.testing.assert_allclose(hsv[0, :4, 1], 1.0, err_msg="los colores puros tienen S = 1")
        assert hsv[0, 4, 1] == pytest.approx(0.0), "un gris tiene S = 0"
        assert hsv[0, 4, 2] == pytest.approx(128 / 255), "V es el máximo de los canales (en [0, 1])"
        assert np.all(np.isfinite(hsv)), "el negro (V = 0) no puede dar NaN: definí S = 0 y H = 0"

    def test_s1_hsv_como_opencv(self):
        cv2 = pytest.importorskip("cv2")
        img = rng.integers(0, 256, (40, 50, 3)).astype(np.uint8)
        hsv = f.rgb_a_hsv(img)
        ref = cv2.cvtColor(img.astype(np.float32) / 255, cv2.COLOR_RGB2HSV)
        dh = np.abs(hsv[..., 0] - ref[..., 0])
        dh = np.minimum(dh, 360 - dh)                       # el tono es circular
        assert dh.max() < 0.01, f"H difiere de OpenCV hasta {dh.max():.3f}°"
        np.testing.assert_allclose(hsv[..., 1:], ref[..., 1:], atol=1e-5)

    def test_s1_hsv_rango_de_h(self):
        img = rng.integers(0, 256, (30, 30, 3)).astype(np.uint8)
        H = f.rgb_a_hsv(img)[..., 0]
        assert H.min() >= 0 and H.max() < 360, "H tiene que estar en [0, 360)"

    def test_s1_pasto_hsv_resiste_la_sombra(self):
        from mv.datos import frame_sintetico
        img = frame_sintetico()
        sombra = (img.astype(float) * 0.25).astype(np.uint8)       # el mismo frame, 4 veces más oscuro
        m_sol = f.mascara_pasto_hsv(img)
        m_sombra = f.mascara_pasto_hsv(sombra)
        assert 0.6 < m_sol.mean() < 0.85, f"fracción de pasto al sol: {m_sol.mean():.2f} (esperado ~0,75)"
        acuerdo = (m_sol == m_sombra).mean()
        assert acuerdo > 0.95, (f"la máscara HSV en sombra coincide solo en {acuerdo:.1%} con la de sol: "
                                "el tono y la saturación no deberían cambiar al oscurecer")

    def test_s1_ecualizar_como_opencv(self):
        cv2 = pytest.importorskip("cv2")
        g = rng.integers(40, 120, (60, 80)).astype(np.uint8)       # imagen "apagada": usa poco rango
        e = f.ecualizar_histograma(g)
        assert e.dtype == np.uint8 and e.shape == g.shape
        dif = np.abs(e.astype(int) - cv2.equalizeHist(g).astype(int)).max()
        assert dif <= 1, f"difiere de cv2.equalizeHist hasta {dif}"
        assert e.min() == 0 and e.max() == 255, "ecualizar estira el histograma a todo el rango"

    def test_s1_ecualizar_constante(self):
        g = np.full((5, 5), 77, dtype=np.uint8)
        np.testing.assert_array_equal(f.ecualizar_histograma(g), g,
                                      err_msg="una imagen constante se devuelve igual (no dividas por cero)")


# ===================================================================== Sesión 2 — convolución

MODOS_SCIPY = {"cero": "constant", "replicar": "nearest", "espejo": "mirror"}


class TestS2Convolucion:
    @pytest.mark.parametrize("modo", ["cero", "replicar", "espejo"])
    def test_s2_correlacionar_como_scipy(self, modo):
        ndi = pytest.importorskip("scipy.ndimage")
        x = rng.normal(size=(30, 40))
        k = rng.normal(size=(3, 5))
        mio = f.correlacionar(x, k, modo)
        assert mio.shape == x.shape, "la salida tiene que tener la misma shape que la entrada"
        np.testing.assert_allclose(mio, ndi.correlate(x, k, mode=MODOS_SCIPY[modo], cval=0), atol=1e-10,
                                   err_msg=f"modo '{modo}': revisá el padding")

    @pytest.mark.parametrize("modo", ["cero", "replicar", "espejo"])
    def test_s2_convolucionar_como_scipy(self, modo):
        ndi = pytest.importorskip("scipy.ndimage")
        x = rng.normal(size=(30, 40))
        k = rng.normal(size=(5, 3))
        np.testing.assert_allclose(f.convolucionar(x, k, modo), ndi.convolve(x, k, mode=MODOS_SCIPY[modo], cval=0),
                                   atol=1e-10, err_msg="convolución = correlación con el kernel dado vuelta")

    def test_s2_convolucion_no_es_correlacion(self):
        x = np.zeros((7, 7)); x[3, 3] = 1.0                   # un impulso
        k = np.arange(9, dtype=float).reshape(3, 3)            # kernel NO simétrico
        np.testing.assert_allclose(f.convolucionar(x, k, "cero")[2:5, 2:5], k,
                                   err_msg="convolucionar un impulso tiene que 'dibujar' el kernel tal cual")
        np.testing.assert_allclose(f.correlacionar(x, k, "cero")[2:5, 2:5], k[::-1, ::-1],
                                   err_msg="correlacionar un impulso dibuja el kernel dado vuelta")

    def test_s2_vectorizado(self):
        x = rng.normal(size=(720, 1280))
        t0 = time.perf_counter()
        f.convolucionar(x, np.ones((5, 5)) / 25)
        dt = time.perf_counter() - t0
        assert dt < 3.0, f"convolucionar 720p con 5×5 tardó {dt:.1f} s (vectorizado: < 0,5 s)"

    def test_s2_kernel_gaussiano(self):
        k = f.kernel_gaussiano(2.0)
        assert k.ndim == 1 and len(k) == 13, f"con σ = 2 y radio ceil(3σ) = 6 hay 13 valores; hay {len(k)}"
        assert k.sum() == pytest.approx(1.0), "el kernel tiene que sumar 1 (no cambia el brillo medio)"
        np.testing.assert_allclose(k, k[::-1], err_msg="tiene que ser simétrico")
        assert k.argmax() == 6
        assert len(f.kernel_gaussiano(1.0, radio=2)) == 5

    def test_s2_separable(self):
        x = rng.normal(size=(40, 50))
        k = f.kernel_gaussiano(1.5)
        np.testing.assert_allclose(f.filtrar_separable(x, k), f.convolucionar(x, np.outer(k, k)), atol=1e-12,
                                   err_msg="filas y después columnas = un kernel 2D que es el producto externo")

    def test_s2_desenfocar_color(self):
        img = rng.integers(0, 256, (30, 40, 3)).astype(np.uint8)
        b = f.desenfocar_gaussiano(img, 1.0)
        assert b.shape == img.shape and b.dtype == np.float64
        np.testing.assert_allclose(b[..., 1], f.filtrar_separable(img[..., 1].astype(float), f.kernel_gaussiano(1.0)),
                                   atol=1e-10, err_msg="en color se filtra cada canal por separado")
        assert b.std() < img.std(), "desenfocar tiene que bajar la variación"

    def test_s2_mediana_como_scipy(self):
        ndi = pytest.importorskip("scipy.ndimage")
        x = rng.normal(size=(30, 40))
        np.testing.assert_allclose(f.filtro_mediana(x, 5), ndi.median_filter(x, 5, mode="mirror"), atol=1e-12)

    def test_s2_mediana_borra_sal_y_pimienta(self):
        x = np.full((20, 20), 100.0)
        x[5, 7] = 255; x[12, 3] = 0
        np.testing.assert_allclose(f.filtro_mediana(x, 3), 100.0, err_msg="la mediana elimina píxeles aislados")


# ===================================================================== Sesión 3 — gradiente

class TestS3Gradiente:
    def test_s3_sobel_rampa(self):
        ys, xs = np.indices((20, 30))
        img = 2.0 * xs + 0.0 * ys
        gx, gy = f.gradiente_sobel(img)
        np.testing.assert_allclose(gx[1:-1, 1:-1], 16.0, err_msg="Sobel sobre una rampa de pendiente 2 da 8·2 = 16")
        np.testing.assert_allclose(gy[1:-1, 1:-1], 0.0, atol=1e-12)

    def test_s3_sobel_signo_y_hacia_abajo(self):
        ys, _ = np.indices((20, 30))
        gx, gy = f.gradiente_sobel(ys.astype(float))
        assert gy[10, 10] > 0, "si la intensidad crece hacia ABAJO, gy tiene que ser positivo (la y de imagen)"

    def test_s3_sobel_como_opencv(self):
        cv2 = pytest.importorskip("cv2")
        x = rng.normal(size=(30, 40))
        gx, gy = f.gradiente_sobel(x)
        np.testing.assert_allclose(gx, cv2.Sobel(x, cv2.CV_64F, 1, 0, ksize=3), atol=1e-10)
        np.testing.assert_allclose(gy, cv2.Sobel(x, cv2.CV_64F, 0, 1, ksize=3), atol=1e-10)

    def test_s3_magnitud_orientacion(self):
        m, t = f.magnitud_orientacion(np.array([3.0, 0.0, -1.0]), np.array([4.0, 2.0, 0.0]))
        np.testing.assert_allclose(m, [5, 2, 1])
        np.testing.assert_allclose(t, [np.arctan2(4, 3), np.pi / 2, np.pi])


# ===================================================================== Sesión 4 — Canny y Hough

class TestS4CannyHough:
    def test_s4_nms_adelgaza(self):
        xs = np.arange(40)
        img = np.tile(np.tanh((xs - 20) / 2.0), (10, 1))      # borde vertical suave centrado en x = 20
        m, t = f.magnitud_orientacion(*f.gradiente_sobel(img))
        n = f.supresion_no_maximos(m, t)
        assert n.shape == m.shape
        np.testing.assert_array_equal((n > 0).sum(axis=1), 1, err_msg="tiene que quedar 1 píxel de borde por fila")
        assert (n[:, 20] > 0).all(), "el máximo está en x = 20"
        np.testing.assert_allclose(n[:, 20], m[:, 20], err_msg="los píxeles que sobreviven conservan su magnitud")

    def test_s4_nms_diagonal(self):
        ys, xs = np.indices((40, 40))
        img = np.tanh((xs + ys - 40) / 3.0)                     # borde diagonal
        m, t = f.magnitud_orientacion(*f.gradiente_sobel(img))
        n = f.supresion_no_maximos(m, t)
        filas = (n[5:-5, 5:-5] > 0).sum(axis=1)
        assert filas.max() <= 2, "con un borde diagonal tienen que quedar 1-2 píxeles por fila, no una franja"

    def test_s4_histeresis_8_vecinos(self):
        ndi = pytest.importorskip("scipy.ndimage")
        mm = rng.random((50, 60))
        res = f.histeresis(mm, 0.6, 0.95)
        lab, _ = ndi.label(mm > 0.6, structure=np.ones((3, 3)))
        conservar = np.unique(lab[mm > 0.95])
        ref = np.isin(lab, conservar[conservar > 0])
        assert res.dtype == bool
        np.testing.assert_array_equal(res, ref, err_msg="un débil se conserva si está conectado (8 vecinos, "
                                                        "aunque sea por otros débiles) a un fuerte")

    def test_s4_histeresis_simple(self):
        m = np.zeros((5, 9))
        m[2, 1] = 1.0                       # fuerte
        m[2, 2:6] = 0.5                     # débiles conectados al fuerte
        m[2, 7] = 0.5                       # débil aislado
        r = f.histeresis(m, 0.3, 0.8)
        np.testing.assert_array_equal(r[2], [0, 1, 1, 1, 1, 1, 0, 0, 0])

    def test_s4_canny_rectangulo(self):
        r = np.random.default_rng(1)
        img = np.zeros((100, 120)); img[30:70, 40:90] = 1.0
        img += r.normal(0, 0.05, img.shape)
        b = f.canny(img, sigma=1.4)
        assert b.dtype == bool and b.shape == img.shape
        verdad = np.zeros_like(b)
        verdad[29:31, 40:90] = verdad[69:71, 40:90] = True
        verdad[30:70, 39:41] = verdad[30:70, 89:91] = True
        def dilatar(m):
            out = np.zeros_like(m)
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    out |= np.roll(np.roll(m, dy, 0), dx, 1)
            return out

        precision = (b & dilatar(verdad)).sum() / max(b.sum(), 1)
        linea = np.zeros_like(b)                      # el contorno, de 1 px de ancho
        linea[30, 42:88] = linea[69, 42:88] = linea[32:68, 40] = linea[32:68, 89] = True
        recall = (linea & dilatar(b)).sum() / linea.sum()
        assert precision > 0.9, f"el {1 - precision:.0%} de los bordes que encontraste no están sobre el rectángulo"
        assert recall > 0.9, f"encontraste solo el {recall:.0%} del contorno (¿umbrales muy altos?)"
        assert 140 < b.sum() < 260, f"el perímetro son ~180 px; encontraste {b.sum()} (¿bordes gruesos? ¿NMS?)"

    def test_s4_hough_encuentra_la_recta(self):
        H, W = 200, 300
        th, rho = np.deg2rad(30), 100.0
        ys, xs = np.indices((H, W))
        b = np.abs(xs * np.cos(th) + ys * np.sin(th) - rho) < 0.5
        acc, thetas, rhos = f.hough_rectas(b)
        assert acc.shape == (len(rhos), len(thetas))
        assert len(thetas) == 180 and thetas[0] == 0 and thetas[-1] < np.pi
        picos = f.picos_hough(acc, thetas, rhos, n=1)
        r0, t0, votos = picos[0]
        assert abs(np.rad2deg(t0) - 30) <= 1 and abs(r0 - rho) <= 1.5, f"pico en ρ={r0}, θ={np.rad2deg(t0):.1f}°"
        assert votos == b.sum(), "todos los píxeles de la recta votan por la misma celda"

    def test_s4_picos_distintos(self):
        H, W = 200, 300
        ys, xs = np.indices((H, W))
        b = (np.abs(ys - 50) <= 1) | (np.abs(xs - 120) <= 1)          # una horizontal y una vertical, de 3 px
        acc, thetas, rhos = f.hough_rectas(b)
        picos = f.picos_hough(acc, thetas, rhos, n=2, vecindad=(10, 10))
        angulos = sorted(round(np.rad2deg(p[1])) for p in picos)
        assert angulos == [0, 90], (f"tenían que salir θ = 0° (x = 120) y θ = 90° (y = 50); salieron {angulos}. "
                                    "Si salieron dos casi iguales, no estás suprimiendo la vecindad del primer pico")

    def test_s4_recta_desde_hough(self):
        r = f.recta_desde_hough(100.0, np.deg2rad(30))
        assert r[0] ** 2 + r[1] ** 2 == pytest.approx(1.0)
        p = np.array([100 * np.cos(np.deg2rad(30)), 100 * np.sin(np.deg2rad(30))])   # el pie de la normal
        assert r[0] * p[0] + r[1] * p[1] + r[2] == pytest.approx(0.0, abs=1e-9)
