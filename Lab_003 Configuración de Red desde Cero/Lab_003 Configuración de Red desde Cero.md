## **🔹 PASO 1: Planificación de VLANs y Direccionamiento**

## 🖥️ **Tabla de Configuración de Dispositivos por VLAN**

| Dispositivo | VLAN | Nombre VLAN | Configuración IP (Formato CLI) | 
|-------------|-------|--------------|----------------------------------------------------| 
| PC_01 | 10 | Usuarios | `ip 192.168.10.10 255.255.255.0 192.168.10.1` |
| PC_02 | 10 | Usuarios | `ip 192.168.10.11 255.255.255.0 192.168.10.1` |
| PC_03 | 20 | Administración| `ip 192.168.20.10 255.255.255.0 192.168.20.1` |
| PC_04 | 30 | Servidores | `ip 192.168.30.10 255.255.255.0 192.168.30.1` |


## **🔹 PASO 2: Configuración de Dispositivos**

### **1. Edge_01 (Router hacia Internet)**

    Router> enable
    Router#
    Router# configure terminal
    Router(config)# hostname Edge_01
    Edge_01(config)#
    
    ! Configurar interfaz hacia Internet
    Edge_01(config)# interface Gi0/0
    Edge_01(config-if)# ip address 203.0.113.1 255.255.255.252
    Edge_01(config-if)# no shutdown
    Edge_01(config-if)# exit
    
    ! Configurar interfaz hacia R_Dist_01
    Edge_01(config)# interface Gi0/2
    Edge_01(config-if)# ip address 192.168.100.1 255.255.255.252
    Edge_01(config-if)# no shutdown
    Edge_01(config-if)# exit
    
    ! Ruta estática hacia Internet
    Edge_01(config)# ip route 0.0.0.0 0.0.0.0 203.0.113.2
    
    ! Rutas hacia redes internas
    Edge_01(config)# ip route 192.168.10.0 255.255.255.0 192.168.100.2
    Edge_01(config)# ip route 192.168.20.0 255.255.255.0 192.168.100.2
    Edge_01(config)# ip route 192.168.30.0 255.255.255.0 192.168.100.2
    
    Edge_01(config)# end
    Edge_01#
    Edge_01# write memory

### **2. R_Dist_01 (Router L3 - Router-on-a-Stick)**

    Router> enable
    Router# configure terminal
    Router(config)# hostname R_Dist_01
    R_Dist_01(config)# ip routing
    
    ! Configurar subinterfaces para VLAN 10
    R_Dist_01(config)# interface Gi0/0.10
    R_Dist_01(config-subif)# encapsulation dot1Q 10
    R_Dist_01(config-subif)# ip address 192.168.10.1 255.255.255.0
    R_Dist_01(config-subif)# no shutdown
    R_Dist_01(config-subif)# exit
    
    ! Configurar subinterfaces para VLAN 20
    R_Dist_01(config)# interface Gi0/0.20
    R_Dist_01(config-subif)# encapsulation dot1Q 20
    R_Dist_01(config-subif)# ip address 192.168.20.1 255.255.255.0
    R_Dist_01(config-subif)# no shutdown
    R_Dist_01(config-subif)# exit
    
    ! Configurar subinterfaces para VLAN 30
    R_Dist_01(config)# interface Gi0/1.30
    R_Dist_01(config-subif)# encapsulation dot1Q 30
    R_Dist_01(config-subif)# ip address 192.168.30.1 255.255.255.0
    R_Dist_01(config-subif)# no shutdown
    R_Dist_01(config-subif)# exit
    
    ! Configurar enlace hacia Edge_01
    R_Dist_01(config)# interface Gi0/2
    R_Dist_01(config-if)# ip address 192.168.100.2 255.255.255.252
    R_Dist_01(config-if)# no shutdown
    R_Dist_01(config-if)# exit
    
    ! Ruta por defecto hacia Edge_01
    R_Dist_01(config)# ip route 0.0.0.0 0.0.0.0 192.168.100.1
    
    R_Dist_01(config)# end
    R_Dist_01# write memory
    Building configuration...
    [OK]
    R_Dist_01#


