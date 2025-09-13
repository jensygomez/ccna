#Netmiko/scripts/db_structure.py
import sqlite3

DB_PATH = "modules/database/net_devices.db"  # Ajusta según tu ruta

def show_db_structure(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Listar todas las tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("📋 Tablas en la base de datos:\n")
    for table_name in tables:
        table = table_name[0]
        print(f"🔹 {table}")
        # Listar columnas de cada tabla
        cursor.execute(f"PRAGMA table_info({table});")
        columns = cursor.fetchall()
        for col in columns:
            print(f"   - {col[1]} ({col[2]})")
        print()

    conn.close()

if __name__ == "__main__":
    show_db_structure(DB_PATH)
