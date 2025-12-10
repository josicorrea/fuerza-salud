@echo off
REM Script para ejecutar el servidor Django en desarrollo

echo.
echo ======================================
echo  Salud & Fuerza AR - Servidor Local
echo ======================================
echo.

REM Activar virtual environment
call venv\Scripts\activate.bat

REM Ejecutar servidor
echo Iniciando servidor en http://127.0.0.1:8000/
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

python manage.py runserver
