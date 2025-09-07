#!/bin/bash
# setup_bastion.sh - Configuración completa para Bastion_01

set -e  # Detener en caso de error

# Solucionar error de repositorio de HashiCorp
if [ -f "/etc/apt/sources.list.d/hashicorp.list" ]; then
    echo -e "${YELLOW}⚠️  Repositorio HashiCorp detectado, solucionando...${NC}"
    # Intentar agregar la clave GPG
    wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | tee /usr/share/keyrings/hashicorp-archive-keyring.gpg 2>/dev/null || \
    echo -e "${YELLOW}⚠️  No se pudo agregar clave GPG, continuando...${NC}"
fi


echo "🔄 Iniciando setup de Bastion_01..."
echo "==========================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para verificar e instalar paquetes
install_package() {
    if dpkg -l | grep -q "$1"; then
        echo -e "${GREEN}✅ $1 ya está instalado${NC}"
    else
        echo -e "${YELLOW}📦 Instalando $1...${NC}"
        apt install -y "$1"
    fi
}

# Función para verificar e instalar pip packages
install_pip() {
    if pip3 list | grep -q "$1"; then
        echo -e "${GREEN}✅ $1 ya está instalado${NC}"
    else
        echo -e "${YELLOW}📦 Instalando $1...${NC}"
        pip3 install "$1"
    fi
}

# Actualizar sistema
echo -e "${YELLOW}🔄 Actualizando lista de paquetes...${NC}"
apt update

# Instalar herramientas del sistema
echo -e "${YELLOW}📦 Instalando herramientas del sistema...${NC}"
install_package git
install_package python3
install_package python3-pip
install_package python3-venv
install_package net-tools
install_package iproute2
install_package curl
install_package wget
install_package openssh-client

# Instalar librerías Python de network automation
echo -e "${YELLOW}📦 Instalando librerías Python...${NC}"
install_pip netmiko
install_pip paramiko
install_pip napalm
install_pip nornir
install_pip scrapli
install_pip textfsm
install_pip jinja2
install_pip pyyaml
install_pip requests

# Configurar Git (opcional)
echo -e "${YELLOW}⚙️ Configurando Git...${NC}"
git config --global user.name "Bastion_01"
git config --global user.email "bastion@network.automation"

# Verificar instalaciones
echo -e "${YELLOW}🔍 Verificando instalaciones...${NC}"
echo -e "Python: $(python3 --version)"
echo -e "Pip: $(pip3 --version)"
echo -e "Git: $(git --version)"

# Verificar librerías Python
echo -e "${YELLOW}🔍 Verificando librerías Python...${NC}"
python3 -c "
import netmiko, paramiko, napalm, nornir
print('✅ Netmiko:', netmiko.__version__)
print('✅ Paramiko:', paramiko.__version__)
print('✅ NAPALM:', napalm.__version__)
print('✅ Todas las librerías instaladas correctamente!')
"

# Clonar repositorio si no existe
if [ ! -d "/opt/ccna" ]; then
    echo -e "${YELLOW}📥 Clonando repositorio...${NC}"
    cd /opt
    git clone https://github.com/jensygomez/ccna.git
else
    echo -e "${GREEN}✅ Repositorio ya existe en /opt/ccna${NC}"
fi

# Crear enlace simbólico si no existe
if [ ! -L "/opt/automation" ]; then
    echo -e "${YELLOW}🔗 Creando enlace simbólico...${NC}"
    ln -s /opt/ccna/Automation /opt/automation
else
    echo -e "${GREEN}✅ Enlace simbólico ya existe${NC}"
fi

# Verificar estructura final
echo -e "${YELLOW}📁 Verificando estructura...${NC}"
ls -la /opt/automation/ 2>/dev/null || echo "⚠️  Carpeta Automation no encontrada"

# Configurar aliases útiles
echo -e "${YELLOW}⚙️ Configurando aliases...${NC}"
cat >> ~/.bashrc << EOF

# Aliases para automation
alias automation='cd /opt/automation'
alias ccna-repo='cd /opt/ccna'
alias update-scripts='cd /opt/ccna && git pull origin main'
alias py='python3'
EOF

echo -e "${GREEN}===========================================${NC}"
echo -e "${GREEN}🎉 Setup de Bastion_01 completado!${NC}"
echo -e "${GREEN}===========================================${NC}"
echo -e ""
echo -e "${YELLOW}📋 Comandos útiles:${NC}"
echo -e "  automation      → Ir a carpeta Automation"
echo -e "  ccna-repo       → Ir al repositorio completo"
echo -e "  update-scripts  → Actualizar scripts desde GitHub"
echo -e "  py              → Ejecutar python3"
echo -e ""
echo -e "${YELLOW}🚀 Para aplicar los aliases:${NC}"
echo -e "  source ~/.bashrc"
echo -e ""
echo -e "${GREEN}✅ Bastion_01 está lista para automation!${NC}"