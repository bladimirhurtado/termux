#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
command -v python >/dev/null 2>&1 || { echo "Python no está instalado en Termux."; exit 1; }
git rev-parse --is-inside-work-tree >/dev/null
mkdir -p logs
PIDFILE="$ROOT/.termux-agent.pid"
if [ -f "$PIDFILE" ]; then
  OLD_PID="$(cat "$PIDFILE" 2>/dev/null || true)"
  if [ -n "$OLD_PID" ] && kill -0 "$OLD_PID" 2>/dev/null; then
    echo "El agente ya está activo (PID $OLD_PID)."
    exit 0
  fi
  rm -f "$PIDFILE"
fi
nohup python "$ROOT/scripts/termux_agent.py" >>"$ROOT/logs/termux-agent.log" 2>&1 </dev/null &
echo "$!" > "$PIDFILE"
echo "Agente iniciado (PID $(cat "$PIDFILE"))."
echo "Log: $ROOT/logs/termux-agent.log"
echo "Requiere autenticación Git local para pull/push sin interacción."
