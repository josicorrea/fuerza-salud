# 🚀 GUÍA PASO A PASO - Despliegue en PythonAnywhere

## ⏱️ Tiempo estimado: 20 minutos

---

## PASO 1: Crear Cuenta en PythonAnywhere ⭐

### 1.1 Registro
1. Ve a https://www.pythonanywhere.com
2. Click en **"Sign up for a beginner account"** (es gratis)
3. Completa el registro:
   - Username: `tu_nombre_usuario` (esto será tu dominio: `tu_nombre_usuario.pythonanywhere.com`)
   - Email: tu email
   - Password: contraseña segura
4. Acepta términos y click "Sign up"
5. **Confirma tu email** - revisa tu bandeja

### 1.2 Ingresa a tu Dashboard
- URL: `https://www.pythonanywhere.com/user/tu_nombre_usuario/`

---

## PASO 2: Subir Archivos del Proyecto 📁

### Opción A: DESDE GIT (Recomendado) ⭐⭐⭐

#### 2A.1 Primero: Push a GitHub
En tu máquina local:
```bash
git add .
git commit -m "Preparar para PythonAnywhere"
git push origin main
```

#### 2A.2 Clonar en PythonAnywhere
1. En Dashboard → **"Bash console"** (ícono de terminal)
2. Ejecuta:
```bash
cd ~
git clone https://github.com/josicorrea/fuerza-salud.git
cd fuerza-salud
pwd  # Anota la ruta completa
```

Resultado esperado:
```
/home/tu_usuario/fuerza-salud
```

---

### Opción B: Upload Manual

1. Dashboard → **"Files"**
2. Click **"Upload a file"**
3. Sube los archivos del proyecto
4. (No recomendado - más lento)

---

## PASO 3: Crear Virtual Environment 🐍

En la consola Bash:

```bash
# Crear virtualenv con Python 3.10
mkvirtualenv --python=/usr/bin/python3.10 salud_fuerza

# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación
pip list | grep Django
```

**Salida esperada:**
```
Django                    5.2.8
gunicorn                  23.0.0
whitenoise                6.7.0
python-decouple           3.8
```

---

## PASO 4: Configurar Variables de Entorno 🔐

### 4.1 Crear archivo .env
En la consola Bash:
```bash
cd ~/fuerza-salud
nano .env
```

### 4.2 Copiar contenido
Pega esto en el editor:
```
DEBUG=False
SECRET_KEY=django-insecure-tu-clave-super-secreta-aqui-minimo-50-caracteres-random
ALLOWED_HOSTS=tu_usuario.pythonanywhere.com
DATABASE_URL=sqlite:////home/tu_usuario/fuerza-salud/db.sqlite3
```

**⚠️ IMPORTANTE: Reemplaza `tu_usuario` con tu username de PythonAnywhere**

### 4.3 Guardar archivo
Presiona:
- `Ctrl + X`
- `Y` (Yes)
- `Enter`

### 4.4 Generar SECRET_KEY única y segura
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copia el resultado y reemplaza en .env

---

## PASO 5: Migrar Base de Datos 🗄️

En la consola Bash:

```bash
cd ~/fuerza-salud

# Hacer migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear usuario administrador
python manage.py createsuperuser
```

**Sigue las indicaciones:**
```
Username: tu_usuario_admin
Email: tu_email@example.com
Password: ******* (tu contraseña segura)
Password (again): *******
```

### Verificar
```bash
python manage.py check
```

Deberías ver:
```
System check identified no issues (0 silenced).
```

---

## PASO 6: Recolectar Archivos Estáticos 📦

```bash
cd ~/fuerza-salud
python manage.py collectstatic --noinput
```

Resultado:
```
123 static files copied, 456 unmodified, 789 post-processed.
```

---

## PASO 7: Crear Web App en PythonAnywhere 🌐

### 7.1 Ir a Web App
Dashboard → **"Web"** → **"Add a new web app"**

### 7.2 Configurar
1. **Next** → Selecciona **"Manual configuration"**
2. **Next** → Elige **Python 3.10**
3. Click **"Next"**

### 7.3 Ver Confirmación
Te mostrará una pantalla diciendo que creó la app.

---

## PASO 8: Configurar WSGI 🔧

### 8.1 Editar archivo WSGI
En Dashboard → **"Web"** → Sección **"Code"** → Click en **WSGI configuration file**

Será algo como: `/var/www/tu_usuario_pythonanywhere_com_wsgi.py`

### 8.2 Reemplazar contenido
Borra TODO y copia esto:

```python
import os
import sys
from pathlib import Path

# Ruta al proyecto
path = '/home/tu_usuario/fuerza-salud'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salud_fuerza.settings')

# Asegúrate que el virtual environment está activado
import site
site.addsitedir('/home/tu_usuario/.virtualenvs/salud_fuerza/lib/python3.10/site-packages')

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

application = DjangoWhiteNoise(get_wsgi_application())
```

