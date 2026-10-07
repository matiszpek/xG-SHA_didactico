# 03 · Cálculo multivariable mínimo, gradiente de imagen y bordes

> **La idea en una frase:** un borde es un lugar donde la intensidad **cambia de golpe**. El cambio se mide con el **gradiente**, el vector de derivadas parciales. Y como derivar amplifica el ruido, **siempre se suaviza antes**: mejor todavía, se deriva una gaussiana.

**Videos:**
- Khan Academy, *Multivariable calculus*: los videos de *partial derivatives* y *gradient* (los da Grant Sanderson, el de 3Blue1Brown).
- First Principles of CV, Módulo 2: *Edge Detection*.
- Stachniss, Photogrammetry I, clase 12 (*Feature Detection – Edge Detection*).

---

## 1. Cálculo multivariable: lo justo

Es lo que faltaba en el diagnóstico (bloque 1, preguntas 11 y 12), y lo vas a necesitar acá, en U3 (entrenar el xG) y en U6 (backprop).

### Derivadas parciales

Para una función de dos variables `f(x, y)`, la **derivada parcial** respecto de x es la derivada de siempre, **tratando y como una constante**:

$$f(x, y) = x^2 + 3xy \quad\Rightarrow\quad \frac{\partial f}{\partial x} = 2x + 3y, \qquad \frac{\partial f}{\partial y} = 3x$$

Es "la pendiente si caminás solo en la dirección x".

### Gradiente

$$\nabla f = \left(\frac{\partial f}{\partial x},\ \frac{\partial f}{\partial y}\right)$$

Tres hechos, y los tres importan:

1. **La derivada en cualquier dirección** u (unitaria) es un producto escalar: `D_u f = ∇f · u`. (Producto escalar de U1, apunte 04.)
2. Entonces la dirección de **máximo crecimiento** es la de ∇f (ahí el coseno vale 1), y la pendiente máxima es **‖∇f‖**.
3. En la dirección **perpendicular** a ∇f, la derivada es 0: el gradiente es **perpendicular a las curvas de nivel**. En una imagen: **el gradiente es perpendicular al borde**.

**Descenso por gradiente** (diagnóstico, bloque 1, pregunta 13, ahora con fundamento): para bajar lo más rápido posible, moverse en `−∇f`. No "prueba puntos": da pasitos en la dirección de mayor bajada.

### Regla de la cadena

Una variable, que ya la sabés: `d/dw g(h(w)) = g'(h(w)) · h'(w)`.

$$L(w) = (wx - y)^2 \quad\Rightarrow\quad \frac{dL}{dw} = 2(wx - y)\cdot x$$

(La "de afuera", `2(·)`, por la "de adentro", `x`.) Es la pregunta 12 del diagnóstico. Con dos parámetros, `L(w, b) = (wx + b − y)²`:

$$\frac{\partial L}{\partial w} = 2(wx + b - y)\,x, \qquad \frac{\partial L}{\partial b} = 2(wx + b - y)$$

Así se entrena una regresión, y así se entrena el modelo de xG en U3.

**Varias variables:** si `x(t)` e `y(t)` dependen de t, entonces `d/dt f(x(t), y(t)) = ∇f · (x'(t), y'(t))`. Backprop (U6) es aplicar esto sistemáticamente sobre un grafo.

**Jacobiano.** Si la función devuelve un vector, se ponen todas las derivadas parciales en una matriz. Aparece en U4 y U6; por ahora, saber que existe.

## 2. La imagen como función: derivadas discretas

Una imagen en grises es `I(x, y)`, pero solo la conocemos en los enteros. La derivada se aproxima con diferencias:

| Aproximación | Fórmula | Como kernel (correlación) |
|---|---|---|
| Hacia adelante | `I(x+1) − I(x)` | `[0, −1, 1]` |
| **Central** | `(I(x+1) − I(x−1)) / 2` | `[−1, 0, 1] / 2` |

La central es simétrica y más precisa. **Derivar es convolucionar.**

## 3. El problema: derivar amplifica el ruido

Supongamos dos píxeles vecinos con ruido independiente de desvío σₙ. La diferencia tiene desvío `σₙ·√2`, **más** ruido que cada píxel. Mientras tanto, en una zona suave la diferencia real entre vecinos es casi 0. Resultado: la derivada de una imagen ruidosa es **casi todo ruido**.

