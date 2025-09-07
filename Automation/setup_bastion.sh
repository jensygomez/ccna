#!/bin/bash
# setup_bastion.sh - Configuración optimizada para Bastion_01 (Root Mode)

set -e  # Detener en caso de error

echo "🔄 Iniciando setup de Bastion_01..."
echo "==========================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Ruta principal del entorno y repositorio
VENV_PATH="/ccna/venv"
REPO_PATH="/ccna"

# Función para verificar e instalar paquetes del sistema
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

# Instalar herramientas del sistema necesarias
echo -e "${YELLOW}📦 Instalando herramientas del sistema...${NC}"
for pkg in git python3 python3-pip python3-venv net-tools iproute2 curl wget openssh-client; do
    install_package "$pkg"
done

# Crear y configurar entorno virtual
echo -e "${YELLOW}⚙️ Configurando entorno virtual Python...${NC}"
if [ ! -d "$VENV_PATH" ]; then
    mkdir -p "$VENV_PATH"
    python3 -m venv "$VENV_PATH"
    echo -e "${GREEN}✅ Entorno virtual creado en $VENV_PATH${NC}"
else
    echo -e "${GREEN}✅ Entorno virtual ya existe${NC}"
fi

# Activar entorno virtual
source "$VENV_PATH/bin/activate"

# Actualizar pip dentro del venv
echo -e "${YELLOW}📦 Actualizando pip dentro del entorno virtual...${NC}"
"$VENV_PATH/bin/pip" install --upgrade pip

# Instalar librerías de automatización
echo -e "${YELLOW}📦 Instalando librerías Python de automatización...${NC}"
"$VENV_PATH/bin/pip" install --upgrade netmiko paramiko napalm nornir scrapli textfsm jinja2 pyyaml requests rich

# Verificar librerías instaladas
source /ccna/venv/bin/activate
python3 - <<EOF
import importlib
libs = ["netmiko", "paramiko", "napalm", "nornir", "scrapli", "textfsm", "jinja2", "pyyaml", "requests", "rich"]
for lib in libs:
    try:
        module = importlib.import_module(lib)
        try:
            version = module.__version__
        except AttributeError:
            import importlib.metadata
            version = importlib.metadata.version(lib)
        print(f"✅ {lib}: {version}")
    except ImportError:
        print(f"❌ {lib} NO instalado")
EOF


# Configurar Git
echo -e "${YELLOW}⚙️ Configurando Git...${NC}"
if command -v git &> /dev/null; then
    git config --global user.name "Jensy Gomez"
    git config --global user.email "jensygomez@gmail.com"
    echo -e "${GREEN}✅ Git configurado correctamente${NC}"
else
    echo -e "${RED}❌ Git no está instalado, revisa instalación${NC}"
    exit 1
fi

# Clonar repositorio si no existe o actualizarlo
if [ ! -d "$REPO_PATH/.git" ]; then
    echo -e "${YELLOW}📥 Clonando repositorio CCNA...${NC}"
    git clone https://github.com/jensygomez/ccna.git "$REPO_PATH"
    echo -e "${GREEN}✅ Repositorio clonado en $REPO_PATH${NC}"
else
    echo -e "${GREEN}✅ Repositorio ya existe, actualizando...${NC}"
    cd "$REPO_PATH" && git pull origin main
fi

# Crear enlace simbólico si no existe
if [ ! -L "/automation" ]; then
    echo -e "${YELLOW}🔗 Creando enlace simbólico...${NC}"
    ln -sf "$REPO_PATH/Automation" /automation
    echo -e "${GREEN}✅ Enlace simbólico creado: /automation${NC}"
fi

# Configurar alias permanentes
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