## **🔹 PASO 3: Configuración de Switches**
### **1. Sw_01 (Switch Principal - Root Bridge)**

    Switch> enable
    Switch# configure terminal
    Switch(config)# hostname Sw_01
    Sw_01(config)# 
    
    ! Crear VLANs
    Sw_01(config)# vlan 10
    Sw_01(config-vlan)# name Usuarios
    Sw_01(config-vlan)# exit
    Sw_01(config)# vlan 20
    Sw_01(config-vlan)# name Administracion
    Sw_01(config-vlan)# exit
    Sw_01(config)# vlan 30
    Sw_01(config-vlan)# name Servidores
    Sw_01(config-vlan)# exit
    
    ! Configurar puertos troncales
    Sw_01(config)# interface range Gi0/0 - 1
    Sw_01(config-if-range)# switchport mode trunk
    Sw_01(config-if-range)# switchport trunk native vlan 999
    Sw_01(config-if-range)# switchport trunk allowed vlan 10,20,30
    Sw_01(config-if-range)# spanning-tree portfast trunk
    Sw_01(config-if-range)# exit
    
    ! Configurar enlaces a Sw_02 y Sw_03
    Sw_01(config)# interface range Gi0/2 - 3 , Gi1/0 - 1
    Sw_01(config-if-range)# switchport mode trunk
    Sw_01(config-if-range)# switchport trunk allowed vlan 10,20,30
    Sw_01(config-if-range)# exit
    
    ! Configurar STP (Root Bridge)
    Sw_01(config)# spanning-tree mode rapid-pvst
    Sw_01(config)# spanning-tree vlan 10,20,30 root primary
    
    Sw_01(config)# end
    Sw_01# write memory
    Building configuration...
    [OK]
    Sw_01#



### **2. Sw_02 (Switch de Acceso - VLAN 10)**

    Switch> enable
    Switch# configure terminal
    Switch(config)# hostname Sw_02
    Sw_02(config)# vlan 10
    Sw_02(config-vlan)# name Usuarios
    Sw_02(config-vlan)# exit
    
    ! Puertos de acceso para PCs
    Sw_02(config)# interface range Gi1/0 - 1
    Sw_02(config-if-range)# switchport mode access
    Sw_02(config-if-range)# switchport access vlan 10
    Sw_02(config-if-range)# spanning-tree portfast
    Sw_02(config-if-range)# exit
    
    ! Enlaces troncales
    Sw_02(config)# interface range Gi0/0 - 3
    Sw_02(config-if-range)# switchport mode trunk
    Sw_02(config-if-range)# switchport trunk allowed vlan 10,20,30
    Sw_02(config-if-range)# exit
    
    ! STP
    Sw_02(config)# spanning-tree mode rapid-pvst
    Sw_02(config)# spanning-tree vlan 10,20,30 root secondary
    
    Sw_02(config)# end
    Sw_02# write memory
    Building configuration...
    [OK]
    Sw_02#


### **3. Sw_03 (Switch de Acceso - VLANs 20 y 30)**

    Switch> enable
    Switch# configure terminal
    Switch(config)# hostname Sw_03
    Sw_03(config)#
    
    ! Crear VLANs
    Sw_03(config)# vlan 20
    Sw_03(config-vlan)# name Administracion
    Sw_03(config-vlan)# exit
    Sw_03(config)# vlan 30
    Sw_03(config-vlan)# name Servidores
    Sw_03(config-vlan)# exit
    
    ! Configurar puertos de acceso
    Sw_03(config)# interface Gi1/0
    Sw_03(config-if)# switchport mode access
    Sw_03(config-if)# switchport access vlan 20
    Sw_03(config-if)# exit
    Sw_03(config)# interface Gi1/1
    Sw_03(config-if)# switchport mode access
    Sw_03(config-if)# switchport access vlan 30
    Sw_03(config-if)# exit
    
    ! Configurar enlaces troncales
    Sw_03(config)# interface range Gi0/0-1 , Gi1/0-1
    Sw_03(config-if-range)# switchport mode trunk
    Sw_03(config-if-range)# switchport trunk allowed vlan 10,20,30
    Sw_03(config-if-range)# exit
    
    ! Configuración de STP
    Sw_03(config)# spanning-tree mode rapid-pvst
    Sw_03(config)# spanning-tree vlan 10,20,30 priority 16384
    
    Sw_03(config)# end
    Sw_03# write memory
    Building configuration...
    [OK]
    Sw_03#

## **🔹 PASO 4: Configuración de PCs (Ejemplo para PC_01)**
PC_01  `ip 192.168.10.10 255.255.255.0 192.168.10.1` 
PC_02 `ip 192.168.10.11 255.255.255.0 192.168.10.1` 
PC_03 `ip 192.168.20.10 255.255.255.0 192.168.20.1` 
PC_04 `ip 192.168.30.10 255.255.255.0 192.168.30.1` 

## **🔹 PASO 5: Verificación y Troubleshooting**
### **Comandos Clave**

1.  **Ver VLANs en switches**:  `show vlan brief`
2. **Ver troncales**: `show interfaces trunk`
4. **Ver rutas en R_Dist_01**: `show ip route`
5. **Probar conectividad desde PCs**: `ping 192.168.20.1  # Desde PC_01 (VLAN 10) al gateway de VLAN 20`

 

