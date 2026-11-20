#!/usr/bin/env python3
"""Primer pase ARK Redwood: inventario existente + spawner ya extraído.

Solo lectura. No extrae nada del PAK y no modifica assets.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from ark_redwood_instance_decoder import inventory_candidates, inspect_package

ARK_ROOT = Path(os.environ.get("ARK_ROOT", Path.home() / "ark")).expanduser()
INVENTORY = ARK_ROOT / "01_INVENTARIO/original/pakchunk1-Android_lista.txt"
SPAWNER = ARK_ROOT / "ARK_MAP_LAB/redwood_spawner/CoreBlueprints/Spawners/DinoSpawnEntriesRedwoods.uasset"


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    report = {
        "tool": "ARK Redwood first pass",
        "mode": "read_only",
        "ark_root": str(ARK_ROOT),
        "inventory": {"path": str(INVENTORY), "exists": INVENTORY.is_file()},
        "spawner": {"path": str(SPAWNER), "exists": SPAWNER.is_file()},
        "candidate_count": 0,
        "candidates": [],
        "package_result": None,
        "errors": [],
        "limits": [
            "Los candidatos del inventario no están extraídos ni validados internamente.",
            "El spawner es un asset de fauna, no contiene necesariamente transforms de árboles.",
            "No se han modificado archivos originales."
        ],
    }

    if INVENTORY.is_file():
        report["inventory"]["sha256"] = file_hash(INVENTORY)
        try:
            report["candidates"] = inventory_candidates(INVENTORY)
            report["candidate_count"] = len(report["candidates"])
        except Exception as exc:
            report["errors"].append({"stage": "inventory", "type": type(exc).__name__, "error": str(exc)})
    else:
        report["errors"].append({"stage": "inventory", "error": "inventory_not_found"})

    if SPAWNER.is_file():
        try:
            report["package_result"] = inspect_package(SPAWNER)
        except Exception as exc:
            report["errors"].append({"stage": "spawner_parse", "type": type(exc).__name__, "error": str(exc)})
    else:
        report["errors"].append({"stage": "spawner", "error": "spawner_not_found"})

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not report["errors"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
