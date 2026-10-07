# xG SHA — versión didáctica

**Machine vision desde cero:** una materia de grado armada a medida para aprender visión por computadora en serio. Incluye la matemática, la teoría, los modelos y el estado del arte, siempre implementando con las propias manos antes de usar librerías.

Es la versión didáctica del proyecto xG SHA. La versión producto vive en otro repo y avanza por separado, a su propio ritmo. Esta materia es personal: no tiene nada que ver con la facultad. La hago porque me interesa y porque quiero llegar a la materia de la carrera con esto ya sabido.

---

## Cómo arrancar

```bash
# 1. Entorno
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .                   # hace que `import mv` funcione desde cualquier lado

# 2. Verificar que todo está en su lugar
pytest -q                          # al principio fallan casi todos los tests: es lo esperado

# 3. Bajar frames reales de un partido (opcional pero recomendado)
python herramientas/bajar_frames.py --partido cissab --desde 600 --segundos 60 --cada 2
```

Después: leé [`meta/metodo.md`](meta/metodo.md) (cómo funciona la materia) y arrancá por [`unidades/U0-herramientas/`](unidades/U0-herramientas/).

---

## Cómo está organizado

```
programa.md              el programa completo de la materia
meta/                    la "metamateria": cómo estudio, cómo voy, qué no entiendo
  metodo.md                cómo funciona la cursada, las entregas y la corrección
  diagnostico.md           el punto de partida (diagnóstico de octubre 2026)
  avance.md                bitácora de sesiones y estado de cada unidad
  dudas.md                 dudas abiertas, para llevar a la próxima sesión
  glosario.md              términos en castellano y en inglés
  recursos.md              todos los videos, libros y cursos, ordenados por unidad
  decisiones.md            decisiones sobre la materia y por qué se tomaron
unidades/
  U0-herramientas/         cada unidad tiene: README (plan), apunte(s), guía de ejercicios, TP
  U1-algebra-lineal/
  ...
mv/                      MI librería de visión: cada TP le agrega funciones implementadas a mano
tests/                   tests automáticos de cada TP (la primera corrección es esta)
herramientas/            scripts provistos (bajar video, extraer frames) — no son parte de los TPs
datos/                   frames y clips (no se versiona)
```

### La idea de `mv/`

Cada TP implementa funciones reales en `mv/`: convolución, homografía, filtro de Kalman, tracker, etc. Al final de la materia, `mv/` es **una librería de visión propia, testeada y entendida línea por línea**, que se puede reusar en proyectos reales. Los notebooks de cada TP *usan* la librería para experimentar y escribir el informe.

---

## Estado

| Unidad | Tema | Material | Estado |
|---|---|---|---|
| U0 | Herramientas: NumPy para imágenes | ✅ completo | ⬜ sin empezar |
| U1 | Álgebra lineal geométrica | ✅ completo | ⬜ |
| U2 | La imagen como señal | ✅ completo | ⬜ |
| U3 | Probabilidad + primer modelo (xG) | ✅ completo | ⬜ |
| U4 | Geometría de la cámara | ✅ completo | ⬜ |
| U5 | Features y movimiento | 📋 ficha | ⬜ |
| U6 | Redes neuronales desde cero | 📋 ficha | ⬜ |
| U7 | Detección | 📋 ficha | ⬜ |
| U8 | Tracking y re-identificación | 📋 ficha | ⬜ |
| U9 | Estado del arte + trabajo final | 📋 ficha | ⬜ |

✅ completo = apuntes, guía, TP y tests escritos. 📋 ficha = objetivos, contenidos, recursos y TP definidos; el material completo se escribe cuando estés por llegar, para ajustarlo a cómo vengas.

El detalle de avance vive en [`meta/avance.md`](meta/avance.md).
