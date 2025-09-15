# network_monitor/modules/db_manager/database.py
# network_monitor/modules/db_manager/database.py

# network_monitor/modules/db_manager/database.py
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "devices.db")


def init_db():
    """Inicializa la base de datos con todas las tablas necesarias."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabla de dispositivos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT UNIQUE,
        hostname TEXT,
        mac TEXT
    )
    """)

    # Tabla de interfaces
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interfaces (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER,
        name TEXT,
        ip_address TEXT,
        status TEXT,
        protocol TEXT,
        FOREIGN KEY(device_id) REFERENCES devices(id),
        UNIQUE(device_id, name)
    )
    """)

    # Tabla de credenciales
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS credentials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER,
        username TEXT,
        password TEXT,
        FOREIGN KEY(device_id) REFERENCES devices(id)
    )
    """)

    # Tabla de logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS device_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER,
        command TEXT,
        output TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(device_id) REFERENCES devices(id)
    )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# Funciones de consulta y guardado
# -----------------------------
def get_credentials(ip):
    """Devuelve las credenciales de un dispositivo por IP."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.username, c.password
        FROM devices d
        JOIN credentials c ON d.id = c.device_id
        WHERE d.ip = ?
    """, (ip,))
    result = cursor.fetchone()
    conn.close()
    return result if result else None


def save_device_and_credentials(ip, hostname, mac, username, password):
    """Guarda dispositivo y credenciales en la DB."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insertar o ignorar el dispositivo
    cursor.execute("""
        INSERT OR IGNORE INTO devices (ip, hostname, mac) VALUES (?, ?, ?)
    """, (ip, hostname, mac))

    # Obtener ID del dispositivo
    cursor.execute("SELECT id FROM devices WHERE ip = ?", (ip,))
    device_id = cursor.fetchone()[0]

    # Insertar credenciales
    cursor.execute("""
        INSERT INTO credentials (device_id, username, password)
        VALUES (?, ?, ?)
    """, (device_id, username, password))

    conn.commit()
    conn.close()


def save_device_log(ip, command, output):
    """Guarda la salida de un comando en device_logs."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM devices WHERE ip = ?", (ip,))
    result = cursor.fetchone()
    if not result:
        conn.close()
        raise ValueError(f"Dispositivo {ip} no encontrado en DB")
    device_id = result[0]

    cursor.execute("""
        INSERT INTO device_logs (device_id, command, output)
        VALUES (?, ?, ?)
    """, (device_id, command, output))

    conn.commit()
    conn.close()


def save_interfaces(ip, interfaces):
    """Guarda interfaces en la DB asociadas a la IP del dispositivo."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM devices WHERE ip = ?", (ip,))
    result = cursor.fetchone()
    if not result:
        conn.close()
        raise ValueError(f"Dispositivo {ip} no encontrado en DB")
    device_id = result[0]

    for intf in interfaces:
        cursor.execute("""
        INSERT INTO interfaces (device_id, name, ip_address, status, protocol)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(device_id, name) DO UPDATE SET
            ip_address=excluded.ip_address,
            status=excluded.status,
            protocol=excluded.protocol
        """, (device_id, intf["name"], intf["ip"], intf["status"], intf["protocol"]))

    conn.commit()
    conn.close()


def show_device_summary(ip):
    """Muestra IP, hostname, MAC y todas las interfaces con estado."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Dispositivo
    cursor.execute("SELECT hostname, ip, mac FROM devices WHERE ip=?", (ip,))
    dev = cursor.fetchone()
    if dev:
        hostname, ip_addr, mac = dev
        print(f"\n📌 Dispositivo: {hostname} | IP: {ip_addr} | MAC: {mac}\n")

    # Interfaces
    cursor.execute("""
        SELECT name, ip_address, status, protocol
        FROM interfaces
        WHERE device_id=(SELECT id FROM devices WHERE ip=?)
    """, (ip,))
    for intf in cursor.fetchall():
        print(f"{intf[0]} | {intf[1]} | {intf[2]} | {intf[3]}")

    conn.close()


def show_device_summary_with_ip(ip):
    """Muestra un resumen del dispositivo y solo las interfaces que tienen IP"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Información del dispositivo
    cursor.execute("SELECT hostname, ip, mac FROM devices WHERE ip=?", (ip,))
    dev = cursor.fetchone()
    if dev:
        hostname, ip_addr, mac = dev
        print(f"\n📌 Dispositivo: {hostname} | IP: {ip_addr} | MAC: {mac}\n")
    else:
        print("Dispositivo no encontrado en la DB.")
        conn.close()
        return

    # Solo interfaces con IP asignada
    cursor.execute("""
        SELECT name, ip_address, status, protocol
        FROM interfaces
        WHERE device_id=(SELECT id FROM devices WHERE ip=?)
        AND ip_address IS NOT NULL AND ip_address != ''
    """, (ip,))
    rows = cursor.fetchall()
    if not rows:
        print(f"No hay interfaces con IP configurada para {hostname}\n")
    else:
        for intf_name, ip_intf, status, proto in rows:
            print(f"💻 {hostname} con IP {ip_intf} está conectado en la interfaz {intf_name} ({status}/{proto})")

    conn.close()





def show_database():
    """Muestra en pantalla el contenido de todas las tablas."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("\n📂 Tabla devices:")
    cursor.execute("SELECT * FROM devices")
    for row in cursor.fetchall():
        print(row)

    print("\n📂 Tabla credentials:")
    cursor.execute("SELECT * FROM credentials")
    for row in cursor.fetchall():
        print(row)

    print("\n📂 Tabla device_logs:")
    cursor.execute("SELECT * FROM device_logs")
    for row in cursor.fetchall():
        print(row)

    print("\n📂 Tabla interfaces:")
    cursor.execute("SELECT * FROM interfaces")
    for row in cursor.fetchall():
        print(row)

    conn.close()


# -----------------------------
# Funciones auxiliares
# -----------------------------
def get_connection():
    """Devuelve una conexión abierta a la DB"""
    return sqlite3.connect(DB_PATH)


def get_all_devices():
    """Devuelve todos los dispositivos registrados en la DB"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, hostname, ip, mac FROM devices")
    devices = cursor.fetchall()
    conn.close()
    return devices


def delete_all_data():
    """Elimina todos los registros de todas las tablas"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for table in ["credentials", "interfaces", "device_logs", "devices"]:
        cursor.execute(f"DELETE FROM {table}")
    conn.commit()
    conn.close()


from tabulate import tabulate

def show_devices_table():
    """Muestra los dispositivos registrados en forma de tabla."""
    devices = get_all_devices()
    if not devices:
        print("No hay dispositivos registrados.")
        return
    
    headers = ["ID", "Hostname", "IP", "MAC"]
    print("\n" + tabulate(devices, headers=headers, tablefmt="fancy_grid") + "\n")
