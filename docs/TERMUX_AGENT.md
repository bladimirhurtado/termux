# Agente Termux ↔ GitHub

## Objetivo
Permitir que ChatGPT publique tareas declarativas en este repositorio y que
Termux las recoja, ejecute tareas locales autorizadas y devuelva resultados
a GitHub. El usuario no tendrá que copiar códigos ni pegar salidas en el chat.

## Límite de activación
GitHub no puede iniciar procesos dentro de un teléfono Android. El agente debe
arrancarse localmente una primera vez y Android debe permitir que siga activo.
El agente sincroniza automáticamente cada 90 segundos (mínimo 30).

## Activación inicial
Desde Termux, dentro de este repositorio, ejecutar una sola vez:

```bash
bash scripts/start_termux_agent.sh
```

Requisitos:
- Python 3 disponible.
- El repositorio debe tener un remoto `origin` funcional.
- Git debe poder hacer `pull` y `push` sin pedir interacción.
- Para persistencia tras reinicios, se puede integrar Termux:Boot en una fase
  posterior; no se presupone que esté instalado.

## Flujo
1. ChatGPT crea una tarea JSON en `jobs/pending/`.
2. El agente hace fetch/pull y valida el tipo de tarea.
3. Ejecuta exclusivamente una función incluida en `ALLOWED_TASKS`.
4. Guarda el informe en `results/`, mueve la tarea a `jobs/completed/`,
   crea un commit y hace push.
5. ChatGPT lee el informe desde GitHub.

## Seguridad
- No se ejecutan comandos shell enviados desde GitHub.
- No se aceptan rutas o programas arbitrarios en el manifiesto.
- No se guardan tokens ni contraseñas en el repositorio.
- Se usan las credenciales Git configuradas localmente en Termux.
- El agente solo publica los directorios `jobs` y `results`.
- Los scripts de análisis ARK deben comenzar en modo de solo lectura.
- Ninguna tarea puede modificar PAK, UASSET, UEXP, UMAP ni archivos originales
  sin una fase de revisión y autorización explícita.

## Estado actual
Primera tarea permitida: `ark_redwood_preflight`.
La lista de tareas se amplía deliberadamente y de forma explícita; no existe
ejecución remota de shell.
