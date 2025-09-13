import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "net_devices.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Agregar columna registered_at si no existe
try:
    cursor.execute("ALTER TABLE devices ADD COLUMN registered_at TIMESTAMP")
    print("✅ Columna 'registered_at' agregada a devices")
except sqlite3.OperationalError:
    print("⚠ Columna 'registered_at' ya existe")

conn.commit()
conn.close()
