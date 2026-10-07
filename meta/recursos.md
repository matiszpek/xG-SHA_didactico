# Recursos

Ordenados por unidad. Cuando un video está en un canal y no tiene link directo, se busca por el **título exacto** dentro del canal.

## Canales y cursos (los que se usan en toda la materia)

| Recurso | Para qué | Link |
|---|---|---|
| **3Blue1Brown** | Intuición geométrica: álgebra, cálculo, probabilidad, redes | [canal](https://www.youtube.com/@3blue1brown) · [3blue1brown.com](https://www.3blue1brown.com/) |
| **First Principles of Computer Vision** (Shree Nayar, Columbia) | El "libro en video" de visión clásica: videos cortos por tema | [canal](https://www.youtube.com/@firstprinciplesofcomputerv3258) · [sitio con monografías](https://fpcv.cs.columbia.edu/) |
| **Cyrill Stachniss** (Bonn) | Clases completas de fotogrametría y visión, más densas | [canal](https://www.youtube.com/@CyrillStachniss) · [Photogrammetry I & II (playlist 2015/16)](https://www.youtube.com/playlist?list=PLgnQpQtFTOGRsi5vzy9PiQpNWHjq-bKN1) · [temario](https://www.ipb.uni-bonn.de/photogrammetry-i-ii/) |
| **CS231n** (Stanford) | Deep learning para visión | [notas del curso](https://cs231n.github.io/) |
| **Neural Networks: Zero to Hero** (Karpathy) | Backprop desde cero, programando | [karpathy.ai/zero-to-hero](https://karpathy.ai/zero-to-hero.html) |

## Libros

| Libro | Uso | Acceso |
|---|---|---|
| Szeliski, *Computer Vision: Algorithms and Applications*, 2.ª ed. | Referencia general | [szeliski.org/Book](https://szeliski.org/Book/) (PDF gratis para uso personal) |
| Hartley & Zisserman, *Multiple View Geometry*, 2.ª ed. | Geometría (U4), cap. 4 sobre todo | Biblioteca / compra |
| *Dive into Deep Learning* | Deep learning en PyTorch (U6–U7) | [d2l.ai](https://d2l.ai/) |

---

## Por unidad

### U0 — NumPy para imágenes
- NumPy: [Indexing](https://numpy.org/doc/stable/user/basics.indexing.html) · [Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html) · [Copies and views](https://numpy.org/doc/stable/user/basics.copies.html)
- OpenCV: [Getting Started with Videos](https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html)

### U1 — Álgebra lineal geométrica
- **3Blue1Brown — [Essence of Linear Algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab)**, caps. 1–15 (el 16, espacios vectoriales abstractos, es opcional).
- Stachniss, Photogrammetry I: clases **11 (Geometric Transformations on Images)** y **15 (Homogeneous Coordinates)**.
- MIT 18.06, Gilbert Strang ([OpenCourseWare](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/)): clases **15 (Projections onto Subspaces)**, **16 (Projection Matrices and Least Squares)** y **29 (Singular Value Decomposition)**.
- Steve Brunton ([canal](https://www.youtube.com/@Eigensteve)), serie *Singular Value Decomposition*: los primeros videos (*Overview*, *Mathematical Overview*).

### U2 — La imagen como señal
- First Principles of CV, Módulo 1: *Image Formation*, *Image Processing I* e *Image Processing II*. Módulo 2: *Edge Detection*.
- 3Blue1Brown: *But what is a convolution?*
- Stachniss, Photogrammetry I: clases **4 (Histograms and Point Operators)**, **9 (Local Operators)** y **12 (Edge Detection)**.
- Cálculo multivariable: [Khan Academy, Multivariable calculus](https://www.khanacademy.org/math/multivariable-calculus) (los videos de derivadas parciales y gradiente los da Grant Sanderson, el de 3Blue1Brown).
- Szeliski, cap. 3 (Image processing) y sec. 7.2 (Edges and contours).

### U3 — Probabilidad + primer modelo
- [Seeing Theory](https://seeing-theory.brown.edu/) (Brown): caps. 1–3 y 5.
- 3Blue1Brown: *Bayes theorem, the geometry of changing beliefs*.
- [StatQuest](https://www.youtube.com/@statquest): *The Normal Distribution*, *Maximum Likelihood, clearly explained*, la serie de *Logistic Regression*.
- Datos: [StatsBomb Open Data](https://github.com/statsbomb/open-data) (uso no comercial con atribución).
- *xG Philosophy*, James Tippett.

### U4 — Geometría de la cámara
- Stachniss, Photogrammetry I: clases **15 (Homogeneous Coordinates)**, **16 (Camera Extrinsics and Intrinsics)** y **17 (Camera Orientation)**.
- First Principles of CV: *Camera Calibration* (Módulo 4) e *Image Stitching* (Módulo 2, homografía + RANSAC).
- Hartley & Zisserman, cap. 4 (*Estimation – 2D Projective Transformations*: DLT, normalización, RANSAC).
- Szeliski, sec. 2.1 (transformaciones geométricas) y cap. 8 (alineamiento de imágenes).

### U5 — Features y movimiento
- First Principles of CV: *SIFT Detector* (Módulo 2) y *Optical Flow* (Módulo 4).
- Stachniss, Photogrammetry I: clases **10 (Matching)** y **13 (Förstner Operator)**.
- Szeliski, caps. 7 y 9.

### U6 — Redes neuronales desde cero
- 3Blue1Brown, serie *Neural networks* (caps. 1–4).
- Karpathy: *The spelled-out intro to neural networks and backpropagation: building micrograd* ([repo micrograd](https://github.com/karpathy/micrograd)).
- [CS231n notas](https://cs231n.github.io/): optimización, backprop, redes convolucionales.
- [PyTorch — Learn the Basics](https://pytorch.org/tutorials/beginner/basics/intro.html).
- d2l.ai, caps. de MLP, CNN y CNN modernas (ResNet).
- Paper: He et al., *Deep Residual Learning for Image Recognition* (ResNet), [arXiv:1512.03385](https://arxiv.org/abs/1512.03385).

### U7 — Detección
- d2l.ai, cap. *Computer Vision*: cajas, *anchors*, NMS, detección.
- Redmon et al., *You Only Look Once* (YOLO), [arXiv:1506.02640](https://arxiv.org/abs/1506.02640).
- [Documentación de Ultralytics](https://docs.ultralytics.com/): entrenamiento, validación, métricas.

### U8 — Tracking y re-identificación
- [How a Kalman filter works, in pictures](https://www.bzarg.com/p/how-a-kalman-filter-works-in-pictures/) (bzarg).
- Stachniss, Photogrammetry II: clase **30 (Linear, Extended, and Unscented Kalman Filter)**.
- First Principles of CV: *Object Tracking* (Módulo 5).
- Papers:
  - SORT, [arXiv:1602.00763](https://arxiv.org/abs/1602.00763)
  - DeepSORT, [arXiv:1703.07402](https://arxiv.org/abs/1703.07402)
  - ByteTrack, [arXiv:2110.06864](https://arxiv.org/abs/2110.06864)
  - HOTA, [arXiv:2009.07736](https://arxiv.org/abs/2009.07736)
- [TrackEval](https://github.com/JonathonLuiten/TrackEval): métricas estándar de tracking.

### U9 — Estado del arte
- Papers:
  - ViT, [arXiv:2010.11929](https://arxiv.org/abs/2010.11929)
  - CLIP, [arXiv:2103.00020](https://arxiv.org/abs/2103.00020)
  - SAM, [arXiv:2304.02643](https://arxiv.org/abs/2304.02643)
  - DINOv2, [arXiv:2304.07193](https://arxiv.org/abs/2304.07193)
- SoccerNet Game State Reconstruction, [arXiv:2404.11335](https://arxiv.org/abs/2404.11335) (CVPRW 2024).
- Keshav, *How to Read a Paper* (3 páginas, el método de las tres pasadas).
