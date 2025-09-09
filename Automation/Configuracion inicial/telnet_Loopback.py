import getpass
import telnetlib
import time

HOST = "192.168.0.102"


def configure_router():
    try:
        print("Conectando al router...")
        tn = telnetlib.Telnet(HOST, timeout=10)

        print("Haciendo login...")
        tn.read_until(b"Username: ", timeout=5)
        tn.write(user.encode('ascii') + b"\n")

        tn.read_until(b"Password: ", timeout=5)
        tn.write(password.encode('ascii') + b"\n")

        # Esperar prompt de comando (#)
        tn.read_until(b"#", timeout=5)
        print("Login exitoso!")

        # Enviar comandos con delays
        commands = [
            "configure terminal",
            "interface loopback 0",
            "ip address 1.1.1.1 255.255.255.255",
            "end",
            "write memory"
        ]

        for cmd in commands:
            print(f"Ejecutando: {cmd}")
            tn.write(cmd.encode('ascii') + b"\n")
            time.sleep(5)  # Mayor delay para routers lentos

        print("Esperando confirmación de guardado...")
        time.sleep(5)  # Dar tiempo al router para guardar

        # Leer output disponible (no esperar indefinidamente)
        output = tn.read_very_eager().decode('ascii')
        print("Output del router:")
        print(output)

        tn.write(b"exit\n")  # Cerrar sesión adecuadamente
        tn.close()
        print("Conexión cerrada. Configuración completada!")

    except Exception as e:
        print(f"Error: {e}")
        # Intentar cerrar conexión aunque falle
        try:
            tn.close()
        except:
            pass


if __name__ == "__main__":
    user = input("Usuario: ")
    password = getpass.getpass("Contraseña: ")
    configure_router()