# NetMonDB/core/table_display/display.py

from tabulate import tabulate

def show_table(parsed_data):
    # Ejemplo simple: mostrar show running config como una línea por fila
    output = parsed_data.get("show_running_config", "").splitlines()
    table = [[line] for line in output]
    headers = ["Running Config"]
    print(tabulate(table, headers=headers, tablefmt="pretty"))
