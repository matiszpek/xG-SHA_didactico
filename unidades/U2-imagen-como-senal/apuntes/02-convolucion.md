# 02 · Convolución, filtros y ruido

> **La idea en una frase:** convolucionar es reemplazar cada píxel por una **suma ponderada de sus vecinos**, con los pesos dados por un kernel chico que se desliza por toda la imagen. Con eso se desenfoca, se deriva y se detectan bordes. Y es la operación central de las redes convolucionales.

**Videos:**
- First Principles of CV, Módulo 1: *Image Processing I*.
- 3Blue1Brown: *But what is a convolution?* (ojo: arranca con probabilidad y llega a imágenes a la mitad; vale todo).

**Lectura:** Szeliski, 3.2 (*Linear filtering*) y 3.3 (*More neighborhood operators*).

---

## 1. De "promedio de vecinos" a kernel

Desenfocar promediando cada píxel con sus 8 vecinos:

$$g[y, x] = \frac{1}{9}\sum_{i=-1}^{1}\sum_{j=-1}^{1} f[y+i,\ x+j]$$

Generalizando, con pesos cualesquiera `k[i, j]`, se obtiene la **correlación**:

$$g[y, x] = \sum_{i,j} k[i, j]\; f[y+i,\ x+j]$$

El array de pesos `k` es el **kernel** (o filtro, o máscara). Si el kernel es (2r + 1) × (2r + 1), los índices van de −r a r.

## 2. Correlación contra convolución

La **convolución** es lo mismo, pero con el kernel **dado vuelta**:

$$(f * k)[y, x] = \sum_{i,j} k[i, j]\; f[y-i,\ x-j]$$

Si el kernel es simétrico (gaussiano, promedio), da exactamente lo mismo. ¿Para qué existen las dos?

**La convolución tiene mejores propiedades algebraicas:**
- **Conmutativa:** `f * k = k * f`.
- **Asociativa:** `(f * k₁) * k₂ = f * (k₁ * k₂)`. Aplicar dos filtros en cadena es lo mismo que aplicar **un** filtro, que es la convolución de los dos. Esto lo usamos enseguida: "desenfocar y después derivar" = "convolucionar con la derivada de una gaussiana".
- **Respuesta al impulso.** Si convolucionás una imagen negra con un único píxel blanco (un *impulso*), sale el kernel tal cual. Con correlación sale dado vuelta. El test `test_s2_convolucion_no_es_correlacion` es exactamente esto.

**En las CNN (U6),** lo que se llama "convolución" es en realidad correlación: no se da vuelta el kernel. No importa, porque los pesos se *aprenden*: el kernel aprendido simplemente sale dado vuelta.

## 3. Lineal e invariante a traslaciones

La convolución es:
- **lineal:** filtrar `a·f + b·h` = `a·(filtrar f) + b·(filtrar h)`;
- **invariante a traslaciones:** mover la imagen y filtrar = filtrar y mover.

Y vale la recíproca: **todo operador lineal e invariante a traslaciones es una convolución.** Por eso aparece en todos lados: "tratar igual todas las posiciones" es justo lo que se quiere cuando no sabés dónde va a estar el jugador. Es la misma razón por la que las CNN funcionan mejor que una capa densa sobre imágenes (diagnóstico, bloque 4, pregunta 9).

## 4. Qué hacer en los bordes

Cerca del borde, el kernel "se sale" de la imagen. Hay que inventar los valores de afuera (*padding*):

| Modo | Relleno | Efecto |
|---|---|---|
| `"cero"` | 0 0 \| a b c d \| 0 0 | El borde se **oscurece** al desenfocar (promediás con negro) |
| `"replicar"` | a a \| a b c d \| d d | Bien para imágenes; estira el último píxel |
| `"espejo"` | c b \| a b c d \| c b | Lo más natural para imágenes: continúa la textura. **Es el default** |

Tamaño de la salida:
- *same*: igual a la entrada, rellenando. Es lo que hacemos.
- *valid*: solo donde el kernel entra completo; se achica (k − 1) píxeles.
- *full*: se agranda.

## 5. Implementarla sin loops sobre píxeles

**Opción A: ventanas deslizantes.** `np.lib.stride_tricks.sliding_window_view(p, (kh, kw))` devuelve un array de shape `(H, W, kh, kw)` donde `[y, x]` es la ventanita alrededor de ese píxel. **No copia memoria: es una vista** (U0, sección 3). Después:

