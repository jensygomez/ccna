# modules/parsers/device_info.py


# modules/parsers/device_info.py
import re

def parse_hostname(output):
    """Extrae el hostname desde show version."""
    match = re.search(r"^(\S+)\s+uptime is", output, re.MULTILINE)
    return match.group(1) if match else "unknown"

def parse_mac(output):
    """Extrae la MAC (Processor board ID) desde show version."""
    match = re.search(r"Processor board ID (\S+)", output)
    return match.group(1) if match else "unknown"
