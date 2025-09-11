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
    """Guarda o actualiza un dispositivo en la base de datos, evitando duplicados por IP."""
    inicializar_db()
    # Leer registros existentes
    registros = []
    with open(ARCHIVO_DB, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        registros = list(reader)

    # Revisar si la IP ya existe
    for registro in registros:
        if registro["IP"] == ip:
            # Actualizar campos existentes
            registro.update({
                "MAC": mac,
                "Red": red,
                "Hostname": hostname,
                "Usuario": usuario,
                "Password": password
            })
            break
    else:
        # Si no existe, agregar nuevo
        registros.append({
            "IP": ip,
            "MAC": mac,
            "Red": red,
            "Hostname": hostname,
            "Usuario": usuario,
            "Password": password
        })

    # Guardar todos los registros de nuevo
    with open(ARCHIVO_DB, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["IP", "MAC", "Red", "Hostname", "Usuario", "Password"])
        writer.writeheader()
        writer.writerows(registros)

    print(f"💾 Dispositivo {hostname} ({ip}) guardado/actualizado en la DB")

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