**Intuición en frecuencias.** La derivada multiplica cada componente por su frecuencia. El ruido es de alta frecuencia y los bordes reales son de frecuencia más baja, así que el ruido sale amplificado.

**La solución:** suavizar antes. Y por la asociatividad de la convolución (apunte 02):

$$\frac{\partial}{\partial x}(I * G_\sigma) = I * \frac{\partial G_\sigma}{\partial x}$$

Desenfocar y después derivar es convolucionar **una sola vez** con la *derivada de una gaussiana*.

Tu respuesta del diagnóstico ("desenfocar me suena contraproducente para buscar bordes") era razonable a primera vista y es justo lo contrario. Lo vas a ver con tus ojos en el notebook.

## 4. Sobel

$$S_x = \begin{bmatrix}-1 & 0 & 1\\ -2 & 0 & 2\\ -1 & 0 & 1\end{bmatrix} = \begin{bmatrix}1\\2\\1\end{bmatrix}\begin{bmatrix}-1 & 0 & 1\end{bmatrix}$$

Es **separable**:
- una **diferencia central** en x, `[−1, 0, 1]`;
- un **suavizado** en y, `[1, 2, 1]`, que es una gaussiana chiquita.

Es una derivada de gaussiana barata. Sy es la transpuesta.

**Escala.** Sobre una rampa de pendiente 1 por píxel, Sx da **8**: el suavizado suma 1 + 2 + 1 = 4, y la diferencia central abarca 2 píxeles. No importa para detectar bordes (los umbrales son relativos), pero sí si querés el valor de la derivada: dividí por 8.

**Signos con la y hacia abajo.** gx > 0 donde la imagen se aclara hacia la derecha y gy > 0 donde se aclara **hacia abajo**.

## 5. Magnitud y orientación

$$\|\nabla I\| = \sqrt{g_x^2 + g_y^2}, \qquad \theta = \operatorname{atan2}(g_y, g_x)$$

- La magnitud dice **cuánto** cambia: es la "fuerza" del borde.
- θ dice **hacia dónde** crece la intensidad. **El borde va perpendicular a θ.**
- Como la y va hacia abajo, los ángulos crecen en sentido **horario** en pantalla.

## 6. Dónde está exactamente el borde

El borde está donde ‖∇I‖ es **máximo** en la dirección del gradiente. En una dimensión: donde la primera derivada es máxima, y eso pasa donde la **segunda derivada cruza el cero**.

Tu intuición del diagnóstico ("donde la derivada es 0") era correcta para la **segunda** derivada. Los detectores basados en el *Laplaciano de gaussiana* (LoG) buscan exactamente esos cruces por cero. Canny (apunte 04) busca los máximos de la primera derivada. Son dos caminos al mismo lugar.

## 7. En la cancha: una línea de cal no es un borde, son dos

Una línea de cal es una franja **clara y angosta** sobre pasto oscuro. El perfil de intensidad a través de la línea sube y después baja. El gradiente tiene **dos picos**:
- uno al entrar en la línea (gradiente apuntando hacia la línea);
- otro al salir (gradiente apuntando hacia afuera).

Canny te va a devolver **dos bordes paralelos** por cada línea, y Hough (apunte 04) puede encontrar **dos rectas** casi iguales. La línea real está en el medio.

Otra forma de verlo: la línea es un "valle" o una "cresta" de la intensidad, y se puede buscar directamente con detectores de *ridges*. Lo mencionamos para que no te sorprenda; en el TP alcanza con saberlo.

---

## Resumen para volver

- **Parcial:** derivar en una variable con la otra fija. **Gradiente:** el vector de parciales.
- `D_u f = ∇f · u`: máximo crecimiento en la dirección ∇f, de tamaño ‖∇f‖. El gradiente es ⊥ a las curvas de nivel (y al borde).
- **Regla de la cadena:** `d/dw (wx − y)² = 2(wx − y)x`. Es la base de entrenar modelos (U3, U6).
- Derivar = convolucionar con `[−1, 0, 1]/2`. **Amplifica el ruido:** hay que suavizar antes (derivada de gaussiana).
- **Sobel** = diferencia central ⊗ suavizado `[1, 2, 1]`. Separable. Escala ×8.
- Magnitud = fuerza del borde. θ = atan2(gy, gx); el borde es ⊥ a θ. La y va hacia abajo.
- Borde = máximo de la primera derivada = cruce por cero de la segunda.
- Una línea de cal da **dos** bordes paralelos.
