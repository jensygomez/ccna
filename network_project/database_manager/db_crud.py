# network_project/database_manager/db_crud.py


# network_project/database_manager/db_crud.py
from database_manager.db_manager import connect  # Importar connect correctamente

# ---------------------------
# CRUD genérico para cualquier tabla
# ---------------------------
def list_all(table):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_by_id(table, record_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table} WHERE id=?", (record_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def update_by_id(table, record_id, **kwargs):
    if not kwargs:
        return
    conn = connect()
    cursor = conn.cursor()
    fields = [f"{k}=?" for k in kwargs.keys()]
    values = list(kwargs.values())
    values.append(record_id)
    cursor.execute(f"UPDATE {table} SET {', '.join(fields)} WHERE id=?", values)
    conn.commit()
    conn.close()

def delete_by_id(table, record_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table} WHERE id=?", (record_id,))
    conn.commit()
    conn.close()
