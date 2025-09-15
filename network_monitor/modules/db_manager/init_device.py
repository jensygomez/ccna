# network_monitor/modules/db_manager/init_device.py


# network_monitor/modules/db_manager/init_device.py

from modules.db_manager.database import save_device_and_credentials, save_interfaces, init_db
import ipaddress

def expand_interface(iface):
    """Convierte abreviaturas como g0/0 o e0/0 en nombres completos de interfaz."""
    if iface.lower().startswith("g"):
        return iface.replace("g", "GigabitEthernet", 1)
    elif iface.lower().startswith("e"):
        return iface.replace("e", "Ethernet", 1)
    return iface

def add_new_device():
    """Flujo para agregar un nuevo dispositivo desde cero."""
    init_db()  # Asegurarse de que la DB exista

    # --- Tipo de dispositivo ---
    device_type = None
    while True:
        print("\nSeleccione el tipo de dispositivo:")
        print("1. Router")
        print("2. Switch")
        choice = input("Ingrese opción (1 o 2): ").strip()
        if choice == "1":
            device_type = "router"
            break
        elif choice == "2":
            device_type = "switch"
            break
        print("Opción inválida, ingrese 1 o 2.")

    # --- Hostname ---
    hostname = input("Hostname del dispositivo: ").strip()

    # --- Interfaz principal ---
    iface_input = input("Interfaz principal (ej: g0/0, e0/0): ").strip()
    interface = expand_interface(iface_input)

    # --- IP y máscara ---
    while True:
        ip_input = input(f"IP para {interface}: ").strip()
        try:
            ip = str(ipaddress.IPv4Address(ip_input))
            break
        except ValueError:
            print("IP inválida, intente nuevamente.")

    while True:
        mask_input = input(f"Máscara para {interface} (ej: 255.255.255.0): ").strip()
        try:
            mask = str(ipaddress.IPv4Network(f"0.0.0.0/{mask_input}", strict=False).netmask)
            break
        except ValueError:
            print("Máscara inválida, intente nuevamente.")

    # --- Gateway ---
    gateway = input("IP del gateway por defecto: ").strip()

    # --- Credenciales ---
    username = input("Usuario admin: ").strip()
    password = input("Contraseña admin: ").strip()

    # --- Generar configuración ---
    cfg_lines = [
        "configure terminal",
        f"hostname {hostname}",
        "lldp run",
        f"interface {interface}",
        f" description Interfaz principal",
        f" ip address {ip} {mask}",
        " no shutdown",
        f"ip route 0.0.0.0 0.0.0.0 {gateway}",
        "ip domain-name lab.local",
        "crypto key generate rsa modulus 1024",
        "ip ssh version 2",
        "line vty 0 4",
        " login local",
        " transport input telnet ssh",
        f"username {username} privilege 15 secret {password}",
        f"enable secret {password}",
        "end",
        "write memory"
    ]

    print("\n🖨️ Configuración generada para copiar al dispositivo:\n")
    print("\n".join(cfg_lines))

    # --- Guardar en DB ---
    save_device_and_credentials(ip, hostname, None, username, password)
    save_interfaces(ip, [{"name": interface, "ip": ip, "status": "up", "protocol": "up"}])
    print("\n✅ Dispositivo guardado en la base de datos con éxito.")
