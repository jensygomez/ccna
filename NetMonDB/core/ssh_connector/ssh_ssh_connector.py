# NetMonDB/core/ssh_connector/ssh_ssh_connector.py

# core/ssh_connector/ssh_ssh_connector.py
from netmiko import ConnectHandler

def connect_and_get_running_config(ip, username, password):
    device = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": username,
        "password": password,
    }

    print(f"🔌 Conectando a {ip} vía SSH...")
    net_connect = ConnectHandler(**device)
    output = net_connect.send_command("show running-config")
    net_connect.disconnect()
    print("✅ Conexión finalizada.")
    return output
