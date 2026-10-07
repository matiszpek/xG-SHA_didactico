# U0 — Apunte: NumPy para imágenes

> **La idea en una frase:** una imagen es un array de números con forma `(alto, ancho, canales)`. Casi todo lo que se hace en visión es operar sobre esos arrays **de una sola vez**, sin recorrer píxel por píxel.

Leelo con una consola de Python abierta. Cada bloque de código está para copiarlo, correrlo y **predecir el resultado antes de ver la salida**.

```python
import numpy as np
```

---

## 1. Una imagen es un array

```python
img = np.zeros((720, 1280, 3), dtype=np.uint8)   # una imagen negra de 1280×720
img.shape      # (720, 1280, 3)
img.ndim       # 3
img.dtype      # uint8
img.nbytes     # 2764800  (720·1280·3 bytes)
```

### ¿Por qué el alto va primero?

Porque un array 2D es una **matriz**, y en una matriz se indexa primero la **fila** y después la **columna**. Las filas recorren la imagen de arriba abajo, así que la cantidad de filas *es* el alto.

```
            columna (x) →
          0   1   2   3  ...  W-1
fila  0 [ ·   ·   ·   ·        ·  ]
(y)   1 [ ·   ·   ·   ·        ·  ]
 ↓    2 [ ·   ·   ·   ·        ·  ]
      .
    H-1 [ ·   ·   ·   ·        ·  ]
```

- El origen `(0, 0)` es la esquina **superior izquierda**.
- La **y crece hacia abajo**, al revés que en los gráficos de la secundaria.
- El píxel en `(x, y)` se lee `img[y, x]`. **Primero y, después x.** Este es el bug número uno de visión por computadora.

La cosa se complica porque las *coordenadas de puntos* y las *cajas* se escriben casi siempre como `(x, y)`, en ese orden: lo hace OpenCV, YOLO y todo el mundo. Así que conviven las dos convenciones:

| Qué | Orden | Ejemplo |
|---|---|---|
| Indexar el array | `[fila, columna]` = `[y, x]` | `img[100, 300]` |
| Shape | `(alto, ancho, canales)` | `(720, 1280, 3)` |
| Un punto | `(x, y)` | `(300, 100)` |
| Una caja | `(x1, y1, x2, y2)` | `(300, 100, 340, 180)` |
| Tamaño en OpenCV (`cv2.resize`) | `(ancho, alto)` | `(1280, 720)` |

Una caja `(x1, y1, x2, y2)` se recorta así: `img[y1:y2, x1:x2]`.

### Otras formas
- Imagen en grises: `(H, W)`, sin eje de canales.
- Video (o un *batch* de imágenes): `(T, H, W, 3)`.
- En PyTorch (U6) se usa `(C, H, W)`, con los canales primero. Lo vemos cuando llegue.

### Cuánto pesa un partido

Un frame 1080p son `1080 · 1920 · 3 = 6.220.800` bytes, unos **6,2 MB**. Un partido de 90 minutos a 25 fps son 135.000 frames, o sea **~840 GB sin comprimir**.

Por eso el video viaja comprimido (H.264, AV1) y por eso casi nunca se procesan todos los frames: se **muestrea** (por ejemplo, 10 por segundo).

### BGR: la trampa de OpenCV

`cv2.imread` y `cv2.VideoCapture` devuelven los canales en orden **B, G, R**, no R, G, B. Si mostrás un frame de OpenCV con matplotlib sin convertirlo, el pasto se ve verde (el canal del medio no cambia) pero la camiseta roja sale azul.

```python
rgb = bgr[..., ::-1]          # invierte el último eje
```

`mv.datos.cargar_frame()` ya te devuelve RGB.

---

## 2. dtype: qué números entran

| dtype | rango | uso típico |
|---|---|---|
| `uint8` | 0 a 255, enteros | imágenes tal como se leen y se guardan |
| `int16`, `int32` | con signo | cuentas intermedias con enteros (restas, sumas grandes) |
| `float32` | reales, ~7 dígitos | cuentas sobre imágenes, redes neuronales |
| `float64` | reales, ~16 dígitos | default de NumPy, estadísticas, geometría |
| `bool` | True / False | máscaras |

### Overflow: `uint8` da la vuelta

```python
a = np.array([200], dtype=np.uint8)
a + np.array([100], dtype=np.uint8)    # array([44], dtype=uint8)   ← 300 mod 256
np.array([50], np.uint8) - np.array([100], np.uint8)   # array([206])  ← -50 mod 256
```

No tira error ni warning: **miente en silencio**. En una imagen se ve como manchas raras donde debería haber blanco.

### Reglas de promoción (NumPy 2)

