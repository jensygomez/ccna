#!/bin/bash
echo "🔍 Verificando instalaciones..."

# Verificar herramientas
echo "📦 Herramientas del sistema:"
tools=("git" "python3" "pip3" "curl" "wget")
for tool in "${tools[@]}"; do
    if command -v $tool &> /dev/null; then
        echo "✅ $tool: $(which $tool)"
    else
        echo "❌ $tool: NO instalado"
    fi
done

# Verificar librerías Python
echo ""
echo "🐍 Librerías Python:"
libs=("netmiko" "paramiko" "napalm" "nornir" "scrapli" "textfsm")
for lib in "${libs[@]}"; do
    python3 -c "import $lib" 2>/dev/null && echo "✅ $lib" || echo "❌ $lib"
done

# Verificar repositorio
echo ""
echo "📁 Repositorio:"
if [ -d "/opt/ccna" ]; then
    echo "✅ Repositorio clonado"
    ls -la /opt/ccna/Automation/ 2>/dev/null || echo "⚠️  Carpeta Automation no encontrada"
else
    echo "❌ Repositorio NO clonado"
fi

echo "✅ Verificación completada"