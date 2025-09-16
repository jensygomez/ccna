# NetMonDB/core/genie_parser/main_genie_parser.py

from .parser import parse_show_with_genie

def genie_main(raw_output):
    """
    Función principal del módulo Genie.
    Devuelve datos estructurados en dict.
    """
    if not raw_output:
        print("⚠️ No hay output para parsear.")
        return None

    print("🧩 Parseando datos con Genie (genérico)...")
    parsed_data = parse_show_with_genie(raw_output)
    return parsed_data

