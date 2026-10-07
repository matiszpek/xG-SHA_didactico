# U0 — Herramientas: NumPy para imágenes

**Sesiones:** 2 (~4 h) · **TP:** TP0 → `mv/imagen.py` y `mv/cinematica.py`

## Por qué esta unidad

En el diagnóstico salió que la lógica la tengo, pero que me falta el **modelo mental de los arrays**: shapes, ejes, broadcasting, vistas, dtypes. Y en visión **todo** es manejo de arrays: una imagen es un array `(H, W, 3)` de `uint8`, un video es una pila de esos, y una caja es un recorte. Si esto no está firme, cada unidad siguiente se vuelve una pelea con los índices en vez de con las ideas.

## Objetivos

Al terminar U0 puedo, sin buscar:
1. Decir la shape y el dtype de un frame leído con OpenCV, y por qué el alto va primero.
2. Predecir si una operación devuelve una **vista** o una **copia**.
3. Predecir el resultado de **broadcasting** entre dos shapes (o si da error) y arreglarlo con `None`.
4. Reducir sobre el **eje correcto** (`axis`), con o sin `keepdims`.
5. Evitar el **overflow de `uint8`** y saber cuándo convertir a float.
6. Escribir operaciones de imagen **sin loops sobre píxeles**.
7. Calcular distancia y velocidad de una trayectoria, filtrando los datos imposibles.

## Plan

| Sesión | Qué hacer | Tiempo |
|---|---|---|
| **1** | Leer [`apunte.md`](apunte.md) entero, con Python abierto al lado probando cada ejemplo. Hacer la [guía](guia.md), ejercicios 1–10 | ~2 h |
| **2** | Guía, ejercicios 11–16. Hacer el [TP0](tp0/enunciado.md): implementar `mv/imagen.py` y `mv/cinematica.py`, y el notebook | ~2 h (+ lo que haga falta) |

Lectura complementaria (opcional, para cuando algo no cierre): NumPy docs, [Indexing](https://numpy.org/doc/stable/user/basics.indexing.html), [Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html) y [Copies and views](https://numpy.org/doc/stable/user/basics.copies.html).

## Antes de arrancar

```bash
pip install -r requirements.txt && pip install -e .
python herramientas/bajar_frames.py --partido cissab --desde 600 --segundos 60 --cada 2   # opcional
pytest tests/test_u0_imagen.py tests/test_u0_cinematica.py -q    # tienen que fallar todos: todavía no implementaste nada
```
