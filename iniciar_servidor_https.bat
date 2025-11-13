@echo off
echo Iniciando servidor HTTPS na porta 8443...
cd /d "%~dp0"
python -m uvicorn config.asgi:application --host 0.0.0.0 --port 8443 --ssl-keyfile certs/server.key --ssl-certfile certs/server.crt
pause

