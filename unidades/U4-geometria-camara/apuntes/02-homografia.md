# 02 · La homografía: de la imagen a la cancha

> **La idea en una frase:** si todos los puntos que te interesan están sobre **un plano** (el césped), la cámara de 3×4 se reduce a una matriz de **3×3 invertible**, la homografía. Esa matriz permite ir y volver entre píxeles y metros.

**Videos:** First Principles of CV, *Image Stitching* (la parte de homografía). **Lectura:** Hartley & Zisserman, cap. 2 (las secciones 2.1–2.4 alcanzan).

---

## 1. De dónde sale

Elegí el mundo de forma que el césped sea el plano Z = 0. Para un punto del césped:

$$P\begin{bmatrix}X\\Y\\0\\1\end{bmatrix} = \big[\,\mathbf p_1\ \ \mathbf p_2\ \ \mathbf p_3\ \ \mathbf p_4\,\big]\begin{bmatrix}X\\Y\\0\\1\end{bmatrix} = \big[\,\mathbf p_1\ \ \mathbf p_2\ \ \mathbf p_4\,\big]\begin{bmatrix}X\\Y\\1\end{bmatrix}$$

La tercera columna se multiplica por 0 y desaparece. Lo que queda es una matriz de 3×3:

$$\mathbf x \simeq H\,\begin{bmatrix}X\\Y\\1\end{bmatrix}, \qquad H = [\,\mathbf p_1\ \mathbf p_2\ \mathbf p_4\,]$$

**Eso es la homografía.** Lleva el plano de la cancha (en metros) al plano de la imagen (en píxeles). Y como en general es invertible, H⁻¹ va de la imagen a la cancha: **de un píxel a una posición en metros**. Es `homografia_desde_camara` del TP4.

## 2. Ocho grados de libertad

H tiene 9 números, pero `H` y `5·H` hacen lo mismo: dividen por W, y la escala se cancela (lo testeaste en el TP1). Así que tiene **8 grados de libertad**, y por eso hacen falta **4 puntos** (cada uno da 2 ecuaciones, x e y) para determinarla.

## 3. Qué conserva y qué no

| Se conserva | No se conserva |
|---|---|
| Rectas (siguen rectas) | Paralelismo: las laterales se juntan |
| Que un punto esté sobre una recta | Ángulos: las esquinas del área no se ven a 90° |
| La razón doble (*cross-ratio*) de 4 puntos alineados | Distancias y razones de distancias: 10 m cerca y 10 m lejos ocupan distinta cantidad de píxeles |

Por eso la cancha se ve como un **trapecio** y no como un rectángulo. Y por eso "corrió 300 píxeles" no significa nada: hay que pasar a metros con H⁻¹.

**Jerarquía de transformaciones** (de U1 hasta acá):

| Transformación | Grados de libertad | Qué conserva |
|---|---|---|
| Traslación | 2 | todo menos la posición |
| Euclídea (rotación + traslación) | 3 | distancias |
| Similitud (+ escala) | 4 | ángulos, razones de distancias |
| Afín (matriz 2×2 cualquiera + traslación) | 6 | paralelismo, razones sobre una recta |
| **Proyectiva (homografía)** | **8** | rectas, razón doble |

## 4. El supuesto que no hay que olvidar: todo está en el plano

H solo es correcta para puntos **sobre el césped**:
- **Los pies del jugador** (el borde inferior de su caja) están en el plano: H⁻¹ da su posición en metros.
- **La cabeza** no: a 1,75 m de altura, H⁻¹ la ubica en otro lugar de la cancha, más lejos de la cámara. Siempre se usa el **punto inferior central** de la caja.
- **La pelota en el aire** tampoco. Con una sola cámara no hay cómo saber su altura (apunte 01), así que su posición en metros es incorrecta mientras vuela.

## 5. Cámara fija contra cámara que panea

- **Cámara fija:** **una sola H para todo el partido**. Se calibra una vez y listo.
- **Cámara que panea** (el stream del club): R cambia en cada frame, así que **H cambia en cada frame**. Hace falta:
  1. calibrar algunos frames clave (*keyframes*);
  2. **propagar** H entre ellos, estimando el movimiento de cámara entre frames (U5).

  Esa propagación fue el cuello de botella del proyecto anterior: 2 de 8 *keyframes* usables y una propagación que solo era confiable hasta ~12 frames.

Esta diferencia es una de las razones por las que la cantidad y el tipo de cámaras es una decisión central de la versión producto.

## 6. Bonus: homografía entre dos imágenes de la misma cámara que rota

Si la cámara **solo rota** (no se traslada), dos imágenes se relacionan con una homografía `H = K R K⁻¹`, **para todos los puntos**, estén o no en un plano. Por eso se pueden "coser" panorámicas, y por eso el paneo de la cámara del club entre dos frames se modela como una homografía (U5).

---

## Resumen para volver

- Puntos del plano Z = 0: P se reduce a **H = [p₁ p₂ p₄]** (3×3, invertible). H: cancha → imagen y H⁻¹: imagen → cancha.
- **8 grados de libertad** (la escala no importa): hacen falta **4 puntos**.
- Conserva rectas; **no** conserva paralelismo, ángulos ni distancias.
- Solo vale para puntos **en el plano**: usar los **pies**. La pelota en el aire queda mal ubicada.
- Cámara fija: una H. Cámara que panea: una H por frame (U5).
- Cámara que solo rota: `H = K R K⁻¹` entre imágenes.
