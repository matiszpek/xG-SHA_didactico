# 01 · El modelo *pinhole*: cómo el mundo 3D cae en la imagen

> **La idea en una frase:** una cámara es una matriz de 3×4 que lleva puntos 3D a píxeles **dividiendo por la profundidad**. Esa división hace que lo lejano se vea chico, que las paralelas se junten en un punto de fuga y que la profundidad se pierda para siempre.

**Videos:** Stachniss, Photogrammetry I, clases **15** (*Homogeneous Coordinates*, repaso) y **16** (*Camera Extrinsics and Intrinsics*). **Lectura:** Szeliski, 2.1.

---

## 1. La cámara estenopeica (*pinhole*)

Una caja cerrada con un agujerito: la luz de cada punto del mundo pasa por el agujero y pega en el fondo. Con la geometría de triángulos semejantes, un punto en coordenadas **de la cámara** (X, Y, Z), con Z = distancia hacia adelante, cae en:

$$x = f\,\frac{X}{Z}, \qquad y = f\,\frac{Y}{Z}$$

f es la **distancia focal**, medida en píxeles.

**Lo lejano se ve más chico** porque se divide por una Z más grande. Un jugador de 1,75 m con f = 1400 px mide 1400·1,75/50 ≈ **49 px** a 50 m y **122 px** a 20 m. Es el mismo orden de magnitud que los 30–230 px medidos en los videos del club (la focal real de esa cámara no la conocemos: f = 1400 es una suposición razonable para 1920 px de ancho, no una medición).

## 2. En homogéneas: la división es la división por W

$$\begin{bmatrix} u\\ v\\ w\end{bmatrix} = \begin{bmatrix} f & 0 & c_x\\ 0 & f & c_y\\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix} X\\ Y\\ Z\end{bmatrix} \quad\Rightarrow\quad (x, y) = \left(\frac{u}{w},\ \frac{v}{w}\right) = \left(f\frac{X}{Z} + c_x,\ f\frac{Y}{Z} + c_y\right)$$

La tercera coordenada vale Z, y **dividir por W es dividir por la profundidad**. Es la "división por W" que pusiste en `aplicar` en el TP1 sin que hiciera nada: acá hace todo.

### Intrínsecos: K
$$K = \begin{bmatrix} f_x & s & c_x\\ 0 & f_y & c_y\\ 0 & 0 & 1\end{bmatrix}$$

- f_x y f_y son la focal en píxeles: iguales si los píxeles son cuadrados.
- (c_x, c_y) es el **punto principal**, donde el eje óptico corta la imagen (≈ el centro).
- s es la inclinación de los píxeles: 0 en cualquier cámara moderna.

Son propiedades **de la cámara**: no cambian si la movés.

### Extrínsecos: R y t
La cámara está en algún lugar del mundo, apuntando para algún lado. Para pasar un punto del mundo a coordenadas de la cámara:

$$\mathbf X_{cam} = R\,\mathbf X_{mundo} + \mathbf t$$

- R (3×3) es una **rotación**: sus filas son los ejes de la cámara (derecha, abajo, adelante) escritos en el mundo.
- t = −R·C, donde C es la posición de la cámara en el mundo.

### La matriz de cámara
$$P = K\,[R \mid \mathbf t] \qquad (3 \times 4)$$

$$\mathbf x \simeq P\,\begin{bmatrix}\mathbf X\\ 1\end{bmatrix}$$

(≃ significa "igual a menos de un factor": las coordenadas homogéneas no tienen escala.)

**Es una matriz de 3×4: de 3D a 2D** (U1, apunte 03). Se pierde una dimensión: todos los puntos sobre el mismo rayo que sale de la cámara caen en el mismo píxel. Por eso **es imposible saber la profundidad con una sola imagen** sin información extra. Es la ambigüedad de altura de la pelota (diagnóstico, bloque 5, pregunta 10).

## 3. Puntos de fuga

Una recta 3D en la dirección d: `X(λ) = X₀ + λ·d`. Cuando λ → ∞, en homogéneas el punto tiende a `(d, 0)`: un punto **en el infinito** (U1, apunte 04). Su imagen es:

$$\mathbf v \simeq P\begin{bmatrix}\mathbf d\\ 0\end{bmatrix} = K R\,\mathbf d$$

**No depende de X₀**, así que **todas las rectas paralelas (misma d) convergen al mismo punto de la imagen**: el punto de fuga. Las dos laterales de la cancha son paralelas y se juntan en un punto. En el TP2 lo calculaste con `interseccion`.

- Si d es paralela al plano de la imagen (perpendicular al eje óptico), la tercera coordenada de KRd es 0: el punto de fuga está en el infinito y las paralelas **se ven paralelas**.
- Es la geometría que usaban los pintores del Renacimiento (y lo de "punto de fuga" en dibujo que mencionaste en el diagnóstico).

## 4. Lo que el modelo deja afuera: distorsión

Las lentes reales, sobre todo las gran angulares (GoPro, cámaras de 180°), **curvan las rectas**: es la distorsión de barril. Se modela con unos pocos coeficientes y se corrige antes de usar el *pinhole* (calibración intrínseca con un tablero de ajedrez, `cv2.calibrateCamera`).

El stream del club no muestra una distorsión fuerte. Una cámara propia gran angular (una de las opciones de la versión producto) sí la tendría: hay que saberlo.

---

## Resumen para volver

- `x = f X/Z + c_x`: dividir por la profundidad. Lo lejano se ve chico (49 px a 50 m y 122 px a 20 m, con f = 1400).
- **K** (intrínsecos: f, c), **R, t** (extrínsecos: dónde está y hacia dónde mira, con t = −RC). **P = K[R | t]**, de 3×4.
- 3D → 2D: la profundidad se pierde. Una pelota en el aire no se ubica con una sola cámara.
- **Punto de fuga** = K R d. Las paralelas se cortan ahí, salvo que sean paralelas a la imagen.
- Las lentes gran angulares distorsionan: se corrige antes.
