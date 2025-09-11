import csv
import os

ARCHIVO_DB = "dispositivos.csv"

def inicializar_db():
    """Crea el archivo CSV si no existe con cabecera."""
    if not os.path.exists(ARCHIVO_DB):
        with open(ARCHIVO_DB, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["IP", "MAC", "Red", "Hostname", "Usuario", "Password"])
        print(f"✅ Base de datos creada: {ARCHIVO_DB}")


def guardar_dispositivo(ip, mac, red, hostname="N/A", usuario="cisco", password="cisco123"):
    """Guarda un nuevo dispositivo en la base de datos."""
    inicializar_db()
    with open(ARCHIVO_DB, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([ip, mac, red, hostname, usuario, password])
    print(f"💾 Dispositivo {hostname} ({ip}) guardado en la DB")


def obtener_redes_de_db():
    """Lee todas las redes únicas desde la base de datos."""
    inicializar_db()
    redes = set()
    with open(ARCHIVO_DB, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            redes.add(row["Red"])
    return list(redes)


def obtener_dispositivos_por_red(red):
    """Devuelve todos los dispositivos de una red en particular."""
    inicializar_db()
    dispositivos = []
    with open(ARCHIVO_DB, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Red"] == red:
                dispositivos.append(row)
    return dispositivos