```python
salida = np.einsum("ijkl,kl->ij", ventanas, kernel)    # suma ponderada en cada ventana
```

`einsum` es una forma de escribir "multiplicar y sumar sobre estos ejes". `"ijkl,kl->ij"` se lee: para cada (i, j), sumar sobre k y l el producto `ventanas[i, j, k, l] · kernel[k, l]`.

**Opción B: loop sobre el kernel** (está permitido: son k² iteraciones, no millones). Por cada posición (i, j) del kernel, sumar `kernel[i, j] · (imagen rellena desplazada)`:

```python
salida = sum(kernel[i, j] * p[i:i+H, j:j+W] for i in range(kh) for j in range(kw))
```

Las dos son O(H · W · k²).

## 6. Filtros de suavizado

### Promedio (*box*)
Todos los pesos iguales, 1/k². Es simple, pero deja artefactos "cuadrados" y no es isotrópico: no trata igual todas las direcciones.

### Gaussiano
$$G_\sigma(x, y) = \frac{1}{2\pi\sigma^2}\, e^{-\frac{x^2 + y^2}{2\sigma^2}}$$

- **σ es la escala:** cuánto se desenfoca. σ = 1 borra detalle de ~1–2 px y σ = 5 borra detalle de ~10 px.
- **Radio ≈ 3σ:** más allá, los pesos son despreciables. Es la regla del 68–95–99,7 del diagnóstico: ±3σ junta el 99,7 %.
- **Normalizado (suma 1):** así no cambia el brillo medio.
- **Separable:** `G(x, y) = g(x) · g(y)`. El kernel 2D es el **producto externo** de dos 1D, `np.outer(g, g)`, una matriz de **rango 1** (U1, apunte 07). Filtrar por filas con g y después por columnas con g da lo mismo que el 2D, con **2k operaciones por píxel en vez de k²**. Con k = 31, son 62 contra 961.
- Gaussiana sobre gaussiana es otra gaussiana, con `σ² = σ₁² + σ₂²`.

**¿Un kernel es separable?** Sí, exactamente cuando tiene rango 1. Para verificarlo: `np.linalg.matrix_rank(K) == 1`. Y la SVD te da los dos vectores: `K = σ₁ u₁ v₁ᵀ`.

## 7. Ruido y la mediana

| Tipo de ruido | De dónde sale | Qué lo arregla |
|---|---|---|
| Gaussiano (cada píxel ± un poco) | sensor, poca luz | gaussiano |
| Sal y pimienta (píxeles sueltos en 0 o 255) | errores de transmisión, píxeles muertos | **mediana** |
| Bloques y *ringing* | compresión | gaussiano suave; no hay arreglo perfecto |

El **filtro de mediana** reemplaza cada píxel por la mediana de su ventana:
- **No es lineal**: no es una convolución.
- Es **robusto**: un valor extremo no la mueve. Es la misma lección que en U0, cuando se prefería el percentil al máximo.
- **Preserva los bordes** mejor que el gaussiano.
- Con `sliding_window_view`, es `np.median(ventanas, axis=(-2, -1))`.

## 8. En la cancha

- Antes de detectar bordes (apunte 03) **siempre** se desenfoca un poco: la compresión de YouTube genera bordes falsos por todos lados.
- **El compromiso de la escala:** la pelota mide ~10 px. Con un σ grande desaparece. No hay un σ "correcto": depende de qué querés ver. (En U7 vas a ver que las redes resuelven esto procesando la imagen en varias escalas.)

---

## Resumen para volver

- **Correlación:** `Σ k[i,j] f[y+i, x+j]`. **Convolución:** igual, con el kernel dado vuelta. Si el kernel es simétrico, da lo mismo.
- La convolución es asociativa y conmutativa: varios filtros en cadena = un solo filtro.
- Lineal + invariante a traslaciones ⟺ convolución.
- Bordes: cero (oscurece), replicar o espejo (el default).
- Implementación: `sliding_window_view` + `einsum`, o un loop sobre el kernel. O(HWk²).
- **Gaussiano:** σ = escala, radio 3σ, suma 1, **separable** (rango 1): 2k operaciones en vez de k².
- **Mediana:** no lineal, robusta, preserva bordes. Ideal para sal y pimienta.
