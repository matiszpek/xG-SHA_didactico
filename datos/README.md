# datos/

Acá van los frames y clips de trabajo. **No se versionan** (están en `.gitignore`), porque pesan y se regeneran.

- `frames/` — imágenes sueltas (`.jpg`). `mv.datos.cargar_frame()` usa la primera que encuentre.
- `clips/` — fragmentos de video.

Para llenarla:

```bash
python herramientas/bajar_frames.py --partido cissab --desde 600 --segundos 60 --cada 2
```
