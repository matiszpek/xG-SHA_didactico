"""Tests del TP3 — mv/prob.py y mv/xg.py

    pytest tests/test_u3_prob_xg.py -v -k prob     # parte A: probabilidad
    pytest tests/test_u3_prob_xg.py -v -k xg       # parte B: el modelo de xG

Estos tests NO necesitan bajar StatsBomb: usan datos simulados con un modelo conocido.
"""

import numpy as np
import pytest

from mv import prob as pr
from mv import xg


# ===================================================================== Parte A — prob

class TestProb:
    def test_prob_al_menos_uno(self):
        assert pr.prob_al_menos_uno([1 / 6, 1 / 6]) == pytest.approx(11 / 36), \
            "al menos un 6 en dos tiradas = 1 − (5/6)² (el complemento, no la suma)"
        assert pr.prob_al_menos_uno([0.1, 0.3, 0.5]) == pytest.approx(1 - 0.9 * 0.7 * 0.5)
        assert isinstance(pr.prob_al_menos_uno([0.5]), float)

    def test_prob_distribucion_goles(self):
        d = pr.distribucion_goles([0.1, 0.3, 0.5])
        assert d.shape == (4,), "con 3 tiros puede haber 0, 1, 2 o 3 goles: 4 valores"
        assert d.sum() == pytest.approx(1.0), "una distribución suma 1"
        assert d[0] == pytest.approx(0.315), "P(0 goles) = 0,9 · 0,7 · 0,5 (diagnóstico, bloque 2, pregunta 9)"
        assert d[3] == pytest.approx(0.015)
        assert (np.arange(4) * d).sum() == pytest.approx(0.9), "la esperanza tiene que ser la suma de los xG"

    def test_prob_distribucion_contra_fuerza_bruta(self):
        ps = np.array([0.05, 0.4, 0.22, 0.7, 0.13])
        brute = np.zeros(6)
        for k in range(2 ** 5):                                 # todos los resultados posibles (gol / no gol)
            bits = np.array([(k >> i) & 1 for i in range(5)])
            brute[bits.sum()] += np.prod(np.where(bits, ps, 1 - ps))
        np.testing.assert_allclose(pr.distribucion_goles(ps), brute, atol=1e-12)

    def test_prob_simular_goles(self):
        rng = np.random.default_rng(0)
        xgs = [0.1, 0.3, 0.5, 0.05]
        sims = pr.simular_goles(xgs, 200_000, rng)
        assert sims.shape == (200_000,)
        assert sims.mean() == pytest.approx(sum(xgs), abs=0.01), "el promedio simulado converge a la suma de los xG"
        frec = np.bincount(sims, minlength=5) / len(sims)
        np.testing.assert_allclose(frec, pr.distribucion_goles(xgs), atol=0.005,
                                   err_msg="Monte Carlo tiene que coincidir con la distribución exacta")

    def test_prob_bayes_detector(self):
        assert pr.bayes(0.2, 0.9, 0.05) == pytest.approx(0.18 / 0.22), \
            "el detector de pelota del diagnóstico (bloque 2, pregunta 3)"

    def test_prob_densidad_normal(self):
        assert pr.densidad_normal(0.0) == pytest.approx(1 / np.sqrt(2 * np.pi))
        x = np.linspace(-20, 20, 40001)
        assert np.trapezoid(pr.densidad_normal(x, 1.0, 2.0), x) == pytest.approx(1.0, abs=1e-6), "integra 1"
        assert pr.densidad_normal(0.0, 0.0, 0.1) > 1, "una densidad SÍ puede valer más que 1 (diagnóstico)"

    def test_prob_normal_multivariada(self):
        stats = pytest.importorskip("scipy.stats")
        mu, S = np.array([0.5, -1.0]), np.array([[2.0, 0.6], [0.6, 1.0]])
        X = np.random.default_rng(1).normal(size=(50, 2))
        mio = pr.densidad_normal_multivariada(X, mu, S)
        assert mio.shape == (50,)
        np.testing.assert_allclose(mio, stats.multivariate_normal(mu, S).pdf(X), rtol=1e-10)

    def test_prob_mahalanobis(self):
        S = np.diag([4.0, 1.0])
        d = pr.mahalanobis(np.array([[2.0, 0.0], [0.0, 1.0], [2.0, 1.0]]), [0, 0], S)
        np.testing.assert_allclose(d, [1, 1, np.sqrt(2)], err_msg="con varianza 4 en x, alejarse 2 en x 'cuesta' 1 desvío")

    def test_prob_elipse(self):
        mu, S = np.array([3.0, 1.0]), np.array([[2.0, 0.8], [0.8, 1.0]])
        E = pr.elipse_confianza(mu, S, k=2.0, n=60)
        assert E.shape == (60, 2)
        np.testing.assert_allclose(pr.mahalanobis(E, mu, S), 2.0, atol=1e-9,
                                   err_msg="todos los puntos de la elipse están a 2 'desvíos' (Mahalanobis) del centro")

    def test_prob_log_verosimilitud(self):
        y = np.array([1, 0, 1]); p = np.array([0.8, 0.3, 0.5])
        assert pr.log_verosimilitud_bernoulli(y, p) == pytest.approx(np.log(0.8) + np.log(0.7) + np.log(0.5))
        assert np.isfinite(pr.log_verosimilitud_bernoulli([1, 0], [0.0, 1.0])), "con p = 0 o 1 hay que recortar (eps)"


