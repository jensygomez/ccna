# network_project/inventory_manager/inventory_utils.py

from tabulate import tabulate

def mostrar_dispositivos(devices):
    """
    Muestra los dispositivos en formato tabla con tabulate.
    Funciona con lista o diccionario de dispositivos.
    Todos los atributos extra aparecen automáticamente.
    """
    if not devices:
        print("⚠️ No hay dispositivos en inventario.")
        return

    # Convertir dict a lista si es necesario
    if isinstance(devices, dict):
        devices_list = list(devices.values())
    elif isinstance(devices, list):
        devices_list = devices
    else:
        print("⚠️ Formato de datos inválido.")
        return

    # Recolectar todas las claves posibles
    all_keys = set()
    for dev_data in devices_list:
        all_keys.update(dev_data.keys())

    prioridad = ["name", "type", "ip", "username", "password"]
    headers = ["#"]
    for key in prioridad:
        if key in all_keys:
            headers.append("Acceso SSH" if key == "ip" else key.capitalize())
            all_keys.remove(key)

    # atributos extra
    for key in sorted(all_keys):
        headers.append(key.capitalize())

    # Construcción de la tabla
    table = []
    for idx, data in enumerate(devices_list, start=1):
        row = [idx]
        for col in headers[1:]:
            key = col.lower() if col != "Acceso SSH" else "ip"
            value = data.get(key, "")

            if isinstance(value, dict):  
                sub_items = []
                for sub_key, attrs in value.items():
                    if isinstance(attrs, dict):
                        sub_items.append(f"{sub_key}: " + ", ".join(f"{k}={v}" for k,v in attrs.items()))
                    else:
                        sub_items.append(f"{sub_key}: {attrs}")
                value = "\n".join(sub_items)

            elif isinstance(value, list):  
                sub_items = []
                for item in value:
                    if isinstance(item, dict):
                        sub_items.append(", ".join(f"{k}={v}" for k,v in item.items()))
                    else:
                        sub_items.append(str(item))
                value = "\n".join(sub_items)

            row.append(value)
        table.append(row)

    print("\n=== 📋 Dispositivos en inventario ===")
    print(tabulate(table, headers=headers, tablefmt="grid"))
