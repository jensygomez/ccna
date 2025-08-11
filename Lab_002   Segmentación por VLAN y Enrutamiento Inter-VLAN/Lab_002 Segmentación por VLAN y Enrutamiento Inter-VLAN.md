
# 🧪 Laboratorio CCNA: Segmentación por VLAN y Enrutamiento Inter-VLAN con Control de Comunicación

----------
## 🔹 Paso 1: Ip para interfaces PC_01

| Interfaz (ethx)   | VLAN | Dirección IP     | Máscara         | Gateway         |
|-------------------|------|------------------|-----------------|-----------------|
| eth0 (FINANZAS)   | 10   | 192.168.10.10    | 255.255.255.0   | 192.168.10.1    |
| eth1 (FINANZAS)   | 10   | 192.168.10.11    | 255.255.255.0   | 192.168.10.1    |
| eth2 (SAC)        | 20   | 192.168.20.10    | 255.255.255.0   | 192.168.20.1    |
| eth3 (SAC)        | 20   | 192.168.20.11    | 255.255.255.0   | 192.168.20.1    |
| eth4 (IT)         | 30   | 192.168.30.10    | 255.255.255.0   | 192.168.30.1    |
| eth5 (IT)         | 30   | 192.168.30.11    | 255.255.255.0   | 192.168.30.1    |
| eth6 (GERENCIA)   | 40   | 192.168.40.10    | 255.255.255.0   | 192.168.40.1    |
| eth7 (GERENCIA)   | 40   | 192.168.40.11    | 255.255.255.0   | 192.168.40.1    |



## 🔹 Paso 1: Planificación de VLANs
 
| Departamento         | Nombre VLAN       | ID VLAN | IP Gateway          |
|----------------------|-------------------|---------|---------------------|
| FINANZAS             | VLAN 10           | 10      | 192.168.10.1/24     |
| SAC                  | VLAN 20           | 20      | 192.168.20.1/24     |
| IT                   | VLAN 30           | 30      | 192.168.30.1/24     |
| GERENCIA             | VLAN 40           | 40      | 192.168.40.1/24     |


## 🔹 Paso 2: Configuración del Router EDGE_1
Este router será el punto de salida a Internet:

Router> enable
Router# configure terminal
Router(config)# hostname EDGE_1
EDGE_1(config)#

! Conexión a ISP (WAN - DHCP)
EDGE_1(config)# interface Gi0/1
EDGE_1(config-if)# ip address dhcp 
EDGE_1(config-if)# no shutdown
EDGE_1(config-if)# exit

! Conexión a Dist_1 (LAN - IP estática)
EDGE_1(config)# interface Gi0/0
EDGE_1(config-if)# ip address 192.168.100.2 255.255.255.0
EDGE_1(config-if)# no shutdown
EDGE_1(config-if)# exit

! NAT para VLANs
EDGE_1(config)# ip nat inside source list 1 interface Gi0/1 overload
EDGE_1(config)# access-list 1 permit 192.168.10.0 0.0.0.255
EDGE_1(config)# access-list 1 permit 192.168.20.0 0.0.0.255
EDGE_1(config)# access-list 1 permit 192.168.30.0 0.0.0.255
EDGE_1(config)# access-list 1 permit 192.168.40.0 0.0.0.255

! Marcado de interfaces NAT
EDGE_1(config)# interface Gi0/0
EDGE_1(config-if)# ip nat inside
EDGE_1(config-if)# interface Gi0/1
EDGE_1(config-if)# ip nat outside
EDGE_1(config-if)# end

! Verificaciones
EDGE_1# show access-lists  ! Verifica las redes permitidas
EDGE_1# show ip nat translations  ! Debe estar vacío hasta que haya tráfico




## 🔹 Paso 3: Configuración del Router EDGE_2
Router> enable
Router# configure terminal
Router(config)# hostname EDGE_2
EDGE_2(config)#

! Conexión a ISP2 (WAN - DHCP o IP estática)
EDGE_2(config)# interface Gi0/1
EDGE_2(config-if)# ip address dhcp  ! O usa IP estática si tu ISP2 lo requiere
EDGE_2(config-if)# no shutdown
EDGE_2(config-if)# exit

