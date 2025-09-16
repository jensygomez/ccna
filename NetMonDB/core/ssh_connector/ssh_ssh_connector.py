# NetMonDB/core/ssh_connector/ssh_ssh_connector.py

from netmiko import ConnectHandler

def connect_device(host, username, password, command):
    device = {
        "device_type": "cisco_ios",
        "host": host,
        "username": username,
        "password": password,
    }
    try:
        conn = ConnectHandler(**device)
        output = conn.send_command(command)
        conn.disconnect()
        return output
    except Exception as e:
        print(f"❌ Error al conectar al dispositivo: {e}")
        return None
