    # network_monitor/modules/db_manager/reset_db.py


def reset_database():
    import os
    from modules.db_manager.database import DB_PATH, init_db, get_connection

    if os.path.exists(DB_PATH):
        print(f"🗑️ Eliminando base de datos existente: {DB_PATH}")
        os.remove(DB_PATH)

    init_db()
    print("✅ Base de datos reseteada con éxito.\n")

    conn = get_connection()
    cursor = conn.cursor()
    for table in ["devices", "interfaces", "credentials", "device_logs"]:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"📂 Tabla {table} → {count} registros")
        if count == 0:
            print("   (vacía)\n")
    conn.close()
