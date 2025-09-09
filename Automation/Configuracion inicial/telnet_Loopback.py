import getpass
import telnetlib
import time
import re


class CiscoTelnetClient:
    def __init__(self, host):
        self.host = host
        self.tn = None
        self.hostname = "Router"
        self.current_mode = "exec"

    def connect(self, username, password):
        """Conectar y hacer login"""
        print(f"🔄 Conectando a {self.host}...")
        self.tn = telnetlib.Telnet(self.host, timeout=10)

        # Login
        self.tn.read_until(b"Username: ", timeout=5)
        self.tn.write(username.encode() + b"\n")

        self.tn.read_until(b"Password: ", timeout=5)
        self.tn.write(password.encode() + b"\n")

        # Detectar hostname del prompt
        output = self.tn.read_until(b"#", timeout=5).decode()
        match = re.search(r'(\S+)#', output)
        if match:
            self.hostname = match.group(1)
        print(f"✅ Login exitoso! Hostname: {self.hostname}")

    def get_prompt(self):
        """Obtener prompt según el modo actual"""
        if self.current_mode == "exec":
            return f"{self.hostname}#"
        elif self.current_mode == "config":
            return f"{self.hostname}(config)#"
        elif self.current_mode == "interface":
            return f"{self.hostname}(config-if)#"
        return f"{self.hostname}#"

    def send_command(self, command, wait_time=5):
        """Enviar comando y leer respuesta"""
        prompt = self.get_prompt()
        print(f"\n📋 {prompt} {command}")

        self.tn.write(command.encode() + b"\n")
        time.sleep(5)

        # Leer respuesta
        output = self.tn.read_until(b"#", timeout=5).decode()
        print(f"📤 Respuesta:\n{output}")

        # Actualizar modo
        if command == "configure terminal":
            self.current_mode = "config"
        elif command.startswith("interface "):
            self.current_mode = "interface"
        elif command == "end":
            self.current_mode = "exec"

        time.sleep(wait_time)
        return output

    def interactive_session(self):
        """Modo interactivo"""
        print(f"\n🎮 Modo interactivo con {self.hostname}")
        print("   Escribe 'exit' para terminar")
        print("=" * 60)

        while True:
            try:
                user_cmd = input(f"{self.get_prompt()} ").strip()
                if user_cmd.lower() in ['exit', 'quit']:
                    break

                self.tn.write(user_cmd.encode() + b"\n")
                output = self.tn.read_until(b"#", timeout=5).decode()
                print(output, end='')

            except KeyboardInterrupt:
                print("\n\n👋 Sesión terminada por usuario")
                break

    def close(self):
        """Cerrar conexión"""
        if self.tn:
            self.tn.write(b"exit\n")
            self.tn.close()
            print("🔌 Conexión cerrada")


# Uso principal
if __name__ == "__main__":
    HOST = "192.168.0.101"

    user = input("👤 Usuario: ")
    password = getpass.getpass("🔒 Contraseña: ")

    client = CiscoTelnetClient(HOST)

    try:
        client.connect(user, password)

        # Comandos de configuración
        config_commands = [
            "configure terminal",
            "interface loopback 0",
            "ip address 1.1.1.1 255.255.255.255",
            "end",
            "write memory"
        ]

        for cmd in config_commands:
            client.send_command(cmd, wait_time=5)

        # Sesión interactiva
        client.interactive_session()

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.close()