# 🔹 Configuración de Edge_01 como cliente DHCP hacia el router de casa y servidor DHCP para la LAN

## 🔹 PASO 1: Configuración de Dispositivos

### 1\. Configuración de Edge_01 (Router)

    Router> enable
    Router# configure terminal
    Router(config)# hostname Edge_01
    Edge_01(config)#
    
    ! Configurar interfaz WAN (recibe IP via DHCP del router de casa)
    Edge_01(config)# interface GigabitEthernet0/0
    Edge_01(config-if)# description Conexion a NET (Router de Casa)
    Edge_01(config-if)# ip address dhcp
    Edge_01(config-if)# ip nat outside
    Edge_01(config-if)# duplex auto
    Edge_01(config-if)# speed auto
    Edge_01(config-if)# no shutdown
    Edge_01(config-if)# exit
    
    ! Configurar interfaz LAN
    Edge_01(config)# interface GigabitEthernet0/1
    Edge_01(config-if)# description Conexion a Sw_01
    Edge_01(config-if)# ip address 192.168.1.1 255.255.255.0
    Edge_01(config-if)# ip nat inside
    Edge_01(config-if)# duplex auto
    Edge_01(config-if)# speed auto
    Edge_01(config-if)# no shutdown
    Edge_01(config-if)# exit
    
    ! Configurar pool DHCP para los clientes LAN
    Edge_01(config)# ip dhcp pool LAN_POOL
    Edge_01(dhcp-config)# network 192.168.1.0 255.255.255.0
    Edge_01(dhcp-config)# default-router 192.168.1.1
    Edge_01(dhcp-config)# dns-server 8.8.8.8 8.8.4.4
    Edge_01(dhcp-config)# domain-name mi-lab.local
    Edge_01(dhcp-config)# lease 1
    Edge_01(dhcp-config)# exit
    
    ! Configurar NAT para permitir salida a Internet
    Edge_01(config)# ip access-list standard NAT_ACL
    Edge_01(config-std-nacl)# permit 192.168.1.0 0.0.0.255
    Edge_01(config-std-nacl)# exit
    
    Edge_01(config)# ip nat inside source list NAT_ACL interface
    GigabitEthernet0/0 overload
    
    ! Configurar ruta por defecto
    Edge_01(config)# ip route 0.0.0.0 0.0.0.0 dhcp
    
    ! Habilitar forwarding IP
    Edge_01(config)# ip forwarding
    
    Edge_01(config)# end
    Edge_01# write memory

### 2. Configuración de Sw_01 (Switch)

    Switch> enable
    Switch# configure terminal
    Switch(config)# hostname Sw_01
    Sw_01(config)#
    
    ! Configurar interfaz uplink al router
    Sw_01(config)# interface GigabitEthernet0/1
    Sw_01(config-if)# description Conexion a Edge_01
    Sw_01(config-if)# switchport mode access
    Sw_01(config-if)# switchport access vlan 1
    Sw_01(config-if)# no shutdown
    Sw_01(config-if)# exit
    
    ! Configurar interfaces para PCs
    Sw_01(config)# interface range GigabitEthernet1/0-3
    Sw_01(config-if-range)# description Conexion a PCs
    Sw_01(config-if-range)# switchport mode access
    Sw_01(config-if-range)# switchport access vlan 1
    Sw_01(config-if-range)# spanning-tree portfast
    Sw_01(config-if-range)# no shutdown
    Sw_01(config-if-range)# exit
    
    Sw_01(config)# end
    Sw_01# write memory

## 🔹 PASO 2: Verificación de conectividad

### 1. En Edge_01 verificar la IP recibida por DHCP:

    show ip interface brief
    show dhcp lease

### 2. Verificar NAT y rutas:

    show ip nat translations
    show ip route

### 3. En las PCs (configuradas para DHCP), verificar que reciben:

    IP en el rango 192.168.1.0/24
    Gateway: 192.168.1.1
    DNS: 8.8.8.8 y 8.8.4.4

