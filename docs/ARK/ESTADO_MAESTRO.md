# ARK — Estado maestro en el repositorio Termux

Última consolidación: 2026-11-20
Repositorio operativo: `bladimirhurtado/termux`, rama `main`.

## Regla de continuidad
Antes de crear herramientas nuevas, revisar este documento y los archivos existentes. No repetir extracción del PAK, inventario ni ARK MAP LAB ya ejecutados. Separar evidencia confirmada, candidatos y tareas pendientes. Mantener los originales intactos y trabajar sobre copias.

## Objetivo activo: Redwood 2.0
Mejorar el bosque Redwood existente de The Island, conservando los árboles gigantes, plataformas arbóreas y la identidad del bioma. La especificación funcional está en [REDWOOD_ADAPTACION_V1.md](REDWOOD_ADAPTACION_V1.md).

Intervenciones previstas:
1. Sotobosque y vegetación secundaria en el núcleo de secuoyas.
2. Claros pequeños y orgánicos.
3. Corredores naturales sin destruir árboles estructurales ni colisiones.
4. Transiciones de ribera sin bloquear agua ni cuevas.
5. Laderas y roquedos con distribución coherente.

## Datos ya obtenidos en el trabajo anterior
- PAK Android: `~/ark/pakchunk1-Android.pak`; no volver a extraerlo.
- Inventario existente: `~/ark/01_INVENTARIO/original/pakchunk1-Android_lista.txt`; alrededor de 23.6 mil recursos validados en la revisión anterior.
- Informe ARK MAP LAB y análisis de zonas ya generados; reutilizar sus resultados.
- Spawner Redwood extraído:
  `~/ark/ARK_MAP_LAB/redwood_spawner/CoreBlueprints/Spawners/DinoSpawnEntriesRedwoods.uasset`
  y pareja `.uexp`.
- Inspección previa de cadenas halló 93 cadenas, incluidas propiedades de spawn y nombres de criaturas. Esto NO equivale a decodificar los valores, pesos o límites.
- No se ha localizado todavía el paquete de nivel/foliage con las instancias Redwood y sus transforms.
- No se ha demostrado un serializador compatible con este build de ARK móvil.

## Herramientas existentes y portadas aquí
- `scripts/ark_redwood_instance_decoder.py`: inspector de solo lectura basado en `uasset_read`; procedente del trabajo previo, no es una herramienta nueva duplicada.
- `tests/ark_redwood_preflight.py`: comprueba los insumos locales y el parser.
- `scripts/termux_agent.py`: agente local con tareas permitidas explícitamente.
- `scripts/start_termux_agent.sh`: lanzador del agente.
- Guía del puente: [TERMUX_AGENT.md](../TERMUX_AGENT.md).

## Estado honesto
**Hecho en GitHub:** especificación Redwood V1, decoder portado, preflight, agente y primera tarea en cola.

**Hecho en el teléfono:** inventario y extracción anteriores ya existen según la evidencia que el usuario compartió en sesiones previas. La tarea preflight está en cola, pero aún no hay resultado devuelto por el agente.

**Pendiente:** activar el agente local una vez; confirmar preflight; localizar paquetes de foliage/instancias y leer transforms; validar parser con los assets reales; solo después diseñar una primera modificación sobre copia.

## Restricciones
- No modificar PAK, UASSET, UEXP, UMAP ni UBULK originales.
- No inventar coordenadas, transforms, pesos de spawn ni referencias.
- No afirmar que una lectura de cadenas equivale a descodificación de propiedades.
- Toda edición futura debe registrar hash original/nuevo, herramienta y versión, y prueba dentro del juego.
- No repetir extracción ni inventario salvo que aparezca una razón técnica demostrable.

## Siguiente paso único
Completar la activación del agente y recibir el resultado automático de `ark-redwood-preflight-001`. Después, continuar con el análisis de los paquetes ya extraídos y del inventario existente.
