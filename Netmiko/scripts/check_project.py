import os
import sys
import sqlite3

# ------------------------------
# Asegurar que Python encuentre los módulos del proyecto
# ------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from modules.database_manager.db_utils import init_db, add_interface, add_credentials, DB_PATH

# Carpetas a ignorar al listar
IGNORE_DIRS = ['netmiko', '__pycache__', 'venv']

# ------------------------------
# Función para mostrar estructura del proyecto
# ------------------------------
def check_structure():
    print("🔹 Checking project structure...\n")
    for root, dirs, files in os.walk(BASE_DIR):
        # Filtrar carpetas a ignorar
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        level = root.replace(BASE_DIR, "").count(os.sep)
        indent = " " * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = " " * 4 * (level + 1)
        for f in files:
            print(f"{sub_indent}{f}")

# ------------------------------
# Función para insertar dispositivo solo si no existe
# ------------------------------
def add_device_if_not_exists(name, type_, ip, mac=None, model=None, location=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM devices WHERE mac=?", (mac,))
    result = cursor.fetchone()
    if result:
        device_id = result[0]
        print(f"⚠ Device with MAC {mac} already exists. Using existing device_id={device_id}")
    else:
        cursor.execute("""
            INSERT INTO devices (name, type, ip, mac, model, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, type_, ip, mac, model, location))
        device_id = cursor.lastrowid
        conn.commit()
        print(f"✅ Added new device {name} with device_id={device_id}")
    conn.close()
    return device_id

# ------------------------------
# Función para testear la base de datos
# ------------------------------
def test_database():
    print("\n🔹 Testing database...")
    # Inicializar la DB y tablas
    init_db()

    # Insertar router de prueba
    device_id = add_device_if_not_exists(
        name="TestRouter",
        type_="Router",
        ip="10.10.10.1",
        mac="AA:BB:CC:DD:EE:FF",
        model="ISR4331",
        location="Lab"
    )

    # Insertar interfaz de prueba
    add_interface(device_id, name="GigabitEthernet0/0", mac="AA:BB:CC:DD:EE:01", ip="10.10.10.1", status="up",
                  description="WAN Test Interface")

    # Insertar credenciales de prueba
    add_credentials(device_id, username="admin", password="cisco123")

    # Mostrar dispositivos en DB
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, ip, mac FROM devices")
    devices = cursor.fetchall()
    print("\nDevices in DB:")
    for d in devices:
        print(f" - ID: {d[0]}, Name: {d[1]}, IP: {d[2]}, MAC: {d[3]}")
    conn.close()

# ------------------------------
# Main
# ------------------------------
if __name__ == "__main__":
    check_structure()
    test_database()
