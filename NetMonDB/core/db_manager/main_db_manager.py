# NetMonDB/core/db_manager/main_db_manager.py

from .db import init_db, insert_or_update_device

def db_main(parsed_data):
    """
    Función principal del módulo DB.
    Guarda o actualiza los datos en SQLite.
    """
    if not parsed_data:
        print("⚠️ No hay datos para guardar en DB.")
        return

    print("💾 Guardando datos en la base de datos...")
    conn = init_db()
    insert_or_update_device(conn, parsed_data)
