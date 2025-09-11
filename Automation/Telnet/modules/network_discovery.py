# modules/network_discovery.py
import netifaces
import ipaddress


def obtener_interfaces_red():
    """Obtiene todas las interfaces de red disponibles"""
    try:
        interfaces = netifaces.interfaces()
        return [iface for iface in interfaces if iface != 'lo']  # Excluir loopback
    except:
        return ['eth0', 'wlan0']  # Fallback


def obtener_direccion_ip(interface):
    """Obtiene la dirección IP de una interfaz específica"""
    try:
        addrs = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addrs:
            return addrs[netifaces.AF_INET][0]['addr']
    except:
        return None
    return None


def descubrir_redes_locales():
    """Descubre todas las redes locales disponibles"""
    print("🔍 Detectando redes locales...")

    interfaces = obtener_interfaces_red()
    redes = []

    for interface in interfaces:
        ip = obtener_direccion_ip(interface)
        if ip and ip != '127.0.0.1':  # Excluir localhost
            try:
                # Asumir máscara /24 para redes comunes
                net = ipaddress.IPv4Network(f"{ip}/24", strict=False)
                redes.append({
                    'interface': interface,
                    'ip': ip,
                    'red': str(net.network_address),
                    'mascara': '255.255.255.0',
                    'hosts': net.num_addresses - 2
                })
                print(f"   ✅ Interfaz {interface}: {ip} -> Red {net.network_address}/24")
            except Exception as e:
                print(f"   ⚠️  Error en interfaz {interface}: {e}")
                continue

    if not redes:
        print("   ℹ️  No se encontraron redes locales, usando red por defecto")
        redes.append({
            'interface': 'eth0',
            'ip': '192.168.1.100',
            'red': '192.168.1.0',
            'mascara': '255.255.255.0',
            'hosts': 254
        })

    return redes


# Función auxiliar para mostrar redes
def mostrar_redes(redes):
    """Muestra la información de las redes detectadas"""
    print("\n📊 REDES LOCALES DETECTADAS:")
    print("=" * 50)
    for i, red in enumerate(redes, 1):
        print(f"{i}. Interfaz: {red['interface']}")
        print(f"   IP: {red['ip']}")
        print(f"   Red: {red['red']}/{red['mascara']}")
        print(f"   Hosts posibles: {red['hosts']}")
        print("-" * 30)