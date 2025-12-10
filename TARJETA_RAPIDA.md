# 🎯 TARJETA DE REFERENCIA RÁPIDA

## Estado: ✅ PROYECTO COMPLETADO

---

## 📌 CUANDO PYTHONANYWHERE VUELVA (5 PASOS)

### 1️⃣ Crear Cuenta
```
https://www.pythonanywhere.com → Sign up → Confirmar email
```

### 2️⃣ Descargar Proyecto
```bash
cd ~
git clone https://github.com/josicorrea/fuerza-salud.git
cd fuerza-salud
```

### 3️⃣ Instalar Dependencias
```bash
mkvirtualenv --python=/usr/bin/python3.10 fuerza-salud-env
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 4️⃣ Configurar Web App
- Dashboard → Web → Add web app
- Manual configuration → Python 3.10
- Editar WSGI: Copiar código de `DESPLIEGUE_ULTRA_SIMPLE.md`
- Static files: `/static/` → `/home/tu_usuario/fuerza-salud/static`
- Media files: `/media/` → `/home/tu_usuario/fuerza-salud/media`
- Virtualenv: `/home/tu_usuario/.virtualenvs/fuerza-salud-env`

### 5️⃣ Reload
Click en botón RELOAD azul arriba → ¡Listo!

---

## 🌍 RESULTADO
```
https://tu_usuario.pythonanywhere.com
```

Admin: `https://tu_usuario.pythonanywhere.com/admin/`

---

## 📚 ARCHIVOS DE REFERENCIA

| Archivo | Contenido | Tiempo |
|---------|----------|--------|
| `DESPLIEGUE_ULTRA_SIMPLE.md` | Versión ultra rápida | 5 min |
| `PYTHONANYWHERE_GUIA_COMPLETA.md` | Paso a paso detallado | 15 min |
| `INICIO_RAPIDO.md` | Resumen ejecutivo | 3 min |
| `PROYECTO_COMPLETADO.md` | Estado final | 5 min |

---

## 🔧 COMANDOS ÚTILES

### Desarrollo local:
```bash
venv\Scripts\activate
python manage.py runserver
# http://127.0.0.1:8000/
```

### Si algo falla:
```bash
python manage.py check
python manage.py migrate
python manage.py collectstatic --noinput
```

---

## 🎯 CHECKLIST PRE-DESPLIEGUE

- [ ] Cuenta creada en PythonAnywhere
- [ ] Proyecto clonado desde GitHub
- [ ] Virtual environment creado
- [ ] Dependencias instaladas
- [ ] Migraciones aplicadas
- [ ] Superuser creado
- [ ] Static files recolectados
- [ ] WSGI file actualizado
- [ ] Static files configurados
- [ ] Media files configurados
- [ ] Virtualenv configurado
- [ ] App recargada
- [ ] Blog accesible en URL
- [ ] Admin funciona
- [ ] Posts visibles

---

## 🆘 SI ALGO FALLA

### Error 500
→ Dashboard → Error log → Leer error

### Las imágenes no cargan
```bash
python manage.py collectstatic --noinput
# Luego Reload
```

### Base de datos error
```bash
python manage.py migrate
```

### Permisos
```bash
chmod -R 755 ~/fuerza-salud/media/
chmod -R 755 ~/fuerza-salud/static/
```

---

## ✨ CARACTERÍSTICAS

✅ Posts con imágenes
✅ Comentarios
✅ Categorías
✅ Filtros
✅ Usuarios
✅ Admin panel
✅ UI profesional
✅ Responsive

---

## 📊 PROYECTO

- **Nombre**: Salud & Fuerza AR
- **Tipo**: Blog de Fitness
- **Framework**: Django 5.2.8
- **Frontend**: Bootstrap 5.3.3
- **Estado**: 🟢 Listo para producción
- **Tiempo despliegue**: ⏱️ 5 minutos

---

## 🚀 ¡LISTO PARA IR EN VIVO!

**Solo falta:**
1. Esperar a PythonAnywhere
2. Seguir guía rápida
3. ¡En vivo!

---

Proyecto completado ✅
Diciembre 2025