```python
x = np.array([200], dtype=np.uint8)
x + 100            # uint8 → 44  (el 100 de Python se adapta al tipo del array)
x + 300            # OverflowError: 300 no entra en uint8
x + np.int16(100)  # int16 → 300 (se promueve al tipo más grande)
x * 1.0            # float64 → 200.0
x / 255            # float64 → 0.784...
```

**Regla práctica:** antes de hacer cuentas con una imagen, convertila.
- Para cuentas "de imagen" (brillo, mezclas, filtros): `float32` en [0, 1], con `img.astype(np.float32) / 255`.
- Para cuentas enteras (restas entre canales, conteos): `astype(np.int16)` o `np.int32`.
- Para volver a `uint8`: **primero `clip`, después `round`, después `astype`.**

```python
def a_uint8_seguro(f):        # f en [0, 1], puede tener valores afuera
    return np.round(np.clip(f, 0, 1) * 255).astype(np.uint8)
```

Ojo: `astype(np.uint8)` sobre un float **trunca**, no redondea, y si el valor está fuera de rango el resultado no está definido. Por eso va primero el clip.

---

## 3. Indexar: vistas y copias

### Slicing básico → **vista**

Un slice con `:` no copia nada: devuelve una **vista**, otro array que mira la *misma memoria*.

```python
img = np.zeros((720, 1280, 3), dtype=np.uint8)
recorte = img[100:200, 300:400]      # vista
recorte[:] = 255                      # ...pinta de blanco ESA zona de img
img[150, 350]                         # array([255, 255, 255])

np.shares_memory(img, recorte)        # True
copia = img[100:200, 300:400].copy()  # ahora sí, independiente
```

Por qué es así: copiar 6 MB cada vez que mirás una zona sería carísimo. Las vistas son gratis. Pero hay que saber cuándo tenés una.

### Indexado avanzado → **copia**

Indexar con **arrays de enteros** o con **máscaras booleanas** siempre devuelve una copia:

```python
filas = np.array([10, 20, 30])
img[filas]                 # copia, shape (3, 1280, 3)
img[img[..., 1] > 100]     # copia, shape (K, 3): los K píxeles que cumplen
```

| Operación | ¿Vista o copia? |
|---|---|
| `a[2:5]`, `a[:, 0]`, `a[..., ::-1]`, `a[::2, ::2]` | vista |
| `a.reshape(...)` (si se puede) | vista |
| `a.T`, `a.transpose(...)` | vista |
| `a[[1, 3, 5]]`, `a[mascara]` | **copia** |
| `a.astype(...)`, `a + 1`, `np.clip(a, ...)` | **copia** (array nuevo) |
| `a.copy()` | copia |

**Atajos útiles:**
- `img[..., 0]`: los `...` significan "todos los ejes de antes". Es el canal 0 sin importar si la imagen es `(H, W, 3)` o `(T, H, W, 3)`.
- `img[::2, ::2]` submuestrea a la mitad. Es una vista y no promedia nada (tiene *aliasing*, lo vemos en U2).
- `img[::-1]` da vuelta la imagen verticalmente y `img[:, ::-1]` la espeja.

---

## 4. Broadcasting

### La regla

Para operar dos arrays de shapes distintas, NumPy:
1. Compara las shapes **de derecha a izquierda**.
2. En cada eje, los tamaños tienen que ser **iguales**, o uno de los dos tiene que ser **1** (o no existir).
3. Los ejes de tamaño 1 se "estiran" (sin copiar memoria) hasta el tamaño del otro.

```
(720, 1280, 3)        imagen
          (3,)        un valor por canal
-------------------
(720, 1280, 3)   ✓    cada píxel se multiplica por los mismos 3 pesos
```

```
(720, 1280, 3)        imagen
   (720, 1280)        máscara
-------------------
     ✗  error: comparando de la derecha, 3 contra 1280
```

Arreglo: agregarle a la máscara un eje de tamaño 1 al final:

```python
m = mascara[..., None]      # (720, 1280) → (720, 1280, 1)
img * m                      # (720, 1280, 3) ✓: apaga los píxeles fuera de la máscara
```

`None` (o `np.newaxis`) dentro de un índice **agrega un eje de tamaño 1** en esa posición.

### El caso del diagnóstico

```python
A = np.ones((3, 4))
b = np.arange(4)    # (4,)  → A + b  funciona: b se suma a cada FILA
c = np.arange(3)    # (3,)  → A + c  error: (3,4) vs (3,), compara 4 con 3
A + c[:, None]      # c pasa a (3, 1) → se suma a cada COLUMNA ✓
```

### El truco que vamos a usar en tracking

¿Distancia entre **todos** los pares de N jugadores del frame t y M jugadores del frame t+1?

