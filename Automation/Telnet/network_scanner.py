# network_scanner.py
import subprocess
import re
import csv
import ipaddress
from datetime import datetime


def scan_network(network_cidr="192.168.0.0/24"):
    """
    Escanea la red para descubrir dispositivos activos
    """
    active_devices = []

    print(f"🔍 Escaneando red {network_cidr}...")

    try:
        # Ejecutar ping a todos los hosts en la red
        network = ipaddress.ip_network(network_cidr)

        for ip in network.hosts():
            ip_str = str(ip)

            # Ejecutar ping (1 intento, timeout de 1 segundo)
            result = subprocess.run(['ping', '-n', '1', '-w', '1000', ip_str],
                                    capture_output=True, text=True)

            if "TTL=" in result.stdout or "ttl=" in result.stdout.lower():
                print(f"✅ Host activo encontrado: {ip_str}")
                active_devices.append(ip_str)
            else:
                print(f"❌ Host inactivo: {ip_str}")

    except Exception as e:
        print(f"Error durante el escaneo: {e}")

    return active_devices


def get_mac_address(ip):
    """
    Intenta obtener la dirección MAC de un dispositivo (solo Windows)
    """
    try:
        # Ejecutar arp -a para obtener la tabla ARP
        result = subprocess.run(['arp', '-a', ip], capture_output=True, text=True)

        # Buscar patrones MAC en la salida
        mac_pattern = r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})"
        match = re.search(mac_pattern, result.stdout)

        if match:
            return match.group(0).replace('-', ':').upper()
        else:
            return "Desconocida"

    except Exception as e:
        print(f"Error obteniendo MAC para {ip}: {e}")
        return "Desconocida"


def identify_device_type(ip, mac):
    """
    Intenta identificar el tipo de dispositivo basado en IP y MAC
    """
    # Patrones para identificar tipos de dispositivos por MAC
    cisco_mac_patterns = [
        r'^00:1A:2B', r'^00:1A:A1', r'^00:1A:A2', r'^00:1C:58',
        r'^00:1D:45', r'^00:1E:7D', r'^00:1E:F6', r'^00:21:55',
        r'^00:22:55', r'^00:23:04', r'^00:23:EB', r'^00:24:14'
    ]

    for pattern in cisco_mac_patterns:
        if re.match(pattern, mac, re.IGNORECASE):
            return "Router" if "101" in ip or "102" in ip or "103" in ip else "Switch"

    # Si no es Cisco, intentar identificar por otros patrones
    if ip.startswith("192.168.0.1"):
        return "Bastion"
    elif "Desconocida" in mac:
        return "Desconocido"
    else:
        return "Otro"


def update_devices_database(active_devices, db_file="db/dispositivos.csv"):
    """
    Actualiza la base de datos con los dispositivos encontrados
    """
    # Leer dispositivos existentes
    existing_devices = {}
    try:
        with open(db_file, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                existing_devices[row['IP']] = row
    except FileNotFoundError:
        print("⚠️  Base de datos no encontrada, creando nueva...")

    # Procesar dispositivos activos
    updated_devices = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    for ip in active_devices:
        mac = get_mac_address(ip)
        device_type = identify_device_type(ip, mac)

        # Generar hostname basado en el tipo
        if device_type == "Router":
            hostname = f"Router-{ip.split('.')[-1]}"
        elif device_type == "Switch":
            hostname = f"Switch-{ip.split('.')[-1]}"
        elif device_type == "Bastion":
            hostname = f"Bastion-{ip.split('.')[-1]}"
        else:
            hostname = f"Device-{ip.split('.')[-1]}"

        # Si el dispositivo ya existe, mantener sus datos pero actualizar timestamp
        if ip in existing_devices:
            device_data = existing_devices[ip]
            device_data['ÚltimaActualización'] = now
            print(f"📝 Actualizando dispositivo existente: {ip} ({hostname})")
        else:
            device_data = {
                'MAC': mac,
                'IP': ip,
                'Hostname': hostname,
                'Tipo': device_type,
                'ÚltimaActualización': now
            }
            print(f"➕ Nuevo dispositivo añadido: {ip} ({hostname})")

        updated_devices.append(device_data)

    # Escribir la base de datos actualizada
    fieldnames = ['MAC', 'IP', 'Hostname', 'Tipo', 'ÚltimaActualización']

    try:
        with open(db_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_devices)

        print(f"💾 Base de datos actualizada con {len(updated_devices)} dispositivos")
        return True

    except Exception as e:
        print(f"❌ Error guardando base de datos: {e}")
        return False


def scan_and_update(network_cidr="192.168.0.0/24"):
    """
    Función principal para escanear y actualizar la base de datos
    """
    print("🚀 Iniciando escaneo de red...")
    active_devices = scan_network(network_cidr)

    if active_devices:
        print(f"\n📊 Dispositivos activos encontrados: {len(active_devices)}")
        for device in active_devices:
            print(f"   - {device}")

        # Preguntar si actualizar la base de datos
        response = input("\n¿Desea actualizar la base de datos? (s/n): ").strip().lower()
        if response == 's':
            success = update_devices_database(active_devices)
            if success:
                print("✅ Base de datos actualizada correctamente")
            else:
                print("❌ Error al actualizar la base de datos")
        else:
            print("⚠️  Base de datos no actualizada")
    else:
        print("❌ No se encontraron dispositivos activos en la red")


if __name__ == "__main__":
    scan_and_update()