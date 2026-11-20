#!/usr/bin/env python3
"""Preflight de solo lectura para el trabajo ARK Redwood en Termux.

No extrae, modifica ni sobrescribe archivos del juego. Comprueba que el
entorno local conserva los insumos necesarios antes de ejecutar herramientas.
Uso: python tests/ark_redwood_preflight.py
"""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sys

HOME = Path.home()
ARK_ROOT = Path(os.environ.get("ARK_ROOT", HOME / "ark")).expanduser()
INVENTORY = ARK_ROOT / "01_INVENTARIO/original/pakchunk1-Android_lista.txt"
REDWOOD_ROOT = ARK_ROOT / "ARK_MAP_LAB/redwood_spawner/CoreBlueprints/Spawners"
SPAWNER_UASSET = REDWOOD_ROOT / "DinoSpawnEntriesRedwoods.uasset"
SPAWNER_UEXP = REDWOOD_ROOT / "DinoSpawnEntriesRedwoods.uexp"
DECODER = HOME / "bladi3ai/scripts/ark_redwood_instance_decoder.py"

def report(label: str, ok: bool, detail: str = "") -> bool:
    status = "OK" if ok else "PENDIENTE"
    print(f"[{status}] {label}" + (f": {detail}" if detail else ""))
    return ok

def main() -> int:
    print("=== ARK REDWOOD · PREFLIGHT DE SOLO LECTURA ===")
    print(f"HOME: {HOME}")
    print(f"ARK_ROOT: {ARK_ROOT}")
    checks: list[bool] = []

    checks.append(report("Python", sys.version_info >= (3, 10), sys.version.split()[0]))
    checks.append(report("Inventario PAK", INVENTORY.is_file(), str(INVENTORY)))
    checks.append(report("Spawner Redwood .uasset", SPAWNER_UASSET.is_file(), str(SPAWNER_UASSET)))
    checks.append(report("Spawner Redwood .uexp", SPAWNER_UEXP.is_file(), str(SPAWNER_UEXP)))
    checks.append(report("Decoder del proyecto anterior", DECODER.is_file(), str(DECODER)))
    checks.append(report("Paquete uasset_read", importlib.util.find_spec("uasset_read") is not None))

    if INVENTORY.is_file():
        try:
            lines = INVENTORY.read_text(errors="replace").splitlines()
            asset_lines = [
                line for line in lines
                if line.strip().lower().endswith((".uasset", ".umap"))
            ]
            print(f"INFO: líneas de inventario={len(lines)}; referencias .uasset/.umap={len(asset_lines)}")
        except OSError as exc:
            checks.append(report("Lectura del inventario", False, str(exc)))

    failed = sum(not item for item in checks)
    print(f"RESULTADO: {len(checks) - failed}/{len(checks)} comprobaciones OK")
    print("NOTA: esta prueba no demuestra que el parser pueda descodificar transforms.")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
