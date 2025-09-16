# network_project/scripts/project_structure.py


import os

def print_tree(root_dir, prefix="", exclude_folders=None):
    """
    Recorre la estructura de carpetas y archivos y la imprime en forma de árbol.
    exclude_folders: lista de nombres de carpetas a excluir
    """
    if exclude_folders is None:
        exclude_folders = []

    entries = sorted(os.listdir(root_dir))
    for index, entry in enumerate(entries):
        if entry in exclude_folders:
            continue

        path = os.path.join(root_dir, entry)
        connector = "└── " if index == len(entries) - 1 else "├── "
        print(prefix + connector + entry)

        if os.path.isdir(path):
            extension = "    " if index == len(entries) - 1 else "│   "
            print_tree(path, prefix + extension, exclude_folders)

if __name__ == "__main__":
    ROOT_DIR = "."  # 👈 Recorrer desde la carpeta actual
    EXCLUDE = ["venv", "__pycache__"]  # 👈 Carpetas a excluir

    print(f"📂 Estructura desde: {os.path.abspath(ROOT_DIR)}\n")
    print_tree(ROOT_DIR, exclude_folders=EXCLUDE)
