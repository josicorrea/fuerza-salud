# 🏋️ Salud & Fuerza AR - Blog de Salud y Fitness

Un blog moderno y completo construido con Django para compartir artículos sobre nutrición, fitness, bienestar y salud. Incluye sistema de usuarios con roles, comentarios, categorización de posts e interfaz responsiva con Bootstrap.

## ✨ Características Principales

- ✅ **CRUD Completo** - Crear, editar y eliminar posts con validaciones
- ✅ **Sistema de Usuarios** con roles (Visitante, Miembro, Colaborador)
- ✅ **Comentarios** - Usuarios pueden comentar en posts
- ✅ **Categorización** - Organiza posts por categorías
- ✅ **Filtrado y Ordenamiento** - Por categoría, fecha, título
- ✅ **Paginación** - 5 posts por página
- ✅ **Upload de Imágenes** - Sube imágenes principales para cada post
- ✅ **Autenticación** - Login, logout, registro con generación automática de perfiles
- ✅ **Interfaz Responsiva** - Bootstrap 5.3.3 con diseño moderno
- ✅ **Mensajes de Feedback** - Confirmaciones al crear, editar o eliminar

## 🛠️ Requisitos Previos

- Python 3.8+
- pip (gestor de paquetes de Python)
- git (opcional, para clonar)

## 📦 Instalación

### 1. Clonar o descargar el proyecto

```bash
git clone <URL-del-repositorio>
cd Proyecto_Final
```

### 2. Crear un virtual environment

```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Realizar migraciones de la base de datos

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear un usuario administrador (superuser)

```bash
python manage.py createsuperuser
```

Sigue las indicaciones para crear el usuario admin.

### 6. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://127.0.0.1:8000/`

## 🚀 Uso

### Acceder al sitio

- **Inicio**: `http://127.0.0.1:8000/`
- **Panel Admin**: `http://127.0.0.1:8000/admin/`
- **Login**: `http://127.0.0.1:8000/accounts/login/`
- **Registro**: `http://127.0.0.1:8000/signup/`

### Roles de Usuario

| Rol | Permisos |
|-----|----------|
| **Visitante** | Ver posts, comentar |
| **Miembro** | Igual a Visitante + comentarios moderados |
| **Colaborador** | Crear, editar, eliminar sus propios posts |
| **Superuser** | Acceso total (admin) |

### Crear un Post

1. Login como usuario con rol "Colaborador" o Superuser
2. Ir a "Crear artículo"
3. Completar título, categoría, contenido e imagen (opcional)
4. Click en "Guardar"

### Comentar

1. Ir a un post
2. Desplazarse hasta "Comentarios"
3. Escribir comentario y presionar "Enviar comentario"

## 📁 Estructura del Proyecto

```
Proyecto_Final/
├── blog/                          # Aplicación principal
│   ├── migrations/                # Migraciones de BD
│   ├── templates/blog/            # Templates HTML
│   │   ├── base.html              # Layout principal
│   │   ├── post_list.html         # Lista de posts
│   │   ├── post_detail.html       # Detalle del post
│   │   ├── post_form.html         # Crear/editar post
│   │   ├── comment_form.html      # Editar comentario
│   │   ├── about.html             # Página about
│   │   ├── contact.html           # Página contacto
│   │   └── post_confirm_delete.html
│   ├── admin.py                   # Configuración admin
│   ├── models.py                  # Modelos (Post, Comment, Category, Profile)
│   ├── views.py                   # Vistas y lógica
│   ├── forms.py                   # Formularios
│   ├── urls.py                    # Rutas de la app
│   ├── signals.py                 # Señales (auto-crear Profile)
│   └── apps.py                    # Config de la app
├── salud_fuerza/                  # Configuración del proyecto
│   ├── settings.py                # Settings (BD, apps, media)
│   ├── urls.py                    # Rutas principales
│   └── wsgi.py / asgi.py         # Servidores web
├── media/                         # Archivos subidos por usuarios
│   └── posts/                     # Imágenes de posts
├── requirements.txt               # Dependencias
├── manage.py                      # Herramienta de Django
└── db.sqlite3                     # Base de datos
```

## 🗄️ Modelos de Datos

### Post
- title (CharField)
- slug (SlugField) - autogenerado
- category (ForeignKey → Category)
- author (ForeignKey → User)
- content (TextField)
- image (ImageField) - opcional
- created_at (DateTimeField)
- updated_at (DateTimeField)
- is_published (BooleanField)

### Comment
- post (ForeignKey → Post)
- author (ForeignKey → User)
- content (TextField)
- created_at (DateTimeField)
- is_active (BooleanField)

### Category
- name (CharField)
- slug (SlugField) - autogenerado

### Profile
- user (OneToOneField → User)
- role (CharField) - visitante/miembro/colaborador

## 🔐 Control de Permisos

| Acción | Visitante | Miembro | Colaborador | Superuser |
|--------|-----------|---------|-------------|-----------|
| Ver posts | ✅ | ✅ | ✅ | ✅ |
| Comentar | ✅ | ✅ | ✅ | ✅ |
| Crear post | ❌ | ❌ | ✅ | ✅ |
| Editar propio post | ❌ | ❌ | ✅ | ✅ |
| Eliminar propio post | ❌ | ❌ | ✅ | ✅ |
| Editar comentario propio | ✅ | ✅ | ✅ | ✅ |
| Moderar posts/comentarios | ❌ | ❌ | ❌ | ✅ |

## 🚀 Despliegue en PythonAnywhere

### Pasos para desplegar:

1. **Crear cuenta en PythonAnywhere** (https://www.pythonanywhere.com)

2. **Subir archivos del proyecto** (via Git o upload)

3. **Crear Virtual Environment**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 salud_fuerza
   pip install -r requirements.txt
   ```

4. **Configurar settings.py**
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['tu_usuario.pythonanywhere.com']
   STATIC_URL = '/static/'
   STATIC_ROOT = '/home/tu_usuario/salud_fuerza/static/'
   ```

5. **Recolectar archivos estáticos**
   ```bash
   python manage.py collectstatic --noinput
   ```

6. **Crear superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Configurar Web App** en PythonAnywhere
   - Seleccionar "Manual configuration"
   - Señalar archivo WSGI
   - Configurar static/media files

8. **Recargar la app**

## 🧪 Testing

Para ejecutar los tests (si existen):

```bash
python manage.py test
```

## 📝 Variables de Entorno

Considera crear un archivo `.env` para producción:

```
DEBUG=False
SECRET_KEY=tu_clave_secreta_aqui
ALLOWED_HOSTS=localhost,127.0.0.1,tu_dominio.com
```

## 🐛 Troubleshooting

### Error: "No se encuentran los templates"
- Verifica que `TEMPLATES` en `settings.py` incluya `'APP_DIRS': True`

### Error: "No such table" en comentarios/posts
- Ejecuta: `python manage.py migrate`

### Las imágenes no se cargan en desarrollo
- Verifica que `MEDIA_URL` y `MEDIA_ROOT` estén configurados en `settings.py`
- Asegúrate que existe la carpeta `media/posts/`

### Error de permisos al crear post
- Verifica que el usuario tenga rol "Colaborador" en su Profile
- El admin (superuser) siempre puede crear posts

## 📞 Soporte

Para reportar issues o sugerencias, contacta al equipo de desarrollo.

## 📄 Licencia

Este proyecto está bajo licencia MIT. Eres libre de usar, modificar y distribuir.

---

**Última actualización**: Diciembre 2025

Hecho con ❤️ para la comunidad de Salud & Fuerza AR
