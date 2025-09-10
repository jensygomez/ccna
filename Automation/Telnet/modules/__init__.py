# modules/__init__.py
from .utils import obtener_interfaces_red
from . import bastion_scanner
from . import network_discovery
from . import internal_scanner

__all__ = ['obtener_interfaces_red', 'bastion_scanner', 'network_discovery', 'internal_scanner']