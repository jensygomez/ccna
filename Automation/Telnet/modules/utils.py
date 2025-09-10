# modules/utils.py (agregar estas funciones)
import csv
import os


def leer_base_datos(db_path="db/dispositivos.csv"):
    """Lee la base de datos de dispositivos"""
    dispositivos = []

    if not os.path.exists(db_path):
        print("⚠️  Base de datos no encontrada. Usando valores por defecto.")
        return dispositivos

    try:
        with open(db_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                dispositivos.append(row)
        return dispositivos
    except Exception as e:
        print(f"❌ Error leyendo base de datos: {e}")
        return []


def obtener_redes_de_db(dispositivos):
    """Extrae las redes únicas de la base de datos"""
    redes = set()

    for dispositivo in dispositivos:
        ip = dispositivo.get('IP', '')
        if ip and '.' in ip:
            # Extraer red (primeros 3 octetos)
            octetos = ip.split('.')
            if len(octetos) == 4:
                red = f"{octetos[0]}.{octetos[1]}.{octetos[2]}.0/24"
                redes.add(red)

    return list(redes)


def obtener_dispositivos_por_red(dispositivos, red):
    """Filtra dispositivos por red"""
    dispositivos_red = []
    red_base = red.split('.0/24')[0]  # Ej: 192.168.0.0/24 → 192.168.0

    for dispositivo in dispositivos:
        ip = dispositivo.get('IP', '')
        if ip and ip.startswith(red_base):
            dispositivos_red.append(dispositivo)

    return dispositivos_red