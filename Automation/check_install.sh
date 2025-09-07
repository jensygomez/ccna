#!/bin/bash
# check_install.sh - Verificación completa de instalación para Bastion_01

echo "🔍 Verificando instalaciones..."
echo "==========================================="

# Rutas principales
VENV_PATH="/ccna/venv"
PYTHON_BIN="$VENV_PATH/bin/python"
PIP_BIN="$VENV_PATH/bin/pip"

# Verificar si el entorno virtual existe
if [ ! -d "$VENV_PATH" ]; then
    echo "❌ No se encontró el entorno virtual en $VENV_PATH"
    echo "⚠️ Ejecuta primero: /ccna/setup_bastion.sh"
    exit 1
fi

echo "✅ Usando entorno virtual: $VENV_PATH"
echo "==========================================="

# Verificar herramientas del sistema
echo ""
echo "📦 Herramientas del sistema:"
tools=("git" "python3" "pip3" "curl" "wget" "net-tools" "ip" "ssh")
for tool in "${tools[@]}"; do
    if command -v $tool &> /dev/null; then
        echo "✅ $tool: $(which $tool)"
    else
        echo "❌ $tool: NO instalado"
    fi
done

# Verificar versión de Python y pip del venv
echo ""
echo "🐍 Entorno virtual:"
echo "Python: $($PYTHON_BIN --version)"
echo "Pip: $($PIP_BIN --version)"

# Verificar librerías Python instaladas en el venv
echo ""
echo "📚 Librerías Python en entorno virtual:"
libs=("netmiko" "paramiko" "napalm" "nornir" "scrapli" "textfsm" "jinja2" "yaml" "requests" "rich")
for lib in "${libs[@]}"; do
    $PYTHON_BIN -c "import $lib; print('✅', '$lib', '->', getattr($lib, '__version__', 'OK'))" 2>/dev/null \
        || echo "❌ $lib NO instalada"
done

# Verificar repositorio CCNA
echo ""
echo "📁 Repositorio:"
if [ -d "/ccna/.git" ]; then
    echo "✅ Repositorio CCNA clonado correctamente"
    if [ -d "/ccna/Automation" ]; then
        echo "✅ Carpeta Automation encontrada"
        ls -la /ccna/Automation/
    else
        echo "⚠️ Carpeta Automation NO encontrada"
    fi
else
    echo "❌ Repositorio CCNA NO clonado"
fi

echo ""
echo "🎉 Verificación completada con éxito"
echo "==========================================="
