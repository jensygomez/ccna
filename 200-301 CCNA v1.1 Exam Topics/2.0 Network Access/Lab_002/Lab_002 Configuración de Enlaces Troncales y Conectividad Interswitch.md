# Lab 2: Configuración de Enlaces Troncales y Conectividad Interswitch

## 📋 Objetivo

Configurar y verificar enlaces troncales entre múltiples switches, implementar el protocolo 802.1Q y configurar la Native VLAN para permitir la conectividad entre dispositivos en la misma VLAN a través de switches diferentes.

## 🔧 Topología Física

- **Switches L2:** Switch_01, Switch_02, Switch_03
- **PCs:** PC1 (VLAN 10), PC2 (VLAN 20), PC3 (VLAN 10), PC4 (VLAN 20)

## 🔌 Conexiones


|Dispositivo A|Interfaz A|Dispositivo B|Interfaz B|
|-------------|----------|-------------|----------|
|Switch_01    |Gi0/1     |Switch_02    |Gi0/1     |
|Switch_02    |Gi0/2     |Switch_03    |Gi0/1     |
|Switch_01    |Gi1/0     |PC1          |e0        |
|Switch_01    |Gi2/0     |PC2          |e0        |
|Switch_03    |Gi1/0     |PC3          |e0        |
|Switch_03    |Gi2/0     |PC4          |e0        |

## 📡 Direccionamiento IP


|Dispositivo|Interfaz |Dirección IP |Máscara      |VLAN|
|-----------|---------|-------------|-------------|----|
|PC1        |e0       |192.168.10.10|255.255.255.0|10  |
|PC2        |e0       |192.168.20.10|255.255.255.0|20  |
|PC3        |e0       |192.168.10.20|255.255.255.0|10  |
|PC4        |e0       |192.168.20.20|255.255.255.0|20  |

## 🚀 Configuración

### 1\. Configurar VLANs en los Switches

**En Switch_01:**

    Switch>en
    Switch#configure terminal
    Switch(config)#hostname Switch_01
    Switch_01(config)#vlan 10
    Switch_01(config-vlan)#name SALES
    Switch_01(config-vlan)#exit
    Switch_01(config)#vlan 20
    Switch_01(config-vlan)#name HR
    Switch_01(config-vlan)#exit
    Switch_01(config)#vlan 99
    Switch_01(config-vlan)#name NATIVE
    Switch_01(config-vlan)#exit

**En Switch_02:**

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



**En Switch_03:**

    Switch>en
    Switch#configure terminal
    Switch(config)#hostname Switch_03
    Switch_03(config)#vlan 10
    Switch_03(config-vlan)#name SALES
    Switch_03(config-vlan)#exit
    Switch_03(config)#vlan 20
    Switch_03(config-vlan)#name HR
    Switch_03(config-vlan)#exit
    Switch_03(config)#vlan 99
    Switch_03(config-vlan)#name NATIVE
    Switch_03(config-vlan)#exit


### 2. Configurar puertos de acceso

**En Switch_01:**
    Switch_01(config)#interface range Gi1/0 - 3
    Switch_01(config-if)#switchport mode access
    Switch_01(config-if)#switchport access vlan 10
    Switch_01(config-if)#no shutdown
    Switch_01(config-if)#exit

    Switch_01(config)#interface Gi2/0
    Switch_01(config-if)#switchport mode access
    Switch_01(config-if)#switchport access vlan 20
    Switch_01(config-if)#no shutdown
    Switch_01(config-if)#exit

**En Switch_03:**

    Switch_03(config)#interface Gi1/0
    Switch_03(config-if)#switchport mode access
    Switch_03(config-if)#switchport access vlan 10
    Switch_03(config-if)#no shutdown
    Switch_03(config-if)#exit

    Switch_03(config)#interface Gi2/0
    Switch_03(config-if)#switchport mode access
    Switch_03(config-if)#switchport access vlan 20
    Switch_03(config-if)#no shutdown
    Switch_03(config-if)#exit

### 3. Configurar puertos de acceso

**En Switch_01:**

    Switch_01(config)#interface Gi0/1
    Switch_01(config-if)#switchport trunk encapsulation dot1q
    Switch_01(config-if)#switchport mode trunk
    Switch_01(config-if)#switchport trunk native vlan 99
    Switch_01(config-if)#switchport trunk allowed vlan 10,20,99
    Switch_01(config-if)#no shutdown
    Switch_01(config-if)#end
    Switch_01#copy running-config startup-config

**En Switch_02:**
    Switch_02(config)#interface range Gi0/1-2
    Switch_02(config-if)#switchport trunk encapsulation dot1q
    Switch_02(config-if-range)#switchport mode trunk
    Switch_02(config-if-range)#switchport trunk native vlan 99
    Switch_02(config-if-range)#switchport trunk allowed vlan 10,20,99
    Switch_02(config-if-range)#no shutdown
    Switch_02(config-if-range)#end
    Switch_02#copy running-config startup-config

**En Switch_03:**
    Switch_03(config)#interface Gi0/0
    Switch_03(config-if)#switchport trunk encapsulation dot1q
    Switch_03(config-if)#switchport mode trunk
    Switch_03(config-if)#switchport trunk native vlan 99
    Switch_03(config-if)#switchport trunk allowed vlan 10,20,99
    Switch_03(config-if)#no shutdown
    Switch_03(config-if)#end
    Switch_03#copy running-config startup-config





### 4. Configurar las PCs

**En PC1:**

    ip 192.168.10.10 255.255.255.0 192.168.10.1


**En PC2:**

    ip 192.168.20.10 255.255.255.0 192.168.20.1

**En PC3:**
    ip 192.168.10.20 255.255.255.0 192.168.10.1

**En PC4:**

    ip 192.168.20.20 255.255.255.0 192.168.20.1





## ✅ Verificación

### Comandos de Verificación Útiles:

- **Ver VLANs:**  show vlan brief
- **Ver troncales:**  show interfaces trunk
- **Ver configuración de interfaz:**  show interfaces [interface] switchport
- **Ver estado de interfaces:**  show interfaces status
- **Ver resumen de IP:**  show ip interface brief

### Comandos de Verificación Útiles:
    Switch_01# show interfaces Gi0/1 trunk
    Switch_02# show interfaces Gi0/1 trunk
    Switch_02# show interfaces Gi0/2 trunk
    Switch_03# show interfaces Gi0/1 trunk


### Pruebas de Conectividad:

- Desde  **PC1**:  ping 192.168.10.20 (debería funcionar - misma VLAN)
- Desde  **PC2**:  ping 192.168.20.20 (debería funcionar - misma VLAN)
- Desde  **PC1**:  ping 192.168.20.10 (no debería funcionar - VLAN diferente)
- Desde  **PC1**:  ping 192.168.20.20 (no debería funcionar - VLAN diferente)


## 🐛 Troubleshooting Tips

- La Native VLAN (VLAN 99) debe ser la misma en ambos extremos del enlace troncal
- Los paquetes de la Native VLAN se envían sin etiqueta 802.1Q
- Todos los switches deben tener las mismas VLANs para que la comunicación funcione correctamente
- Los puertos troncales permiten el tráfico de múltiples VLANs, a diferencia de los puertos de acceso

