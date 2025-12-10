#!/bin/bash
# Script de despliegue automatizado para PythonAnywhere
# Uso: bash deploy_pythonanywhere.sh

set -e  # Salir si hay error

echo "🚀 Iniciando despliegue en PythonAnywhere..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variables
PROJECT_DIR="/home/$(whoami)/fuerza-salud"
VENV_NAME="salud_fuerza"

echo -e "${YELLOW}📁 Directorio del proyecto: ${PROJECT_DIR}${NC}"

# 1. Actualizar código
echo -e "\n${YELLOW}1️⃣ Actualizando código desde GitHub...${NC}"
cd "$PROJECT_DIR"
git pull origin main || echo "⚠️ No hay cambios o error en git"

# 2. Instalar dependencias
echo -e "\n${YELLOW}2️⃣ Instalando dependencias...${NC}"
workon "$VENV_NAME"
pip install -r requirements.txt --upgrade

# 3. Aplicar migraciones
echo -e "\n${YELLOW}3️⃣ Aplicando migraciones...${NC}"
python manage.py migrate

# 4. Recolectar static files
echo -e "\n${YELLOW}4️⃣ Recolectando archivos estáticos...${NC}"
python manage.py collectstatic --noinput

# 5. Verificar que todo esté bien
echo -e "\n${YELLOW}5️⃣ Verificando integridad del proyecto...${NC}"
python manage.py check

echo -e "\n${GREEN}✅ ¡Despliegue completado!${NC}"
echo -e "${GREEN}Ahora ve a Dashboard → Web → Reload para recargar la app${NC}"
