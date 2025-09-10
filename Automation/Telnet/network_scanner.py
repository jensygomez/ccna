# network_scanner.py
import subprocess
import re
import csv
import ipaddress
from datetime import datetime
import threading
import time


def escanear_dispositivo(ip, resultados, lock, total_dispositivos, progreso_actual):
    """
    Escanea un dispositivo individual y actualiza el progreso
    """
    try:
        # Ejecutar ping (1 intento, timeout de 1 segundo)
        result = subprocess.run(['ping', '-n', '1', '-w', '1000', ip],
                                capture_output=True, text=True)

        if "TTL=" in result.stdout or "ttl=" in result.stdout.lower():
            mac = get_mac_address(ip)
            tipo = identify_device_type(ip, mac)
            nombre = generar_hostname(ip, tipo)

            with lock:
                resultados.append({
                    'ip': ip,
                    'mac': mac,
                    'tipo': tipo,
                    'nombre': nombre,
                    'estado': 'activo'
                })
                print(f"✅ [{progreso_actual[0]}/{total_dispositivos}] {ip} ({nombre}) - {tipo}")
        else:
            with lock:
                resultados.append({
                    'ip': ip,
                    'mac': 'Desconocida',
                    'tipo': 'Inactivo',
                    'nombre': f'Inactive-{ip.split(".")[-1]}',
                    'estado': 'inactivo'
                })
                print(f"❌ [{progreso_actual[0]}/{total_dispositivos}] {ip} - Inactivo")

    except Exception as e:
        with lock:
            resultados.append({
                'ip': ip,
                'mac': 'Error',
                'tipo': 'Error',
                'nombre': f'Error-{ip.split(".")[-1]}',
                'estado': 'error'
            })
            print(f"⚠️  [{progreso_actual[0]}/{total_dispositivos}] {ip} - Error: {e}")

    finally:
        with lock:
            progreso_actual[0] += 1


def mostrar_barra_progreso(actual, total, longitud=50):
    """
    Muestra una barra de progreso visual
    """
    porcentaje = actual / total
    barras_llenas = int(longitud * porcentaje)
    barras_vacias = longitud - barras_llenas
    barra = "█" * barras_llenas + "░" * barras_vacias
    return f"[{barra}] {porcentaje:.1%} ({actual}/{total})"


def scan_network(network_cidr="192.168.0.0/24", max_hilos=10):
    """
    Escanea la red para descubrir dispositivos activos con visualización mejorada
    """
    resultados = []
    lock = threading.Lock()

    print(f"🔍 Escaneando red {network_cidr}...")
    print("=" * 60)

    try:
        # Obtener todos los hosts de la red
        network = ipaddress.ip_network(network_cidr)
        hosts = [str(ip) for ip in network.hosts()]
        total_dispositivos = len(hosts)

        # Variable compartida para el progreso
        progreso_actual = [0]

        # Mostrar información inicial
        print(f"📊 Total de dispositivos a escanear: {total_dispositivos}")
        print(f"🚀 Iniciando escaneo con {max_hilos} hilos simultáneos...")
        print()

        # Crear y iniciar hilos
        hilos = []
        for i, ip in enumerate(hosts):
            # Esperar si hay demasiados hilos activos
            while threading.active_count() > max_hilos + 1:
                time.sleep(0.1)
                # Actualizar barra de progreso periódicamente
                if threading.active_count() <= max_hilos + 1:
                    with lock:
                        actual = progreso_actual[0]
                        print(f"\r📈 Progreso: {mostrar_barra_progreso(actual, total_dispositivos)}", end="", flush=True)

            # Crear nuevo hilo
            hilo = threading.Thread(
                target=escanear_dispositivo,
                args=(ip, resultados, lock, total_dispositivos, progreso_actual)
            )
            hilo.daemon = True
            hilo.start()
            hilos.append(hilo)

        # Esperar a que todos los hilos terminen
        for hilo in hilos:
            hilo.join()

        # Mostrar barra de progreso final
        print(f"\r📈 Progreso: {mostrar_barra_progreso(total_dispositivos, total_dispositivos)}")

    except Exception as e:
        print(f"❌ Error durante el escaneo: {e}")

    # Filtrar solo dispositivos activos
    dispositivos_activos = [r for r in resultados if r['estado'] == 'activo']

    print("=" * 60)
    print(f"🎯 Escaneo completado!")
    print(f"✅ Dispositivos activos: {len(dispositivos_activos)}")
    print(f"❌ Dispositivos inactivos: {len(resultados) - len(dispositivos_activos)}")

    return [d['ip'] for d in dispositivos_activos]


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


