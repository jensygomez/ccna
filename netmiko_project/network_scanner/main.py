#netmiko_project/network_scanner/main.py
# #!/usr/bin/env python3
"""
network_scanner/main.py
Orquestador pequeño del scanner. No contiene lógica complicada.
Recibe --config (ruta JSON) y --workers (nº de hilos).
"""

import argparse
import sys
from pathlib import Path

from core import run_scan_from_config

def parse_args():
    parser = argparse.ArgumentParser(description="Network scanner minimal y modular")
    parser.add_argument(
        "-c", "--config", type=str, default=None,
        help="Archivo de configuración JSON (si no se pasa, usa config.json en el mismo directorio)."
    )
    parser.add_argument(
        "-w", "--workers", type=int, default=None,
        help="Número de workers (threads). Si no se pasa, se decide automáticamente."
    )
    return parser.parse_args()

def main():
    args = parse_args()
    project_root = Path(__file__).resolve().parent
    cfg_path = Path(args.config) if args.config else project_root / "config.json"

    if not cfg_path.exists():
        print(f"[ERROR] No se encontró config: {cfg_path}", file=sys.stderr)
        sys.exit(1)

    rc = run_scan_from_config(cfg_path, workers=args.workers)
    sys.exit(0 if rc else 2)

if __name__ == "__main__":
    main()
