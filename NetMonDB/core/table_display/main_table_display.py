# NetMonDB/core/table_display/main_table_display.py

from .display import show_table

def table_main(parsed_data):
    """
    Función principal del módulo Table Display.
    Muestra los datos en consola en formato tabla.
    """
    if not parsed_data:
        print("⚠️ No hay datos para mostrar.")
        return

    print("📊 Mostrando datos en tabla...")
    show_table(parsed_data)
