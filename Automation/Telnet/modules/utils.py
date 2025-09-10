# modules/utils.py
import subprocess
import ipaddress
import netifaces

def validar_ip(ip):
    """Validar formato de dirección IP"""
    try:
        ipaddress.ip_address(ip)
        return True
    except:
        return False

def obtener_interfaces_red():
    """Obtiene todas las interfaces de red activas"""
    interfaces = []
    for interface in netifaces.interfaces():
        try:
            # Obtener direcciones IPv4
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                for addr_info in addrs[netifaces.AF_INET]:
                    if 'addr' in addr_info and addr_info['addr'] != '127.0.0.1':
                        interfaces.append({
                            'interface': interface,
                            'ip': addr_info['addr'],
                            'netmask': addr_info.get('netmask', '255.255.255.0'),
                            'gateway': obtener_gateway(interface)
                        })
        except:
            continue
    return interfaces

def obtener_gateway(interface):
    """Obtiene el gateway de una interfaz"""
    try:
        gateways = netifaces.gateways()
        if netifaces.AF_INET in gateways:
            for gw in gateways[netifaces.AF_INET]:
                if gw[1] == interface:
                    return gw[0]
    except:
        return None
    return None

def calcular_cidr(netmask):
    """Convierte máscara de red a notación CIDR"""
    try:
        return sum(bin(int(x)).count('1') for x in netmask.split('.'))
    except:
        return 24  # Valor por defecto