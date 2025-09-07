#!/bin/bash
echo "🔍 Verificando instalaciones..."
echo "==========================================="

# Ruta del entorno virtual
VENV_PATH="/ccna/venv"
PYTHON_BIN="$VENV_PATH/bin/python"
PIP_BIN="$VENV_PATH/bin/pip"

# Verificar si el entorno virtual existe
if [ ! -d "$VENV_PATH" ]; then
    echo "❌ No se encontró el entorno virtual en $VENV_PATH"
    echo "⚠️  Ejecuta primero: sudo /ccna/setup_bastion.sh"
    exit 1
fi

echo "✅ Usando entorno virtual: $VENV_PATH"
echo "==========================================="

# Verificar herramientas del sistema
echo ""
echo "📦 Herramientas del sistema:"
tools=("git" "python3" "pip3" "curl" "wget")
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
libs=("netmiko" "paramiko" "napalm" "nornir" "scrapli" "textfsm" "jinja2" "pyyaml" "requests" "rich")
for lib in "${libs[@]}"; do
    $PYTHON_BIN -c "import $lib" 2>/dev/null \
        && echo "✅ $lib" \
        || echo "❌ $lib"
done

# Verificar repositorio CCNA
echo ""
echo "📁 Repositorio:"
if [ -d "/ccna" ]; then
    echo "✅ Repositorio clonado en /ccna"
    if [ -d "/ccna/Automation" ]; then
        echo "✅ Carpeta Automation encontrada"
        ls -la /ccna/Automation/
    else
        echo "⚠️  Carpeta Automation NO encontrada"
    fi
else
    echo "❌ Repositorio CCNA NO clonado"
fi

echo ""
echo "🎉 Verificación completada con éxito"
echo "==========================================="
