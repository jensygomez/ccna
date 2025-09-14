# network_monitor/scripts/project_structure.py
import os

def print_tree(root_dir, prefix=""):
    """
    Imprime la estructura de carpetas y archivos en forma de árbol.
    """
    entries = sorted(os.listdir(root_dir))
    for index, entry in enumerate(entries):
        path = os.path.join(root_dir, entry)
        connector = "└── " if index == len(entries) - 1 else "├── "
        print(prefix + connector + entry)

        if os.path.isdir(path):
            extension = "    " if index == len(entries) - 1 else "│   "
            print_tree(path, prefix + extension)

if __name__ == "__main__":
    root_dir = os.getcwd()  # Detecta automáticamente la carpeta actual
    print(f"\n🌳 Estructura del proyecto {root_dir}:\n")
    print_tree(root_dir)
