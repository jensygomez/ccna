#!/usr/bin/env python3
"""
Script: network_mapper.py
Propósito: Escanea la red local para detectar dispositivos activos (IP y MAC)
            y prepara la base para conectarse automáticamente a dispositivos Cisco vía SSH.
Autor: Jensy Gomez
Fecha: 2025-08-21

Notas de ejecución:
==================
1) Activar tu entorno virtual DevNet:
   source ~/DevNet/bin/activate

2) Ejecutar el script con permisos root (Scapy requiere acceso a capa 2):
   sudo ~/DevNet/bin/python ~/network_mapper.py

3) Opcional: crear un alias para no escribir todo cada vez:
   alias mapnet='sudo ~/DevNet/bin/python ~/network_mapper.py'
   Luego ejecutar:
   mapnet
"""

import ipaddress
from scapy.all import ARP, Ether, srp

# ==========================
# CONFIGURACIÓN DE LA RED
# ==========================
network_cidr = "192.168.1.0/24"  # Cambia esto a tu subred si es distinta

# ==========================
# FUNCIONES
# ==========================
def scan_network(network):
    """Escanea la red usando ARP y devuelve lista de dispositivos con IP y MAC."""
    print(f"[+] Escaneando la red {network}...")
    arp = ARP(pdst=str(network))
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    # Enviar y recibir paquetes
    result = srp(packet, timeout=2, verbose=0)[0]

    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    return devices

# ==========================
# PROGRAMA PRINCIPAL
# ==========================
def main():
    net = ipaddress.ip_network(network_cidr, strict=False)
    devices = scan_network(net)

    print("\n=== Dispositivos detectados ===")
    for d in devices:
        print(f"IP: {d['ip']}  |  MAC: {d['mac']}")

if __name__ == "__main__":
    main()

