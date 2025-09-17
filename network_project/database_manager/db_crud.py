# network_project/database_manager/db_crud.py

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "cisco_inventory.db")

def connect():
    return sqlite3.connect(DB_PATH)

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

def insert(table, **kwargs):
    conn = connect()
    cursor = conn.cursor()
    keys = ", ".join(kwargs.keys())
    placeholders = ", ".join("?" for _ in kwargs)
    values = tuple(kwargs.values())
    cursor.execute(f"INSERT INTO {table} ({keys}) VALUES ({placeholders})", values)
    conn.commit()
    conn.close()

def update_by_id(table, record_id, **kwargs):
    if not kwargs:
        return
    conn = connect()
    cursor = conn.cursor()
    fields = ", ".join(f"{k}=?" for k in kwargs.keys())
    values = list(kwargs.values())
    values.append(record_id)
    cursor.execute(f"UPDATE {table} SET {fields} WHERE id=?", values)
    conn.commit()
    conn.close()

def delete_by_id(table, record_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table} WHERE id=?", (record_id,))
    conn.commit()
    conn.close()
