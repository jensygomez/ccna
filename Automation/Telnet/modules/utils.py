# modules/utils.py
import subprocess
import re
import csv
import os


def validar_ip(ip):
    """Validar formato de dirección IP"""
    try:
        import ipaddress
        ipaddress.ip_address(ip)
        return True
    except:
        return False


def obtener_interfaces_red():
    """Obtiene todas las interfaces de red activas usando comandos del sistema"""
    interfaces = []

    try:
        # Obtener interfaces en Linux
        result = subprocess.run(['ip', 'addr', 'show'], capture_output=True, text=True)
        output = result.stdout

        # Parsear la salida
        current_interface = None
        for line in output.split('\n'):
            # Buscar líneas de interfaz
            if match := re.match(r'^\d+:\s+(\w+):', line):
                current_interface = match.group(1)

            # Buscar direcciones IPv4
            elif current_interface and 'inet ' in line:
                if match := re.search(r'inet (\d+\.\d+\.\d+\.\d+)/(\d+)', line):
                    ip = match.group(1)
                    cidr = match.group(2)
                    interfaces.append({
                        'interface': current_interface,
                        'ip': ip,
                        'netmask': cidr_a_netmask(int(cidr)),
                        'cidr': int(cidr),
                        'gateway': obtener_gateway_linux(current_interface)
                    })

    except Exception as e:
        print(f"⚠️ Error obteniendo interfaces: {e}")

    return interfaces


def cidr_a_netmask(cidr):
    """Convierte CIDR a máscara de red"""
    bits = 0xffffffff ^ (1 << 32 - cidr) - 1
    return f"{(bits >> 24) & 0xff}.{(bits >> 16) & 0xff}.{(bits >> 8) & 0xff}.{bits & 0xff}"


def obtener_gateway_linux(interface):
    """Obtiene el gateway para una interfaz en Linux"""
    try:
        result = subprocess.run(['ip', 'route', 'show', 'default'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if f'dev {interface}' in line:
                if match := re.search(r'via (\d+\.\d+\.\d+\.\d+)', line):
                    return match.group(1)
    except:
        pass
    return None


def calcular_cidr(netmask):
    """Convierte máscara de red a notación CIDR"""
    try:
        if isinstance(netmask, str) and '.' in netmask:
            # Es una máscara de red (255.255.255.0)
            return sum(bin(int(x)).count('1') for x in netmask.split('.'))
        else:
            # Ya es un número CIDR
            return int(netmask)
    except:
        return 24  # Valor por defecto


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


def normalizar_red(red_input):
    """Asegura que la red tenga formato CIDR"""
    if '/' not in red_input:
        if red_input.endswith('.0'):
            return red_input + '/24'
        else:
            octetos = red_input.split('.')
            if len(octetos) == 4:
                return '.'.join(octetos[:3]) + '.0/24'
    return red_input