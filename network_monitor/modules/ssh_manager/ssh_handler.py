from netmiko import ConnectHandler

def connect_and_run(ip, username, password, command="show version"):
    """
    Establece conexión SSH al dispositivo y ejecuta un comando.
    Retorna la salida del comando o lanza excepción.
    """
    device = {
        "device_type": "cisco_ios",
        "ip": ip,
        "username": username,
        "password": password,
    }

    try:
        print(f"🔌 Conectando al dispositivo {ip} ...")
        connection = ConnectHandler(**device)
        print("✅ Conexión establecida correctamente.")

        # Ejecutar comando
        output = connection.send_command(command)

        connection.disconnect()
        print("🔒 Sesión cerrada.")

        return output

    except Exception as e:
        raise RuntimeError(f"Error al conectar con {ip}: {e}")