# ===================================================================== Parte B — xg

def _datos_simulados(n=4000, semilla=0):
    """Tiros con un modelo logístico CONOCIDO, para verificar que el entrenamiento lo recupera."""
    rng = np.random.default_rng(semilla)
    x = rng.uniform(80, 119, n)
    y = rng.uniform(15, 65, n)
    dist, ang = xg.distancia_y_angulo(x, y)
    X = np.column_stack([dist, ang])
    Xs, _, _ = xg.estandarizar(X)
    w_real, b_real = np.array([-0.9, 0.5]), -2.2
    p = 1 / (1 + np.exp(-(Xs @ w_real + b_real)))
    goles = (rng.random(n) < p).astype(int)
    partidos = rng.integers(0, 150, n)
    return Xs, goles, p, partidos, w_real, b_real


class TestXG:
    def test_xg_distancia_angulo_penal(self):
        d, a = xg.distancia_y_angulo(np.array([108.0]), np.array([40.0]))
        assert d[0] == pytest.approx(12.0), "el punto penal está a 12 yardas del centro del arco"
        assert np.rad2deg(a[0]) == pytest.approx(2 * np.rad2deg(np.arctan(4 / 12))), \
            "desde el penal se ve el arco (8 yd de ancho) con un ángulo de 2·atan(4/12) ≈ 36,9°"

    def test_xg_angulo_desde_la_linea_de_fondo(self):
        d, a = xg.distancia_y_angulo(np.array([120.0, 119.9]), np.array([20.0, 40.0]))
        assert np.rad2deg(a[0]) == pytest.approx(0.0, abs=1e-9), "sobre la línea de fondo, fuera del arco, no se ve arco"
        assert np.rad2deg(a[1]) > 170, "pegado al arco y de frente, se ve casi todo el semiplano"

    def test_xg_angulo_simetrico(self):
        _, a1 = xg.distancia_y_angulo(np.array([100.0]), np.array([30.0]))
        _, a2 = xg.distancia_y_angulo(np.array([100.0]), np.array([50.0]))
        assert a1[0] == pytest.approx(a2[0]), "el ángulo es simétrico respecto del centro del arco"

    def test_xg_estandarizar(self):
        X = np.random.default_rng(2).normal([5, -3], [2, 0.5], size=(1000, 2))
        Xs, m, s = xg.estandarizar(X)
        np.testing.assert_allclose(Xs.mean(axis=0), 0, atol=1e-12)
        np.testing.assert_allclose(Xs.std(axis=0), 1, atol=1e-12)
        Xt, _, _ = xg.estandarizar(X[:10] + 1, m, s)
        np.testing.assert_allclose(Xt, (X[:10] + 1 - m) / s, err_msg="con media y desvío dados, se usan esos "
                                                                   "(los del TRAIN), no se recalculan")

    def test_xg_sigmoide_estable(self):
        z = np.array([-1000.0, -5.0, 0.0, 5.0, 1000.0])
        with np.errstate(over="raise"):
            s = xg.sigmoide(z)
        np.testing.assert_allclose(s, [0, 1 / (1 + np.e ** 5), 0.5, 1 / (1 + np.e ** -5), 1], atol=1e-12)

    def test_xg_log_loss(self):
        y = np.array([1, 0, 1, 0]); p = np.array([0.9, 0.2, 0.6, 0.1])
        esperado = -np.mean(np.log([0.9, 0.8, 0.6, 0.9]))
        assert xg.log_loss(y, p) == pytest.approx(esperado)
        assert np.isfinite(xg.log_loss(np.array([1]), np.array([0.0])))

    def test_xg_gradiente_contra_diferencias_finitas(self):
        Xs, y, _, _, _, _ = _datos_simulados(300)
        w, b = np.array([0.3, -0.2]), 0.1
        dw, db = xg.gradiente_log_loss(Xs, y, w, b)
        h = 1e-6
        num_w = [(xg.log_loss(y, xg.predecir_proba(Xs, w + h * e, b)) -
                  xg.log_loss(y, xg.predecir_proba(Xs, w - h * e, b))) / (2 * h) for e in np.eye(2)]
        num_b = (xg.log_loss(y, xg.predecir_proba(Xs, w, b + h)) - xg.log_loss(y, xg.predecir_proba(Xs, w, b - h))) / (2 * h)
        np.testing.assert_allclose(dw, num_w, rtol=1e-5, err_msg="tu gradiente no coincide con la derivada numérica")
        assert db == pytest.approx(num_b, rel=1e-5)

    def test_xg_entrenar_recupera_el_modelo(self):
        Xs, y, _, _, w_real, b_real = _datos_simulados(8000)
        w, b, hist = xg.entrenar_logistica(Xs, y, lr=0.5, n_iter=3000)
        assert len(hist) == 3000
        assert hist[-1] < hist[0], "la pérdida tiene que bajar"
        assert np.all(np.diff(hist) <= 1e-9), "con un lr razonable, la log loss no sube nunca"
        np.testing.assert_allclose(w, w_real, atol=0.15, err_msg="con 8000 tiros hay que recuperar los pesos reales")
        assert b == pytest.approx(b_real, abs=0.15)

    def test_xg_entrenar_como_sklearn(self):
        lm = pytest.importorskip("sklearn.linear_model")
        Xs, y, _, _, _, _ = _datos_simulados(3000, semilla=3)
        w, b, _ = xg.entrenar_logistica(Xs, y, lr=0.5, n_iter=4000)
        ref = lm.LogisticRegression(C=1e8, max_iter=10000).fit(Xs, y)
        np.testing.assert_allclose(w, ref.coef_[0], atol=2e-3)
        assert b == pytest.approx(ref.intercept_[0], abs=2e-3)

    def test_xg_auc(self):
        assert xg.auc(np.array([0, 0, 1, 1]), np.array([0.1, 0.4, 0.35, 0.8])) == pytest.approx(0.75)
        assert xg.auc(np.array([0, 1]), np.array([0.5, 0.5])) == pytest.approx(0.5), "empate = media chance"
        met = pytest.importorskip("sklearn.metrics")
        r = np.random.default_rng(4)
        y = r.random(500) < 0.2
        p = np.round(r.random(500) * 0.5 + 0.3 * y, 2)                  # con empates
        assert xg.auc(y, p) == pytest.approx(met.roc_auc_score(y, p))

    def test_xg_calibracion(self):
        r = np.random.default_rng(5)
        p = r.uniform(0, 1, 200_000)                     # probabilidades "verdaderas"
        y = (r.random(200_000) < p).astype(int)          # resultados generados con esas probabilidades
        p_media, frec, cuenta = xg.curva_calibracion(y, p, n_bins=10)
        assert p_media.shape == frec.shape == cuenta.shape == (10,)
        assert cuenta.sum() == 200_000
        np.testing.assert_allclose(p_media, np.arange(10) / 10 + 0.05, atol=0.01,
                                   err_msg="con p uniforme, la p media de cada intervalo es su centro")
        np.testing.assert_allclose(frec, p_media, atol=0.02,
                                   err_msg="con las probabilidades VERDADERAS, la curva cae sobre la diagonal")

    def test_xg_calibracion_intervalos_vacios(self):
        with np.errstate(all="raise"):
            p_media, frec, cuenta = xg.curva_calibracion(np.array([0, 1]), np.array([0.05, 0.07]), n_bins=10)
        assert cuenta[0] == 2 and cuenta[1:].sum() == 0
        assert np.isnan(frec[1:]).all(), "los intervalos vacíos van con NaN, sin warnings"

    def test_xg_split_por_partido(self):
        partidos = np.repeat(np.arange(50), 20)
        test = xg.split_por_partido(partidos, 0.2, np.random.default_rng(0))
        assert test.dtype == bool and test.shape == partidos.shape
        assert len(np.intersect1d(partidos[test], partidos[~test])) == 0, \
            "ningún partido puede tener tiros en train Y en test"
        assert len(np.unique(partidos[test])) == 10, "20 % de 50 partidos = 10 partidos en test"
