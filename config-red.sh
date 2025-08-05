#!/bin/bash

# Verificar que se ejecute como root
if [ "$(id -u)" -ne 0 ]; then
    echo "Este script debe ejecutarse como root" >&2
    exit 1
fi

set -e # Salir ante cualquier error

# Función para validar IP
validate_ip() {
    local ip=$1
    local stat=1

    if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        OIFS=$IFS
        IFS='.'
        ip=($ip)
        IFS=$OIFS
        [[ ${ip[0]} -le 255 && ${ip[1]} -le 255 && \
           ${ip[2]} -le 255 && ${ip[3]} -le 255 ]]
        stat=$?
    fi
    return $stat
}

# Verificar si usamos netplan o interfaces tradicional
if [ -d /etc/netplan ]; then
    CONFIG_MODE="netplan"
    echo "[+] Se detectó netplan como sistema de configuración"
else
    CONFIG_MODE="interfaces"
    echo "[+] Se detectó /etc/network/interfaces como sistema de configuración"
fi

# Listar interfaces disponibles
interfaces=($(ip link show | awk -F': ' '/^[0-9]+: e/ {print $2}' | grep -vE '^(lo|docker|virbr)'))

if [ ${#interfaces[@]} -eq 0 ]; then
    echo "Error: No se encontraron interfaces físicas disponibles" >&2
    exit 1
fi

echo -e "\n[+] Interfaces de red disponibles:"
for i in "${!interfaces[@]}"; do
    echo "$((i+1)). ${interfaces[$i]}"
done

# Preguntar si configurar todas las interfaces
while true; do
    read -p $'\n¿Deseas configurar todas las interfaces? (s/n): ' config_all
    if [[ "$config_all" =~ ^[SsNn]$ ]]; then
        break
    fi
    echo "Por favor ingresa 's' o 'n'"
done

if [[ "$config_all" =~ ^[Ss]$ ]]; then
    interfaces_to_config=("${interfaces[@]}")
    echo -e "\n[+] Configurando todas las interfaces"
else
    interfaces_to_config=()
    echo -e "\nSelecciona las interfaces a configurar (ej. 1 3 4):"
    read -a selected_indices
    
    for index in "${selected_indices[@]}"; do
        if [[ "$index" =~ ^[0-9]+$ ]] && [ "$index" -ge 1 ] && [ "$index" -le ${#interfaces[@]} ]; then
            interfaces_to_config+=("${interfaces[$((index-1))]}")
        else
            echo "Advertencia: Índice $index inválido, será omitido" >&2
        fi
    done
    
    if [ ${#interfaces_to_config[@]} -eq 0 ]; then
        echo "Error: No se seleccionaron interfaces válidas" >&2
        exit 1
    fi
fi

# Configurar cada interfaz
for iface in "${interfaces_to_config[@]}"; do
    echo -e "\n--- Configurando interfaz $iface ---"
    
    # Preguntar por DHCP o estático
    while true; do
        read -p "¿Configurar $iface con DHCP? (s/n): " use_dhcp
        if [[ "$use_dhcp" =~ ^[SsNn]$ ]]; then
            break
        fi
        echo "Por favor ingresa 's' o 'n'"
    done
    
    if [[ "$use_dhcp" =~ ^[Ss]$ ]]; then
        # Configuración DHCP
        if [ "$CONFIG_MODE" == "netplan" ]; then
            echo "  Configurando $iface con DHCP (netplan)..."
            cat > "/etc/netplan/90-${iface}-config.yaml" <<EOF
network:
  version: 2
  ethernets:
    $iface:
      dhcp4: true
      optional: true
EOF
        else
            echo "  Configurando $iface con DHCP (interfaces)..."
            cat >> "/etc/network/interfaces" <<EOF

auto $iface
iface $iface inet dhcp
EOF
        fi
    else
        # Configuración estática
        while true; do
            read -p "Ingresa la IP para $iface (ej. 192.168.1.10/24): " ip_addr
            if [[ "$ip_addr" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/[0-9]+$ ]] && validate_ip "${ip_addr%/*}"; then
                break
            else
                echo "Formato de IP inválido. Usa formato CIDR (ej. 192.168.1.10/24)"
            fi
        done

        while true; do
            read -p "Ingresa el gateway para $iface (ej. 192.168.1.1): " gateway
            if validate_ip "$gateway"; then
                break
            else
                echo "Dirección IP inválida. Intenta nuevamente."
            fi
        done

        while true; do
            read -p "Ingresa los DNS (separados por espacios, ej. 8.8.8.8 8.8.4.4): " dns_servers
            # Validar cada DNS ingresado
            invalid_dns=0
            for dns in $dns_servers; do
                if ! validate_ip "$dns"; then
                    echo "DNS inválido: $dns"
                    invalid_dns=1
                    break
                fi
            done
            [ $invalid_dns -eq 0 ] && break
        done
        
        if [ "$CONFIG_MODE" == "netplan" ]; then
            echo "  Configurando $iface con IP estática (netplan)..."
            # Convertir espacios a comas en los DNS para Netplan
            dns_servers_comma=$(echo "$dns_servers" | tr ' ' ',')
            cat > "/etc/netplan/90-${iface}-config.yaml" <<EOF
network:
  version: 2
  ethernets:
    $iface:
      addresses: [$ip_addr]
      routes:
        - to: 0.0.0.0/0
          via: $gateway
      nameservers:
        addresses: [$dns_servers_comma]
EOF
        else
            echo "  Configurando $iface con IP estática (interfaces)..."
            # Calcular máscara de red
            netmask=$(ipcalc -m $ip_addr | cut -d'=' -f2)
            cat >> "/etc/network/interfaces" <<EOF

auto $iface
iface $iface inet static
    address ${ip_addr%/*}
    netmask $netmask
    gateway $gateway
    dns-nameservers $dns_servers
EOF
        fi
    fi
    
    echo -e "\n[+] Interfaz $iface configurada:"
    if [[ "$use_dhcp" =~ ^[Ss]$ ]]; then
        echo "  - Modo: DHCP"
    else
        echo "  - IP: $ip_addr"
        echo "  - Gateway: $gateway"
        echo "  - DNS: $dns_servers"
    fi
done

# Aplicar cambios
echo -e "\n[+] Aplicando configuración..."
if [ "$CONFIG_MODE" == "netplan" ]; then
    # Validar configuración netplan antes de aplicar
    if netplan generate; then
        if netplan apply; then
            echo "Configuración aplicada con netplan correctamente"
        else
            echo "Error al aplicar netplan" >&2
            exit 1
        fi
    else
        echo "Error: La configuración de netplan no es válida" >&2
        exit 1
    fi
else
    if systemctl restart networking; then
        echo "Configuración aplicada reiniciando el servicio de red"
    else
        echo "Error al reiniciar el servicio de red" >&2
        exit 1
    fi
fi

echo -e "\n[+] Configuración completada exitosamente!"
echo "Puedes verificar la configuración con los siguientes comandos:"
echo "  ip addr show"
echo "  ip route show"
echo "  ping -c 3 8.8.8.8"
echo "  systemctl status networking"

exit 0
