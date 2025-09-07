#!/bin/bash
# setup_bastion_root.sh - Configuración completa para Bastion_01 como root

set -e

echo "🔄 Iniciando setup de Bastion_01 como root..."
echo "==========================================="

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Función para instalar paquetes si no existen
install_package() {
    if dpkg -l | grep -qw "$1"; then
        echo -e "${GREEN}✅ $1 ya está instalado${NC}"
    else
        echo -e "${YELLOW}📦 Instalando $1...${NC}"
        apt install -y "$1"
    fi
}

# Actualizar sistema
echo -e "${YELLOW}🔄 Actualizando lista de paquetes...${NC}"
apt update || echo -e "${YELLOW}⚠️ Apt update tuvo errores, continuando...${NC}"

# Instalar herramientas
echo -e "${YELLOW}📦 Instalando herramientas del sistema...${NC}"
for pkg in git python3 python3-pip python3-venv net-tools iproute2 curl wget openssh-client; do
    install_package $pkg
done

# Crear entorno virtual
VENV_PATH="/ccna/venv"
if [ ! -d "$VENV_PATH" ]; then
    mkdir -p /ccna
    python3 -m venv "$VENV_PATH"
    echo -e "${GREEN}✅ Entorno virtual creado en $VENV_PATH${NC}"
else
    echo -e "${GREEN}✅ Entorno virtual ya existe${NC}"
fi

# Activar entorno virtual
source "$VENV_PATH/bin/activate"

# Actualizar pip
echo -e "${YELLOW}📦 Actualizando pip...${NC}"
pip install --upgrade pip

# Instalar librerías Python
echo -e "${YELLOW}📦 Instalando librerías Python...${NC}"
pip install --upgrade netmiko paramiko napalm nornir scrapli textfsm jinja2 pyyaml requests rich

# Verificar librerías instaladas CORRECTAMENTE
echo -e "${YELLOW}🔍 Verificando librerías...${NC}"
python3 -c "
try:
    from netmiko import ConnectHandler
    print('✅ netmiko: OK')
except ImportError:
    print('❌ netmiko: NO instalado')

try:
    import paramiko
    print('✅ paramiko:', paramiko.__version__)
except ImportError:
    print('❌ paramiko: NO instalado')

try:
    import napalm
    print('✅ napalm: OK')
except ImportError:
    print('❌ napalm: NO instalado')

try:
    import nornir
    print('✅ nornir:', nornir.__version__)
except ImportError:
    print('❌ nornir: NO instalado')

try:
    import scrapli
    print('✅ scrapli:', scrapli.__version__)
except ImportError:
    print('❌ scrapli: NO instalado')

try:
    import textfsm
    print('✅ textfsm: OK')
except ImportError:
    print('❌ textfsm: NO instalado')

try:
    import jinja2
    print('✅ jinja2:', jinja2.__version__)
except ImportError:
    print('❌ jinja2: NO instalado')

try:
    import yaml
    print('✅ pyyaml: OK')
except ImportError:
    print('❌ pyyaml: NO instalado')

try:
    import requests
    print('✅ requests:', requests.__version__)
except ImportError:
    print('❌ requests: NO instalado')

try:
    import rich
    print('✅ rich: OK')
except ImportError:
    print('❌ rich: NO instalado')
"

# Configurar Git
echo -e "${YELLOW}⚙️ Configurando Git...${NC}"
git config --global user.name "Jensy Gomez"
git config --global user.email "jensygomez@gmail.com"
echo -e "${GREEN}✅ Git configurado correctamente${NC}"

# Clonar o actualizar repositorio CCNA
if [ ! -d "/ccna/.git" ]; then
    echo -e "${YELLOW}📥 Clonando repositorio CCNA...${NC}"
    git clone https://github.com/jensygomez/ccna.git /ccna
    echo -e "${GREEN}✅ Repositorio clonado${NC}"
else
    echo -e "${YELLOW}🔄 Repositorio existente, actualizando...${NC}"
    cd /ccna && git pull origin main
fi

# Crear enlace simbólico /automation
if [ ! -L "/automation" ]; then
    ln -sf /ccna/Automation /automation
    echo -e "${GREEN}✅ Enlace simbólico /automation creado${NC}"
fi

# Permisos
chown -R root:root /ccna /automation

# Configurar aliases
grep -qxF 'alias activate-ccna="source /ccna/venv/bin/activate"' ~/.bashrc || echo 'alias activate-ccna="source /ccna/venv/bin/activate"' >> ~/.bashrc
grep -qxF 'alias automation="cd /automation || cd /ccna/Automation"' ~/.bashrc || echo 'alias automation="cd /automation || cd /ccna/Automation"' >> ~/.bashrc
grep -qxF 'alias ccna-repo="cd /ccna"' ~/.bashrc || echo 'alias ccna-repo="cd /ccna"' >> ~/.bashrc

echo -e "${GREEN}===========================================${NC}"
echo -e "${GREEN}🎉 Setup de Bastion_01 completado${NC}"
echo -e "${GREEN}===========================================${NC}"
echo -e "${YELLOW}💡 Para activar el entorno virtual usa:${NC} source /ccna/venv/bin/activate"
echo -e "  o simplemente: activate-ccna"