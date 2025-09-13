#Netmiko/modules/bastion_router/connect_bastion.py
from netmiko import ConnectHandler
import re

class BastionManager:
    def __init__(self, host, username, password, secret, device_type="cisco_ios"):
        self.conn_info = {
            "device_type": device_type,
            "host": host,
            "username": username,
            "password": password,
            "secret": secret,
        }
        self.conn = None

    def connect(self):
        try:
            self.conn = ConnectHandler(**self.conn_info)
            self.conn.enable()
            print(f"✅ Conectado al Bastion {self.conn_info['host']}")
            return True
        except Exception as e:
            print(f"❌ Error conectando al Bastion: {e}")
            self.conn = None
            return False

    def disconnect(self):
        if self.conn:
            self.conn.disconnect()
            print("🔌 Desconectado del Bastion.")

    def get_lldp_neighbors(self):
        if not self.conn:
            print("❌ No hay conexión al Bastion")
            return []

        output = self.conn.send_command("show lldp neighbors detail")
        neighbors = []

        blocks = output.split("\n\n")
        for block in blocks:
            neighbor = {}

        # System Name
        match_name = re.search(r"System Name:\s*(\S+)", block)
        neighbor_name = match_name.group(1) if match_name else None
        neighbor["neighbor_name"] = neighbor_name

        # Local Interface
        match_local = re.search(r"Local Intf:\s*(\S+ \S+)", block)
        neighbor["local_intf"] = match_local.group(1) if match_local else None

        # Neighbor Port
        match_port = re.search(r"Port id:\s*(\S+)", block)
        neighbor["neighbor_port"] = match_port.group(1) if match_port else None

        # System Capabilities / Type
        match_type = re.search(r"System Capabilities:\s*(.+)", block)
        neighbor["neighbor_type"] = match_type.group(1) if match_type else None

        # Model
        match_model = re.search(r"System Name:\s*(\S+)", block)
        neighbor["neighbor_model"] = match_model.group(1) if match_model else None

        # Management IP (captura IP aunque tenga espacios delante)
        match_ip = re.search(r"^\s*IP:\s*(\S+)", block, re.MULTILINE)
        neighbor["neighbor_ip"] = match_ip.group(1) if match_ip else None

        # Solo agregar si tiene nombre o IP
        if neighbor_name or neighbor["neighbor_ip"]:
            neighbors.append(neighbor)

        return neighbors

    def _parse_lldp_output(self, output):
        neighbors = []
        blocks = output.split("\n\n")
        for block in blocks:
            neighbor = {}

            match_name = re.search(r"Device ID: (\S+)", block) or re.search(r"System Name: (\S+)", block)
            neighbor["neighbor_name"] = match_name.group(1) if match_name else "N/A"

            match_local = re.search(r"Local Intf: (\S+ \S+)", block)
            neighbor["local_intf"] = match_local.group(1) if match_local else "N/A"

            match_remote = re.search(r"Port id: (\S+)", block)
            neighbor["neighbor_port"] = match_remote.group(1) if match_remote else "N/A"

            match_type = re.search(r"System Capabilities: (.+)", block)
            neighbor["neighbor_type"] = match_type.group(1) if match_type else "N/A"

            match_model = re.search(r"System Description: (.+)", block)
            neighbor["neighbor_model"] = match_model.group(1) if match_model else "N/A"

            match_ip = re.search(r"Management Address: (?:IP: )?(\S+)", block)
            neighbor["neighbor_ip"] = match_ip.group(1) if match_ip else None

            neighbors.append(neighbor)
        return neighbors
