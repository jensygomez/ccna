#!/bin/bash
# setup_bastion.sh - Configuración inteligente para Bastion_01 (con entorno virtual)

set -e  # Detener en caso de error

echo "🔄 Iniciando setup de Bastion_01..."
echo "==========================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para detectar si necesita sudo
needs_sudo() {
    [ "$(id -u)" -ne 0 ]
}

# Función de ejecución inteligente
run_cmd() {
    if needs_sudo; then
        sudo "$@"
    else
        "$@"
    fi
}

# Función para verificar e instalar paquetes del sistema
install_package() {
    if dpkg -l | grep -qw "$1"; then
        echo -e "${GREEN}✅ $1 ya está instalado${NC}"
    else
        echo -e "${YELLOW}📦 Instalando $1...${NC}"
        run_cmd apt install -y "$1"
    fi
}

# Detectar si estamos en modo root o usuario normal
if needs_sudo; then
    echo -e "${YELLOW}👤 Modo usuario: Se usará sudo cuando sea necesario${NC}"
else
    echo -e "${GREEN}🛡️  Modo root: Ejecutando directamente${NC}"
fi

# Actualizar sistema
echo -e "${YELLOW}🔄 Actualizando lista de paquetes...${NC}"
run_cmd apt update || echo -e "${YELLOW}⚠️ Apt update tuvo errores, continuando...${NC}"

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

# Configurar entorno virtual
echo -e "${YELLOW}⚙️ Configurando entorno virtual Python...${NC}"
VENV_PATH="/ccna/venv"
if [ ! -d "$VENV_PATH" ]; then
    run_cmd mkdir -p /ccna
    python3 -m venv "$VENV_PATH"
    echo -e "${GREEN}✅ Entorno virtual creado en $VENV_PATH${NC}"
else
    echo -e "${GREEN}✅ Entorno virtual ya existe${NC}"
fi

# Activar entorno virtual
source "$VENV_PATH/bin/activate"

# Actualizar pip dentro del venv
echo -e "${YELLOW}📦 Actualizando pip dentro del entorno virtual...${NC}"
pip install --upgrade pip

# Instalar librerías de automatización dentro del venv
echo -e "${YELLOW}📦 Instalando librerías Python de automatización...${NC}"
pip install netmiko paramiko napalm nornir scrapli textfsm jinja2 pyyaml requests rich

# Verificar librerías instaladas
echo -e "${YELLOW}🔍 Verificando librerías instaladas...${NC}"
python3 - <<EOF
try:
    import netmiko, paramiko, napalm, nornir, scrapli
    print("✅ Netmiko:", netmiko.__version__)
    print("✅ Paramiko:", paramiko.__version__)
    print("✅ NAPALM:", napalm.__version__)
    print("✅ Scrapli:", scrapli.__version__)
    print("🎉 Todas las librerías están instaladas correctamente!")
except ImportError as e:
    print("❌ Error importando librerías:", e)
EOF

# Configurar Git
echo -e "${YELLOW}⚙️ Configurando Git...${NC}"
if command -v git &> /dev/null; then
    git config --global user.name "Jensy Gomez"
    git config --global user.email "jensygomez@gmail.com"
    echo -e "${GREEN}✅ Git configurado correctamente${NC}"
else
    echo -e "${RED}❌ Git no está instalado, instalando...${NC}"
    install_package git
    git config --global user.name "Jensy Gomez"
    git config --global user.email "jensygomez@gmail.com"
fi

# Clonar repositorio si no existe
if [ ! -d "/ccna/.git" ]; then
    echo -e "${YELLOW}📥 Clonando repositorio CCNA...${NC}"
    run_cmd git clone https://github.com/jensygomez/ccna.git /ccna
    echo -e "${GREEN}✅ Repositorio clonado en /ccna${NC}"
else
    echo -e "${GREEN}✅ Repositorio ya existe, actualizando...${NC}"
    cd /ccna && git pull origin main
fi

# Crear enlace simbólico si no existe
if [ ! -L "/automation" ]; then
    echo -e "${YELLOW}🔗 Creando enlace simbólico...${NC}"
    run_cmd ln -sf /ccna/Automation /automation
    echo -e "${GREEN}✅ Enlace simbólico creado: /automation${NC}"
fi

# Configurar permisos adecuados
if needs_sudo; then
    echo -e "${YELLOW}🔐 Ajustando permisos...${NC}"
    run_cmd chown -R $(id -u):$(id -g) /ccna /automation
fi

# Configurar alias para usar el entorno virtual automáticamente
echo -e "${YELLOW}⚙️ Configurando aliases...${NC}"
grep -qxF 'alias activate-ccna="source /ccna/venv/bin/activate"' ~/.bashrc || echo 'alias activate-ccna="source /ccna/venv/bin/activate"' >> ~/.bashrc
grep -qxF 'alias automation="cd /automation || cd /ccna/Automation"' ~/.bashrc || echo 'alias automation="cd /automation || cd /ccna/Automation"' >> ~/.bashrc
grep -qxF 'alias ccna-repo="cd /ccna"' ~/.bashrc || echo 'alias ccna-repo="cd /ccna"' >> ~/.bashrc

echo -e "${GREEN}===========================================${NC}"
echo -e "${GREEN}🎉 Setup de Bastion_01 completado${NC}"
echo -e "${GREEN}===========================================${NC}"
echo -e "${YELLOW}💡 Para activar el entorno virtual usa:${NC}"
echo -e "  source /ccna/venv/bin/activate"
echo -e ""
echo -e "${YELLOW}💡 O simplemente:${NC}"
echo -e "  activate-ccna"
echo -e ""
echo -e "${GREEN}✅ Bastion_01 está lista para automatización de redes!${NC}"
