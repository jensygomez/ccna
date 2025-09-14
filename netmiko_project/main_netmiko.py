#!/usr/bin/env python3
"""
main_netmiko.py — Orquestador mínimo e inmutable.
Su única tarea: delegar la ejecución al network_scanner/main.py
sin contener lógica propia de escaneo.
"""

import os
import sys
from pathlib import Path

def main():
    # Ruta relativa a la raíz del proyecto (ajusta si tu estructura difiere)
    project_root = Path(__file__).resolve().parent
    scanner = project_root / "network_scanner" / "main.py"

    if not scanner.exists():
        print(f"[ERROR] No se encontró {scanner}", file=sys.stderr)
        sys.exit(1)

    # Reemplaza el proceso actual por el interpreter que ejecuta el scanner,
    # pasando todos los argumentos recibidos.
    os.execv(sys.executable, [sys.executable, str(scanner)] + sys.argv[1:])

if __name__ == "__main__":
    main()
