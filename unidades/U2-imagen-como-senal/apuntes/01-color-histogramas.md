# 01 · Color, formación de imagen e histogramas

> **La idea en una frase:** un píxel no es "el color de la cosa". Es lo que llegó al sensor, después de pasar por la luz del momento, la cámara y la compresión. Elegir **cómo representar el color** decide si un cambio de luz (sol contra sombra) te rompe el algoritmo o no.

**Videos:**
- First Principles of CV, Módulo 1: *Image Formation* e *Image Sensing* (los conceptos, sin las derivaciones ópticas).
- Stachniss, Photogrammetry I, clase 4 (*Histograms and Point Operators*).

---

## 1. De la luz al número (lo mínimo)

```
luz → objeto (refleja según su material) → lente → sensor → cuantización → procesado → compresión → tu array
```

- **Sensor.** Una grilla de fotositos cuenta fotones. Cada fotosito mide **un solo color**: tiene encima un filtro rojo, verde o azul en el patrón de Bayer, que tiene el doble de verdes. Los otros dos canales de cada píxel se **interpolan** de los vecinos (*demosaicing*). O sea que buena parte de tu imagen RGB está inventada por interpolación. El verde es el canal más confiable.
- **Cuantización:** 8 bits por canal, 256 niveles.
- **Gamma.** Los valores **no** son proporcionales a la luz: el estándar sRGB aplica una curva (≈ `v = luz^(1/2.2)`) para usar mejor los 8 bits donde el ojo distingue más. Un píxel de 128 no recibió la mitad de luz que uno de 255, sino ~22 %.
- **Compresión** (H.264 en YouTube): bloques de 8×8 o 16×16, pérdida de detalle fino y *ringing* cerca de los bordes. Es peor justo en el movimiento rápido.

**Consecuencia práctica:** lo que bajás de YouTube pasó por interpolación, una curva no lineal y una compresión con pérdida. Todo algoritmo tiene que tolerar ese ruido, y por eso la sesión 2 es sobre filtrar.

## 2. RGB y su problema

Un color RGB es un punto en el cubo [0, 255]³. El problema para nosotros: **un cambio de iluminación mueve los tres canales juntos**. En sombra, la misma camiseta da aproximadamente `k · (R, G, B)` con k < 1: el vector color se **acorta** pero casi no cambia de **dirección**. Es el ejercicio A4 de la guía de U1.

Las reglas tipo "G > R + 20" del TP0 comparan **diferencias absolutas**, y en sombra todas las diferencias se achican. Por eso fallan.

## 3. HSV: separar "qué color" de "cuánta luz"

HSV reorganiza RGB en un cilindro:

| Componente | Qué mide | Cálculo (con R, G, B en [0, 1]) |
|---|---|---|
| **H** (*hue*, tono) | qué color: el ángulo en la rueda de colores | según cuál canal es el máximo (ver abajo) |
| **S** (saturación) | qué tan "puro" es, frente a qué tan gris | `(max − min) / max` |
| **V** (valor) | cuánta luz | `max` |

Con M = max, m = min y C = M − m (el *croma*):
- H = 60° · ((G − B)/C mod 6) si M = R
- H = 60° · ((B − R)/C + 2) si M = G
- H = 60° · ((R − G)/C + 4) si M = B

La rueda arranca en rojo (0°), pasa por amarillo (60°), verde (120°), cian (180°), azul (240°) y magenta (300°), y vuelve a rojo.

### Por qué resiste la sombra

Si multiplicás (R, G, B) por k:
- **V** se multiplica por k: **cambia**;
- **S** = C/M: numerador y denominador se multiplican por k, así que **no cambia**;
- **H** depende de cocientes como (G − B)/C, así que **no cambia**.

La regla "tono verde y saturación suficiente" sobrevive a la sombra. El TP2 lo testea literalmente: oscurece el frame a un 25 % y pide que la máscara casi no cambie.

### Dónde HSV falla (y hay que saberlo)

