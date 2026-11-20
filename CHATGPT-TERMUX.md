# Puente Termux <-> GitHub <-> ChatGPT

Este repositorio es el espacio de trabajo de Termux en Android.

## Regla de trabajo
- ChatGPT crea y actualiza directamente aquí los scripts, pruebas, documentación y archivos de trabajo.
- No pedir al usuario que copie código o resultados entre el chat y Termux como flujo habitual.
- El agente local `scripts/termux_agent.py` sincroniza los cambios de GitHub, ejecuta únicamente tareas autorizadas y publica sus resultados.
- La primera activación del agente requiere una acción local única. Consultar `docs/TERMUX_AGENT.md`.
- Si el agente no está activo, se mantiene el flujo manual `git pull` / `git push`.

## Seguridad y ARK
- No ejecutar comandos arbitrarios recibidos desde GitHub.
- Las tareas deben estar incluidas expresamente en la lista permitida del agente.
- No modificar archivos originales del juego ni PAK/ UASSET/ UEXP/ UMAP/ UBULK sin una autorización explícita y una estrategia de copia/validación.
- Consultar `docs/ARK/ESTADO_MAESTRO.md` antes de continuar ARK; no repetir inventarios, extracciones o análisis ya hechos.
- Diferenciar siempre entre datos confirmados, candidatos y resultados pendientes de ejecutar.

## Repositorio
- Rama operativa: `main`.
- Los cambios de ChatGPT se hacen directamente en este repositorio.