! Conexión a Dist_2 (LAN - IP estática, diferente a EDGE_1)
EDGE_2(config)# interface Gi0/0
EDGE_2(config-if)# ip address 192.168.100.3 255.255.255.0  ! Única en la red
EDGE_2(config-if)# no shutdown
EDGE_2(config-if)# exit

! NAT para VLANs (mismo ACL que EDGE_1, pero con interfaz Gi0/1 de EDGE_2)
EDGE_2(config)# ip nat inside source list 1 interface Gi0/1 overload
EDGE_2(config)# access-list 1 permit 192.168.10.0 0.0.0.255
EDGE_2(config)# access-list 1 permit 192.168.20.0 0.0.0.255
EDGE_2(config)# access-list 1 permit 192.168.30.0 0.0.0.255
EDGE_2(config)# access-list 1 permit 192.168.40.0 0.0.0.255

! Marcado de interfaces NAT
EDGE_2(config)# interface Gi0/0
EDGE_2(config-if)# ip nat inside
EDGE_2(config-if)# interface Gi0/1
EDGE_2(config-if)# ip nat outside
EDGE_2(config-if)# end

! Verificaciones clave
EDGE_2# show ip interface brief  ! Gi0/0 y Gi0/1 deben estar up/up
EDGE_2# show ip route  ! Debe mostrar la ruta por defecto via Gi0/1
EDGE_2# ping 8.8.8.8  ! Prueba conectividad a Internet (sin NAT aún)

## 🔹 Paso 4: Configuración del Dist_1

    Router>
    Router> enable
    Router#
    Router# configure terminal
    Routerno(config)#hostname Dist_1
    Dist_1(config)#
    
    ! Activar el enrutamiento
    Dist_1(config)# ip routing
    
    ! Subinterfaces por VLAN
    Dist_1(config)# interface Gi0/0.10
    Dist_1(config-subif)# encapsulation dot1Q 10
    Dist_1(config-subif)# ip address 192.168.10.1 255.255.255.0
    Dist_1(config-if)# no shutdown
    Dist_1(config-subif)# exit

    Dist_1(config)# interface Gi0/1.20
    Dist_1(config-subif)# encapsulation dot1Q 20
    Dist_1(config-subif)# ip address 192.168.20.1 255.255.255.0
    Dist_1(config-if)# no shutdown
    Dist_1(config-subif)# exit
    
    Dist_1(config)# interface G0/2.30
    Dist_1(config-subif)# encapsulation dot1Q 30
    Dist_1(config-subif)# ip address 192.168.30.1 255.255.255.0
    Dist_1(config-if)# no shutdown
    Dist_1(config-subif)# exit
    
    Dist_1(config)# interface Gi0/3.40
    Dist_1(config-subif)# encapsulation dot1Q 40
    Dist_1(config-subif)# ip address 192.168.40.1 255.255.255.0
    Dist_1(config-if)# no shutdown
    Dist_1(config-subif)# exit
        
    
    Dist_1(config)# end
    Dist_1# write memory

## 🔹 Paso 5: Configuración del Dist_2

    Router>
    Router> enable
    Router#
    Router# configure terminal
    Routerno(config)#hostname Dist_2
    Dist_2(config)#
    
    ! Activar el enrutamiento
    Dist_2(config)# ip routing
    
    ! Subinterfaces por VLAN
    Dist_2(config)# interface Gi0/3.10
    Dist_2(config-subif)# encapsulation dot1Q 10
    Dist_2(config-subif)# ip address 192.168.10.1 255.255.255.0
    Dist_2(config-if)# no shutdown
    Dist_2(config-subif)# exit

    Dist_2(config)# interface Gi0/2.20
    Dist_2(config-subif)# encapsulation dot1Q 20
    Dist_2(config-subif)# ip address 192.168.20.1 255.255.255.0
    Dist_2(config-if)# no shutdown
    Dist_2(config-subif)# exit
    
    Dist_2(config)# interface G0/1.30
    Dist_2(config-subif)# encapsulation dot1Q 30
    Dist_2(config-subif)# ip address 192.168.30.1 255.255.255.0
    Dist_2(config-if)# no shutdown
    Dist_2(config-subif)# exit
    
    Dist_2(config)# interface Gi0/0.40
    Dist_2(config-subif)# encapsulation dot1Q 40
    Dist_2(config-subif)# ip address 192.168.40.1 255.255.255.0
    Dist_2(config-if)# no shutdown
    Dist_2(config-subif)# exit
        
    
    Dist_2(config)# end
    Dist_2# write memory





