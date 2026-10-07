"""Baja un tramo de un partido de Hebraica y extrae frames — herramienta PROVISTA.

Ejemplos:

    # 60 s del partido vs Cissab, empezando 10 min después del arranque del Sub-21, un frame cada 2 s
    python herramientas/bajar_frames.py --partido cissab --desde 600 --segundos 60 --cada 2

    # cualquier video de YouTube, desde el segundo absoluto 1234
    python herramientas/bajar_frames.py --url https://www.youtube.com/watch?v=XXXX --desde 1234 --segundos 30

    # solo extraer frames de un video que ya tenés
    python herramientas/bajar_frames.py --archivo datos/clips/mi_clip.mp4 --cada 1

Requisitos: yt-dlp (>= 2026.08) y ffmpeg instalados (ffmpeg hace el corte del tramo).

Trampas que ya se pagaron en el proyecto anterior y que este script evita:
- Se pide H.264 (avc1) explícitamente. Si no, yt-dlp elige AV1, y OpenCV "abre" el archivo
  pero devuelve 0 frames sin tirar ningún error.
- Los streams del club duran ~4 h y traen varios partidos. Por eso se baja solo el tramo pedido.
- El corte cae en el keyframe anterior, así que el clip puede empezar unos segundos antes de lo pedido.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CLIPS = RAIZ / "datos" / "clips"
FRAMES = RAIZ / "datos" / "frames"

# Partidos Sub-21 2026 del canal @HebraicaArgentina.
# `inicio_sub21` = segundo del stream donde arranca el partido Sub-21 (verificado con los capítulos de YouTube).
PARTIDOS = {
    "cissab": {"video_id": "7iHm2S5ysiA", "inicio_sub21": 9926, "nota": "Hebraica azul marino vs rojo y blanco a rayas"},
    "hacoaj": {"video_id": "RP0xj_n_kMU", "inicio_sub21": 7939, "nota": "nublado, rival de blanco (caso difícil)"},
    "sosiego": {"video_id": "DO-4yF218VE", "inicio_sub21": 9325, "nota": "sol fuerte y cortes de conexión (caso feo)"},
}

FORMATO_H264 = "bestvideo[height<=1080][vcodec^=avc1]/bestvideo[height<=1080]"


def bajar_tramo(url: str, desde: float, segundos: float, destino: Path) -> Path:
    destino.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "-f", FORMATO_H264,
        "--download-sections", f"*{desde:.0f}-{desde + segundos:.0f}",
        "--force-keyframes-at-cuts",
        "-o", str(destino),
        url,
    ]
    print("→", " ".join(cmd))
    subprocess.run(cmd, check=True)
    if not destino.exists():
        raise FileNotFoundError(f"yt-dlp terminó pero no encuentro {destino}")
    return destino


def extraer_frames(video: Path, cada: float, prefijo: str) -> list[Path]:
    import cv2

    cap = cv2.VideoCapture(str(video))
    if not cap.isOpened():
        raise RuntimeError(f"OpenCV no pudo abrir {video}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    paso = max(1, round(cada * fps))
    FRAMES.mkdir(parents=True, exist_ok=True)

    guardados, i = [], 0
    while True:
        ok, frame = cap.read()            # frame viene en BGR
        if not ok:
            break
        if i % paso == 0:
            ruta = FRAMES / f"{prefijo}_f{i:06d}.jpg"
            cv2.imwrite(str(ruta), frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
            guardados.append(ruta)
        i += 1
    cap.release()

    if i == 0:
        raise RuntimeError(f"Se abrió {video} pero no se leyó ningún frame. ¿Es AV1? Probá: ffprobe {video}")
    print(f"✓ {len(guardados)} frames guardados en {FRAMES} ({i} frames leídos, {fps:.1f} fps)")
    return guardados


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    fuente = p.add_mutually_exclusive_group(required=True)
    fuente.add_argument("--partido", choices=sorted(PARTIDOS), help="partido del corpus (el tiempo es relativo al Sub-21)")
    fuente.add_argument("--url", help="cualquier URL de YouTube (el tiempo es absoluto)")
    fuente.add_argument("--archivo", type=Path, help="video local: solo extrae frames")
    p.add_argument("--desde", type=float, default=0, help="segundo de inicio (default 0)")
    p.add_argument("--segundos", type=float, default=60, help="duración del tramo (default 60)")
    p.add_argument("--cada", type=float, default=2, help="un frame cada tantos segundos (default 2)")
    a = p.parse_args()

    if a.archivo:
        extraer_frames(a.archivo, a.cada, a.archivo.stem)
        return

    if a.partido:
        info = PARTIDOS[a.partido]
        url = f"https://www.youtube.com/watch?v={info['video_id']}"
        inicio = info["inicio_sub21"] + a.desde
        nombre = f"{a.partido}_{int(a.desde):05d}_{int(a.segundos)}s"
        print(f"Partido: {a.partido} — {info['nota']}")
    else:
        url, inicio = a.url, a.desde
        nombre = f"yt_{int(a.desde):05d}_{int(a.segundos)}s"

    clip = bajar_tramo(url, inicio, a.segundos, CLIPS / f"{nombre}.mp4")
    extraer_frames(clip, a.cada, nombre)


if __name__ == "__main__":
    main()
