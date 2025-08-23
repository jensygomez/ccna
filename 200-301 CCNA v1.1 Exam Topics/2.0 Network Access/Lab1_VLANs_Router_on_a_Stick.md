# Lab 1: VLANs & Router-on-a-Stick (Topología Actualizada)

## 📋 Objetivo

Configurar y verificar VLANs en múltiples switches y establecer conectividad
inter-VLAN utilizando Router-on-a-Stick.

## 🔧 Topología Física

- **Router:** R_iosv-1 (Interface: Gi0/1)
- **Switches L2:** Switch_01, Switch_02
- **PCs:** PC1, PC2

## 🔌 Conexiones


|Dispositivo A|Interfaz A|Dispositivo B|Interfaz B|
|-------------|----------|-------------|----------|
|R_iosv-1     |Gi0/1     |Switch_02    |Gi0/1     |
|Switch_02    |Gi0/0     |Switch_01    |Gi0/  0   |
|Switch_01    |Gi1/0     |PC1          |e0        |
|Switch_01    |Gi2/0     |PC2          |e0        |

## 📡 Direccionamiento IP


|Dispositivo|Interfaz |Dirección IP |Máscara      |VLAN|
|-----------|---------|-------------|-------------|----|
|PC1        |e0       |192.168.10.10|255.255.255.0|10  |
|PC2        |e0       |192.168.20.10|255.255.255.0|20  |
|R_iosv-1   |Gi0/1.10 |192.168.10.1 |255.255.255.0|10  |
|R_iosv-1   |Gi0/1.20 |192.168.20.1 |255.255.255.0|20  |

## 🚀 Configuración

### 1\. Configurar VLANs en los Switches

**En Switch_01:**

    Switch>
    Switch>en
    Switch#configure terminal
    Switch(config)#hostname Switch_01
    Switch_01(config)#

    Switch_01(config)#vlan 10
    Switch_01(config-vlan)#name SALES
    Switch_01(config-vlan)#exit

    Switch_01(config)# vlan 20
    Switch_01(config-vlan)#name HR
    Switch_01(config-vlan)#exit

    Switch_01(config)#vlan 99
    Switch_01(config-vlan)#name NATIVE
    Switch_01(config-vlan)#exit

    Switch_01(config)# interface range Gi1/0 - 3
    Switch_01(config-if-range)#switchport mode access
    Switch_01(config-if-range)#switchport access vlan 10
    Switch_01(config-if-range)#no shutdown 


    Switch_01(config)#interface range Gi2/0 - 3
    Switch_01(config-if-range)#switchport mode access
    Switch_01(config-if-range)#switchport access vlan 20
    Switch_01(config-if-range)#no shutdown
    Switch_01(config-if-range)#end


    Switch_01# copy running-config startup-config

    Switch_01# show vlan brief
    Switch_01# show interfaces status
    Switch_01# show ip interface brief

    Switch_01#configure terminal
    Switch_01(config)#interface Gi0/0
    Switch_01(config-if)#switchport trunk encapsulation dot1q
    Switch_01(config-if)#switchport mode trunk
    Switch_01(config-if)# switchport trunk native vlan 99
    Switch_01(config-if)# switchport trunk allowed vlan 10,20,99
    Switch_01(config-if)# no shutdown
    Switch_01(config-if)# end
    Switch_01#write memory

    Switch_01# show interfaces Gi0/0 trunk
    Switch_01# show interfaces Gi0/0 switchport

**En Switch_02:**

    Switch>
    Switch>en
    Switch#configure terminal
    Switch(config)#hostname Switch_02

    Switch_02(config)#vlan 10
    Switch_02(config-vlan)#name SALES
    Switch_02(config-vlan)#exit

    Switch_02(config)#vlan 20
    Switch_02(config-vlan)#name HR
    Switch_02(config-vlan)#exit

    Switch_02(config)#vlan 99
    Switch_02(config-vlan)#name NATIVE
    Switch_02(config-vlan)#exit
    Switch_02(config)#end
    Switch_02#

    Switch_02#configure terminal
    Switch_02(config)#interface Gi0/0
    Switch_02(config-if)#switchport trunk encapsulation dot1q
    Switch_02(config-if)#switchport mode trunk
    Switch_02(config-if)#switchport trunk native vlan 99
    Switch_02(config-if)#switchport trunk allowed vlan 10,20,99
    Switch_02(config-if)#no shutdown
    Switch_02(config-if)#exit
    Switch_02(config)#

    Switch_02(config)#interface Gi0/1
    Switch_02(config-if)#switchport trunk encapsulation dot1q
    Switch_02(config-if)#switchport mode trunk
    Switch_02(config-if)#switchport trunk native vlan 99
    Switch_02(config-if)#switchport trunk allowed vlan 10,20,99
    Switch_02(config-if)#no shutdown
    Switch_02(config-if)#end
    Switch_02#write memory

    Switch_02# show vlan brief
    Switch_02# show interfaces status
    Switch_02# show ip interface brief
    Switch_02# show interfaces Gi0/0 trunk
    Switch_02# show interfaces Gi0/0 switchport
    Switch_02# show interfaces Gi0/1 switchport





### 2. Configurar Router-on-a-Stick en R_iosv-1

**En R_iosv-1:**

    R_iosv-1#configure terminal
    R_iosv-1(config)#interface Gi0/1
    R_iosv-1(config-if)#no shutdown
    R_iosv-1(config-if)#end

# Configure correct subinterfaces
    R_iosv-1(config)#interface Gi0/1.10
    R_iosv-1(config-subif)#encapsulation dot1Q 10
    R_iosv-1(config-subif)#ip address 192.168.10.1 255.255.255.0
    R_iosv-1(config-subif)#exit

    R_iosv-1(config)#interface Gi0/1.20
    R_iosv-1(config-subif)#encapsulation dot1Q 20
    R_iosv-1(config-subif)#ip address 192.168.20.1 255.255.255.0
    R_iosv-1(config-subif)#exit
    R_iosv-1(config-if)#end
    R_iosv-1#copy run start





### 3. Configurar las PCs

**En PC1:**

    ip 192.168.10.10 255.255.255.0 192.168.10.1

**En PC2:**

    ip 192.168.20.10 255.255.255.0 192.168.20.1

## ✅ Verificación

### Comandos de Verificación Útiles:

- **Ver VLANs:**  show vlan brief
- **Ver troncales:**  show interfaces trunk
- **Ver interfaces del router:**  show ip interface brief
- **Ver tablas ARP:**  show arp

### Pruebas de Conectividad:

- Desde  **PC1**:  ping 192.168.20.10
- Desde  **PC2**:  ping 192.168.10.10
- Desde  **R_iosv-1**:  ping 192.168.10.10  y  ping 192.168.20.10

## 🐛 Troubleshooting Tips

- Asegúrate de que las VLANs estén creadas en  **ambos switches**.
- Verifica que los puertos trunk permitan el paso de las VLANs  **10, 20 y 99**.
- Confirma que las subinterfaces del router estén  **UP/UP**.
- Revisa que los gateways predeterminados en las PCs estén correctos.

