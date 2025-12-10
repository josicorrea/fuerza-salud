# 🚀 GUÍA DE DESPLIEGUE - Salud & Fuerza AR

## Opción 1: Despliegue en PythonAnywhere (Recomendado - Fácil)

### Paso 1: Crear cuenta en PythonAnywhere
1. Ingresa a https://www.pythonanywhere.com
2. Click en "Sign up for a beginner account" (gratis)
3. Completa el registro con email y contraseña
4. Confirma tu email

### Paso 2: Subir archivos del proyecto
**Opción A: Usando Git (Recomendado)**
```bash
# En la consola de PythonAnywhere Bash:
git clone https://github.com/josicorrea/fuerza-salud.git
cd fuerza-salud
```

**Opción B: Upload manual**
1. En Dashboard → Files
2. Sube todos los archivos del proyecto

### Paso 3: Crear Virtual Environment
En la consola Bash de PythonAnywhere:
```bash
# Entrar al directorio del proyecto
cd ~/fuerza-salud

# Crear virtual environment con Python 3.10+
mkvirtualenv --python=/usr/bin/python3.10 salud-fuerza

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 4: Configurar Variables de Entorno
En la consola Bash:
```bash
# Crear archivo .env
nano .env
```
Añade las siguientes líneas:
```
DEBUG=False
SECRET_KEY=genera-una-clave-aleatoria-aqui-minimo-50-caracteres
ALLOWED_HOSTS=tu_usuario.pythonanywhere.com
DATABASE_URL=sqlite:////home/tu_usuario/fuerza-salud/db.sqlite3
```

Presiona Ctrl+X, luego Y, luego Enter para guardar.

**Generar SECRET_KEY segura:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Paso 5: Crear/Migrar Base de Datos
```bash
cd ~/fuerza-salud
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Crea usuario admin
python manage.py collectstatic --noinput  # Recolecta archivos estáticos
```

### Paso 6: Configurar Web App
1. En Dashboard → Web
2. Click en "Add a new web app"
3. Selecciona "Manual configuration"
4. Elige Python 3.10
5. En WSGI configuration file, edita el archivo:

Reemplaza el contenido con esto:
```python
import os
import sys
from pathlib import Path

# Añade el directorio del proyecto al path
path = '/home/tu_usuario/fuerza-salud'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salud_fuerza.settings')

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

application = DjangoWhiteNoise(get_wsgi_application())
```

### Paso 7: Configurar Static y Media Files
En el mismo Web App, desplázate hasta "Static files" y añade:

**Static files:**
- URL: `/static/`
- Directory: `/home/tu_usuario/fuerza-salud/static`

**Media files:**
- URL: `/media/`
- Directory: `/home/tu_usuario/fuerza-salud/media`

### Paso 8: Configurar Virtual Environment
En Web App → Virtualenv:
- Path: `/home/tu_usuario/.virtualenvs/salud-fuerza`

### Paso 9: Recargar la App
Click en el botón **"Reload"** en la parte superior azul

### ✅ ¡Listo!
Tu sitio está disponible en: `https://tu_usuario.pythonanywhere.com`

Panel Admin: `https://tu_usuario.pythonanywhere.com/admin/`

---

## Opción 2: Despliegue en Heroku

### Paso 1: Preparar archivos
Crea un archivo `Procfile` en la raíz:
```
web: gunicorn salud_fuerza.wsgi
```

Crea un archivo `runtime.txt`:
```
python-3.10.15
```

### Paso 2: Instalar Heroku CLI
Descarga desde https://devcenter.heroku.com/articles/heroku-cli

### Paso 3: Desplegar
```bash
heroku login
heroku create tu-app-nombre
git push heroku main

# Ejecutar migraciones
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
heroku run python manage.py collectstatic --noinput
```

---

## Opción 3: Despliegue en Railway.app

### Paso 1: Crear cuenta
https://railway.app - Conecta con GitHub

### Paso 2: Nuevo proyecto
1. Click "New Project"
2. "Deploy from GitHub repo"
3. Selecciona el repositorio

### Paso 3: Configurar variables
En Settings → Variables:
```
DEBUG=False
SECRET_KEY=tu-clave-generada
ALLOWED_HOSTS=tu-dominio.railway.app
```

### Paso 4: ¡Listo!
Railway despliega automáticamente

---

## Opción 4: Despliegue en Replit

### Paso 1: Crear proyecto
1. https://replit.com
2. Click "Import GitHub Repository"
3. Pega la URL del repo

### Paso 2: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 3: Configurar
Crea `.env`:
```
DEBUG=False
SECRET_KEY=tu-clave-generada
ALLOWED_HOSTS=.replit.dev
```

### Paso 4: Correr
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:3000
```

---

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'decouple'"
```bash
pip install python-decouple
```

### Error: "No such table" al acceder
```bash
python manage.py migrate
python manage.py createsuperuser
```

### Las imágenes no se cargan
- Asegúrate que `STATIC_ROOT` está configurado
- Ejecuta `python manage.py collectstatic --noinput`
- Verifica que la carpeta `media/` tiene permisos de escritura

### Error de permisos en PythonAnywhere
```bash
chmod -R 755 ~/fuerza-salud/media/
chmod -R 755 ~/fuerza-salud/static/
```

---

## Monitoreo y Logs

**En PythonAnywhere:**
- Error log: Dashboard → Web → Error log
- Server log: Dashboard → Web → Server log

**En Heroku:**
```bash
heroku logs --tail
```

**En Railway:**
- Ver en el dashboard de Railway bajo "Logs"

---

## Próximos Pasos

1. **Dominio personalizado**: Compra un dominio y configúralo
2. **Email**: Configura servicio de email para notificaciones
3. **Backups**: Implementa backups automáticos de BD
4. **Monitoreo**: Usa Sentry para monitorear errores
5. **CDN**: Usa Cloudflare para mejorar velocidad

---

¿Preguntas? Contacta al equipo de desarrollo.

Hecho con ❤️ para Salud & Fuerza AR
