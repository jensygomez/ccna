# network_project/database_manager/db_crud.py


# db_crud.py
from .db_manager import connect

# ---------------------------
# FUNCIONES GENÉRICAS CRUD
# ---------------------------

def list_records(table, columns="*", where=None):
    """
    Lista registros de cualquier tabla.
    `columns` -> lista de columnas o "*" para todo
    `where` -> condición opcional, ejemplo: "id=1"
    """
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT {columns} FROM {table}"
    if where:
        query += f" WHERE {where}"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


def update_record(table, record_id, **fields):
    """
    Actualiza cualquier registro de cualquier tabla.
    `table` -> nombre de la tabla
    `record_id` -> id del registro
    `fields` -> diccionario {columna: valor}
    """
    if not fields:
        return
    conn = connect()
    cursor = conn.cursor()
    set_clause = ", ".join(f"{k}=?" for k in fields.keys())
    values = list(fields.values()) + [record_id]
    cursor.execute(f"UPDATE {table} SET {set_clause} WHERE id=?", values)
    conn.commit()
    conn.close()


def delete_record(table, record_id):
    """
    Elimina cualquier registro de cualquier tabla por ID.
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table} WHERE id=?", (record_id,))
    conn.commit()
    conn.close()
