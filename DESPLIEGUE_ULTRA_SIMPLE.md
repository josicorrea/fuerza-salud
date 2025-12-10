# 🎯 DESPLIEGUE EN PYTHONANYWHERE - VERSIÓN ULTRA SIMPLE

## Estado: ⏳ Esperando que PythonAnywhere se recupere

PythonAnywhere tiene problemas técnicos temporales.
Tu proyecto está **100% listo**.

---

## 📌 CUANDO PYTHONANYWHERE VUELVA - 5 PASOS

### PASO 1️⃣ - CREAR CUENTA (1 minuto)
```
1. Ve a: https://www.pythonanywhere.com
2. Click "Sign up for a beginner account"
3. Completa registro
4. Confirma email
```

### PASO 2️⃣ - DESCARGAR TU PROYECTO (2 minutos)
En Dashboard → Consoles → Bash:

```bash
cd ~
git clone https://github.com/josicorrea/fuerza-salud.git
cd fuerza-salud
```

### PASO 3️⃣ - INSTALAR DEPENDENCIAS (3 minutos)
```bash
mkvirtualenv --python=/usr/bin/python3.10 fuerza-salud-env
pip install -r requirements.txt
```

### PASO 4️⃣ - PREPARAR BASE DE DATOS (1 minuto)
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### PASO 5️⃣ - CONFIGURAR EN PYTHONANYWHERE (2 minutos)

**En Dashboard → Web:**
1. Click "Add a new web app"
2. "Manual configuration" 
3. Python 3.10
4. Editar WSGI file (reemplaza todo con el código de abajo)

```python
import os
import sys

path = '/home/tu_usuario/fuerza-salud'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salud_fuerza.settings')

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

application = DjangoWhiteNoise(get_wsgi_application())
```

**⚠️ Reemplaza `tu_usuario` con tu username real**

5. Configurar Static files:
   - URL: `/static/`
   - Directory: `/home/tu_usuario/fuerza-salud/static`

6. Configurar Media files:
   - URL: `/media/`
   - Directory: `/home/tu_usuario/fuerza-salud/media`

7. Virtualenv: `/home/tu_usuario/.virtualenvs/fuerza-salud-env`

8. Click **RELOAD** (botón azul arriba)

---

## ✅ ¡LISTO!

Tu blog está en:
```
https://tu_usuario.pythonanywhere.com
```

Admin: `https://tu_usuario.pythonanywhere.com/admin/`

---

## 🆘 SI ALGO FALLA

**Error 500:**
- Dashboard → Web → Error log
- Lee el error
- Vuelve aquí y revisa

**Las imágenes no cargan:**
```bash
python manage.py collectstatic --noinput
```
Luego Reload en Web App

**Base de datos error:**
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```
Luego Reload

---

## 📞 PREGUNTAS?

Para guía completa: lee `PYTHONANYWHERE_GUIA_COMPLETA.md`

Ahí está TODO explicado paso a paso.

---

¡Listo! Tu proyecto está en vivo 🚀