```python
A = np.random.rand(5, 2)    # N=5 posiciones (x, y)
B = np.random.rand(7, 2)    # M=7 posiciones
D = np.linalg.norm(A[:, None, :] - B[None, :, :], axis=-1)
# (5,1,2) - (1,7,2) → (5,7,2) → norma sobre el último eje → (5, 7)
D.shape                      # (5, 7): D[i, j] = distancia entre A[i] y B[j]
```

Sin un solo loop. En U8, esta matriz es la **matriz de costos** del algoritmo húngaro.

---

## 5. `axis`: reducir sobre un eje

En `mean`, `sum`, `max`, `min`, `std` y compañía, `axis` dice **qué eje desaparece**.

```python
img.shape                    # (720, 1280, 3)
img.mean()                   # un número: promedio de todo
img.mean(axis=2).shape       # (720, 1280): promedio de los 3 canales en cada píxel
img.mean(axis=(0, 1)).shape  # (3,): color promedio de la imagen (uno por canal)

P = np.random.rand(100, 2)   # trayectoria: 100 posiciones (x, y)
P.mean(axis=0)               # (2,): posición media  ← lo que había que hacer en el diagnóstico
P.mean(axis=1)               # (100,): promedio de x e y en cada instante (no significa nada)
```

**Truco mnemotécnico:** el `axis` que pasás es el que se *aplasta*. Si querés quedarte con "uno por canal", aplastá los ejes de alto y ancho.

### `keepdims`: reducir y poder volver a operar

```python
media = img.mean(axis=(0, 1), keepdims=True)   # (1, 1, 3) en vez de (3,)
centrada = img - media                          # broadcasting directo
```

### `np.diff`: diferencias consecutivas

```python
P = np.array([[0, 0], [3, 0], [3, 4]], dtype=float)
np.diff(P, axis=0)          # [[3, 0], [0, 4]]: los "pasos" entre posiciones
```

---

## 6. Máscaras booleanas

Una comparación devuelve un array de `bool` de la misma shape:

```python
G = img[..., 1].astype(np.int16)
R = img[..., 0].astype(np.int16)
verde = G > R + 20          # (H, W) bool
verde.mean()                # fracción de píxeles verdes (True cuenta como 1)
verde.sum()                 # cantidad
```

- Se combinan con `&` (y), `|` (o) y `~` (no). **Siempre con paréntesis**: `(G > R) & (G > B)`. Sin paréntesis, `G > R & G > B` se evalúa como `G > (R & G) > B` (porque `&` tiene más precedencia que `>`), y explota con un `ValueError: truth value ... is ambiguous`.
- `img[mascara]` devuelve los píxeles seleccionados como un array `(K, 3)`. De ahí, `img[mascara].mean(axis=0)` es el color promedio de esos píxeles.
- `np.where(cond, a, b)` elige elemento a elemento: `a` donde la condición es True y `b` donde no.

---

## 7. Vectorizar: por qué y cómo

Un `for` de Python sobre los 2 millones de píxeles de un frame 1080p hace 2 millones de iteraciones del intérprete, a ~50–100 ns cada una como mínimo. Son segundos por frame. La misma cuenta vectorizada corre en C sobre memoria contigua y tarda milisegundos: **100 a 1000 veces más rápido**.

```python
# con loop: varios segundos
gris = np.zeros(img.shape[:2])
for y in range(img.shape[0]):
    for x in range(img.shape[1]):
        r, g, b = img[y, x]
        gris[y, x] = 0.299 * r + 0.587 * g + 0.114 * b

# vectorizado: milisegundos
gris = img.astype(np.float32) @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
```

¿Por qué funciona el `@`? Con un array de N dimensiones y un vector, `@` hace el producto escalar sobre el **último eje**: `(H, W, 3) @ (3,) → (H, W)`. Es la misma idea que `x @ w` del diagnóstico, aplicada a cada píxel a la vez.

**Patrones para vectorizar:**
| En vez de... | Usá... |
|---|---|
| loop que transforma cada elemento | operaciones elemento a elemento (`+`, `*`, `np.clip`, `np.sqrt`) |
| loop que acumula | `sum`, `mean`, `max` con `axis` |
| loop con `if` | máscara booleana o `np.where` |
| loop que compara todos contra todos | broadcasting con `None` |
| loop que cuenta valores | `np.bincount` |
| loop sobre posiciones consecutivas | `np.diff`, `np.cumsum` |

---

## 8. Trayectorias: distancia y velocidad bien hechas

Una trayectoria es `P` con shape `(N, 2)`: posiciones `(x, y)` en metros, una cada `1/fps` segundos.

