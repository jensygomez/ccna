def normalizar_red(red_input):
    """Asegura que la red tenga formato CIDR"""
    if '/' not in red_input:
        if red_input.endswith('.0'):
            return red_input + '/24'
        else:
            octetos = red_input.split('.')
            if len(octetos) == 4:
                return '.'.join(octetos[:3]) + '.0/24'
    return red_input  # <- ESTA LÍNEA DEBE SER ASÍ, sin el "(telnet)..." al final