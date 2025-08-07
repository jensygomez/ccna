
# 🧪 Laboratorio CCNA: Segmentación por VLAN y Enrutamiento Inter-VLAN con Control de Comunicación

----------

## 🔹 Paso 1: Planificación de VLANs
 
| Departamento         | Nombre VLAN       | ID VLAN | IP Gateway          |
|----------------------|-------------------|---------|---------------------|
| FINANZAS             | VLAN 10           | 10      | 192.168.10.1/24     |
| SAC                  | VLAN 20           | 20      | 192.168.20.1/24     |
| IT                   | VLAN 30           | 30      | 192.168.30.1/24     |
| GERENCIA             | VLAN 40           | 40      | 192.168.40.1/24     |


## 🔹 Paso 2: Asignación de Interfaces en el Switch FINANZAS
| Puerto Switch      | Departamento         | VLAN |
|--------------------|----------------------|------|
| FINANZAS G1/0      | eth0 (e0)            | 10   |
| FINANZAS G1/1      | eth1 (e1)            | 10   |

    Switch>
    Switch> enable
    Switch#
    Switch# configure terminal
    Switch(config)#hostname FINANZAS
    FINANZAS(config)#

    FINANZAS(config)# vlan 10
    FINANZAS(config-vlan)# name FINANZAS
    FINANZAS(config-vlan)# exit

    ! Asignar puertos a cada VLAN
    FINANZAS(config)# interface range G1/0 - 1
    FINANZAS(config-if-range)# switchport mode access
    FINANZAS(config-if-range)# switchport access vlan 10
    FINANZAS(config-if-range)# exit

    ! Configurar el puerto TRUNK hacia el Dist_1
    FINANZAS(config)# interface G0/0
    FINANZAS(config-if)# switchport mode trunk
    FINANZAS(config-if)# exit
    
    ! Configurar el puerto TRUNK hacia el Dist_2
    FINANZAS(config)# interface G0/3
    FINANZAS(config-if)# switchport mode trunk
    FINANZAS(config-if)# exit
    FINANZAS(config)# end
    FINANZAS# write memory

## 🔹 Paso 3: Asignación de Interfaces en el Switch SAC
| SAC      G1/0      | eth2 (e2)            | 20   |
| SAC      G1/1      | eth3 (e3)            | 20   |

    Switch>
    Switch> enable
    Switch#
    Switch# configure terminal
    Switch(config)#hostname SAC
    SAC(config)#

    SAC(config)# vlan 20
    SAC(config-vlan)# name SAC
    SAC(config-vlan)# exit

    ! Asignar puertos a cada VLAN
    SAC(config)# interface range G1/0 - 1
    SAC(config-if-range)# switchport mode access
    SAC(config-if-range)# switchport access vlan 20
    SAC(config-if-range)# exit

    ! Configurar el puerto TRUNK hacia el Dist_1
    SAC(config)# interface G0/1
    SAC(config-if)# switchport mode trunk
    SAC(config-if)# exit
    
    ! Configurar el puerto TRUNK hacia el Dist_2
    SAC(config)# interface G0/2
    SAC(config-if)# switchport mode trunk
    SAC(config-if)# exit
    SAC(config)# end
    SAC# write memory


## 🔹 Paso 4: Asignación de Interfaces en el Switch IT
| IT       G1/0      | eth4 (e4)            | 30   |
| IT       G1/1      | eth5 (e5)            | 30   |

    Switch>
    Switch> enable
    Switch#
    Switch# configure terminal
    Switch(config)#hostname IT
    IT(config)#

    IT(config)# vlan 30
    IT(config-vlan)# name IT
    IT(config-vlan)# exit

    ! Asignar puertos a cada VLAN
    IT(config)# interface range G1/0 - 1
    IT(config-if-range)# switchport mode access
    IT(config-if-range)# switchport access vlan 30
    IT(config-if-range)# exit

    ! Configurar el puerto TRUNK hacia el Dist_1
    IT(config)# interface G0/2
    IT(config-if)# switchport mode trunk
    IT(config-if)# exit

    ! Configurar el puerto TRUNK hacia el Dist_2
    IT(config)# interface G0/1
    IT(config-if)# switchport mode trunk
    IT(config-if)# exit
    IT(config)# end
    IT# write memory


## 🔹 Paso 5: Asignación de Interfaces en el Switch GERENCIA
| Gerencia G1/0      | eth6 (e6)            | 40   |
| Gerencia Gi1/1     | eth7 (e7)            | 40   |


    Switch>
    Switch> enable
    Switch#
    Switch# configure terminal
    Switch(config)#hostname GERENCIA
    GERENCIA(config)#

    GERENCIA(config)# vlan 40
    GERENCIA(config-vlan)# name IT
    GERENCIA(config-vlan)# exit

    ! Asignar puertos a cada VLAN
    GERENCIA(config)# interface range G1/0 - 1
    GERENCIA(config-if-range)# switchport mode access
    GERENCIA(config-if-range)# switchport access vlan 40
    IT(config-if-range)# exit

    ! Configurar el puerto TRUNK hacia el Dist_1
    GERENCIA(config)# interface G0/3
    GERENCIA(config-if)# switchport mode trunk
    GERENCIA(config-if)# exit

    ! Configurar el puerto TRUNK hacia el Dist_2
    GERENCIA(config)# interface G0/0
    GERENCIA(config-if)# switchport mode trunk
    GERENCIA(config-if)# exit
    GERENCIA(config)# end
    GERENCIA# write memory






__________________________


## 🔹 Paso 6: Configuración del Dist_1

    Router>
    Router> enable
    Router#
    Router# configure terminal
    Routerno(config)#hostname Dist_1
    Dist_1(config)#
    
    ! Activar el enrutamiento
    Dist_1(config)# ip routing
    
    ! Subinterfaces por VLAN
    Dist_1(config)# interface gigabitEthernet0/0.10
    Dist_1(config-subif)# encapsulation dot1Q 10
    Dist_1(config-subif)# ip address 192.168.10.1 255.255.255.0
    Dist_1(config-subif)# exit
    
    Dist_1(config)# interface gigabitEthernet0/0.20
    Dist_1(config-subif)# encapsulation dot1Q 20
    Dist_1(config-subif)# ip address 192.168.20.1 255.255.255.0
    Dist_1(config-subif)# exit
    
    Dist_1(config)# interface gigabitEthernet0/0.30
    Dist_1(config-subif)# encapsulation dot1Q 30
    Dist_1(config-subif)# ip address 192.168.30.1 255.255.255.0
    Dist_1(config-subif)# exit
    
    Dist_1(config)# interface gigabitEthernet0/0.40
    Dist_1(config-subif)# encapsulation dot1Q 40
    Dist_1(config-subif)# ip address 192.168.40.1 255.255.255.0
    Dist_1(config-subif)# exit
    
    Dist_1(config)# interface gigabitEthernet0/0
    Dist_1(config-if)# no shutdown
    Dist_1(config-if)# exit
    
    Dist_1(config)# end
    Dist_1# write memory

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