```python
pasos = np.diff(P, axis=0)                     # (N-1, 2): desplazamiento en cada tramo
dist = np.linalg.norm(pasos, axis=1)           # (N-1,): metros de cada tramo (Pitágoras)
total = dist.sum()                             # distancia recorrida
v_ms = dist * fps                              # metros por segundo (cada tramo dura 1/fps)
v_kmh = v_ms * 3.6
```

### Los datos reales están sucios, de dos formas

**1. Ruido.** La posición medida tiembla unos centímetros alrededor de la real. Como la distancia suma *normas* (siempre positivas), el ruido **no se cancela, se acumula**: un jugador parado "recorre" metros. En el proyecto anterior se midió que un jugador quieto acumulaba 2,4 m en 10 segundos.
- Soluciones: suavizar la trayectoria antes de medir (U2) o ignorar los pasos más chicos que el ruido.

**2. Saltos.** El tracker confunde a un jugador con otro y la posición salta 20 metros en 0,1 s. Son 720 km/h.
- Solución: **descartar lo físicamente imposible**. Ningún Sub-21 supera los ~35–38 km/h.

**Estadísticos robustos.** El máximo de las velocidades lo define *el peor error*. Por eso, como "velocidad tope", se usa un **percentil alto** (95 o 99): ignora el 5 % o el 1 % más extremo. Es la misma lógica de preferir la mediana a la media cuando hay valores atípicos.

---

## 9. Leer video con OpenCV

```python
import cv2
cap = cv2.VideoCapture("datos/clips/cissab_00600_60s.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)            # p. ej. 60.0
n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # aproximado en algunos formatos

i = 0
while True:
    ok, frame = cap.read()                 # frame: (H, W, 3) uint8 en BGR
    if not ok:
        break
    if i % 6 == 0:                         # muestrear a 10 fps de un video de 60 fps
        ...                                # procesar frame[..., ::-1] (RGB)
    i += 1
cap.release()
```

Trampas que ya costaron caro en el proyecto anterior:
- **AV1:** si el video está en AV1, OpenCV puede "abrirlo" e informar bien el ancho y el alto, pero `read()` devuelve `False` desde el primer frame. No hay error: hay 0 frames. Por eso `herramientas/bajar_frames.py` pide H.264.
- **Índice del frame contra índice de la muestra:** si muestreás 1 de cada 6 frames, la muestra número 10 es el **frame 60** del video. Si guardás el número de muestra y después dividís por los fps del video, todas las velocidades salen 6 veces mal. Pasó, y desactivó en silencio un filtro de velocidades imposibles. **Regla: guardá siempre el índice del frame del video original.**
- `cap.set(cv2.CAP_PROP_POS_FRAMES, k)` para saltar a un frame no siempre es exacto en video comprimido: puede caer en el keyframe anterior.

---

## 10. Errores comunes (checklist)

- [ ] ¿Indexé `img[x, y]` en vez de `img[y, x]`?
- [ ] ¿Hice cuentas en `uint8` que pueden pasar de 255 o bajar de 0?
- [ ] ¿Convertí a `uint8` sin `clip` o sin `round`?
- [ ] ¿Modifiqué un recorte que era una vista y rompí la imagen original?
- [ ] ¿Mostré con matplotlib una imagen BGR?
- [ ] ¿Reduje sobre el `axis` equivocado? (Mirá la shape del resultado.)
- [ ] ¿Combiné máscaras sin paréntesis?
- [ ] ¿Usé `*` cuando quería `@`, o al revés?
- [ ] ¿Usé el máximo cuando los datos tienen errores?

## Resumen para volver

| Concepto | En una línea |
|---|---|
| Shape de imagen | `(H, W, C)`: alto, ancho, canales. `img[y, x]` |
| OpenCV | BGR. `img[..., ::-1]` para pasar a RGB |
| `uint8` | 0–255 y da la vuelta: `200 + 100 = 44`. Para hacer cuentas, `float32` o `int16` |
| Volver a `uint8` | `np.round(np.clip(f, 0, 1) * 255).astype(np.uint8)` |
| Vista | Slicing con `:`. Comparte memoria. `.copy()` para independizar |
| Copia | Indexado con arrays o máscaras, y cualquier operación aritmética |
| Broadcasting | Shapes comparadas de derecha a izquierda; iguales o 1. `x[..., None]` agrega un eje |
| `axis` | El eje que pasás es el que desaparece. `keepdims=True` para seguir operando |
| Máscaras | `(a > b) & (c < d)`, `img[m]` → `(K, C)`, `m.mean()` = fracción |
| `*` y `@` | `*` elemento a elemento; `@` producto matricial o escalar sobre el último eje |
| Distancia | `np.linalg.norm(np.diff(P, axis=0), axis=1).sum()` |
| Datos sucios | Filtrar lo imposible y usar percentiles, no el máximo |
