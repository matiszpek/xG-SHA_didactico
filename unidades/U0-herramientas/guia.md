# U0 — Guía de ejercicios

**Cómo usarla:** primero escribí tu respuesta (en papel o en un archivo); después corré el código para verificar, si aplica; recién al final abrí la respuesta. Los ejercicios de "predecí" valen solo si predecís **antes** de correr.

---

## Bloque A — Shapes y dtypes (sesión 1)

**1.** Un frame de un video 4K (3840×2160) leído con OpenCV:
- (a) ¿qué `shape` y qué `dtype` tiene?
- (b) ¿cuántos MB ocupa?
- (c) ¿cómo accedés al píxel que está en x = 100, y = 50?

**2.** Predecí el resultado y el dtype de cada línea:
```python
a = np.array([250, 10], dtype=np.uint8)
a + 10
a - 20
a.astype(np.int16) - 20
a / 2
a // 2
```

**3.** Tenés `f = np.array([-0.1, 0.004, 0.5, 0.999, 1.2])`, que representa intensidades en [0, 1] (con un par de valores afuera). Escribí en **una línea** la conversión correcta a `uint8` y decí qué valores da.

**4.** ¿Por qué `np.uint8(0.999 * 255)` da 254 y no 255? ¿Qué cambia si redondeás?

## Bloque B — Vistas, copias e indexado

**5.** Predecí qué imprime:
```python
img = np.zeros((4, 6), dtype=np.uint8)
a = img[1:3, 2:5]
b = img[[1, 2]]
a += 7
b += 100
print(img)
```

**6.** Escribí la expresión para cada caso (`img` es `(H, W, 3)`):
- (a) el canal verde;
- (b) la mitad izquierda de la imagen;
- (c) la imagen espejada horizontalmente;
- (d) la imagen a la mitad de resolución (un píxel de cada dos);
- (e) la fila del medio, como array `(W, 3)`.

**7.** Caja `(x1, y1, x2, y2) = (300, 100, 340, 180)`. ¿Qué shape tiene `img[y1:y2, x1:x2]`? ¿Cuánto mide de alto y cuánto de ancho la caja, en píxeles?

## Bloque C — Broadcasting y axis

**8.** Para cada par de shapes, decí si se puede operar y la shape del resultado:
- (a) `(720, 1280, 3)` y `(3,)`
- (b) `(720, 1280, 3)` y `(720, 1280)`
- (c) `(720, 1280, 3)` y `(720, 1280, 1)`
- (d) `(5, 1, 2)` y `(1, 7, 2)`
- (e) `(4, 3)` y `(4,)`
- (f) `(10, 2)` y `(2,)`

**9.** `video` tiene shape `(T, H, W, 3)`. Escribí:
- (a) el color promedio de cada frame, de shape `(T, 3)`;
- (b) la imagen promedio del video (*background*), de shape `(H, W, 3)`;
- (c) el brillo promedio de cada frame, de shape `(T,)`.

**10.** Normalizá una imagen float `(H, W, 3)` para que **cada canal** tenga media 0 y desvío 1, en dos líneas y sin loops.

## Bloque D — Máscaras y vectorización (sesión 2)

**11.** Escribí, sin loops, la cantidad de píxeles de `img` (RGB, `uint8`) que son "casi blancos": los tres canales ≥ 200.

**12.** ¿Qué está mal acá, y cómo lo arreglás?
```python
mascara = img[..., 1] > img[..., 0] + 30 & img[..., 1] > img[..., 2] + 30
```
(Hay **dos** problemas.)

**13.** Tenés las posiciones de 11 jugadores en el frame t, `A` de shape `(11, 2)`, y de 10 jugadores en el frame t+1, `B` de shape `(10, 2)`. Para cada jugador de `A`, encontrá el índice del jugador de `B` más cercano, **sin loops**.

**14.** Reescribí sin loops:
```python
cuenta = [0] * 256
for v in canal.ravel():
    cuenta[v] += 1
```

## Bloque E — Trayectorias

**15.** `P = np.array([[0,0],[0,0.1],[0,0],[0,0.1],[0,0]])` es un jugador **quieto** cuya medición tiembla 10 cm. ¿Qué distancia total "recorrió"? Si el temblor siguiera así durante 90 minutos a 10 fps, ¿cuántos km fantasma serían?

**16.** Un jugador tiene velocidades (km/h) `[12, 14, 13, 15, 650, 14, 30, 31, 29, 13]`. Calculá el máximo, la media, la mediana y el percentil 90. ¿Cuál describe mejor su "velocidad tope real"? (No hace falta exactitud en el percentil.)

