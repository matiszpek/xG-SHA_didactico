# 01 · Probabilidad básica, condicional y Bayes

> **La idea en una frase:** la probabilidad es contar casos con cuidado. Casi todos los errores vienen de dos lugares: **sumar cosas que se solapan** y **confundir P(A|B) con P(B|A)**.

**Videos y lectura:**
- [Seeing Theory](https://seeing-theory.brown.edu/), caps. 1 (*Basic Probability*) y 2 (*Compound Probability*). Es interactivo: tocá todo.
- 3Blue1Brown: *Bayes theorem, the geometry of changing beliefs*.

---

## 1. El lenguaje

- **Experimento:** algo con resultado incierto (un tiro, una tirada de dado, un frame que el detector procesa).
- **Espacio muestral Ω:** todos los resultados posibles.
- **Evento:** un subconjunto de Ω ("sale par", "es gol", "el detector dice pelota").
- **Probabilidad:** una función que cumple que P(Ω) = 1, P(A) ≥ 0, y que si A y B **no se solapan**, P(A ∪ B) = P(A) + P(B).

Todo lo demás se deduce de esas tres reglas.

## 2. El complemento: "al menos uno"

$$P(\text{no } A) = 1 - P(A)$$

**El error del diagnóstico** (bloque 2, pregunta 1): P(al menos un 6 en dos tiradas) **no** es 1/6 + 1/6. Esa suma cuenta **dos veces** el caso "6 y 6": los eventos "6 en la primera" y "6 en la segunda" se solapan. La regla general es la inclusión-exclusión:

$$P(A \cup B) = P(A) + P(B) - P(A \cap B) = \tfrac16 + \tfrac16 - \tfrac1{36} = \tfrac{11}{36}$$

Pero el camino cómodo es el complemento: "al menos un 6" es lo contrario de "ningún 6".

$$P(\text{al menos uno}) = 1 - P(\text{ninguno}) = 1 - \left(\tfrac56\right)^2 = \tfrac{11}{36}$$

**Con xG** (pregunta 9 del diagnóstico): la probabilidad de **no** meter ninguno de tres tiros con xG 0,1, 0,3 y 0,5 es `0,9 · 0,7 · 0,5 = 0,315`, y la de meter al menos uno es 0,685. Ese "1 − 0,9" que propusiste no tiene sentido: 0,9 es una **cantidad esperada** de goles, no una probabilidad (apunte 02). Si los xG sumaran 1,5, daría negativo.

## 3. Independientes no es lo mismo que excluyentes

| | Definición | Ejemplo de fútbol |
|---|---|---|
| **Excluyentes** | no pueden pasar juntos: P(A ∩ B) = 0 | "el tiro fue gol" y "el tiro fue atajado" |
| **Independientes** | saber uno no cambia la probabilidad del otro: P(A ∩ B) = P(A)·P(B) | "gol en el tiro 1" y "gol en el tiro 7" (en el modelo de xG; en la realidad, discutible) |

Dos eventos con probabilidad positiva **no pueden** ser las dos cosas: si son excluyentes, P(A ∩ B) = 0 ≠ P(A)·P(B). Saber que pasó uno te dice que el otro **no** pasó, y eso es depender muchísimo.

## 4. Probabilidad condicional

$$P(A \mid B) = \frac{P(A \cap B)}{P(B)}$$

"De los casos en que pasa B, ¿en qué fracción pasa también A?" Restringís el universo a B.

**Regla del producto:** `P(A ∩ B) = P(A | B)·P(B)`. Con independencia, `P(A | B) = P(A)`, y se recupera la multiplicación simple.

**Probabilidad total.** Si B puede pasar "con A" o "sin A":

$$P(B) = P(B \mid A)\,P(A) + P(B \mid \text{no }A)\,P(\text{no }A)$$

## 5. Bayes

Dar vuelta una condicional:

$$P(A \mid B) = \frac{P(B \mid A)\,P(A)}{P(B)}$$

**El detector de pelota del diagnóstico.** La pelota está visible en el 20 % de los frames. Si está, el detector la ve el 90 % de las veces; si no está, dice "pelota" igual el 5 % de las veces.

$$P(\text{está} \mid \text{dice}) = \frac{0{,}9 \cdot 0{,}2}{0{,}9 \cdot 0{,}2 + 0{,}05 \cdot 0{,}8} = \frac{0{,}18}{0{,}22} \approx 0{,}82$$

Ahora el mismo detector, pero buscando la pelota en **recortes chicos**, donde aparece en el 2 % de los casos:

$$\frac{0{,}9 \cdot 0{,}02}{0{,}9 \cdot 0{,}02 + 0{,}05 \cdot 0{,}98} \approx 0{,}27$$

¡Casi 3 de cada 4 "pelotas" son falsas! El detector no cambió: cambió la **tasa base**, P(A). Ignorarla es el error más común con Bayes (*base rate fallacy*). Y es exactamente por qué la *accuracy* no sirve con clases desbalanceadas (diagnóstico, bloque 4, pregunta 10).

**Intuición de 3Blue1Brown:** pensá en 1000 casos concretos. 20 tienen pelota, de los cuales el detector ve 18. 980 no tienen, y el detector dice "pelota" en 49. De 67 "pelotas", 18 son reales.

## 6. Precisión y *recall* son condicionales

Esto va a volver en U7 con todo:
- **Precisión** = P(es real | el detector lo detectó). "De lo que marqué, ¿cuánto estaba bien?"
- ***Recall*** = P(el detector lo detectó | es real). "De lo que había, ¿cuánto encontré?"

Son condicionales **en sentido contrario**. Confundirlas es confundir P(A|B) con P(B|A).

---

## Resumen para volver

- **Complemento:** P(al menos uno) = 1 − P(ninguno). No sumar eventos que se solapan.
- **Excluyentes** (no pueden pasar juntos) ≠ **independientes** (uno no informa sobre el otro).
- `P(A|B) = P(A ∩ B) / P(B)`. Producto: `P(A ∩ B) = P(A|B) P(B)`.
- **Bayes:** `P(A|B) = P(B|A) P(A) / P(B)`, con P(B) por probabilidad total. **La tasa base importa.**
- Precisión = P(real | detectado). *Recall* = P(detectado | real).