⚠️ **IMPORTANTE: Reemplaza `tu_usuario` con tu username**

Presiona Ctrl+X → Y → Enter para guardar.

---

## PASO 9: Configurar Static Files 🖼️

En Dashboard → **"Web"**

Desplázate hasta la sección **"Static files:"**

### 9.1 Configurar Static
Click en **"Add a new static files mapping"**
```
URL: /static/
Directory: /home/tu_usuario/fuerza-salud/static
```

### 9.2 Configurar Media
Click en **"Add a new static files mapping"**
```
URL: /media/
Directory: /home/tu_usuario/fuerza-salud/media
```

**Resultado:**
```
/static/         /home/tu_usuario/fuerza-salud/static
/media/          /home/tu_usuario/fuerza-salud/media
```

---

## PASO 10: Configurar Virtual Environment 🐍

En Dashboard → **"Web"** → Sección **"Virtualenv:"**

Haz click o escribe:
```
/home/tu_usuario/.virtualenvs/salud_fuerza
```

---

## PASO 11: Recargar la App ♻️

En Dashboard → **"Web"** → Botón azul **"Reload"** en la parte superior

⏳ Espera 10 segundos...

---

## ✅ LISTO! 🎉

Tu sitio está disponible en:

### 🌐 Sitio Principal
```
https://tu_usuario.pythonanywhere.com
```

### 👨‍💼 Panel Admin
```
https://tu_usuario.pythonanywhere.com/admin
```

Inicia sesión con:
- Username: `tu_usuario_admin`
- Password: `tu_contraseña`

---

## 🧪 Verificación

### Pruebas rápidas:

1. **Página principal**: Deberías ver artículos
2. **Crear artículo**: Ve a `/admin` y crea uno con imagen
3. **Ver artículo**: Haz click en el artículo, la imagen debería verse
4. **Comentarios**: Intenta comentar (requiere login)
5. **Filtros**: Usa categorías y ordenamiento
6. **Mobile**: Abre desde celular, debe verse bien

---

## 🐛 Troubleshooting

### ❌ Error 500 (Server Error)

**Solución:**
```bash
# Ver error log
cat /var/log/tu_usuario.pythonanywhere.com.error.log
```

Causas comunes:
- Falta importar `decouple` → `pip install python-decouple`
- WSGI mal configurado → Revisar ruta
- BD no migrada → `python manage.py migrate`

---

### ❌ Error "No module named 'decouple'"

**Solución en Bash:**
```bash
workon salud_fuerza  # Activar venv
pip install python-decouple
```

---

### ❌ Las imágenes no se cargan

**Solución:**
```bash
# En Bash, asegúrate que collectstatic se ejecutó
python manage.py collectstatic --noinput

# Recargar app en Dashboard → Web → Reload
```

---

### ❌ Error "No such table"

**Solución:**
```bash
python manage.py migrate
```

---

### ❌ Cambios en código no se reflejan

**Solución:**
1. Dashboard → Web → **Reload**
2. O ejecuta en Bash: `touch /var/www/tu_usuario_pythonanywhere_com_wsgi.py`

---

## 📊 Monitoreo

### Ver Logs en tiempo real

Dashboard → **"Web"** → Desplázate hacia abajo:

- **Error log**: Errores de la aplicación
- **Server log**: Tráfico HTTP

---

## 🔄 Actualizar Código

Si cambias algo en el código:

### Opción 1: Desde Bash
```bash
cd ~/fuerza-salud
git pull origin main
python manage.py migrate  # Si hay nuevas migraciones
python manage.py collectstatic --noinput
```

### Opción 2: Recargar desde Dashboard
Dashboard → Web → **Reload**

---

## 🎓 Próximos Pasos

### 1. Dominio Personalizado
- Compra un dominio (godaddy, namecheap, etc.)
- En Dashboard → "Account" → "Web address" → Apunta al dominio

### 2. Certificado SSL
- PythonAnywhere lo da automático en dominio personalizado

### 3. Email
- Configura SMTP para enviar notificaciones

### 4. Backups
- Descarga BD regularmente desde Files

---

## 📞 Ayuda

### Documentación oficial
- https://www.pythonanywhere.com/help/

### Chat de soporte
- En el Dashboard → Chat (ícono inferior derecho)

### Mi Contacto
- Para dudas específicas, contacta al desarrollador

---

## ✨ ¡Felicidades! 🎉

Tu proyecto **Salud & Fuerza AR** está en línea y disponible para todo el mundo.

**Hecho con ❤️ y Django**

---

**Última actualización:** Diciembre 2025
**Versión:** 1.0
