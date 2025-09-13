
#Netmiko/modules/scanner/network_scanner.py
from scapy.all import ARP, Ether, srp

def scan_network(network_range="192.168.0.0/24"):
    """
    Escanea la red dada y devuelve una lista de dispositivos activos.
    Cada dispositivo será un diccionario con {ip, mac}.
    """
    print(f"📡 Escaneando red {network_range}...")

    # Crear paquete ARP
    arp = ARP(pdst=network_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    # Enviar paquete y recibir respuesta
    result = srp(packet, timeout=2, verbose=0)[0]

    devices = []
    for sent, received in result:
        devices.append({
            "ip": received.psrc,
            "mac": received.hwsrc
        })

    return devices


if __name__ == "__main__":
    # Test rápido si lo ejecutas directamente
    found = scan_network("192.168.0.0/24")
    print("\n🔍 Dispositivos encontrados:")
    for dev in found:
        print(f" - IP: {dev['ip']}, MAC: {dev['mac']}")
