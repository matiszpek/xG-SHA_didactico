# Glosario

Término en castellano, término en inglés (el que vas a encontrar en papers y código) y una definición corta. Se agregan términos a medida que aparecen.

| Castellano | Inglés | Definición corta | Unidad |
|---|---|---|---|
| arreglo / array | array | Bloque de números del mismo tipo con forma (`shape`) fija | U0 |
| forma | shape | Tupla con el tamaño de cada dimensión. Una imagen color es `(alto, ancho, 3)` | U0 |
| eje | axis | Una dimensión del array. Reducir sobre un eje lo "colapsa" | U0 |
| difusión | broadcasting | Regla de NumPy para operar arrays de shapes distintas, estirando las dimensiones de tamaño 1 | U0 |
| vista | view | Array que comparte memoria con otro: modificarlo modifica el original | U0 |
| desbordamiento | overflow | Cuando un valor no entra en el `dtype`. En `uint8`, 300 → 44 | U0 |
| transformación lineal | linear transformation | Función que preserva sumas y escalados. Se representa con una matriz | U1 |
| determinante | determinant | Factor por el que una transformación multiplica las áreas (con signo) | U1 |
| autovector / autovalor | eigenvector / eigenvalue | Dirección que la transformación solo estira (por el autovalor), sin rotarla | U1 |
| coordenadas homogéneas | homogeneous coordinates | Agregar un 1 a `(x, y)` para escribir traslaciones y perspectivas como matrices | U1 |
| cuadrados mínimos | least squares | La "mejor" solución de un sistema sin solución exacta: minimiza ‖Ax − b‖² | U1 |
| descomposición en valores singulares | singular value decomposition (SVD) | A = UΣVᵀ: rotación · estiramiento · rotación | U1 |
| interpolación bilineal | bilinear interpolation | Estimar el valor entre píxeles promediando los 4 vecinos según la distancia | U1 |
| convolución | convolution | Deslizar un kernel por la imagen y, en cada posición, calcular una suma ponderada | U2 |
| gradiente | gradient | Vector de derivadas parciales. Apunta hacia donde la función crece más rápido | U2 |
| esperanza | expectation | Valor promedio ponderado por la probabilidad. El xG de un partido es una esperanza | U3 |
| máxima verosimilitud | maximum likelihood | Elegir los parámetros que hacen más probables los datos observados | U3 |
| homografía | homography | Matriz 3×3 que lleva un plano a otro en perspectiva (imagen ↔ cancha) | U4 |
| flujo óptico | optical flow | Cuánto se movió cada píxel entre dos frames | U5 |
| retropropagación | backpropagation | Calcular el gradiente de la pérdida respecto de cada peso con la regla de la cadena | U6 |
| fuga de datos | data leakage | Información del test que se filtra al entrenamiento e infla las métricas | U6 |
| intersección sobre unión | IoU | Área de intersección dividida por área de unión de dos cajas | U7 |
| supresión de no máximos | non-maximum suppression (NMS) | Quedarse con la mejor caja de un grupo de cajas solapadas | U7 |
| filtro de Kalman | Kalman filter | Estimador que predice y corrige el estado de algo con incertidumbre gaussiana | U8 |
| re-identificación | re-identification (re-ID) | Reconocer que un objeto que reaparece es el mismo que ya se había visto | U8 |
