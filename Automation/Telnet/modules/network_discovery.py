# modules/network_discovery.py
from .utils import obtener_interfaces_red, calcular_cidr


def descubrir_redes_locales():
    """Descubre y muestra todas las redes locales disponibles"""
    print("🔍 Escaneando redes locales...")
    interfaces = obtener_interfaces_red()

    if not interfaces:
        print("❌ No se encontraron interfaces de red activas")
        return None

    print("\n📊 REDES DISPONIBLES:")
    print("=" * 60)
    for i, iface in enumerate(interfaces, 1):
        cidr = calcular_cidr(iface['netmask'])
        print(f"{i}. {iface['interface']:12} - {iface['ip']:15} /{cidr}")
        if iface['gateway']:
            print(f"   Gateway: {iface['gateway']}")
        print()

    return interfaces


def seleccionar_red(interfaces):
    """Permite al usuario seleccionar una red"""
    if not interfaces:
        return None

    print("=" * 60)
    try:
        seleccion = int(input("Selecciona la red donde está el Bastion (número): ").strip())
        idx = seleccion - 1

        if 0 <= idx < len(interfaces):
            red_seleccionada = interfaces[idx]
            cidr = calcular_cidr(red_seleccionada['netmask'])
            red_seleccionada['cidr'] = cidr
            red_seleccionada['network_cidr'] = f"{red_seleccionada['ip']}/{cidr}"

            print(f"✅ Red seleccionada: {red_seleccionada['network_cidr']}")
            return red_seleccionada
        else:
            print("❌ Selección inválida")
            return None
    except ValueError:
        print("❌ Por favor ingresa un número válido")
        return None