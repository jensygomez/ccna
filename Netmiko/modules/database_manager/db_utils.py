import sqlite3
import os

# ------------------------------
# Rutas de la base de datos
# ------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FOLDER = os.path.join(BASE_DIR, "database")
os.makedirs(DB_FOLDER, exist_ok=True)  # Crear carpeta si no existe
DB_PATH = os.path.join(DB_FOLDER, "net_devices.db")

# ------------------------------
# Inicialización de la DB
# ------------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)  # SQLite crea el archivo automáticamente
    cursor = conn.cursor()

    # Tabla de dispositivos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        ip TEXT NOT NULL UNIQUE,
        mac TEXT UNIQUE,
        model TEXT,
        location TEXT,
        registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Tabla de interfaces
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interfaces (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        mac TEXT,
        ip TEXT,
        status TEXT,
        description TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
    )
    """)

    # Tabla de credenciales
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS credentials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
    )
    """)

    # Tabla de logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER NOT NULL,
        command TEXT,
        output TEXT,
        executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()
    print(f"✅ Database initialized at {DB_PATH}")

# ------------------------------
# Funciones CRUD
# ------------------------------
def add_device(name, type_, ip, mac=None, model=None, location=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO devices (name, type, ip, mac, model, location)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, type_, ip, mac, model, location))
    device_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return device_id

def add_interface(device_id, name, mac=None, ip=None, status=None, description=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO interfaces (device_id, name, mac, ip, status, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (device_id, name, mac, ip, status, description))
    conn.commit()
    conn.close()

def add_credentials(device_id, username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO credentials (device_id, username, password)
        VALUES (?, ?, ?)
    """, (device_id, username, password))
    conn.commit()
    conn.close()

def get_devices():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, type, ip FROM devices")
    devices = cursor.fetchall()
    conn.close()
    return devices

# ------------------------------
# Inicialización si se ejecuta directamente
# ------------------------------
if __name__ == "__main__":
    init_db()
