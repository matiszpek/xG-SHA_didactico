# U6 — Redes neuronales desde cero

**Sesiones:** 6 · **TP:** TP6 → `mv/nn/` · **Estado:** 📋 ficha

## Por qué
El bloque 4 del diagnóstico mostró buen vocabulario pero mecánica floja:
- confundir backprop (que **calcula** gradientes) con el optimizador (que los **usa**);
- no saber por qué hace falta la no linealidad;
- las soluciones al overfitting al revés;
- no ver el *data leakage* entre frames.

La forma de arreglarlo es construir una red **a mano**, desde el autograd, y recién después usar PyTorch, sabiendo exactamente qué hace `loss.backward()`.

## Objetivos
1. Neurona, capa, MLP. Por qué sin no linealidad colapsa a una matriz (U1).
2. Pérdidas: MSE y *cross-entropy* (U3). *Softmax*.
3. **Backpropagation** como regla de la cadena sobre un grafo de cómputo. Implementar un **autograd mínimo** (estilo micrograd).
4. Optimizadores: SGD, *momentum*, Adam. *Learning rate* (qué pasa si es muy grande o muy chico).
5. Regularización: *weight decay*, *dropout*, ***data augmentation*** (que combate el **over**fitting), *early stopping*. Train/val/test y *leakage*.
6. **CNN**: convolución aprendida (U2), *pooling*, campo receptivo. LeNet → VGG → **ResNet** (*skip connections*). *Batch normalization*.
7. **PyTorch**: tensores, `autograd`, `nn.Module`, *training loop* escrito a mano, `DataLoader`.
8. ***Transfer learning*** y *fine-tuning*.

## Contenidos y recursos por sesión

| Sesión | Contenido | Recursos |
|---|---|---|
| 1 | Neurona, MLP, pérdidas, descenso por gradiente | 3Blue1Brown, *Neural networks*, caps. 1–2 |
| 2 | Backprop como regla de la cadena. Autograd mínimo | 3Blue1Brown, caps. 3–4 · Karpathy: *building micrograd* |
| 3 | Optimizadores, inicialización, regularización, curvas de entrenamiento | CS231n, notas de *Optimization* y *Neural Networks 2–3* |
| 4 | PyTorch: tensores, autograd, `nn.Module`, *training loop* | PyTorch, *Learn the Basics* |
| 5 | CNN: convolución, *pooling*, LeNet/VGG/ResNet, *batch norm* | CS231n, notas de *ConvNets* · d2l.ai, caps. 7–8 · paper de ResNet |
| 6 | *Transfer learning* y *fine-tuning*. Dataset propio de recortes | d2l.ai, *Fine-Tuning* |

## TP6 (borrador)
- `mv/nn/autograd.py`: un `Valor` con `+`, `*`, `tanh`, `relu`, `exp` y `backward()`, verificado contra gradientes numéricos (diferencias finitas).
- `mv/nn/mlp.py`: un MLP entrenado con ese autograd sobre un problema 2D de juguete.
- `mv/nn/clasificador.py`, en PyTorch: una CNN que clasifique recortes en **jugador / árbitro / pelota / fondo**, a partir de frames del club etiquetados.

Notebook:
- curvas de *loss* de train y validación;
- el efecto de la *data augmentation* (combate el overfitting) y de la cantidad de datos;
- desde cero contra *fine-tuning* de un ResNet preentrenado;
- *split* por partido contra por frame (el *leakage*, medido).

## Conexión con el producto
Los detectores y clasificadores del producto son CNN (o *transformers*) preentrenados y *fine-tuneados*. Entender esto es entender qué se puede pedirle a un modelo y cómo evaluarlo honestamente.
