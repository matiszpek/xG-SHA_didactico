# Método — cómo funciona la materia

## Ritmo

- **Entre 2 y 4 h por semana**, según cómo venga la facultad. Sin fechas fijas: el programa se mide en **sesiones de ~2 h**.
- Una sesión típica dura **~45 min de teoría** (video y apunte) y **~75 min de práctica** (guía o TP).
- Si una semana no hay tiempo, no pasa nada. Lo que importa es no perder el hilo: **anotar en `avance.md` dónde quedé** antes de cerrar cada sesión.

## El ciclo de cada unidad

```
README de la unidad  →  videos + apunte  →  guía de ejercicios  →  TP  →  entrega  →  corrección + coloquio  →  avance.md
```

1. **README de la unidad.** Dice qué se aprende, en cuántas sesiones y qué ver o leer en cada una.
2. **Videos y apunte.** Los videos dan la intuición; el apunte la ordena, agrega la matemática que falta y la conecta con el código y con el fútbol.
3. **Guía de ejercicios.** Son ejercicios cortos, de lápiz y de código, con las respuestas finales al pie para autocorregirse. **Hacelos antes de mirar las respuestas.**
4. **TP.** Se implementa en `mv/` y se experimenta en el notebook del TP.
5. **Entrega.** Commit + push. En el chat con Claude: *"entrego el TPn"*.
6. **Corrección.** Claude corre los tests, lee el código y el informe, y devuelve una corrección escrita y un **coloquio**: preguntas sobre tu propio código que tenés que poder contestar sin mirar nada.
7. **Cierre.** Se anota en `avance.md` y las dudas que quedaron van a `dudas.md`.

## Reglas de juego

- **Los TPs los escribo yo.** Puedo preguntarle a Claude (o a quien sea) por *conceptos*, pedir que me explique algo de otra forma o pedir una pista. No puedo pedir el código del TP.
  - Si uso Claude Code dentro de este repo, el `CLAUDE.md` ya le dice que actúe como docente.
- **Primero intento, después pregunto.** Si me trabo más de 20–30 minutos en lo mismo, lo anoto en `dudas.md` y pregunto.
- **Los tests no son el enemigo.** Si un test falla, el mensaje dice qué se esperaba. Leerlo antes de preguntar.
- **Escribir el resultado siempre**, aunque esté seguro. (Lección del diagnóstico.)
- **Nada de "me da fiaca hacer la cuenta".** 😉

## Cómo se corrige un TP

| Criterio | Qué se mira |
|---|---|
| **Correctitud** | Pasan los tests. El código hace lo que dice que hace, en los casos borde también |
| **Comprensión** | El coloquio: puedo explicar cada línea, por qué se eligió así y qué pasaría si la cambio |
| **Código** | Vectorizado donde corresponde, nombres claros, sin copiar y pegar |
| **Informe** | Experimentos bien diseñados, gráficos legibles y **honestidad**: qué anda, qué no y con qué datos se midió |

La nota es cualitativa: *aprobado*, *aprobado con correcciones* (se rehace una parte) o *rehacer*. El objetivo es entender, no la nota.

## Cómo usar los recursos

- **3Blue1Brown:** intuición geométrica. Verlo con atención, pausando, sin multitarea. Al terminar cada video, intentar explicar la idea en voz alta o por escrito.
- **First Principles of CV (Nayar):** videos cortos y muy claros, ordenados por tema. Es el "libro en video" de la materia.
- **Stachniss:** clases de universidad completas, más densas. Están para profundizar en los temas que el README indica, no para verlas todas.
- **Szeliski:** el libro de referencia. Se lee por secciones puntuales, no de corrido.
- **Papers:** a partir de U7. Primero abstract, figuras y conclusiones; después, el método.

## Material que se escribe sobre la marcha

U0 y U1 están completas. Del resto hay una **ficha** con objetivos, contenidos, recursos y TP. El material completo (apuntes, guía, TP y tests) de la unidad N+1 se escribe **cuando arranco la unidad N**, así se ajusta a cómo vengo: si algo costó, se refuerza; si algo salió fácil, se acelera.
