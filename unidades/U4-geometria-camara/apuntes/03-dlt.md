# 03 · DLT: estimar la homografía con la SVD

> **La idea en una frase:** cada correspondencia (punto de la cancha ↔ píxel) da **dos ecuaciones lineales** en los 9 números de H. Con todas juntas queda un sistema `A h = 0`, y la mejor solución (con ruido) es la **última columna de V** de la SVD de A: el truco del apunte 07 de U1. Normalizar los puntos antes hace que el problema esté bien condicionado.

**Videos:** Stachniss, Photogrammetry I, clase **17** (*Camera Orientation*: DLT). **Lectura:** Hartley & Zisserman, 4.1–4.4 (**la referencia**: vale la pena leerla).

---

## 1. De una correspondencia a dos ecuaciones

Un punto de la cancha `(x, y)` va al píxel `(u, v)`:

$$\begin{bmatrix}u\\v\\1\end{bmatrix} \simeq H\begin{bmatrix}x\\y\\1\end{bmatrix}, \qquad H = \begin{bmatrix} h_1 & h_2 & h_3\\ h_4 & h_5 & h_6\\ h_7 & h_8 & h_9\end{bmatrix}$$

Con la división por W explícita:

$$u = \frac{h_1 x + h_2 y + h_3}{h_7 x + h_8 y + h_9}, \qquad v = \frac{h_4 x + h_5 y + h_6}{h_7 x + h_8 y + h_9}$$

**Multiplicando** por el denominador (el truco que lo hace lineal):

$$u\,(h_7 x + h_8 y + h_9) - (h_1 x + h_2 y + h_3) = 0$$
$$v\,(h_7 x + h_8 y + h_9) - (h_4 x + h_5 y + h_6) = 0$$

Son **lineales en los hᵢ**. Con `h = (h₁, …, h₉)`, cada correspondencia aporta las dos filas:

$$\begin{bmatrix} -x & -y & -1 & 0 & 0 & 0 & ux & uy & u\\ 0 & 0 & 0 & -x & -y & -1 & vx & vy & v\end{bmatrix}\mathbf h = \mathbf 0$$

Apilando N correspondencias: **A h = 0**, con A de 2N × 9. Es `matriz_dlt` del TP4.

(El nombre: *Direct Linear Transformation*, porque pasa directo a un sistema lineal.)

## 2. Resolverlo

- **4 puntos (en posición general):** 8 ecuaciones, 9 incógnitas. El espacio nulo de A es una recta, y h queda determinado salvo la escala: solución **exacta**.
- **Más de 4, con ruido:** no hay solución exacta. Se busca:

$$\hat{\mathbf h} = \arg\min_{\|\mathbf h\| = 1} \|A\mathbf h\|$$

(La condición ‖h‖ = 1 evita la solución trivial h = 0.) Por el apunte 07 de U1: **ĥ es el vector singular derecho del menor valor singular** de A, o sea, `Vt[-1]` en NumPy. Después: `H = ĥ.reshape(3, 3)` y se divide por H[2, 2].

**Si la configuración es degenerada** (3 o más puntos alineados, todos amontonados), A tiene **dos** valores singulares chicos: hay varias "soluciones" casi igual de buenas, y la que devuelve la SVD es basura. Lo vas a ver en el TP.

## 3. Normalización de Hartley: por qué y cómo

Mirá las columnas de A con coordenadas crudas: en la cancha, x e y van de 0 a 100 (metros); en la imagen, u y v van de 0 a ~2000 (píxeles). Las columnas `ux`, `uy` y `u` tienen valores de hasta ~200.000, y las columnas `−1` valen 1. **Escalas de 5 órdenes de magnitud dentro de la misma matriz:** el problema está muy mal condicionado (U1, apunte 03). La relación entre el mayor y el octavo valor singular de A es enorme.

**La receta de Hartley.** A cada conjunto de puntos (origen y destino, **por separado**):
1. trasladar para que el centroide quede en el origen;
2. escalar para que la distancia media al origen sea **√2** (o sea, que un punto "típico" sea (1, 1)).

Las dos cosas juntas son una matriz de similitud T de 3×3. Entonces:

$$\hat H_{norm} = \text{DLT}(T_s\,\mathbf x,\ T_d\,\mathbf u) \qquad\Rightarrow\qquad H = T_d^{-1}\,\hat H_{norm}\,T_s$$

(De derecha a izquierda: normalizar el origen, aplicar Ĥ, des-normalizar el destino.)

### Lo que se midió (honesto)
Con la cámara sintética del TP (es la sección 2 del notebook: 10 puntos de la zona visible, 300 sorteos):
- normalizar baja la relación σ₁/σ₈ de A de **~450.000 a ~6**;
- **sin ruido** (correspondencias exactas), el error puramente numérico baja unas **1000 veces** en `float64` (de ~4·10⁻¹¹ m a ~3·10⁻¹⁴ m) y unas 5 veces haciendo la SVD en `float32` (de ~5·10⁻⁶ m a ~1·10⁻⁶ m);
- **pero con 2 px de ruido** en los clicks, el error final es **el mismo** con y sin normalizar: ~0,24 m de mediana en los dos casos, también en `float32`. El error de los clicks es millones de veces más grande que el error numérico, y lo tapa.

La normalización no es magia que "mejora la precisión" en todos los casos. Lo que hace, medido, es achicar el error **numérico**; y además hace que el resultado **no dependa** de en qué unidades o con qué origen medís. Hartley & Zisserman muestran casos donde el DLT sin normalizar sí da resultados malos (coordenadas más grandes, configuraciones casi degeneradas); acá **no lo medimos**, así que tomalo como lo que dicen ellos, no como algo que viste. Igual es el estándar, porque cuesta dos líneas.

## 4. Error algebraico contra error geométrico

El DLT minimiza **‖Ah‖**, el error **algebraico**: un número sin significado físico directo. Lo que importa es el error **geométrico**: la distancia en píxeles (o en metros) entre donde H manda un punto y donde realmente está. Es el **error de reproyección**:

$$e_i = \big\| \text{aplicar}(H, \mathbf x_i) - \mathbf u_i \big\|$$

No son lo mismo. El DLT es una muy buena **inicialización**. Después se puede **refinar** minimizando el error geométrico con un optimizador no lineal (Levenberg-Marquardt), y es lo que hace `cv2.findHomography`. Medido con 15 puntos y 1,5 px de ruido: según qué puntos toquen, el DLT queda entre ~5 % (sección 2 del notebook) y ~15 % (el test `test_dlt_como_opencv`) peor que OpenCV en error de reproyección.

---

## Resumen para volver

- Cada correspondencia da 2 ecuaciones **lineales** en h (multiplicando por el denominador). En total, `A h = 0`, con A de 2N × 9.
- 4 puntos: solución exacta. Más de 4 con ruido: **`h = Vt[-1]`**, el menor valor singular.
- **Hartley:** normalizar origen y destino (centroide 0, distancia media √2). `H = Td⁻¹ Ĥ Ts`. Mejora muchísimo el condicionamiento y achica el error numérico; con clicks reales (ruido de píxeles) el resultado final medido no cambia, pero deja de depender de las unidades.
- DLT = error **algebraico**. Lo que importa es el **geométrico** (reproyección), y se puede refinar después.
