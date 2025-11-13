@echo off
echo Iniciando servidor HTTPS na porta 8443...
cd /d "%~dp0"
set CERT_PATH=%~dp0certs
python -m uvicorn config.asgi:application --host 0.0.0.0 --port 8443 --ssl-keyfile "%CERT_PATH%\server.key" --ssl-certfile "%CERT_PATH%\server.crt"
pause


