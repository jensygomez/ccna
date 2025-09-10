# reparar_db.py
import csv
import os


def reparar_base_datos():
    db_file = "db/dispositivos.csv"

    if not os.path.exists(db_file):
        print("❌ No existe la base de datos")
        return

    print("🔧 Verificando y reparando base de datos...")

    try:
        # Leer el archivo actual
        with open(db_file, 'r', newline='', encoding='utf-8') as csvfile:
            lines = csvfile.readlines()

        # Verificar si la primera línea tiene los encabezados correctos
        if lines and not lines[0].startswith('MAC,IP,Hostname,Tipo,ÚltimaActualización'):
            print("⚠️  Encabezados incorrectos, reparando...")

            # Crear nuevos encabezados
            nuevos_encabezados = "MAC,IP,Hostname,Tipo,ÚltimaActualización\n"

            # Si hay datos, intentar preservarlos
            if len(lines) > 1:
                # Escribir el archivo corregido
                with open(db_file, 'w', newline='', encoding='utf-8') as csvfile:
                    csvfile.write(nuevos_encabezados)
                    # Escribir el resto de las líneas (asumiendo que tienen 5 campos)
                    for line in lines:
                        if line.count(',') >= 4:  # Al menos 4 comas = 5 campos
                            csvfile.write(line)

                print("✅ Base de datos reparada")
            else:
                # Solo escribir encabezados si no hay datos
                with open(db_file, 'w', newline='', encoding='utf-8') as csvfile:
                    csvfile.write(nuevos_encabezados)
                print("✅ Base de datos reparada (solo encabezados)")
        else:
            print("✅ La base de datos parece estar correcta")

    except Exception as e:
        print(f"❌ Error reparando base de datos: {e}")


if __name__ == "__main__":
    reparar_base_datos()