## 🔹 Paso 6: Asignación de Interfaces en el Switch FINANZAS
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

## 🔹 Paso 7: Asignación de Interfaces en el Switch SAC
| Puerto Switch      | Departamento         | VLAN |
|--------------------|----------------------|------|
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


## 🔹 Paso 8: Asignación de Interfaces en el Switch IT
| Puerto Switch      | Departamento         | VLAN |
|--------------------|----------------------|------|
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


## 🔹 Paso 9: Asignación de Interfaces en el Switch GERENCIA
| Puerto Switch      | Departamento         | VLAN |
|--------------------|----------------------|------|
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




## 🔹 Paso 10: Control de Comunicación entre VLANs DIST_1
Bloquear que Finanzas se comunique con Atención al Cliente:
! Bloquear comunicación entre VLAN 10 (Finanzas) y VLAN 20 (SAC)
Dist_1(config)# ip access-list extended BLOQUEAR_FINANZAS_SAC
Dist_1(config-ext-nacl)# deny ip 192.168.10.0 0.0.0.255 192.168.20.0 0.0.0.255
Dist_1(config-ext-nacl)# deny ip 192.168.20.0 0.0.0.255 192.168.10.0 0.0.0.255
Dist_1(config-ext-nacl)# permit ip any any  ! Permite todo el resto de tráfico
Dist_1(config-ext-nacl)# exit

! Aplicar ACL a las subinterfaces afectadas
Dist_1(config)# interface Gi0/0.10  ! Subinterfaz VLAN 10
Dist_1(config-subif)# ip access-group BLOQUEAR_FINANZAS_SAC in
Dist_1(config-subif)# exit

Dist_1(config)# interface Gi0/1.20  ! Subinterfaz VLAN 20
Dist_1(config-subif)# ip access-group BLOQUEAR_FINANZAS_SAC in
Dist_1(config-subif)# exit

! Opcional: Bloquear VLAN 10 -> VLAN 30 (IT) si es necesario
Dist_1(config)# ip access-list extended BLOQUEAR_FINANZAS_IT
Dist_1(config-ext-nacl)# deny ip 192.168.10.0 0.0.0.255 192.168.30.0 0.0.0.255
Dist_1(config-ext-nacl)# permit ip any any
Dist_1(config-ext-nacl)# exit
Dist_1(config)# interface Gi0/0.10
Dist_1(config-subif)# ip access-group BLOQUEAR_FINANZAS_IT in




## 🔹 Paso 11: Control de Comunicación entre VLANs DIST_1
! Configuración simétrica a Dist_1 (para redundancia)
Dist_2(config)# ip access-list extended BLOQUEAR_FINANZAS_SAC
Dist_2(config-ext-nacl)# deny ip 192.168.10.0 0.0.0.255 192.168.20.0 0.0.0.255
Dist_2(config-ext-nacl)# deny ip 192.168.20.0 0.0.0.255 192.168.10.0 0.0.0.255
Dist_2(config-ext-nacl)# permit ip any any
Dist_2(config-ext-nacl)# exit

! Aplicar ACLs
Dist_2(config)# interface Gi0/3.10  ! VLAN 10
Dist_2(config-subif)# ip access-group BLOQUEAR_FINANZAS_SAC in
Dist_2(config-subif)# exit

Dist_2(config)# interface Gi0/2.20  ! VLAN 20
Dist_2(config-subif)# ip access-group BLOQUEAR_FINANZAS_SAC in
Dist_2(config-subif)# exit

## 🔹 Paso 10: Control de Comunicación entre VLANs DIST_1
