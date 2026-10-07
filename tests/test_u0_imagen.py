"""Tests del TP0, parte A — mv/imagen.py

Correr solo estos:   pytest tests/test_u0_imagen.py -v
Si un test falla, leé el mensaje: dice qué se esperaba y qué devolviste.
"""

import time

import numpy as np
import pytest

from mv import imagen as im


@pytest.fixture
def img_uint8():
    rng = np.random.default_rng(0)
    return rng.integers(0, 256, size=(40, 60, 3), dtype=np.uint8)


# --------------------------------------------------------------------- a_float / a_uint8

def test_a_float_rango_y_dtype(img_uint8):
    f = im.a_float(img_uint8)
    assert f.dtype == np.float32, f"a_float tiene que devolver float32, devolvió {f.dtype}"
    assert f.shape == img_uint8.shape, "a_float no tiene que cambiar la shape"
    assert f.min() >= 0.0 and f.max() <= 1.0, "a_float tiene que devolver valores en [0, 1]"
    np.testing.assert_allclose(f, img_uint8 / 255.0, rtol=1e-6)


def test_a_float_no_modifica_la_entrada(img_uint8):
    original = img_uint8.copy()
    im.a_float(img_uint8)
    np.testing.assert_array_equal(img_uint8, original, err_msg="a_float modificó la imagen de entrada")


def test_a_uint8_clip_y_redondeo():
    x = np.array([[-0.3, 0.0, 1.6 / 255, 0.2, 1.0, 1.7]], dtype=np.float32)
    u = im.a_uint8(x)
    assert u.dtype == np.uint8, f"a_uint8 tiene que devolver uint8, devolvió {u.dtype}"
    assert u[0, 0] == 0, "un valor negativo tiene que dar 0: ¿hiciste clip ANTES de convertir?"
    assert u[0, 2] == 2, "1,6 tiene que redondear a 2; si te dio 1, estás truncando en vez de redondear"
    assert u[0, 5] == 255, "1,7 tiene que dar 255; si te dio otra cosa, faltó el clip (overflow)"
    np.testing.assert_array_equal(u, [[0, 0, 2, 51, 255, 255]])


def test_ida_y_vuelta(img_uint8):
    np.testing.assert_array_equal(im.a_uint8(im.a_float(img_uint8)), img_uint8,
                                  err_msg="a_uint8(a_float(img)) tiene que devolver img exacta")


# --------------------------------------------------------------------- bgr_a_rgb

def test_bgr_a_rgb(img_uint8):
    r = im.bgr_a_rgb(img_uint8)
    np.testing.assert_array_equal(r[..., 0], img_uint8[..., 2])
    np.testing.assert_array_equal(r[..., 1], img_uint8[..., 1])
    np.testing.assert_array_equal(r[..., 2], img_uint8[..., 0])
    np.testing.assert_array_equal(im.bgr_a_rgb(r), img_uint8, err_msg="aplicarla dos veces tiene que volver al original")


# --------------------------------------------------------------------- a_gris

def test_a_gris_valores(img_uint8):
    g = im.a_gris(img_uint8)
    assert g.shape == img_uint8.shape[:2], f"a_gris tiene que devolver (H, W), devolvió {g.shape}"
    assert g.dtype == np.float32, f"a_gris tiene que devolver float32, devolvió {g.dtype}"
    esperado = (0.299 * img_uint8[..., 0].astype(float) + 0.587 * img_uint8[..., 1]
                + 0.114 * img_uint8[..., 2])
    np.testing.assert_allclose(g, esperado, rtol=1e-5, atol=1e-3)


def test_a_gris_pesos_custom(img_uint8):
    g = im.a_gris(img_uint8, pesos=(0.0, 0.0, 1.0))
    np.testing.assert_allclose(g, img_uint8[..., 2].astype(np.float32),
                               err_msg="con pesos (0,0,1) el gris tiene que ser el canal B")


def test_a_gris_con_float():
    img = np.full((5, 5, 3), 0.5, dtype=np.float32)
    g = im.a_gris(img)
    np.testing.assert_allclose(g, 0.5, rtol=1e-5,
                               err_msg="con entrada float en [0,1] la salida tiene que quedar en [0,1]")


def test_a_gris_vectorizado():
    img = np.random.default_rng(1).integers(0, 256, size=(1080, 1920, 3), dtype=np.uint8)
    t0 = time.perf_counter()
    im.a_gris(img)
    dt = time.perf_counter() - t0
    assert dt < 1.0, (f"a_gris tardó {dt:.2f} s en un frame 1080p. Vectorizado tarda ~0,02 s; "
                      "si tarda segundos, hay un loop sobre píxeles")


# --------------------------------------------------------------------- recortar

def test_recortar_basico():
    img = np.arange(100 * 200).reshape(100, 200)
    r = im.recortar(img, (10, 20, 30, 25))           # x1=10, y1=20, x2=30, y2=25
    assert r.shape == (5, 20), (f"la caja (x1=10, y1=20, x2=30, y2=25) son 5 filas y 20 columnas; "
                                f"devolviste shape {r.shape}. ¿Confundiste x con y?")
    np.testing.assert_array_equal(r, img[20:25, 10:30])


def test_recortar_color():
    img = np.zeros((50, 80, 3), dtype=np.uint8)
    assert im.recortar(img, (0, 0, 10, 5)).shape == (5, 10, 3)


