# Programa — Machine Vision desde cero

**Modalidad:** autodidacta guiada. Claude escribe los apuntes, arma los TPs y los corrige.
**Dedicación:** flexible, entre 2 y 4 h por semana. El programa se mide en **sesiones de ~2 h**.
**Duración estimada:** 44 sesiones. Son unos 10 meses a 2 h por semana o unos 5 meses a 4 h por semana.
**Inicio:** octubre 2026.

---

## Objetivos

Al terminar la materia tengo que poder:

1. **Entender la matemática** que hay debajo de la visión por computadora: álgebra lineal, cálculo, probabilidad y optimización. Y verla **geométricamente**, no solo hacer las cuentas.
2. **Implementar desde cero** los algoritmos clásicos: convolución, detección de bordes, homografía con RANSAC, flujo óptico, filtro de Kalman, backpropagation, un tracker.
3. **Entrenar, evaluar y ajustar** modelos de deep learning para detección, con las métricas correctas y sin hacer trampa con los datos.
4. **Leer el estado del arte** (papers, repos) y saber qué problema resuelve cada cosa y qué supone.
5. **Tener una librería propia** (`mv/`), testeada, con todo lo implementado, y un trabajo final que la use sobre video real.

## Principios

- **Primero a mano, después la librería.** Algo se usa de OpenCV o PyTorch recién cuando ya se implementó y se entendió.
- **Siempre sobre imágenes reales.** Cada unidad, incluso las de matemática, tiene un TP sobre frames de partidos.
- **El "por qué" antes que el "cómo".** El diagnóstico mostró que sé el *qué* y el *para qué*, y que me falta el *cómo* y el *por qué*. La materia apunta ahí.
- **Material para volver.** Los apuntes están escritos para releerse meses después, y cada uno termina con un resumen.

---

## Unidades

| # | Unidad | Sesiones | TP (va a `mv/`) |
|---|---|---|---|
| U0 | Herramientas: NumPy para imágenes | 2 | `imagen.py`, `cinematica.py`: anatomía de un frame y trayectorias |
| U1 | Álgebra lineal geométrica | 7 | `geometria.py`: transformaciones, *warp* con interpolación, ajuste de rectas |
| U2 | La imagen como señal | 4 | `filtros.py`: convolución, gaussiano, Sobel, Canny, líneas de cancha |
| U3 | Probabilidad + primer modelo | 5 | `prob.py`, `xg.py`: modelo de xG por máxima verosimilitud |
| U4 | Geometría de la cámara | 5 | `camara.py`: DLT normalizado + RANSAC, homografía cámara→cancha |
| U5 | Features y movimiento | 3 | `features.py`: Harris, *matching*, Lucas-Kanade, movimiento de cámara |
| U6 | Redes neuronales desde cero | 6 | `nn/`: autograd mínimo, MLP, CNN en PyTorch |
| U7 | Detección | 4 | `deteccion.py`: IoU, NMS, mAP; *fine-tuning* de YOLO |
| U8 | Tracking y re-identificación | 5 | `tracking.py`: Kalman + húngaro (SORT), equipos por K-means |
| U9 | Estado del arte + trabajo final | 3 | Pipeline sobre un clip real |
| | **Total** | **44** | |

### U0 — Herramientas: NumPy para imágenes (2 sesiones)
Una imagen es un array `(H, W, C)`. Contenidos:
- Shapes y ejes, y el orden `(fila, columna)` frente a `(x, y)`.
- `dtype` y overflow de `uint8`.
- Vistas frente a copias.
- Broadcasting.
- Reducciones con `axis`.
- Máscaras booleanas y vectorización.
- Leer video con OpenCV (BGR, fps, índices de frame).

**TP0:** anatomía de un frame (canales, grises, recortes, histogramas, máscara de pasto, mosaico) y cinemática de trayectorias.

