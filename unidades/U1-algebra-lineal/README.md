# U1 — Álgebra lineal geométrica

**Sesiones:** 7 (~14 h, más el TP) · **TP:** TP1 → `mv/geometria.py`

## Por qué esta unidad

El diagnóstico fue claro: **sé hacer las cuentas, pero no veo qué significan**. Y en visión el álgebra lineal es geometría pura:
- una cámara es una matriz que proyecta el mundo en la imagen;
- la homografía cámara → cancha es una matriz de 3×3;
- un filtro de Kalman propaga gaussianas con matrices;
- una red neuronal es una cadena de matrices con no linealidades en el medio.

Si no **veo** lo que hace una matriz, todo eso son fórmulas de memoria.

Esta unidad además coincide con Álgebra en la facu: lo que veas acá te sirve allá y al revés.

## Objetivos

Al terminar U1 puedo, sin buscar:
1. Mirar una matriz de 2×2 y **dibujar** lo que le hace al plano: las columnas son a dónde van los vectores base.
2. Explicar el determinante como **factor de área** y conectar det = 0 ⟺ aplasta el espacio ⟺ no invertible ⟺ `Ax = 0` tiene solución no trivial.
3. Componer transformaciones y saber en qué orden se aplican.
4. Usar **coordenadas homogéneas** para escribir traslaciones (y, en U4, perspectivas) como matrices de 3×3.
5. Calcular e interpretar **autovalores y autovectores**.
6. Plantear y resolver un problema de **cuadrados mínimos**, y explicar la solución como una **proyección**.
7. Explicar la **SVD** como rotación · estiramiento · rotación, y usarla para resolver `min ‖Ax‖` con `‖x‖ = 1`. Ese es *el* truco de la homografía en U4.

## Plan

Los capítulos son de [Essence of Linear Algebra (3Blue1Brown)](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab).

| Sesión | Videos | Apunte | Práctica |
|---|---|---|---|
| **1** | Caps. 1–2: *Vectors*, *Linear combinations, span, and basis vectors* | [01 · Vectores y bases](apuntes/01-vectores.md) | Guía A |
| **2** | Caps. 3–4: *Linear transformations and matrices*, *Matrix multiplication as composition* (cap. 5, 3D, opcional) | [02 · Matrices como transformaciones](apuntes/02-transformaciones.md) | Guía B |
| **3** | Caps. 6–8: *The determinant*, *Inverse matrices, column space and null space*, *Nonsquare matrices* | [03 · Determinante, inversa y espacios](apuntes/03-determinante-inversa.md) | Guía C |
| **4** | Caps. 9 y 13: *Dot products and duality*, *Change of basis* + Stachniss, clase 15 (*Homogeneous Coordinates*), primeros ~30 min | [04 · Producto escalar y coordenadas homogéneas](apuntes/04-producto-escalar-homogeneas.md) | Guía D + **TP1, parte A** |
| **5** | Caps. 14–15: *Eigenvectors and eigenvalues*, *A quick trick for computing eigenvalues* | [05 · Autovectores](apuntes/05-autovectores.md) | Guía E + terminar TP1 A |
| **6** | MIT 18.06 (Strang), clases 15–16: *Projections onto subspaces*, *Projection matrices and least squares* | [06 · Cuadrados mínimos](apuntes/06-cuadrados-minimos.md) | Guía F |
| **7** | MIT 18.06, clase 29: *Singular value decomposition* (o Brunton, *SVD Overview* + *Mathematical Overview*) | [07 · SVD](apuntes/07-svd.md) | Guía G + **TP1, parte B** |

Los videos de 3Blue1Brown hay que verlos **pausando**: cuando él pregunta "¿a dónde va este vector?", pará y respondé antes de que lo muestre.

Strang es una clase de pizarrón de MIT de 50 minutos. Se puede ver a 1,25×.

## Guía y TP

- [Guía de ejercicios](guia.md): bloques A–G, uno por sesión, con respuestas al pie.
- [TP1 — Geometría de la imagen](tp1/enunciado.md): transformaciones y *warp* con interpolación (parte A), y ajuste de rectas de la cancha (parte B).
