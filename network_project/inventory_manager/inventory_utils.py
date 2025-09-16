# network_project/inventory_manager/inventory_utils.py


from tabulate import tabulate

def mostrar_dispositivos(devices: dict):
    """
    Muestra los dispositivos en formato tabla con tabulate de forma dinámica.
    Todos los atributos extra aparecen automáticamente.
    """
    if not devices:
        print("⚠️ No hay dispositivos en inventario.")
        return

    # Recolectar todas las claves posibles en el inventario
    all_keys = set()
    for dev_data in devices.values():
        all_keys.update(dev_data.keys())

    # Ordenamos las columnas con prioridad
    prioridad = ["name", "type", "ip", "username", "password"]
    headers = ["#"]
    for key in prioridad:
        if key in all_keys:
            headers.append("Acceso SSH" if key == "ip" else key.capitalize())
            all_keys.remove(key)

    # Lo que sobra (atributos extra) se agrega dinámicamente
    for key in sorted(all_keys):
        headers.append(key.capitalize())

    # Construcción de la tabla
    table = []
    for idx, (name, data) in enumerate(devices.items(), start=1):
        row = [idx]
        for col in headers[1:]:  # saltamos "#"
            key = col.lower() if col != "Acceso SSH" else "ip"
            value = data.get(key, "")

            # Mostrar interfaces, vlans, rutas, etc. como lista multilinea
            if isinstance(value, dict):  
                # caso interfaces: {g0/0: {...}, g0/1: {...}}
                sub_items = []
                for sub_key, attrs in value.items():
                    if isinstance(attrs, dict):
                        sub_items.append(f"{sub_key}: " + ", ".join([f"{k}={v}" for k, v in attrs.items()]))
                    else:
                        sub_items.append(f"{sub_key}: {attrs}")
                value = "\n".join(sub_items)

            elif isinstance(value, list):  
                # caso vlans: [{"id":10,"name":"Users"}, {...}]
                sub_items = []
                for item in value:
                    if isinstance(item, dict):
                        sub_items.append(", ".join([f"{k}={v}" for k, v in item.items()]))
                    else:
                        sub_items.append(str(item))
                value = "\n".join(sub_items)

            row.append(value)
        table.append(row)

    print("\n=== 📋 Dispositivos en inventario ===")
    print(tabulate(table, headers=headers, tablefmt="grid"))
