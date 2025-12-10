# 🚀 GUÍA DEFINITIVA DE DESPLIEGUE EN PYTHONANYWHERE

## Salud & Fuerza AR Blog

Este es el método más fácil y recomendado para desplegar tu proyecto Django.

---

## 📋 REQUISITOS PREVIOS

- ✅ Cuenta en GitHub con tu proyecto
- ✅ Cuenta gratuita en PythonAnywhere (https://www.pythonanywhere.com)
- ✅ Tu proyecto localmente funcionando

---

## 🔐 PASO 1: CREAR CUENTA EN PYTHONANYWHERE

1. Ve a https://www.pythonanywhere.com
2. Click en **"Sign up for a beginner account"**
3. Elige username (será parte de tu URL: `username.pythonanywhere.com`)
4. Completa el registro
5. Confirma tu email
6. ¡Login!

> **Nota**: La cuenta gratis incluye 1 app web, perfecto para nuestro proyecto.

---

## 📂 PASO 2: DESCARGAR TU PROYECTO EN PYTHONANYWHERE

Abre la **consola Bash** (en el dashboard, izquierda → Consoles → Bash):

### Opción A: Clonar desde GitHub (RECOMENDADO)
```bash
cd ~
git clone https://github.com/josicorrea/fuerza-salud.git
cd fuerza-salud
```

### Opción B: Subir archivos manualmente
Si no usas GitHub:
1. Dashboard → Files
2. Sube todos los archivos en una carpeta llamada `fuerza-salud`

---

## 🐍 PASO 3: CREAR VIRTUAL ENVIRONMENT

En la consola Bash:

```bash
cd ~/fuerza-salud

# Crear virtual environment para Python 3.10
mkvirtualenv --python=/usr/bin/python3.10 fuerza-salud-env

# Verificar que estés dentro (verás el nombre en paréntesis)
# (fuerza-salud-env) user@pythonanywhere:/home/user/fuerza-salud$
```

---

## 📦 PASO 4: INSTALAR DEPENDENCIAS

Asegúrate de estar en el virtual environment, luego:

```bash
pip install --upgrade pip

pip install -r requirements.txt
```

**Espera a que termine** (puede tomar 2-3 minutos)

---

## ⚙️ PASO 5: CONFIGURAR VARIABLES DE ENTORNO

Crea archivo `.env`:

```bash
nano .env
```

Copia esto (reemplaza `tu_usuario` con tu username de PythonAnywhere):

```
DEBUG=False
SECRET_KEY=django-insecure-9@7w_(0t92kzo89!+rrrl1dc)iri%v0mmfs-v9!-bu^8u!x0h2
ALLOWED_HOSTS=tu_usuario.pythonanywhere.com,127.0.0.1,localhost
```

Para guardar:
- Presiona **Ctrl + X**
- Presiona **Y** (Yes)
- Presiona **Enter**

### Generar SECRET_KEY nueva (opcional pero recomendado):

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copia el resultado y reemplázalo en `.env`

---

## 🗄️ PASO 6: MIGRAR BASE DE DATOS

```bash
cd ~/fuerza-salud

# Hacer migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Recolectar archivos estáticos
python manage.py collectstatic --noinput
```

---

## 👤 PASO 7: CREAR SUPERUSER (ADMIN)

```bash
python manage.py createsuperuser
```

Sigue las instrucciones:
- Username: `admin` (o lo que prefieras)
- Email: tu email
- Password: contraseña segura
- Confirm password: repite la contraseña

**Guarda estos datos**, los necesitarás para acceder al panel admin.

---

## 🌐 PASO 8: CONFIGURAR WEB APP EN PYTHONANYWHERE

1. En el Dashboard, vete a **Web** (izquierda)
2. Click en **"Add a new web app"**
3. Selecciona **"Manual configuration"**
4. Elige **Python 3.10**
5. Click **"Next"**

### Verás una pantalla de configuración. IMPORTANTE:

**En la sección "WSGI configuration file"**, encontrarás un link azul. Haz click en él para editar el archivo.

**Reemplaza TODO el contenido** con esto:

```python
import os
import sys
from pathlib import Path

# Agregar el directorio del proyecto al path
path = '/home/tu_usuario/fuerza-salud'
if path not in sys.path:
    sys.path.append(path)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salud_fuerza.settings')

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

application = DjangoWhiteNoise(get_wsgi_application())
```

⚠️ **IMPORTANTE**: Reemplaza `tu_usuario` con tu username de PythonAnywhere

Guarda (Ctrl+S)

---

## 📁 PASO 9: CONFIGURAR ARCHIVOS ESTÁTICOS Y MEDIA

Vuelve a la página de Web App. Desplázate hacia abajo hasta "Static files:"

Haz click en **"Edit"** y configura así:

### Static files:
```
URL: /static/
Directory: /home/tu_usuario/fuerza-salud/static
```

### Media files:
```
URL: /media/
Directory: /home/tu_usuario/fuerza-salud/media
```

Click en **"Save"**

---

## 🔧 PASO 10: CONFIGURAR VIRTUALENV

En la misma página de Web App, encuentra **"Virtualenv"**:

```
/home/tu_usuario/.virtualenvs/fuerza-salud-env
```

---

## ✅ PASO 11: RECARGAR LA APP

En la parte superior azul de la página Web App, encontrarás un botón **"Reload"** (o refresh icon).

Click en él. Espera 5-10 segundos.

---

## 🎉 ¡LISTO! Tu sitio está en vivo

Tu blog está disponible en:

```
https://tu_usuario.pythonanywhere.com
```

### Accesos importantes:
- **Home**: `https://tu_usuario.pythonanywhere.com/`
- **Panel Admin**: `https://tu_usuario.pythonanywhere.com/admin/`
  - Username: el que creaste
  - Password: la que estableciste
- **Login**: `https://tu_usuario.pythonanywhere.com/accounts/login/`
- **Registro**: `https://tu_usuario.pythonanywhere.com/signup/`

---

## 🧪 VERIFICAR QUE TODO FUNCIONA

1. Abre tu navegador e ingresa a `https://tu_usuario.pythonanywhere.com`
2. Deberías ver la página de inicio del blog
3. Intenta hacer login con las credenciales del superuser
4. Ve a `/admin/` para acceder al panel de administración
5. Sube un post de prueba con imagen

---

## 🐛 TROUBLESHOOTING

### "500 Server Error"
1. Ve a Dashboard → Web
2. Click en "Error log"
3. Lee el error y busca qué está mal
4. Usa el Bash para revisar:
```bash
cd ~/fuerza-salud
python manage.py shell
# Aquí puedes probar cosas
```

### "No such table" o errores de base de datos
```bash
cd ~/fuerza-salud
python manage.py migrate
python manage.py collectstatic --noinput
```

Luego reload la app.

### Las imágenes no cargan
1. Verifica que la carpeta `media/` existe:
```bash
ls -la ~/fuerza-salud/media/
```

2. Asegúrate que has recolectado statics:
```bash
python manage.py collectstatic --noinput
```

3. Reload la app

### Error de permisos
```bash
chmod -R 755 ~/fuerza-salud/media/
chmod -R 755 ~/fuerza-salud/static/
```

### "Secret key" o variable de entorno no cargada
1. Abre `.env` y verifica que está en el directorio correcto:
```bash
cat ~/.env  # Si está en home
cat ~/fuerza-salud/.env  # Si está en el proyecto
```

2. Verifica que `settings.py` carga bien:
```bash
cd ~/fuerza-salud
python manage.py check
```

---

## 📝 LOGS Y MONITOREO

### Ver logs de error
Dashboard → Web → Error log

### Ver logs del servidor
Dashboard → Web → Server log

### Actualizar código desde GitHub
Cuando hagas cambios en GitHub:

```bash
cd ~/fuerza-salud
git pull origin main
python manage.py migrate
python manage.py collectstatic --noinput
```

Luego reload la app.

---

## 🔐 SEGURIDAD - Checklist Final

Antes de dejar en producción:

- [ ] Cambiar DEBUG=False en `.env`
- [ ] Generar nuevo SECRET_KEY
- [ ] Crear superuser con contraseña fuerte
- [ ] Verificar ALLOWED_HOSTS correcto
- [ ] Probar login/logout funciona
- [ ] Verificar imágenes cargan correctamente
- [ ] Probar en móvil (responsive)
- [ ] Revisar logs por errores

---

## 💡 TIPS Y TRUCOS

### Acceder a la base de datos
```bash
cd ~/fuerza-salud
python manage.py dbshell
```

### Ver usuarios creados
```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.all()
```

### Resetear base de datos (⚠️ CUIDADO - BORRA TODO)
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Ver logs en tiempo real
```bash
cd ~/fuerza-salud
tail -f /var/log/pythonanywhere/tu_usuario.pythonanywhere.com.error.log
```

---

## 🚀 PRÓXIMOS PASOS

1. **Dominio personalizado**: Compra un dominio y apunta a PythonAnywhere
2. **Email**: Configura servicio de email para notificaciones
3. **Backups**: Descarga regularmente tu base de datos
4. **SSL/HTTPS**: PythonAnywhere lo da gratis ✅
5. **Actualizaciones**: Mantén Django y packages actualizados

---

## 📞 AYUDA

Si tienes errores:

1. Revisa el Error Log (Dashboard → Web → Error log)
2. Busca el error en Google
3. Lee la documentación Django: https://docs.djangoproject.com/
4. Contacta a soporte de PythonAnywhere

---

## ✨ ¡FELICIDADES!

Tu blog **Salud & Fuerza AR** está publicado en internet 🎉

Ahora puedes:
- Compartir el link con amigos
- Publicar posts sobre fitness y salud
- Interactuar con usuarios que dejan comentarios

**Hecho con ❤️ y Django ⚡**

---

**Última actualización**: Diciembre 2025