---

## Respuestas

<details>
<summary>Bloque A</summary>

**1.**
- (a) `(2160, 3840, 3)`, `uint8`.
- (b) 2160·3840·3 = 24.883.200 bytes ≈ 24,9 MB.
- (c) `img[50, 100]`.

**2.**
- `a + 10` → `[4, 20]` uint8 (250 + 10 = 260 → 4).
- `a - 20` → `[230, 246]` uint8 (10 − 20 = −10 → 246).
- `a.astype(np.int16) - 20` → `[230, -10]` int16.
- `a / 2` → `[125., 5.]` float64.
- `a // 2` → `[125, 5]` uint8.

**3.** `np.round(np.clip(f, 0, 1) * 255).astype(np.uint8)` → `[0, 1, 128, 255, 255]`. (0,004·255 = 1,02 → 1; 0,5·255 = 127,5 → 128; 0,999·255 = 254,7 → 255.)

**4.** 0,999·255 = 254,745, y convertir a entero **trunca**: queda 254. Con `np.round` da 255. Al pasar muchas veces de float a `uint8` y de vuelta, truncar va oscureciendo la imagen de a poco.
</details>

<details>
<summary>Bloque B</summary>

**5.** `a` es una vista: suma 7 en las filas 1–2, columnas 2–4 de `img`. `b` es una copia (indexado con lista): sumarle 100 no toca `img`.
```
[[0 0 0 0 0 0]
 [0 0 7 7 7 0]
 [0 0 7 7 7 0]
 [0 0 0 0 0 0]]
```

**6.**
- (a) `img[..., 1]`
- (b) `img[:, :img.shape[1] // 2]`
- (c) `img[:, ::-1]`
- (d) `img[::2, ::2]`
- (e) `img[img.shape[0] // 2]`

**7.** `(80, 40, 3)`: 80 de alto (180 − 100) y 40 de ancho (340 − 300).
</details>

<details>
<summary>Bloque C</summary>

**8.**
- (a) ✓ `(720, 1280, 3)`
- (b) ✗ (compara 3 con 1280)
- (c) ✓ `(720, 1280, 3)`
- (d) ✓ `(5, 7, 2)`
- (e) ✗ (3 contra 4). Con `b[:, None]` sí funciona.
- (f) ✓ `(10, 2)`

**9.**
- (a) `video.mean(axis=(1, 2))`
- (b) `video.mean(axis=0)`
- (c) `video.mean(axis=(1, 2, 3))`

**10.**
```python
mu = img.mean(axis=(0, 1), keepdims=True); sd = img.std(axis=(0, 1), keepdims=True)
norm = (img - mu) / sd
```
Esto es exactamente lo que hacen las redes con ImageNet: restar la media y dividir por el desvío de cada canal.
</details>

<details>
<summary>Bloque D</summary>

**11.** `(img >= 200).all(axis=2).sum()`

**12.**
- (1) Faltan paréntesis: `&` tiene más precedencia que `>`.
- (2) Hay overflow de `uint8` en `img[..., 0] + 30`.

Arreglado:
```python
x = img.astype(np.int16)
mascara = (x[..., 1] > x[..., 0] + 30) & (x[..., 1] > x[..., 2] + 30)
```

**13.**
```python
D = np.linalg.norm(A[:, None, :] - B[None, :, :], axis=-1)   # (11, 10)
cercano = D.argmin(axis=1)                                    # (11,)
```
Ojo: dos jugadores de A pueden elegir el mismo de B. Para que la asignación sea **uno a uno** hace falta el algoritmo húngaro (U8).

**14.** `cuenta = np.bincount(canal.ravel(), minlength=256)`
</details>

<details>
<summary>Bloque E</summary>

**15.** 4 tramos de 0,1 m: 0,4 m en 0,4 s. En 90 min a 10 fps hay 54.000 tramos · 0,1 m = **5,4 km fantasma**, sin moverse. Por eso hay que filtrar y suavizar.

**16.**
- Máximo: 650.
- Media: ≈ 82,1.
- Mediana: 14,5.
- Percentil 90: ≈ 93 (con interpolación lineal, entre 31 y 650).

Ninguno es perfecto con 10 datos, pero el problema es claro: un solo error domina el máximo y la media. Con datos reales (miles de tramos) el percentil 95 o 99 funciona bien. Lo más sano es **primero descartar lo imposible** (650 km/h) y después tomar un percentil alto.
</details>
