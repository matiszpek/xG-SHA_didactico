# 01 · Vectores, combinaciones lineales y bases

> **La idea en una frase:** un vector es una flecha (o un punto) que se escribe con coordenadas, y esas coordenadas **solo tienen sentido respecto de una base**: dicen "cuántas veces cada vector base".

**Videos:** 3Blue1Brown, *Essence of Linear Algebra*, caps. 1 y 2.

---

## 1. Tres miradas sobre un vector

| Mirada | Un vector es... | En visión |
|---|---|---|
| Física | una flecha: dirección y largo | el desplazamiento de un jugador entre dos frames |
| Computación | una lista de números | un píxel RGB `(R, G, B)`, una posición `(x, y)` |
| Matemática | algo que se puede sumar y escalar | todo lo anterior, y también imágenes enteras, que son vectores de 2 millones de componentes |

Las dos operaciones fundamentales:
- **Suma:** poner una flecha a continuación de la otra. `(1, 2) + (3, 1) = (4, 3)`.
- **Producto por escalar:** estirar, achicar o dar vuelta. `2 · (1, 2) = (2, 4)`, `−1 · (1, 2) = (−1, −2)`.

## 2. Las coordenadas son una receta

Los **vectores base canónicos** del plano son î = (1, 0) y ĵ = (0, 1). Cuando escribimos v = (3, −2), en realidad decimos:

$$v = 3\,\hat\imath + (-2)\,\hat\jmath$$

"Andá 3 veces î y −2 veces ĵ." Las coordenadas son **los coeficientes de una receta**. Si cambiás los ingredientes (la base), la misma receta da otro vector. Y el mismo vector tiene otra receta.

**Ejemplo de fútbol.** La posición de un jugador en *píxeles* y en *metros de cancha* describe el mismo punto con dos "bases" distintas (más un origen distinto). Pasar de una a la otra es exactamente la homografía de U4.

## 3. Combinaciones lineales y span

Una **combinación lineal** de v y w es cualquier `a·v + b·w`, con a y b números reales.

El **span** de un conjunto de vectores es el conjunto de **todas** sus combinaciones lineales: todo lo que se puede alcanzar con esos ingredientes.

En el plano:
- Si v y w apuntan en direcciones distintas, su span es **todo el plano**.
- Si v y w son paralelos (uno es múltiplo del otro), su span es **una recta**. Agregar w no aportó nada nuevo.
- Si los dos son el vector cero, el span es **un punto**.

## 4. Independencia lineal y bases

Un conjunto de vectores es **linealmente dependiente** si alguno se puede escribir como combinación de los otros (es redundante). Si no, es **linealmente independiente**.

Equivalente, y más útil para hacer cuentas: los vectores v₁, …, vₖ son independientes si la única forma de lograr

$$c_1 v_1 + \dots + c_k v_k = 0$$

es con todos los cᵢ = 0.

Una **base** de un espacio es un conjunto de vectores que:
1. son linealmente independientes (sin redundancia), y
2. generan todo el espacio (span = el espacio).

La cantidad de vectores de cualquier base es la **dimensión**. En el plano, cualquier par de vectores no paralelos es una base.

## 5. Por qué importa en visión

- **Píxeles como vectores.** Un color RGB es un vector en un espacio de 3 dimensiones. "Separar equipos por color" (U8) es buscar que las camisetas de cada equipo formen dos nubes separadas en ese espacio.
- **Cambio de base de color.** RGB, HSV y Lab son *bases* (bueno, HSV no es lineal) distintas para el mismo color. Elegir la base correcta hace que el problema sea fácil o imposible.
- **Imágenes como vectores.** Un recorte de 64×32 en grises es un vector de 2048 componentes. Cuando en U8 comparemos recortes de jugadores con *embeddings*, vamos a medir distancias y ángulos entre vectores en espacios de muchas dimensiones.

## 6. En NumPy

```python
import numpy as np
v = np.array([3.0, -2.0])
w = np.array([1.0, 1.0])
2 * v + 0.5 * w            # combinación lineal

# ¿v y w son independientes? Ponelos como columnas y mirá el rango (lo vemos en 03):
np.linalg.matrix_rank(np.column_stack([v, w]))   # 2 → independientes
```

---

## Resumen para volver

- Un vector se puede sumar y escalar. Sus coordenadas son **coeficientes respecto de una base**.
- **Span:** todo lo alcanzable combinando.
- **Independientes:** ninguno es redundante. Equivale a que solo la combinación con todos los coeficientes en cero da el vector cero.
- **Base:** independientes y generan todo el espacio. La cantidad de vectores es la dimensión.
- El mismo punto tiene coordenadas distintas en bases distintas (píxeles y metros).