- **Si S o V son chicos, H es basura.** En un gris casi puro, C ≈ 0 y el tono depende del ruido. Por eso la máscara pide `s_min` y `v_min`.
- **Blanco contra negro no se separa por tono.** Ninguno tiene tono. Hebraica de blanco contra un rival de negro (el partido vs Sosiego) se separa por **V** (o L de Lab), y eso sí cambia con la sombra. Por eso el proyecto anterior comparaba el brillo de la camiseta **contra el pasto de al lado**: el pasto recibe la misma luz y sirve de referencia local.
- **H es circular:** 355° y 5° son dos rojos casi iguales, a 10° de distancia, no a 350°. Toda distancia entre tonos tiene que usar `min(|a − b|, 360 − |a − b|)`.

## 4. Lab: distancias que se parecen a lo que ve el ojo

**CIE Lab** está diseñado para que la **distancia euclídea** entre dos colores se parezca a cuán distintos los percibimos:
- **L** = luminosidad;
- **a** = eje verde ↔ rojo;
- **b** = eje azul ↔ amarillo.

Es una transformación no lineal de RGB (no la implementamos: `cv2.cvtColor(img, cv2.COLOR_RGB2LAB)`). Sirve para *clustering* de colores (K-means en U8): si vas a medir distancias entre colores, que las distancias signifiquen algo.

**Lección del proyecto anterior:** las tres componentes de Lab tienen escalas muy distintas. Medido: desvío estándar de 48 en L contra 13 y 15 en a y b. K-means con distancia euclídea quedaba dominado por L y separaba **sol de sombra** en vez de equipos. Estandarizar cada componente (restar la media y dividir por el desvío) subió el acierto de 83,7 % a 97,7 %. Vuelve en U8.

## 5. Operadores puntuales e histogramas

Un **operador puntual** cambia cada píxel según su propio valor, sin mirar a los vecinos: `salida = f(entrada)`.

- Brillo y contraste: `α·v + β` (TP0).
- Gamma: `v^γ`, para aclarar u oscurecer los tonos medios.
- Umbral: `v > t`.

Como `v` solo toma 256 valores, `f` se precalcula en una **tabla** (LUT) y se aplica con `lut[img]`: indexado avanzado, sin loops. Así lo hace OpenCV.

### Ecualización de histograma

**Problema:** un frame nublado o a contraluz usa solo una parte del rango (todo entre 40 y 120, por ejemplo).

**Idea:** buscar la f que haga que el histograma de salida sea lo más **plano** posible, usando todos los niveles por igual.

**Resultado** (vale la pena entenderlo, es probabilidad pura): si `F` es la **función de distribución acumulada** (CDF) de los valores, `F(v)` tiene distribución **uniforme** en [0, 1]. ¿Por qué? Porque la fracción de píxeles con `F(v) ≤ u` es exactamente u. Entonces:

$$f(v) = \text{round}\left(\frac{\text{cdf}(v) - \text{cdf}_{min}}{N - \text{cdf}_{min}} \cdot 255\right)$$

(El `− cdf_min` hace que el valor más oscuro presente vaya a 0.)

**Cuidado:**
- Ecualizar también **amplifica el ruido** en las zonas planas.
- Es global: una zona muy oscura y otra muy clara compiten.
- La versión local (CLAHE) lo mejora; la usás con OpenCV.

**Otsu.** Para elegir un umbral automáticamente, buscá el t que separa el histograma en dos grupos con la **mínima varianza dentro de cada grupo**. Se menciona para que lo reconozcas; no está en el TP.

---

## Resumen para volver

- El píxel pasó por luz, Bayer (interpolación), gamma y compresión. Hay ruido y artefactos siempre.
- En RGB, la sombra mueve los 3 canales juntos: cambia el largo del vector color, no su dirección.
- **HSV:** H (tono, en grados, circular), S = C/M, V = M. Escalar la luz cambia solo V.
- H no sirve con S o V chicos. Blanco contra negro se separa por V/L, y relativo al pasto.
- **Lab:** distancias perceptuales. **Estandarizar** antes de hacer *clustering*.
- Operadores puntuales: una LUT y `lut[img]`. Ecualización: `f = CDF` normalizada.
