# scripts/reset_db_full.py
import os
import shutil
from datetime import datetime

BASE_PATH = os.path.dirname(os.path.dirname(__file__))  # carpeta Netmiko
DB_MANAGER_PATH = os.path.join(BASE_PATH, "modules", "database_manager")
DB_FOLDER_PATH = os.path.join(BASE_PATH, "modules", "database")
DB_FILE_PATH = os.path.join(DB_MANAGER_PATH, "net_devices.db")

def remove_old_db():
    # Borrar carpeta database_manager
    if os.path.exists(DB_MANAGER_PATH):
        shutil.rmtree(DB_MANAGER_PATH)
        print("✅ Carpeta database_manager eliminada.")

    # Borrar carpeta database
    if os.path.exists(DB_FOLDER_PATH):
        shutil.rmtree(DB_FOLDER_PATH)
        print("✅ Carpeta database eliminada.")

def recreate_db_structure():
    os.makedirs(DB_MANAGER_PATH, exist_ok=True)
    os.makedirs(DB_FOLDER_PATH, exist_ok=True)
    print("📂 Carpetas database_manager y database creadas.")

    # Crear __init__.py vacío
    open(os.path.join(DB_MANAGER_PATH, "__init__.py"), "w").close()

    # Crear db_utils.py con init_db
    db_utils_path = os.path.join(DB_MANAGER_PATH, "db_utils.py")
    with open(db_utils_path, "w") as f:
        f.write(f'''# Auto-generado db_utils.py
import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "net_devices.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Tabla devices
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        type TEXT,
        ip TEXT,
        mac TEXT,
        model TEXT,
        location TEXT,
        registered_at TIMESTAMP
    )
    """)
    # Tabla credentials
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS credentials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER,
        username TEXT,
        password TEXT
    )
    """)
    # Tabla lldp_neighbors
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lldp_neighbors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER,
        local_interface TEXT,
        neighbor_name TEXT,
        neighbor_port TEXT,
        neighbor_ip TEXT,
        neighbor_type TEXT,
        neighbor_model TEXT,
        last_seen TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()
    print("✅ Base de datos creada con tablas iniciales.")
''')
    print("📄 Archivo db_utils.py generado.")

def main():
    print("🔹 Reiniciando base de datos y estructura...")
    remove_old_db()
    recreate_db_structure()
    print("✅ Reinicio completo. Ahora puedes correr main_netmiko.py sin errores.")

if __name__ == "__main__":
    main()
