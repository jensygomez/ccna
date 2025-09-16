# NetMonDB/core/genie_parser/parser.py

from genie.conf.base import Device
from genie.libs.parser.ios.show_running_config import ShowRunningConfig

def parse_show_with_genie(output, command):
    """
    Aquí se puede extender para usar Genie y convertir output a dict/JSON.
    """
    # Placeholder simple: devuelve output en dict
    return {"show_running_config": output}
