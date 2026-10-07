# Decisiones sobre la materia

Decisiones de diseño de la materia, con su porqué. Si en algún momento algo no cierra, se revisa acá y se cambia.

## M1. Materia completa, no un tutorial (2026-10-06)
Programa de grado: teoría, matemática, implementación y estado del arte. El objetivo es entender, no solo hacer andar algo. Es independiente de la facultad y de la versión producto.

## M2. Ritmo flexible, medido en sesiones (2026-10-06)
Dedicación de entre 2 y 4 h por semana. Por eso el programa se cuenta en **sesiones de ~2 h** (44 en total) y no en semanas. A 2 h por semana son ~10 meses; a 4 h, ~5.

## M3. Sin parciales (2026-10-06)
La evaluación es por TPs bien armados (tests + informe + coloquio) y un trabajo final. Los TPs dejan **implementaciones reales y reutilizables** en `mv/` y apuntes para volver a consultar.

## M4. NumPy primero, librerías después (2026-10-06)
Todo algoritmo se implementa primero a mano en NumPy. OpenCV, scikit-learn o PyTorch se usan después, para comparar o cuando lo propio ya está entendido. Excepción: herramientas de E/S (leer video, mostrar imágenes).

## M5. PyTorch para deep learning (2026-10-06)
Para U6–U9 se usa **PyTorch** y no TensorFlow/Keras.
- **Investigación:** ~85 % de los papers de deep learning en conferencias top usan PyTorch.
- **Ecosistema de visión:** Ultralytics/YOLO, SoccerNet, *trackers*, timm y Hugging Face Transformers son PyTorch. Transformers v5 (dic 2025) dejó TensorFlow y Flax para quedarse solo con PyTorch.
- **Didáctica:** en PyTorch el *training loop* se escribe a mano (*forward*, *loss*, *backward*, *step*). Eso deja a la vista exactamente la mecánica que el diagnóstico mostró floja. Keras la esconde detrás de `fit()`.
- **Lo que se pierde:** el *deployment* móvil y edge de TensorFlow es más maduro. No importa para esta materia, y para el producto se resuelve exportando a ONNX si hace falta.
- Lo que sé de Keras sigue sirviendo: los conceptos (capas, pérdida, optimizador, epochs) son los mismos.

## M6. Material escrito una unidad por delante (2026-10-06)
U0 y U1 completas desde el arranque. Del resto, ficha con objetivos, contenidos, recursos y TP. El material completo de la unidad N+1 se escribe al empezar la N, para adaptarlo a cómo vengo.

## M7. Siempre sobre material propio (2026-10-06)
Los TPs usan frames de partidos de Hebraica (canal de YouTube del club) siempre que se pueda. Cuando no hay datos reales a mano, `mv/datos.py` genera un frame sintético para poder trabajar igual.