def test_recortar_fuera_de_borde():
    img = np.arange(100 * 200).reshape(100, 200)
    r = im.recortar(img, (-10, 50, 30, 400))
    assert r.shape == (50, 30), f"la caja se sale de la imagen: tenías que recortarla a los bordes; shape {r.shape}"
    np.testing.assert_array_equal(r, img[50:100, 0:30])


def test_recortar_devuelve_copia():
    img = np.zeros((50, 80, 3), dtype=np.uint8)
    r = im.recortar(img, (5, 5, 20, 20))
    r[:] = 255
    assert img.max() == 0, ("modificar el recorte modificó la imagen original: devolviste una VISTA, "
                            "no una copia")


# --------------------------------------------------------------------- histograma

def test_histograma(img_uint8):
    h = im.histograma(img_uint8[..., 0])
    assert h.shape == (256,), f"el histograma tiene que tener exactamente 256 posiciones, tiene {h.shape}"
    esperado, _ = np.histogram(img_uint8[..., 0], bins=256, range=(0, 256))
    np.testing.assert_array_equal(h, esperado)
    assert h.sum() == img_uint8[..., 0].size


def test_histograma_valores_altos_ausentes():
    canal = np.zeros((10, 10), dtype=np.uint8)
    h = im.histograma(canal)
    assert h.shape == (256,), "aunque no aparezcan valores altos, el histograma tiene que medir 256"
    assert h[0] == 100 and h[1:].sum() == 0


# --------------------------------------------------------------------- brillo / contraste

def test_brillo_satura():
    img = np.array([[0, 100, 200, 250]], dtype=np.uint8)
    r = im.ajustar_brillo_contraste(img, alfa=1.0, beta=100)
    assert r.dtype == np.uint8
    np.testing.assert_array_equal(r, [[100, 200, 255, 255]],
                                  err_msg="200 + 100 tiene que saturar en 255; si te dio 44 es overflow de uint8")


def test_contraste_y_negativos():
    img = np.array([[10, 100, 200]], dtype=np.uint8)
    r = im.ajustar_brillo_contraste(img, alfa=2.0, beta=-50)
    np.testing.assert_array_equal(r, [[0, 150, 255]])


def test_brillo_redondea():
    img = np.array([[10]], dtype=np.uint8)
    assert im.ajustar_brillo_contraste(img, alfa=1.0, beta=0.6)[0, 0] == 11, "hay que redondear, no truncar"


# --------------------------------------------------------------------- mascara_pasto

def test_mascara_pasto_basica():
    img = np.array([[[60, 140, 50], [200, 40, 40], [235, 235, 230], [30, 45, 150]]], dtype=np.uint8)
    m = im.mascara_pasto(img)
    assert m.dtype == bool and m.shape == (1, 4)
    np.testing.assert_array_equal(m, [[True, False, False, False]])


def test_mascara_pasto_trampa_overflow():
    # R = 250: con uint8, R + 20 da la vuelta y vale 14. G = 100 NO es mayor que 270.
    img = np.array([[[250, 100, 0]]], dtype=np.uint8)
    assert not im.mascara_pasto(img)[0, 0], ("un píxel con R=250, G=100 no es pasto. Si te dio True, "
                                             "R + margen hizo overflow en uint8")


def test_mascara_pasto_en_frame_sintetico():
    from mv.datos import frame_sintetico
    img = frame_sintetico()
    frac = im.mascara_pasto(img).mean()
    assert 0.6 < frac < 0.85, f"en el frame sintético ~3/4 es pasto; te dio {frac:.2f}"


# --------------------------------------------------------------------- color_medio

def test_color_medio():
    img = np.zeros((4, 4, 3), dtype=np.uint8)
    img[:2] = [10, 20, 30]
    img[2:] = [100, 200, 250]
    m = np.zeros((4, 4), dtype=bool)
    m[:2] = True
    c = im.color_medio(img, m)
    assert c.shape == (3,)
    np.testing.assert_allclose(c, [10, 20, 30])
    m[2, 0] = True                              # agrego un píxel del otro color: 8 de un color + 1 del otro
    np.testing.assert_allclose(im.color_medio(img, m), (8 * np.array([10, 20, 30]) + [100, 200, 250]) / 9)


def test_color_medio_mascara_vacia():
    img = np.ones((4, 4, 3), dtype=np.uint8)
    with np.errstate(all="raise"):
        c = im.color_medio(img, np.zeros((4, 4), dtype=bool))
    assert c.shape == (3,) and np.isnan(c).all(), "con máscara vacía hay que devolver NaN, sin warnings"


# --------------------------------------------------------------------- mosaico

def test_mosaico_completo():
    imgs = [np.full((2, 3, 3), k, dtype=np.uint8) for k in range(4)]
    m = im.mosaico(imgs, columnas=2)
    assert m.shape == (4, 6, 3), f"4 imágenes de 2×3 en 2 columnas → (4, 6, 3); devolviste {m.shape}"
    assert m.dtype == np.uint8
    assert m[0, 0, 0] == 0 and m[0, 3, 0] == 1 and m[2, 0, 0] == 2 and m[2, 3, 0] == 3, \
        "el orden es de izquierda a derecha y de arriba abajo"


def test_mosaico_con_huecos():
    imgs = [np.full((2, 2, 3), 7, dtype=np.uint8) for _ in range(5)]
    m = im.mosaico(imgs, columnas=3)
    assert m.shape == (4, 6, 3), f"5 imágenes en 3 columnas → 2 filas → (4, 6, 3); devolviste {m.shape}"
    assert m[2:, 4:].max() == 0, "el hueco final tiene que quedar en cero"
    assert m[:2].min() == 7 and m[2:, :4].min() == 7
