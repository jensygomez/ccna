#!/bin/bash
# setup_bastion_menu.sh - Menú interactivo para configuración de Bastion

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Función para mostrar el menú
show_menu() {
    clear
    echo -e "${BLUE}"
    echo "==========================================="
    echo "           MENÚ CONFIGURACIÓN BASTION"
    echo "==========================================="
    echo -e "${NC}"
    echo -e "${GREEN}1. Verificar estado actual"
    echo -e "2. Instalar/Actualizar dependencias del sistema"
    echo -e "3. Configurar entorno virtual Python"
    echo -e "4. Instalar/Actualizar librerías Python"
    echo -e "5. Configurar Git y repositorio"
    echo -e "6. Configurar aliases y permisos"
    echo -e "7. Ejecutar verificación completa"
    echo -e "8. Instalación COMPLETA (todo)"
    echo -e "${RED}9. Salir${NC}"
    echo ""
    echo -e "${YELLOW}Seleccione una opción [1-9]:${NC} "
}

# Función para pausar y volver al menú
pause() {
    echo ""
    read -n 1 -s -r -p "Presione cualquier tecla para continuar..."
}

# Verificar estado actual
check_status() {
    echo -e "${YELLOW}🔍 Verificando estado actual...${NC}"
    echo "==========================================="
    
    # Verificar dependencias del sistema
    echo -e "${BLUE}📦 Dependencias del sistema:${NC}"
    local sys_deps=("git" "python3" "python3-pip" "python3-venv" "net-tools" "curl")
    for dep in "${sys_deps[@]}"; do
        if dpkg -l | grep -qw "$dep"; then
            echo -e "  ✅ $dep"
        else
            echo -e "  ❌ $dep"
        fi
    done
    
    # Verificar entorno virtual
    echo -e "${BLUE}🐍 Entorno virtual:${NC}"
    if [ -d "/ccna/venv" ]; then
        echo -e "  ✅ /ccna/venv existe"
    else
        echo -e "  ❌ /ccna/venv no existe"
    fi
    
    # Verificar librerías Python
    echo -e "${BLUE}🐍 Librerías Python:${NC}"
    local py_libs=("netmiko" "paramiko" "scrapli" "requests" "yaml" "jinja2")
    for lib in "${py_libs[@]}"; do
        if source /ccna/venv/bin/activate 2>/dev/null && python3 -c "import $lib" 2>/dev/null; then
            echo -e "  ✅ $lib"
        else
            echo -e "  ❌ $lib"
        fi
    done
    
    # Verificar repositorio
    echo -e "${BLUE}📁 Repositorio:${NC}"
    if [ -d "/ccna/.git" ]; then
        echo -e "  ✅ Repositorio clonado"
    else
        echo -e "  ❌ Repositorio no clonado"
    fi
    
    pause
}

# Instalar dependencias del sistema
install_system_deps() {
    echo -e "${YELLOW}📦 Instalando dependencias del sistema...${NC}"
    echo "==========================================="
    
    apt update
    local deps=(
        git python3 python3-pip python3-venv python3-dev
        build-essential libssl-dev libffi-dev net-tools
        iproute2 curl wget openssh-client rustc cargo pkg-config
    )
    
    for dep in "${deps[@]}"; do
        if dpkg -l | grep -qw "$dep"; then
            echo -e "${GREEN}✅ $dep ya está instalado${NC}"
        else
            echo -e "${YELLOW}📦 Instalando $dep...${NC}"
            apt install -y "$dep"
        fi
    done
    
    echo -e "${GREEN}✅ Dependencias del sistema instaladas${NC}"
    pause
}

# Configurar entorno virtual
setup_virtualenv() {
    echo -e "${YELLOW}🐍 Configurando entorno virtual...${NC}"
    echo "==========================================="
    
    mkdir -p /ccna
    
    if [ ! -d "/ccna/venv" ]; then
        python3 -m venv /ccna/venv --without-pip
        echo -e "${GREEN}✅ Entorno virtual creado${NC}"
        
        # Instalar pip manualmente
        source /ccna/venv/bin/activate
        curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
        python3 /tmp/get-pip.py
        pip install --upgrade pip setuptools wheel
        echo -e "${GREEN}✅ Pip instalado en el entorno virtual${NC}"
    else
        echo -e "${GREEN}✅ Entorno virtual ya existe${NC}"
        source /ccna/venv/bin/activate
    fi
    
    pause
}

# Instalar librerías Python
install_python_libs() {
    echo -e "${YELLOW}🐍 Instalando librerías Python...${NC}"
    echo "==========================================="
    
    if [ ! -d "/ccna/venv" ]; then
        echo -e "${RED}❌ Primero debe crear el entorno virtual (Opción 3)${NC}"
        pause
        return
    fi
    
    source /ccna/venv/bin/activate
    
    # Instalar dependencias base primero
    echo -e "${YELLOW}📦 Instalando dependencias base...${NC}"
    pip install --upgrade cryptography cffi pyopenssl setuptools_rust
    
    # Instalar librerías principales
    echo -e "${YELLOW}📦 Instalando librerías de networking...${NC}"
    local libs=(
        netmiko paramiko scrapli textfsm jinja2 pyyaml requests rich nornir napalm
    )
    
    for lib in "${libs[@]}"; do
        if python3 -c "import $lib" 2>/dev/null; then
            echo -e "${GREEN}✅ $lib ya está instalado${NC}"
        else
            echo -e "${YELLOW}📦 Instalando $lib...${NC}"
            pip install --upgrade "$lib"
        fi
    done
    
    # Verificar instalaciones
    echo -e "${YELLOW}🔍 Verificando instalaciones...${NC}"
    check_library "from netmiko import ConnectHandler" "Netmiko"
    check_library "import paramiko; print('Paramiko:', paramiko.__version__)" "Paramiko"
    check_library "import requests; print('Requests:', requests.__version__)" "Requests"
    
    echo -e "${GREEN}✅ Librerías Python instaladas${NC}"
    pause
}

