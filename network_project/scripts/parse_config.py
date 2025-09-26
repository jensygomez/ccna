from ciscoconfparse import CiscoConfParse
import json
import yaml

# Ruta del archivo de configuración
config_file = "run.txt"

# Parsear la configuración
parse = CiscoConfParse(config_file)

# === Hostname ===
hostname = None
for obj in parse.find_objects(r"^hostname"):
    hostname = obj.text.split()[1]

# === Interfaces ===
interfaces = []
for intf in parse.find_objects(r"^interface"):
    intf_dict = {"name": intf.text.split()[1], "config": []}
    for child in intf.children:
        intf_dict["config"].append(child.text.strip())
    interfaces.append(intf_dict)

# === Rutas estáticas ===
static_routes = [route.text for route in parse.find_objects(r"^ip route")]

# === ACLs ===
acls = []
for acl in parse.find_objects(r"^access-list"):
    acls.append(acl.text)

# === Protocolos de enrutamiento (ej: OSPF, EIGRP, BGP) ===
routing_protocols = {}
for proto in ["router ospf", "router eigrp", "router bgp", "router rip"]:
    blocks = parse.find_objects(rf"^{proto}")
    if blocks:
        routing_protocols[proto] = []
        for block in blocks:
            block_conf = {"process": block.text, "config": []}
            for child in block.children:
                block_conf["config"].append(child.text.strip())
            routing_protocols[proto].append(block_conf)

# === VLANs (para switches) ===
vlans = []
for vlan in parse.find_objects(r"^vlan\s+\d+"):
    vlan_dict = {"id": vlan.text.split()[1], "config": []}
    for child in vlan.children:
        vlan_dict["config"].append(child.text.strip())
    vlans.append(vlan_dict)

# === Diccionario final ===
config_dict = {
    "hostname": hostname,
    "interfaces": interfaces,
    "static_routes": static_routes,
    "acls": acls,
    "routing_protocols": routing_protocols,
    "vlans": vlans
}

# Guardar en JSON
with open("run.json", "w") as json_file:
    json.dump(config_dict, json_file, indent=4)

with open("run.yaml", "w") as yaml_file:
    yaml.dump(config_dict, yaml_file, default_flow_style=False, sort_keys=False)

print("✅ Archivos run.json y run.yaml creados por secciones")
