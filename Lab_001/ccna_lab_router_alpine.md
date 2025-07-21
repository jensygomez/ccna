
# Laboratorio: Configuración Básica de Router Cisco y Cliente Alpine

---

## Configuración del Router Cisco

1. Accede a la consola del router.

2. Entra en modo privilegiado:

   ```
   enable
   ```

3. Entra en modo de configuración global:

   ```
   configure terminal
   ```

4. Cambia el nombre del router (opcional):

   ```
   hostname R1
   ```

5. Configura la interfaz que conecta al cliente (Ejemplo: Ethernet0/1):

   ```
   interface Ethernet0/1
   ip address 192.168.1.1 255.255.255.0
   no shutdown
   exit
   ```

6. Sal del modo de configuración:

   ```
   end
   ```

7. Guarda la configuración:

   ```
   write memory
   ```

8. Verifica que la interfaz esté activa y con IP asignada:

   ```
   show ip interface brief
   ```

---

## Configuración del Cliente Alpine Linux

1. Accede a la consola de Alpine.

2. Verifica el nombre de la interfaz de red (normalmente `eth0`):

   ```
   ip link
   ```

3. Asigna una dirección IP con máscara /24 a la interfaz:

   ```
   sudo ip addr add 192.168.1.10/24 dev eth0
   ```

4. Activa la interfaz:

   ```
   sudo ip link set eth0 up
   ```

5. Verifica que la IP haya sido asignada correctamente:

   ```
   ip addr show dev eth0
   ```

6. Agrega la ruta por defecto (gateway) hacia el router:

   ```
   sudo ip route add default via 192.168.1.1
   ```

7. Verifica la tabla de rutas:

   ```
   ip route show
   ```

8. Prueba conectividad hacia el router:

   ```
   ping 192.168.1.1
   ```

---

## Notas

- Los comandos con `sudo` son necesarios si no estás en modo root en Alpine.
- La configuración IP en Alpine con `ip addr add` es temporal y se perderá al reiniciar a menos que se configure de forma persistente.
- Este laboratorio no incluye configuración DHCP; todo es estático.