# Función para verificar librerías
check_library() {
    python3 -c "
import sys
try:
    $1
    print('✅ $2: OK')
except ImportError as e:
    print('❌ $2: FALLÓ -', str(e))
    sys.exit(1)
except Exception as e:
    print('⚠️  $2: Advertencia -', str(e))
"
}

# Configurar Git y repositorio
setup_git_repo() {
    echo -e "${YELLOW}⚙️ Configurando Git y repositorio...${NC}"
    echo "==========================================="
    
    # Configurar Git
    git config --global user.name "Jensy Gomez"
    git config --global user.email "jensygomez@gmail.com"
    echo -e "${GREEN}✅ Git configurado${NC}"
    
    # Clonar o actualizar repositorio
    if [ ! -d "/ccna/.git" ]; then
        echo -e "${YELLOW}📥 Clonando repositorio...${NC}"
        git clone https://github.com/jensygomez/ccna.git /ccna
        echo -e "${GREEN}✅ Repositorio clonado${NC}"
    else
        echo -e "${YELLOW}🔄 Actualizando repositorio...${NC}"
        cd /ccna && git pull origin main
        echo -e "${GREEN}✅ Repositorio actualizado${NC}"
    fi
    
    # Crear enlace simbólico
    ln -sf /ccna/Automation /automation 2>/dev/null || true
    echo -e "${GREEN}✅ Enlace simbólico creado${NC}"
    
    pause
}

# Configurar aliases y permisos
setup_aliases_permissions() {
    echo -e "${YELLOW}⚙️ Configurando aliases y permisos...${NC}"
    echo "==========================================="
    
    # Configurar aliases
    if ! grep -q "activate-ccna" ~/.bashrc; then
        cat << 'EOF' >> ~/.bashrc

# Aliases para CCNA
alias activate-ccna="source /ccna/venv/bin/activate"
alias automation="cd /automation 2>/dev/null || cd /ccna/Automation"
alias ccna-repo="cd /ccna"
alias netmiko-test="python3 -c \"from netmiko import ConnectHandler; print('Netmiko funciona correctamente')\""
EOF
        echo -e "${GREEN}✅ Aliases configurados${NC}"
    else
        echo -e "${GREEN}✅ Aliases ya estaban configurados${NC}"
    fi
    
    # Configurar permisos
    chown -R root:root /ccna /automation 2>/dev/null || true
    echo -e "${GREEN}✅ Permisos configurados${NC}"
    
    echo -e "${YELLOW}💡 Recarga .bashrc con: source ~/.bashrc${NC}"
    pause
}

# Verificación completa
full_check() {
    echo -e "${YELLOW}🔍 Ejecutando verificación completa...${NC}"
    echo "==========================================="
    
    check_status
    echo ""
    
    # Verificación detallada de Python
    if [ -d "/ccna/venv" ]; then
        source /ccna/venv/bin/activate
        echo -e "${BLUE}🐍 Verificación detallada Python:${NC}"
        python3 -c "
try:
    from netmiko import ConnectHandler
    print('✅ Netmiko: FUNCIONA')
except Exception as e:
    print('❌ Netmiko: ERROR -', str(e))

try:
    import paramiko
    print('✅ Paramiko:', paramiko.__version__)
except Exception as e:
    print('❌ Paramiko: ERROR -', str(e))

try:
    import requests
    print('✅ Requests:', requests.__version__)
except Exception as e:
    print('❌ Requests: ERROR -', str(e))
"
    fi
    
    pause
}

# Instalación completa
full_installation() {
    echo -e "${YELLOW}🚀 Iniciando instalación COMPLETA...${NC}"
    echo "==========================================="
    
    install_system_deps
    echo ""
    setup_virtualenv
    echo ""
    install_python_libs
    echo ""
    setup_git_repo
    echo ""
    setup_aliases_permissions
    echo ""
    full_check
    
    echo -e "${GREEN}"
    echo "==========================================="
    echo "🎉 INSTALACIÓN COMPLETA FINALIZADA"
    echo "==========================================="
    echo -e "${NC}"
    echo "📋 Comandos útiles:"
    echo "   activate-ccna    # Activar entorno virtual"
    echo "   netmiko-test     # Probar Netmiko"
    echo "   automation       # Ir a directorio automation"
    echo ""
    pause
}

# Main loop
while true; do
    show_menu
    read choice
    
    case $choice in
        1) check_status ;;
        2) install_system_deps ;;
        3) setup_virtualenv ;;
        4) install_python_libs ;;
        5) setup_git_repo ;;
        6) setup_aliases_permissions ;;
        7) full_check ;;
        8) full_installation ;;
        9) 
            echo -e "${GREEN}👋 ¡Hasta luego!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Opción inválida${NC}"
            pause
            ;;
    esac
done