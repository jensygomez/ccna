# modules/bastion_router/bastion_connection.py

from netmiko import ConnectHandler, NetMikoAuthenticationException, NetMikoTimeoutException

# ---- Configuración del Bastion ----
BASTION = {
    "device_type": "cisco_ios",
    "host": "192.168.18.110",
    "username": "bastion",
    "password": "bastion",
    "secret": "bastion",
}

def connect_to_bastion():
    """
    Conecta al Bastion vía SSH, ejecuta show ip interface brief y retorna la salida.
    """
    try:
        print("🔹 Connecting to Bastion via SSH...")
        net_connect = ConnectHandler(**BASTION)
        net_connect.enable()
        print("✅ Connected to Bastion")

        # Comando de prueba
        output = net_connect.send_command("show ip interface brief")
        net_connect.disconnect()
        print("🔹 Disconnected from Bastion")
        return output
    except (NetMikoAuthenticationException, NetMikoTimeoutException) as e:
        print(f"⚠ SSH failed: {e}")
        return None
    except Exception as e:
        print(f"⚠ Other error: {e}")
        return None
