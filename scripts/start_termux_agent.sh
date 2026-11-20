#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
command -v python >/dev/null 2>&1 || { echo "Python no está instalado en Termux."; exit 1; }
git rev-parse --is-inside-work-tree >/dev/null
mkdir -p logs
if pgrep -f "$ROOT/scripts/termux_agent.py" >/dev/null 2>&1; then
  echo "El agente ya está activo."
  exit 0
fi
nohup python "$ROOT/scripts/termux_agent.py" >>"$ROOT/logs/termux-agent.log" 2>&1 </dev/null &
echo "Agente iniciado. Log: $ROOT/logs/termux-agent.log"
echo "Necesita que Git tenga autenticación push ya configurada."
