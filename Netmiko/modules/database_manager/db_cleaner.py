# modules/database_manager/db_cleaner.py
from modules.database_manager.db_utils import init_db, DB_PATH
import sqlite3

def clean_db():
    # Inicializar DB (crea tablas si no existen)
    init_db()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Borrar todo el contenido
    cursor.execute("DELETE FROM logs")
    cursor.execute("DELETE FROM interfaces")
    cursor.execute("DELETE FROM devices")

    # Reiniciar autoincremento de cada tabla
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='devices'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='interfaces'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='logs'")

    conn.commit()
    conn.close()
    print("✅ Base de datos completamente limpia. Los IDs se reiniciarán desde 1.")

# ------------------------------
# Función main exportable
# ------------------------------
def main():
    clean_db()

# Mantener ejecución directa
if __name__ == "__main__":
    main()
