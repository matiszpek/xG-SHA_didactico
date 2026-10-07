# Diagnóstico inicial — octubre 2026

Hecho antes de armar el programa. Son 5 bloques de preguntas, respondidos sin buscar nada y sin IA. Sirve para saber desde dónde arranco y, al final de la materia, para comparar.

## Resumen

| Área | Estado | Qué implica en el programa |
|---|---|---|
| Álgebra lineal | 🟡 Sé hacer las cuentas (Gauss, determinantes, inversas), pero no veo la geometría | U1 completa, prioridad alta. Coincide con la cursada de Álgebra |
| Cálculo | 🟢 Una variable · 🔴 multivariable | Mini-módulo dentro de U2 (gradiente, regla de la cadena) |
| Probabilidad y estadística | 🔴 Casi desde cero, con buena intuición | U3 completa |
| Python | 🟢 Sólido | — |
| NumPy | 🟡 Conceptos de arrays flojos: shape, axis, broadcasting, vistas, dtypes | U0 |
| ML / DL | 🟡 Buen vocabulario e intuición; la mecánica, floja | U6 desde cero |
| Visión | 🔴 Teoría · 🟢 muy buen sentido común | La materia entera |

**El patrón, presente en los 5 bloques:** sé el *qué* y el *para qué*; me falta el *cómo* y el *por qué*.

## Detalle por bloque

### 1. Álgebra lineal y cálculo
- ✅ Determinante ≠ 0 ⟺ invertible; Gauss-Jordan; derivada de un producto; `AB ≠ BA`.
- ❌ Qué hace geométricamente una matriz. No sabía que las columnas son a dónde van los vectores base.
- ❌ Qué significa el determinante (el factor de escala de las áreas).
- ❌ Autovalores y autovectores. ❌ Cuadrados mínimos. ❌ SVD.
- 🟡 Coordenadas homogéneas: "posición en el espacio". Falta saber para qué sirven: escribir traslaciones y perspectivas como matrices.
- ❌ Gradiente. ❌ No reconocí `d/dw (wx − y)² = 2(wx − y)x`, que es la regla de la cadena.
- 🟡 Descenso por gradiente: la intuición está, pero confundía "punto de inflexión" con mínimo y creía que "prueba puntos".

### 2. Probabilidad y estadística
- ✅ P(6) = 1/6. ✅ Media y mediana. ✅ Correlación no implica causalidad (variable de confusión).
- ✅ **Sumar los xG de los tiros da los goles esperados**: es la linealidad de la esperanza, usada sin saberlo.
- ❌ "Al menos uno" se calcula con el complemento, no sumando probabilidades. ❌ P(0 goles) ≠ 1 − Σ xG.
- ❌ Bayes, varianza, densidad, gaussiana, covarianza, máxima verosimilitud.
- ❌ Correlación 0 no implica independencia.

### 3. Programación
- ✅ `x @ w`, indexado booleano, la idea de vectorizar.
- ❌ Shape de una imagen: es `(alto, ancho, 3)`, alto primero. ❌ `uint8`: 200 + 100 = 44 (da la vuelta, no satura).
- ❌ Un slice de NumPy es una **vista**. ❌ Broadcasting. ❌ `axis`. ❌ `*` frente a `@`.
- ❌ **Distancia recorrida = suma de las normas de las diferencias entre posiciones consecutivas.** Esto fue geometría, no sintaxis.
- Autoevaluación: git 3, venv 3, Jupyter 3, clases 2, debugger 2, OpenCV 1, PyTorch/Keras 2.

### 4. ML / DL
- ✅ Supervisado y no supervisado, overfitting y underfitting, accuracy engañosa con clases desbalanceadas, idea de *fine-tuning*.
- ❌ Puse las soluciones al revés: *data augmentation* combate el **over**fitting, y sacar datos lo empeora.
- ❌ Backprop *calcula gradientes*; el optimizador *actualiza*. Son cosas distintas.
- ❌ Sin activaciones no lineales, la red colapsa a una sola transformación lineal.
- ❌ *Data leakage*: frames consecutivos en train y en test. Hay que separar **por partido**.
- ❌ Cross-entropy, *pooling*, *batch norm*, ResNet. 🟡 Convolución.

### 5. Visión
- ✅ **Tracking por proximidad + embeddings**: es la idea de DeepSORT.
- ✅ **Las dificultades de la pelota**, incluida la ambigüedad de altura con una sola cámara.
- ✅ Homografía con 4 puntos (del proyecto anterior).
- ❌ HSV: el tono es estable frente a sol y sombra. ❌ Bordes: están donde la derivada es *grande*.
- ❌ Por qué desenfocar antes de derivar: la derivada amplifica el ruido.
- ❌ IoU. ❌ Optical flow.

## Para la evaluación final

Al terminar U9, repetir este diagnóstico con las **mismas preguntas** y comparar.
