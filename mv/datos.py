"""Datos de trabajo — módulo PROVISTO (no es parte de ningún TP).

- `cargar_frame`: devuelve un frame real de `datos/frames/` si hay, o uno sintético si no.
- `frame_sintetico`: dibuja una "cancha" falsa con jugadores, para poder trabajar sin datos reales.
- `trayectoria_ejemplo`: posiciones (en metros) de un jugador, con ruido y con saltos de tracking.
- `mostrar`: muestra una o varias imágenes con matplotlib.

Podés leer este código (está bueno hacerlo: usa todo lo de U0), pero no hace falta modificarlo.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
DATOS = RAIZ / "datos"
FRAMES = DATOS / "frames"

_EXTENSIONES = {".jpg", ".jpeg", ".png"}


# ---------------------------------------------------------------------------
# Frames
# ---------------------------------------------------------------------------

def listar_frames() -> list[Path]:
    """Lista los frames reales disponibles en datos/frames/ (ordenados por nombre)."""
    if not FRAMES.exists():
        return []
    return sorted(p for p in FRAMES.iterdir() if p.suffix.lower() in _EXTENSIONES)


def cargar_frame(ruta: str | Path | None = None, rgb: bool = True) -> np.ndarray:
    """Devuelve un frame como array uint8 de shape (H, W, 3).

    - Si `ruta` es None, usa el primer frame de datos/frames/; si no hay ninguno,
      genera uno sintético (y avisa).
    - `rgb=True` devuelve los canales en orden R, G, B. OpenCV lee en B, G, R:
      la conversión se hace acá adentro para que no te muerda.
    """
    if ruta is None:
        frames = listar_frames()
        if not frames:
            print("[mv.datos] No hay frames en datos/frames/ → uso un frame sintético. "
                  "Para bajar frames reales: python herramientas/bajar_frames.py --help")
            return frame_sintetico()
        ruta = frames[0]

    import cv2  # import diferido: el resto del módulo no necesita OpenCV

    img = cv2.imread(str(ruta), cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"No se pudo leer la imagen: {ruta}")
    return img[..., ::-1].copy() if rgb else img


def frame_sintetico(alto: int = 720, ancho: int = 1280, semilla: int = 0) -> np.ndarray:
    """Dibuja un frame falso de un partido: tribuna, césped a franjas, líneas, jugadores y pelota.

    Devuelve uint8 RGB de shape (alto, ancho, 3). Todo con NumPy vectorizado.
    """
    rng = np.random.default_rng(semilla)
    img = np.zeros((alto, ancho, 3), dtype=np.uint8)

    filas = np.arange(alto)[:, None]      # (H, 1)
    cols = np.arange(ancho)[None, :]      # (1, W)

    # Tribuna (franja superior gris con ruido)
    h_tribuna = alto // 6
    img[:h_tribuna] = rng.integers(90, 140, size=(h_tribuna, ancho, 1), dtype=np.uint8)

    # Césped a franjas: el ancho de las franjas crece hacia abajo (perspectiva barata)
    y = filas[h_tribuna:] - h_tribuna
    escala = 1.0 + 2.0 * y / (alto - h_tribuna)
    franja = ((cols / (90 * escala)).astype(int) % 2).astype(bool)          # (H', W)
    verde_claro = np.array([60, 140, 55], dtype=np.uint8)
    verde_oscuro = np.array([45, 115, 45], dtype=np.uint8)
    cesped = np.where(franja[..., None], verde_claro, verde_oscuro)
    ruido = rng.integers(-8, 9, size=cesped.shape)
    img[h_tribuna:] = np.clip(cesped.astype(int) + ruido, 0, 255).astype(np.uint8)

    # Líneas de cal: lateral lejana, lateral cercana inclinada y línea de medio campo
    blanco = np.array([235, 235, 230], dtype=np.uint8)
    lejana = np.abs(filas - (h_tribuna + 20)) <= 1
    cercana = np.abs(filas - (alto - 40 - 0.08 * (cols - ancho / 2))) <= 3
    medio = np.abs(cols - (ancho / 2 + 0.35 * (filas - h_tribuna))) <= 2
    lineas = (lejana | cercana | medio) & (filas >= h_tribuna)
    img[lineas] = blanco

    # Jugadores: rectángulos cuyo alto crece hacia abajo (más cerca de la cámara)
    equipos = {
        "local": np.array([30, 45, 150], dtype=np.uint8),       # azul
        "visitante": np.array([200, 40, 40], dtype=np.uint8),   # rojo
        "arbitro": np.array([240, 220, 30], dtype=np.uint8),    # amarillo
    }
    cantidades = {"local": 7, "visitante": 7, "arbitro": 1}
    for equipo, n in cantidades.items():
        for _ in range(n):
            pie_y = int(rng.integers(h_tribuna + 40, alto - 10))
            pie_x = int(rng.integers(20, ancho - 20))
            h = int(30 + 110 * (pie_y - h_tribuna) / (alto - h_tribuna))
            w = max(6, h // 3)
            y1, x1 = max(0, pie_y - h), max(0, pie_x - w // 2)
            torso = slice(y1, y1 + int(0.55 * h)), slice(x1, x1 + w)
            piernas = slice(y1 + int(0.55 * h), pie_y), slice(x1, x1 + w)
            img[torso] = equipos[equipo]
            img[piernas] = np.array([25, 25, 25], dtype=np.uint8)

    # Pelota: un disco blanco chico
    by, bx = int(0.6 * alto), int(0.45 * ancho)
    disco = (filas - by) ** 2 + (cols - bx) ** 2 <= 5 ** 2
    img[disco] = np.array([250, 250, 250], dtype=np.uint8)

    return img


# ---------------------------------------------------------------------------
# Trayectorias
# ---------------------------------------------------------------------------

def trayectoria_ejemplo(segundos: float = 60.0, fps: float = 10.0, semilla: int = 1,
                        con_saltos: bool = True) -> tuple[np.ndarray, float]:
    """Trayectoria (en metros) de un jugador sobre la cancha, muestreada a `fps`.

    Simula trote, dos piques y algo de quietud, más ruido de medición (~0,15 m).
    Con `con_saltos=True` agrega dos "saltos de tracking": frames donde el tracker
    confundió al jugador con otro a 15–25 m. Es exactamente el tipo de error que
    infla la distancia recorrida si no se filtra.

    Devuelve (P, fps) con P de shape (N, 2): columnas (x, y) en metros.
    """
    rng = np.random.default_rng(semilla)
    n = int(segundos * fps)
    t = np.arange(n) / fps

    # Velocidad (m/s) por tramos: trote 3, pique 7, quieto 0.3, trote 3.5, pique 6.5
    v = np.select(
        [t < 15, t < 20, t < 30, t < 50, t >= 50],
        [3.0, 7.0, 0.3, 3.5, 6.5],
    )
    rumbo = np.cumsum(rng.normal(0, 0.08, size=n))   # el rumbo cambia de a poco
    paso = (v / fps)[:, None] * np.stack([np.cos(rumbo), np.sin(rumbo)], axis=1)
    P = np.array([30.0, 34.0]) + np.cumsum(paso, axis=0)

    P = P + rng.normal(0, 0.15, size=P.shape)         # ruido de medición

    if con_saltos:
        for i, (dx, dy) in zip([int(0.3 * n), int(0.75 * n)], [(18.0, -6.0), (-12.0, 20.0)]):
            P[i] = P[i] + np.array([dx, dy])

    return P, fps


# ---------------------------------------------------------------------------
# Visualización
# ---------------------------------------------------------------------------

def mostrar(*imagenes: np.ndarray, titulos: list[str] | None = None, ancho: float = 6.0,
            cmap: str = "gray") -> None:
    """Muestra una o más imágenes lado a lado. Grises (H, W) se muestran con `cmap`."""
    import matplotlib.pyplot as plt

    n = len(imagenes)
    fig, ejes = plt.subplots(1, n, figsize=(ancho * n, ancho * 0.6), squeeze=False)
    for k, (eje, img) in enumerate(zip(ejes[0], imagenes)):
        if img.ndim == 2:
            eje.imshow(img, cmap=cmap)
        else:
            eje.imshow(img)
        eje.axis("off")
        if titulos and k < len(titulos):
            eje.set_title(titulos[k])
    plt.tight_layout()
    plt.show()
