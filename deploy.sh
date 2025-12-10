#!/bin/bash
# Script para recolectar archivos estáticos en producción

python manage.py collectstatic --noinput
python manage.py migrate
echo "✅ Archivos estáticos recolectados y migraciones aplicadas"
