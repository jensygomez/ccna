
# 🧪 Laboratorio CCNA: Segmentación por VLAN y Enrutamiento Inter-VLAN con Control de Comunicación

----------

## 🔹 Paso 1: Planificación de VLANs

| Departamento         | Nombre VLAN       | ID VLAN | IP Gateway         |
|----------------------|-------------------|---------|---------------------|
| Finanzas             | VLAN10            | 10      | 192.168.10.1/24     |
| Atención al Cliente  | VLAN20            | 20      | 192.168.20.1/24     |
| IT                   | VLAN30            | 30      | 192.168.30.1/24     |
| Gerencia             | VLAN40            | 40      | 192.168.40.1/24     |


## 🔹 Tabla 2: Asignación de Interfaces en el Switch L2 (SW1)
| Puerto Switch | Departamento         | VLAN |
|---------------|----------------------|------|
| Gi0/0         | Finanzas (Host1)     | 10   |
| Gi0/1         | Finanzas (Host2)     | 10   |
| Gi0/2         | Atención Cliente     | 20   |
| Gi0/3         | Atención Cliente     | 20   |
| Gi1/0         | IT (Host5)           | 30   |
| Gi1/1         | IT (Host6)           | 30   |
| Gi1/2         | Gerencia (Host7)     | 40   |
| Gi1/3         | Gerencia (Host8)     | 40   |

## ## 🔹 Paso 3: Configuración del Switch de Acceso (SW1)

    SW1> enable
    SW1# configure terminal
    ! Crear las VLANs
    SW1(config)# vlan 10
    SW1(config-vlan)# name Finanzas
    SW1(config-vlan)# exit
    
    SW1(config)# vlan 20
    SW1(config-vlan)# name AtencionCliente
    SW1(config-vlan)# exit
    
    SW1(config)# vlan 30
    SW1(config-vlan)# name IT
    SW1(config-vlan)# exit
    
    SW1(config)# vlan 40
    SW1(config-vlan)# name Gerencia
    SW1(config-vlan)# exit
    
    ! Asignar puertos a cada VLAN
    SW1(config)# interface range gi0/0 - 0/1
    SW1(config-if-range)# switchport mode access
    SW1(config-if-range)# switchport access vlan 10
    SW1(config-if-range)# exit
    
    SW1(config)# interface range gi0/2 - 0/3
    SW1(config-if-range)# switchport mode access
    SW1(config-if-range)# switchport access vlan 20
    SW1(config-if-range)# exit
    
    SW1(config)# interface range gi1/0 - 1/1
    SW1(config-if-range)# switchport mode access
    SW1(config-if-range)# switchport access vlan 30
    SW1(config-if-range)# exit
    
    SW1(config)# interface range gi1/2 - 1/3
    SW1(config-if-range)# switchport mode access
    SW1(config-if-range)# switchport access vlan 40
    SW1(config-if-range)# exit
    
    ! Configurar el puerto TRUNK hacia el Switch Capa 3
    SW1(config)# interface gi2/0
    SW1(config-if)# switchport mode trunk
    SW1(config-if)# exit
    
    SW1(config)# end
    SW1# write memory




__________________________


## 🔹 Paso 4: Configuración del Switch Layer 3 (Router-on-a-Stick)

    L3-SW> enable
    L3-SW# configure terminal
    
    ! Activar el enrutamiento
    L3-SW(config)# ip routing
    
    ! Subinterfaces por VLAN
    L3-SW(config)# interface gigabitEthernet0/0.10
    L3-SW(config-subif)# encapsulation dot1Q 10
    L3-SW(config-subif)# ip address 192.168.10.1 255.255.255.0
    L3-SW(config-subif)# exit
    
    L3-SW(config)# interface gigabitEthernet0/0.20
    L3-SW(config-subif)# encapsulation dot1Q 20
    L3-SW(config-subif)# ip address 192.168.20.1 255.255.255.0
    L3-SW(config-subif)# exit
    
    L3-SW(config)# interface gigabitEthernet0/0.30
    L3-SW(config-subif)# encapsulation dot1Q 30
    L3-SW(config-subif)# ip address 192.168.30.1 255.255.255.0
    L3-SW(config-subif)# exit
    
    L3-SW(config)# interface gigabitEthernet0/0.40
    L3-SW(config-subif)# encapsulation dot1Q 40
    L3-SW(config-subif)# ip address 192.168.40.1 255.255.255.0
    L3-SW(config-subif)# exit
    
    L3-SW(config)# interface gigabitEthernet0/0
    L3-SW(config-if)# no shutdown
    L3-SW(config-if)# exit
    
    L3-SW(config)# end
    L3-SW# write memory

## 🔹 Paso 5: Control de Comunicación entre VLANs (Opcional)
Bloquear que Finanzas se comunique con Atención al Cliente:

    L3-SW(config)# access-list 100 deny ip 192.168.10.0 0.0.0.255 192.168.20.0 0.0.0.255
    L3-SW(config)# access-list 100 permit ip any any
    
    L3-SW(config)# interface gigabitEthernet0/0.10
    L3-SW(config-subif)# ip access-group 100 in
    L3-SW(config-subif)# exit

## 🔹 Paso 6: Configuración del Router Edge
Este router será el punto de salida a Internet:

    EDGE-RTR> enable
    EDGE-RTR# configure terminal
    
    ! IP interna hacia el L3-SW
    EDGE-RTR(config)# interface gi0/0
    EDGE-RTR(config-if)# ip address 192.168.100.2 255.255.255.0
    EDGE-RTR(config-if)# no shutdown
    EDGE-RTR(config-if)# exit
    
    ! IP externa hacia el proveedor (simulado)
    EDGE-RTR(config)# interface gi0/1
    EDGE-RTR(config-if)# ip address 200.1.1.1 255.255.255.252
    EDGE-RTR(config-if)# no shutdown
    EDGE-RTR(config-if)# exit
    
    ! Ruta por defecto
    EDGE-RTR(config)# ip route 0.0.0.0 0.0.0.0 200.1.1.2
    EDGE-RTR(config)# end
    EDGE-RTR# write memory



## 🔹 Paso 7: Enrutamiento Estático en el L3-SW (si es necesario)

    L3-SW(config)# ip route 0.0.0.0 0.0.0.0 192.168.100.2

