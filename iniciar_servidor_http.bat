@echo off
echo Iniciando servidor HTTP na porta 8080...
cd /d "%~dp0"
python manage.py runserver 0.0.0.0:8080
pause

