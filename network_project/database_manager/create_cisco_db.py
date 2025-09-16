# network_project/database_manager/create_cisco_db.py
import sqlite3

DB_FILE = "cisco_inventory.db"

def create_tables():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # -------------------------------
    # Tabla principal de dispositivos
    # -------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        type TEXT NOT NULL,
        ip_management TEXT,
        username TEXT,
        password TEXT
    )
    """)

    # -------------------------------
    # Interfaces de cada dispositivo
    # -------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interfaces (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        ip TEXT,
        status TEXT,
        mode TEXT,
        description TEXT,
        FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE,
        UNIQUE(device_id, name)
    )
    """)

    # -------------------------------
    # VLANs disponibles
    # -------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vlans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        number INTEGER NOT NULL UNIQUE,
        description TEXT
    )
    """)

    # -------------------------------
    # Relación N:M dispositivos - VLANs
    # -------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS device_vlans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER NOT NULL,
        vlan_id INTEGER NOT NULL,
        interfaces TEXT,  -- opcional: lista de interfaces que usan esta VLAN
        FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE,
        FOREIGN KEY (vlan_id) REFERENCES vlans(id) ON DELETE CASCADE,
        UNIQUE(device_id, vlan_id)
    )
    """)

    # -------------------------------
    # Protocolos soportados
    # -------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS protocols (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT
    )
    """)

    # -------------------------------
    # Relación N:M dispositivos - protocolos
    # -------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS device_protocols (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER NOT NULL,
        protocol_id INTEGER NOT NULL,
        config TEXT, -- campo libre para guardar detalles de configuración
        FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE,
        FOREIGN KEY (protocol_id) REFERENCES protocols(id) ON DELETE CASCADE,
        UNIQUE(device_id, protocol_id)
    )
    """)

    # -------------------------------
    # Rutas estáticas
    # -------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS routes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER NOT NULL,
        destination TEXT NOT NULL,
        mask TEXT NOT NULL,
        next_hop TEXT NOT NULL,
        protocol TEXT,
        FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
    )
    """)

    # -------------------------------
    # Enlaces físicos entre interfaces
    # -------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        interface_a_id INTEGER NOT NULL,
        interface_b_id INTEGER NOT NULL,
        description TEXT,
        FOREIGN KEY (interface_a_id) REFERENCES interfaces(id) ON DELETE CASCADE,
        FOREIGN KEY (interface_b_id) REFERENCES interfaces(id) ON DELETE CASCADE,
        UNIQUE(interface_a_id, interface_b_id)
    )
    """)

    # -------------------------------
    # Atributos extra dinámicos
    # -------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS extra_attributes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER NOT NULL,
        attribute_name TEXT NOT NULL,
        attribute_value TEXT,
        FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()
    print(f"✅ Base de datos '{DB_FILE}' creada con todas las tablas.")

if __name__ == "__main__":
    create_tables()
