# 04 · Errores y estabilidad: cuándo una homografía es confiable

> **La idea en una frase:** que la homografía pase por tus puntos **no** prueba que sea buena. Con exactamente 4 puntos siempre pasa, aunque sea basura. Lo que valida es el error en puntos **que no usaste para ajustar**, y eso depende de cuántos puntos tenés y **dónde** están.

**Lectura:** Hartley & Zisserman, 4.2 (errores) y 5.1 (análisis de error, por encima).

---

## 1. La trampa de los 4 puntos

Con 4 correspondencias, el DLT resuelve 8 ecuaciones con 8 incógnitas: el ajuste es **exacto**. El error de reproyección en esos 4 puntos da **0**, siempre, aunque un click esté corrido 10 píxeles.

**El número que uno miraría para validar no valida nada.**

En el proyecto anterior pasó esto (D24): en dos pares de *keyframes* cercanos, anotados con 4 puntos cada uno, la homografía de un frame y la propagada desde el otro diferían en **14 y 22 metros** en un mismo punto de prueba. Los cuadriláteros de puntos eran muy achatados (~150 px de alto contra más de 1000 de ancho) y se concluyó que, con el mínimo de puntos, un par de píxeles de ruido cambiaban todo.

La historia tiene una segunda parte que vale tanto como la primera. D24 decía que la cámara "no se había movido" entre esos frames, y lo usaba como evidencia. Después (D29) se midió con dos métodos independientes y **la cámara sí se había movido ~40 px**. El argumento matemático de que 4 puntos son inestables sigue en pie (lo vas a medir vos en el TP), pero esos 14 y 22 m mezclaban dos errores, y nadie sabe cuánto venía de cada uno. La lección doble: con 4 puntos no se puede validar, y una explicación que "cierra" no está medida hasta que se mide.

## 2. Cuánto empeora: lo medido

Con la cámara sintética del TP (al costado, a 9 m de altura, f = 1400) **paneada hacia el área izquierda**, que deja 14 puntos notables a la vista. En cada prueba se eligen n de esos puntos al azar, se les suma **2 px de ruido** y se mide el error en metros sobre la parte visible de la cancha. Son 300 pruebas por fila (sección 3 del notebook):

| Puntos | Error mediano | Percentil 90 | Pruebas con más de 5 m |
|---|---|---|---|
| 4 | **~2,2 m** | **~36 m** | **35 %** |
| 5 | ~0,5 m | ~1,6 m | 4 % |
| 6 | ~0,3 m | ~0,7 m | 0 % |
| 8 | ~0,26 m | ~0,46 m | 0 % |
| 12 | ~0,18 m | ~0,31 m | 0 % |

Con 4 puntos, **una de cada tres** calibraciones se equivoca en más de 5 metros, y todas tienen error de reproyección 0. Pasar a 6 puntos baja el percentil 90 **unas 50 veces**. Con 6 o más, la sobredeterminación promedia el ruido. Además deja **residuos** que se pueden mirar: si un punto queda con error grande, es sospechoso.

(Ojo con generalizar: son números de **esta** cámara sintética y de **este** ruido. Con la cámara real hay que medirlo de nuevo, y es lo que hace la sección 5 del TP.)

## 3. Dónde están los puntos importa tanto como cuántos

- **Alineados:** si 3 de los 4 están sobre la misma recta, el problema es degenerado (U1, guía C5): hay infinitas homografías compatibles. En la cancha es muy fácil que pase: la esquina y las cuatro esquinas de las áreas sobre la línea de fondo son **5 puntos alineados**. Medido en otra tanda de 300 pruebas de 5 puntos: 9 erraron por más de 5 m, y en 8 de esas 9 había **4 puntos sobre la misma recta** (es poca muestra, pero el patrón es claro). Con 4 puntos, un tercio de las calibraciones malas tenía 3 alineados, con un error mediano de ~36 m.
- **Amontonados en una zona:** la homografía queda bien ahí y **extrapola mal** lejos. Medido con 6 puntos: si son todos del área, el error sobre la zona visible es ~0,6 m (p90 ~1,3 m); si están repartidos (con alguno en la línea de medio), ~0,25 m (p90 ~0,5 m). Dentro del área, los dos dan ~0,3 m.
- **Bien repartidos:** que cubran la zona donde vas a medir (los dos lados del área, la línea de medio, puntos lejanos y cercanos).
- **Vistos muy de costado:** un cuadrilátero muy achatado en la imagen (por ejemplo, las 4 esquinas del área vistas desde una cámara baja) está cerca de la degeneración. Pequeños errores verticales son enormes en metros.

## 4. Cómo validar de verdad

1. **Más de 4 puntos** (6 o más) y mirar los **residuos** de cada uno.
2. **Validación con puntos retenidos** (*held-out*): ajustar con todos menos uno, medir el error en el que quedó afuera, y repetir con cada punto. Es la misma idea de train/test de U3.
3. **Mirar:** dibujar el modelo de la cancha reproyectado sobre la imagen (las líneas tienen que caer sobre la cal) y la vista cenital (la cancha tiene que verse rectangular). El ojo detecta en un segundo lo que un número promedio esconde. Es la regla del proyecto: mirar las salidas, no solo los agregados.
4. **Convertir el error a metros, y en la zona que importa:** 3 px de error cerca de la cámara son centímetros; en la lateral lejana pueden ser metros.

## 5. Del error en la homografía al error en las estadísticas

Un error de 0,5 m en la posición se arrastra a todo lo demás:
- la **distancia recorrida** acumula los errores de cada tramo (U0: el ruido no se cancela, se suma);
- la **velocidad** divide por 0,1 s: 0,5 m de error son 18 km/h de error en un tramo;
- el **xG** depende de distancia y ángulo: un tiro mal ubicado 2 m cambia su xG.

Por eso la calidad de la homografía es una de las primeras cosas que hay que **medir** antes de reportar estadísticas en metros.

---

## Resumen para volver

- Con 4 puntos, el ajuste es exacto y el error de reproyección = 0 **siempre**. No valida nada.
- Medido (cámara sintética, 2 px de ruido): con 4 puntos, el 35 % de las calibraciones erra por más de 5 m (p90 ~36 m); con 6, ~0,3 m (p90 ~0,7 m). **Usar 6 o más**, y que no estén todos sobre la línea de fondo.
- Importa **dónde** están: nada de alineados ni amontonados; que cubran la zona de interés.
- Validar con **puntos retenidos** y **mirando** (cancha reproyectada, vista cenital).
- El error en metros se arrastra a distancia, velocidad y xG.
