# 🏋️ Salud & Fuerza AR - Blog de Salud y Fitness

Un blog moderno y completo construido con Django para compartir artículos sobre nutrición, fitness, bienestar y salud. Incluye sistema de usuarios con roles, comentarios, categorización de posts e interfaz responsiva con Bootstrap.

## Características Principales

- ✅ **CRUD Completo** - Crear, editar y eliminar posts con validaciones
- ✅ **Sistema de Usuarios** con roles (Visitante, Miembro, Colaborador)
- ✅ **Comentarios** - Usuarios pueden comentar en posts
- ✅ **Categorización** - Organiza posts por categorías
- ✅ **Filtrado y Ordenamiento** - Por categoría, fecha, título
- ✅ **Paginación** - 5 posts por página
- ✅ **Upload de Imágenes** - Sube imágenes principales para cada post
- ✅ **Autenticación** - Login, logout, registro con generación automática de perfiles


## Instalación

### 1. Clonar o descargar el proyecto

```bash
git clone https://github.com/josicorrea/fuerza-salud
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

## Uso

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

## Control de Permisos

| Acción | Visitante | Miembro | Colaborador | Superuser |
|--------|-----------|---------|-------------|-----------|
| Ver posts | ✅ | ✅ | ✅ | ✅ |
| Comentar | ✅ | ✅ | ✅ | ✅ |
| Crear post | ❌ | ❌ | ✅ | ✅ |
| Editar propio post | ❌ | ❌ | ✅ | ✅ |
| Eliminar propio post | ❌ | ❌ | ✅ | ✅ |
| Editar comentario propio | ✅ | ✅ | ✅ | ✅ |
| Moderar posts/comentarios | ❌ | ❌ | ❌ | ✅ |