### U1 — Álgebra lineal geométrica (7 sesiones)
Contenidos:
- Vectores, combinaciones lineales, span y bases.
- **Matrices como transformaciones**: las columnas son a dónde van los vectores base.
- Composición, determinante (factor de área), inversa, rango, espacio columna y espacio nulo.
- Producto escalar y proyección. Cambio de base.
- **Coordenadas homogéneas** y transformaciones afines.
- Autovalores y autovectores.
- **Cuadrados mínimos** (ecuaciones normales, proyección).
- **SVD** y cuadrados mínimos totales.

**TP1:**
- Transformaciones 2D sobre puntos e imágenes: rotar, escalar y deformar con *inverse mapping* + interpolación bilineal.
- Ajustar rectas de la cancha por cuadrados mínimos ordinarios y totales.
- Ver por qué los ordinarios fallan con rectas casi verticales.

### U2 — La imagen como señal (4 sesiones)
Contenidos:
- Formación de imagen (lo mínimo).
- Espacios de color: RGB, HSV, Lab.
- Histogramas y operadores puntuales.
- **Convolución** y su relación con la correlación. Bordes y *padding*.
- Filtros: promedio, gaussiano, mediana.
- **Cálculo multivariable mínimo**: derivadas parciales, gradiente, regla de la cadena.
- Gradiente de imagen, Sobel, Canny.
- Transformada de Hough (introducción).

**TP2:**
- Convolución 2D desde cero, vectorizada.
- Pipeline de bordes.
- Detectar las líneas de la cancha en un frame real.
- Máscara de pasto en HSV.

### U3 — Probabilidad + primer modelo (5 sesiones)
Contenidos:
- Probabilidad condicional, independencia, **Bayes**.
- Variables aleatorias, esperanza y varianza, linealidad de la esperanza.
- Distribuciones: Bernoulli, binomial, normal.
- **Gaussiana multivariada** y matriz de covarianza.
- **Máxima verosimilitud**.
- Regresión logística como modelo probabilístico. Cross-entropy = log-verosimilitud negativa.
- Descenso por gradiente.
- Evaluación: *log loss*, AUC, calibración.
- *Data leakage* y splits por partido.

**TP3:**
- Modelo de **xG desde cero** en NumPy (regresión logística entrenada por máxima verosimilitud) con StatsBomb Open Data.
- Validado y calibrado.
- Aplicado a tiros de Hebraica marcados a mano.

### U4 — Geometría de la cámara (5 sesiones)
Contenidos:
- Modelo *pinhole* y proyección perspectiva.
- Parámetros intrínsecos y extrínsecos.
- **Homografía** plano a plano.
- **DLT** (cuadrados mínimos homogéneos con SVD) y normalización de Hartley.
- Errores algebraico y geométrico. Error de reproyección.
- **RANSAC** (y por qué funciona, con probabilidad).
- Por qué 4 puntos exactos no validan nada.

**TP4:**
- Homografía cámara → cancha desde cero sobre un frame de Hebraica.
- Proyectar jugadores a la vista 2D de la cancha.
- Estudiar la estabilidad según la cantidad de puntos y su ubicación.

### U5 — Features y movimiento (3 sesiones)
Contenidos:
- Esquinas: Harris, a partir de los autovalores del tensor de estructura.
- Descriptores (idea de SIFT y ORB) y *matching*.
- **Flujo óptico** (Lucas-Kanade) y la ecuación de restricción de brillo.
- Chequeo *forward-backward*.
- Movimiento de cámara entre frames.

**TP5:**
- Estimar el paneo de la cámara entre frames consecutivos.
- Medir hasta qué distancia temporal la estimación es confiable. Sobre césped falla en silencio.

