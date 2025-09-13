#Netmiko/core/scanner.py
import os
import platform
import ipaddress

def ping_host(ip):
    """
    Verifica si un host responde al ping.
    """
    param = "-n 1" if platform.system().lower() == "windows" else "-c 1 -W 1"
    command = f"ping {param} {ip} > /dev/null 2>&1"
    return os.system(command) == 0

def scan_network(network_cidr):
    """
    Escanea una red completa y devuelve una lista de IPs activas.
    """
    network = ipaddress.ip_network(network_cidr, strict=False)
    active_hosts = []

    for host in network.hosts():
        if ping_host(str(host)):
            active_hosts.append(str(host))

    return active_hosts
