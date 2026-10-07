# U8 — Tracking y re-identificación

**Sesiones:** 5 · **TP:** TP8 → `mv/tracking.py` · **Estado:** 📋 ficha

## Por qué
Sin identidad persistente no hay estadísticas por jugador. Es el cuello de botella del proyecto anterior: 103 IDs para 22 jugadores en 90 segundos.

En el diagnóstico propusiste **proximidad + embeddings**. Es la idea de DeepSORT. Te faltaban dos piezas, que son el corazón de esta unidad:
- **predecir** dónde va a estar cada jugador (Kalman);
- asignar **globalmente y uno a uno** (algoritmo húngaro).

## Objetivos
1. El problema de asociación de datos. Matriz de costos (el truco de broadcasting de U0).
2. **Filtro de Kalman**: estado, predicción y corrección, todo con gaussianas multivariadas (U3) y matrices (U1). Derivar las ecuaciones entendiendo cada término.
3. **Algoritmo húngaro** (asignación óptima uno a uno).
4. SORT → DeepSORT → ByteTrack: qué agrega cada uno y por qué.
5. *Embeddings* de apariencia y re-ID. Similitud coseno. Límites con camisetas iguales y resolución baja.
6. Separar equipos por *clustering* (K-means en Lab/HSV, **estandarizando** las *features*).
7. Métricas de tracking: MOTA, IDF1 y **HOTA**. Qué mide cada una y cuál engaña.

## Contenidos y recursos por sesión

| Sesión | Contenido | Recursos |
|---|---|---|
| 1 | Asociación, matriz de costos, algoritmo húngaro | Paper de SORT (Bewley 2016) |
| 2 | Filtro de Kalman 1D y después 2D con velocidad constante | bzarg, *How a Kalman filter works, in pictures* · Stachniss, clase 30 |
| 3 | SORT completo. ByteTrack (asociar también las detecciones de baja confianza) | Papers de SORT y ByteTrack · First Principles of CV: *Object Tracking* |
| 4 | Apariencia: *embeddings*, coseno, DeepSORT. K-means para equipos | Paper de DeepSORT |
| 5 | Métricas: MOTA, IDF1, HOTA. TrackEval | Paper de HOTA · TrackEval |

## TP8 (borrador)
`mv/tracking.py`:
- `KalmanCV` (velocidad constante)
- `matriz_costos`
- `asignar` (el húngaro, usando `scipy.optimize.linear_sum_assignment` **después** de haber implementado una versión simple)
- `TrackerSORT`
- `equipos_kmeans`

Notebook:
- un clip real con *ground truth* etiquetado a mano (un minuto, a 5 fps);
- medir HOTA e IDF1 de tu tracker, con y sin Kalman y con y sin la restricción de equipo;
- analizar **por qué** se corta cada track: mirando frames, no solo el número.

## Conexión con el producto
Es el problema más difícil del producto. Entenderlo a fondo es lo que va a permitir decidir con criterio (en la versión producto) cuánto automatizar y cuánto resolver con un humano corrigiendo.