def generar_hostname(ip, tipo):
    """
    Genera un nombre de host basado en el tipo y la IP
    """
    ultimo_octeto = ip.split('.')[-1]

    if tipo == "Router":
        return f"Router-{ultimo_octeto}"
    elif tipo == "Switch":
        return f"Switch-{ultimo_octeto}"
    elif tipo == "Bastion":
        return f"Bastion-{ultimo_octeto}"
    elif tipo == "Desconocido":
        return f"Unknown-{ultimo_octeto}"
    else:
        return f"Device-{ultimo_octeto}"


def mostrar_resumen_escaneo(dispositivos_activos):
    """
    Muestra un resumen bonito de los dispositivos encontrados
    """
    if not dispositivos_activos:
        print("📭 No se encontraron dispositivos activos")
        return

    print("\n" + "=" * 60)
    print("📋 RESUMEN DE DISPOSITIVOS ACTIVOS")
    print("=" * 60)

    for i, ip in enumerate(dispositivos_activos, 1):
        mac = get_mac_address(ip)
        tipo = identify_device_type(ip, mac)
        nombre = generar_hostname(ip, tipo)

        emoji = "🖥️ " if tipo == "Otro" else "🔄" if tipo == "Router" else "🔀" if tipo == "Switch" else "🛡️ " if tipo == "Bastion" else "❓"

        print(f"{emoji} {i:2d}. {ip:15} → {nombre:15} ({tipo:10}) - MAC: {mac}")


def update_devices_database(active_devices, db_file="db/dispositivos.csv"):
    """
    Actualiza la base de datos con los dispositivos encontrados
    """
    # Leer dispositivos existentes
    existing_devices = {}
    try:
        with open(db_file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                existing_devices[row['IP']] = row
    except FileNotFoundError:
        print("⚠️  Base de datos no encontrada, creando nueva...")

    # Procesar dispositivos activos
    updated_devices = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    nuevos = 0
    actualizados = 0

    for ip in active_devices:
        mac = get_mac_address(ip)
        device_type = identify_device_type(ip, mac)
        hostname = generar_hostname(ip, device_type)

        # Si el dispositivo ya existe, mantener sus datos pero actualizar timestamp
        if ip in existing_devices:
            device_data = existing_devices[ip]
            device_data['ÚltimaActualización'] = now
            actualizados += 1
        else:
            device_data = {
                'MAC': mac,
                'IP': ip,
                'Hostname': hostname,
                'Tipo': device_type,
                'ÚltimaActualización': now
            }
            nuevos += 1

        updated_devices.append(device_data)

    # Escribir la base de datos actualizada
    fieldnames = ['MAC', 'IP', 'Hostname', 'Tipo', 'ÚltimaActualización']

    try:
        with open(db_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_devices)

        print(f"\n💾 Base de datos actualizada:")
        print(f"   ✅ Dispositivos totales: {len(updated_devices)}")
        print(f"   ➕ Nuevos dispositivos: {nuevos}")
        print(f"   🔄 Dispositivos actualizados: {actualizados}")
        return True

    except Exception as e:
        print(f"❌ Error guardando base de datos: {e}")
        return False


def scan_and_update(network_cidr="192.168.0.0/24"):
    """
    Función principal para escanear y actualizar la base de datos
    """
    print("🚀 Iniciando escaneo de red...")
    print("⏰ Esto puede tomar varios minutos...")
    print()

    active_devices = scan_network(network_cidr)

    if active_devices:
        # Mostrar resumen detallado
        mostrar_resumen_escaneo(active_devices)

        # Preguntar si actualizar la base de datos
        print("\n" + "=" * 60)
        response = input("¿Desea actualizar la base de datos con estos dispositivos? (s/n): ").strip().lower()

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