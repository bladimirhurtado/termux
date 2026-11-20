#!/usr/bin/env python3
"""Agente local de tareas ARK: GitHub -> Termux -> GitHub.

Solo ejecuta tareas incluidas en ALLOWED_TASKS. Nunca interpreta comandos
shell recibidos desde GitHub. Usa las credenciales Git ya configuradas localmente.
"""
from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
PENDING = ROOT / "jobs" / "pending"
DONE = ROOT / "jobs" / "completed"
RESULTS = ROOT / "results"
POLL_SECONDS = max(30, int(os.environ.get("TERMUX_AGENT_POLL_SECONDS", "90")))
BRANCH = os.environ.get("TERMUX_AGENT_BRANCH", "main")

ALLOWED_TASKS = {
    "ark_redwood_preflight": "tests/ark_redwood_preflight.py",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True, capture_output=True,
        check=check, timeout=180,
    )


def sync_from_github() -> None:
    git("fetch", "origin", BRANCH)
    git("pull", "--ff-only", "origin", BRANCH)


def publish_changes(message: str) -> None:
    git("add", "jobs", "results")
    changed = git("diff", "--cached", "--quiet", check=False).returncode != 0
    if changed:
        git("commit", "-m", message)
        git("push", "origin", BRANCH)


def execute_job(job_path: Path) -> None:
    job = json.loads(job_path.read_text(encoding="utf-8"))
    task_id = str(job.get("id", job_path.stem))
    task = job.get("task")
    if not task_id.replace("-", "").replace("_", "").isalnum():
        raise ValueError("ID de tarea no válido")
    if task not in ALLOWED_TASKS:
        raise ValueError(f"Tarea no permitida: {task!r}")

    script = ROOT / ALLOWED_TASKS[task]
    if not script.is_file():
        raise FileNotFoundError(f"No existe el script autorizado: {script}")

    output = io.StringIO()
    started = utc_now()
    exit_code = 1
    error = None
    try:
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            namespace = {"__name__": "termux_agent_task", "__file__": str(script)}
            source = script.read_text(encoding="utf-8")
            exec(compile(source, str(script), "exec"), namespace)
            main = namespace.get("main")
            if callable(main):
                exit_code = int(main())
            else:
                exit_code = 0
    except SystemExit as exc:
        exit_code = int(exc.code or 0) if isinstance(exc.code, (int, type(None))) else 1
    except Exception:
        error = traceback.format_exc()
        output.write("\n" + error)

    result = {
        "id": task_id, "task": task, "status": "success" if exit_code == 0 else "failed",
        "exit_code": exit_code, "started_at": started, "finished_at": utc_now(),
        "device": {"platform": platform.platform(), "python": sys.version.split()[0]},
        "output": output.getvalue()[-30000:], "error": error,
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / f"{task_id}.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    DONE.mkdir(parents=True, exist_ok=True)
    job_path.rename(DONE / job_path.name)


def main() -> int:
    if not (ROOT / ".git").exists():
        print(f"ERROR: {ROOT} no es un repositorio Git", file=sys.stderr)
        return 2
    PENDING.mkdir(parents=True, exist_ok=True)
    DONE.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    print(f"Agente Termux activo en {ROOT}; rama={BRANCH}; intervalo={POLL_SECONDS}s")
    while True:
        try:
            sync_from_github()
            jobs = sorted(PENDING.glob("*.json"))
            for path in jobs:
                try:
                    execute_job(path)
                    publish_changes(f"Complete Termux task {path.stem}")
                except Exception as exc:
                    print(f"[{utc_now()}] tarea {path.name}: {exc}", file=sys.stderr)
                    # Un manifiesto inválido se conserva en pending para inspección.
            time.sleep(POLL_SECONDS)
        except KeyboardInterrupt:
            print("Agente detenido.")
            return 0
        except Exception as exc:
            print(f"[{utc_now()}] sincronización: {exc}", file=sys.stderr)
            time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    raise SystemExit(main())
