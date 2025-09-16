# NetMonDB/core/genie_parser/parser.py

# core/genie_parser/parser.py
def parse_show_with_genie(output, command="show running-config"):
    """
    Función genérica para devolver el output en formato dict.
    Se puede extender luego para parsers específicos.
    """
    if not output:
        return {}

    # Simple: cada línea en una lista dentro del dict
    lines = output.splitlines()
    return {"show_running_config": lines}
