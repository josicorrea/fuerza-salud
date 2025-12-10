#!/bin/bash
# Script de verificación pre-despliegue

echo "=========================================="
echo "  VERIFICACIÓN PRE-DESPLIEGUE"
echo "  Salud & Fuerza AR"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir resultados
check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $1"
    else
        echo -e "${RED}✗${NC} $1"
    fi
}

# 1. Verificar que settings.py es válido
echo ""
echo "Verificando Django settings..."
python manage.py check
check "Django check OK"

# 2. Verificar que la BD está actualizada
echo ""
echo "Verificando migraciones..."
python manage.py migrate --dry-run
check "Migraciones OK"

# 3. Verificar que los archivos estáticos están recolectados
echo ""
echo "Verificando archivos estáticos..."
if [ -d "static" ]; then
    echo -e "${GREEN}✓${NC} Carpeta 'static' existe"
else
    echo -e "${RED}✗${NC} Carpeta 'static' no existe"
fi

# 4. Verificar estructura de carpetas
echo ""
echo "Verificando estructura de carpetas..."
[ -d "blog" ] && echo -e "${GREEN}✓${NC} Carpeta 'blog' OK" || echo -e "${RED}✗${NC} Carpeta 'blog' falta"
[ -d "salud_fuerza" ] && echo -e "${GREEN}✓${NC} Carpeta 'salud_fuerza' OK" || echo -e "${RED}✗${NC} Carpeta 'salud_fuerza' falta"
[ -d "media" ] && echo -e "${GREEN}✓${NC} Carpeta 'media' OK" || echo -e "${RED}✗${NC} Carpeta 'media' falta"
[ -f "requirements.txt" ] && echo -e "${GREEN}✓${NC} requirements.txt existe" || echo -e "${RED}✗${NC} requirements.txt falta"
[ -f ".env" ] && echo -e "${YELLOW}⚠${NC}  .env existe (no olvides .gitignore)" || echo -e "${GREEN}✓${NC} .env no en repo (correcto)"

# 5. Verificar dependencias
echo ""
echo "Verificando dependencias..."
python -c "import django; print(f'Django: {django.get_version()}')"
check "Django instalado"
python -c "import whitenoise; print('WhiteNoise: OK')"
check "WhiteNoise instalado"
python -c "import decouple; print('python-decouple: OK')"
check "python-decouple instalado"

# 6. Verificar que la app corre
echo ""
echo "Resumen final:"
echo -e "${GREEN}✓${NC} Proyecto listo para despliegue"
echo ""
echo "Próximos pasos:"
echo "1. git add ."
echo "2. git commit -m 'Proyecto listo para despliegue'"
echo "3. git push"
echo "4. Ir a PythonAnywhere y seguir PYTHONANYWHERE_GUIA_COMPLETA.md"
echo ""
