#!/bin/bash
# setup_bastion_root.sh - Configuración para Bastion_01 ejecutando como root

set -e  # Detener en caso de error

echo "🔄 Iniciando setup de Bastion_01 como root..."
echo "==========================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para instalar paquetes del sistema si no están presentes
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

# Instalar herramientas básicas
echo -e "${YELLOW}📦 Instalando herramientas del sistema...${NC}"
for pkg in git python3 python3-pip python3-venv net-tools iproute2 curl wget openssh-client; do
    install_package "$pkg"
done

# Configurar entorno virtual
echo -e "${YELLOW}⚙️ Configurando entorno virtual Python...${NC}"
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

# Actualizar pip dentro del venv
echo -e "${YELLOW}📦 Actualizando pip dentro del entorno virtual...${NC}"
pip install --upgrade pip

# Instalar librerías Python de automatización dentro del venv
echo -e "${YELLOW}📦 Instalando librerías Python de automatización...${NC}"
pip install netmiko paramiko napalm nornir scrapli textfsm jinja2 pyyaml requests rich

# Verificar librerías instaladas dentro del venv
echo -e "${YELLOW}🔍 Verificando librerías instaladas...${NC}"
python3 - <<EOF
import importlib, importlib.metadata
libs = ["netmiko","paramiko","napalm","nornir","scrapli","textfsm","jinja2","pyyaml","requests","rich"]
for lib in libs:
    try:
        module = importlib.import_module(lib)
        try:
            version = module.__version__
        except AttributeError:
            version = importlib.metadata.version(lib)
        print(f"✅ {lib}: {version}")
    except ImportError:
        print(f"❌ {lib} NO instalado")
EOF

# Configurar Git
echo -e "${YELLOW}⚙️ Configurando Git...${NC}"
git config --global user.name "Jensy Gomez"
git config --global user.email "jensygomez@gmail.com"
echo -e "${GREEN}✅ Git configurado correctamente${NC}"

# Clonar o actualizar repositorio CCNA
if [ -d "/ccna/.git" ]; then
    echo -e "${YELLOW}🔄 Repositorio existente, actualizando...${NC}"
    cd /ccna && git pull origin main
else
    echo -e "${YELLOW}📥 Clonando repositorio CCNA...${NC}"
    git clone https://github.com/jensygomez/ccna.git /ccna
fi

# Crear enlace simbólico si no existe
if [ ! -L "/automation" ]; then
    echo -e "${YELLOW}🔗 Creando enlace simbólico...${NC}"
    ln -sf /ccna/Automation /automation
    echo -e "${GREEN}✅ Enlace simbólico creado: /automation${NC}"
fi

# Configurar alias en root
echo -e "${YELLOW}⚙️ Configurando aliases...${NC}"
grep -qxF 'alias activate-ccna="source /ccna/venv/bin/activate"' ~/.bashrc || echo 'alias activate-ccna="source /ccna/venv/bin/activate"' >> ~/.bashrc
grep -qxF 'alias automation="cd /automation || cd /ccna/Automation"' ~/.bashrc || echo 'alias automation="cd /automation || cd /ccna/Automation"' >> ~/.bashrc
grep -qxF 'alias ccna-repo="cd /ccna"' ~/.bashrc || echo 'alias ccna-repo="cd /ccna"' >> ~/.bashrc

echo -e "${GREEN}===========================================${NC}"
echo -e "${GREEN}🎉 Setup de Bastion_01 completado como root${NC}"
echo -e "${GREEN}===========================================${NC}"
echo -e "${YELLOW}💡 Para activar el entorno virtual usa:${NC}"
echo -e "  source /ccna/venv/bin/activate"
echo -e ""
echo -e "${YELLOW}💡 O simplemente:${NC}"
echo -e "  activate-ccna"
echo -e ""
echo -e "${GREEN}✅ Bastion_01 está lista para automatización de redes!${NC}"
