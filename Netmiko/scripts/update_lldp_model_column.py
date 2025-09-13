import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "net_devices.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE lldp_neighbors ADD COLUMN neighbor_model TEXT")
    print("✅ Columna 'neighbor_model' agregada a lldp_neighbors")
except sqlite3.OperationalError:
    print("⚠️ La columna 'neighbor_model' ya existe")
finally:
    conn.commit()
    conn.close()