### U6 — Redes neuronales desde cero (6 sesiones)
Contenidos:
- Neurona, MLP y por qué hace falta la no linealidad.
- Funciones de pérdida: MSE y cross-entropy.
- **Backpropagation** como regla de la cadena sobre un grafo.
- Optimizadores: SGD, *momentum*, Adam.
- Regularización: *weight decay*, *dropout*, *data augmentation*, *early stopping*.
- Train/val/test.
- **CNN**: convolución aprendida, *pooling*, campo receptivo.
- Arquitecturas: LeNet → VGG → **ResNet**. *Batch normalization*.
- **Transfer learning** y *fine-tuning*. **PyTorch**.

**TP6:**
- *Autograd* mínimo en NumPy (estilo micrograd) y MLP entrenado con él.
- Después, CNN en PyTorch que clasifique recortes en jugador, árbitro, pelota o fondo.
- Comparar el entrenamiento desde cero con el *fine-tuning*.

### U7 — Detección (4 sesiones)
Contenidos:
- De la ventana deslizante a los detectores de una etapa.
- *Anchors* frente a *anchor-free*.
- **IoU**, **NMS**.
- **Precision-recall**, **AP / mAP**.
- YOLO por dentro.
- Datasets y anotación.
- *Fine-tuning* sobre material propio.
- Errores típicos: resolución de inferencia, dominio, objetos chicos.

**TP7:**
- IoU, NMS y mAP implementados a mano.
- Evaluar un YOLO preentrenado sobre frames etiquetados del club.
- *Fine-tunearlo* y medir la mejora por tamaño de objeto.

### U8 — Tracking y re-identificación (5 sesiones)
Contenidos:
- El problema de asociación de datos.
- **Filtro de Kalman**: predicción y corrección, con gaussianas.
- **Algoritmo húngaro**.
- SORT → DeepSORT → ByteTrack.
- *Embeddings* de apariencia y re-ID.
- Separación de equipos por *clustering* (K-means en HSV/Lab, estandarizando).
- Métricas: MOTA, IDF1, **HOTA**.

**TP8:**
- Tracker estilo SORT desde cero.
- Asignación de equipos.
- Medir la fragmentación en un clip real con métricas estándar.

### U9 — Estado del arte + trabajo final (3 sesiones)
Contenidos:
- *Transformers* y ViT.
- Modelos fundacionales: CLIP, DINOv2, SAM.
- SoccerNet y *Game State Reconstruction*.
- Cómo leer un paper.

**Trabajo final:** pipeline didáctico sobre un clip de 1 minuto.
- Detección → tracking → homografía → mapa de calor + distancia recorrida.
- Usando la librería `mv/` y un informe que diga honestamente qué anda y qué no.

---

## Evaluación

- **Sin parciales.** La materia se aprueba con los TPs.
- Cada TP tiene tres partes:
  1. **Tests automáticos** (`pytest`). Verifican que la implementación sea correcta. Son la primera corrección, no la única.
  2. **Informe en notebook**: experimentos, gráficos y respuestas a preguntas conceptuales.
  3. **Coloquio**: preguntas sobre mi propio código y mis resultados. Sirven para verificar que lo *entendí*, no solo que funciona.
- **Criterios:** correctitud, comprensión, claridad del código y honestidad del informe (decir qué no anda).
- El **trabajo final** integra todo.

## Bibliografía

**Libros principales:**
- Szeliski, *Computer Vision: Algorithms and Applications*, 2.ª ed. (2022). PDF gratis para uso personal en szeliski.org/Book.
- Hartley & Zisserman, *Multiple View Geometry in Computer Vision*, 2.ª ed. (2004). Es *la* referencia de geometría, para U4.
- Zhang, Lipton, Li & Smola, *Dive into Deep Learning* (d2l.ai). Gratis y en PyTorch, para U6–U7.

**Cursos en video:** 3Blue1Brown, First Principles of Computer Vision (Columbia, Shree Nayar), Cyrill Stachniss (Bonn), CS231n (Stanford), Andrej Karpathy.

La lista completa por unidad está en [`meta/recursos.md`](meta/recursos.md).
