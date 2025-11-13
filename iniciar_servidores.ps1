# Script para iniciar ambos os servidores
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "========================================"
Write-Host "  Iniciando Servidores Imovel Prime"
Write-Host "========================================"
Write-Host ""

# Verificar se os certificados existem
if (-not (Test-Path "certs\server.key") -or -not (Test-Path "certs\server.crt")) {
    Write-Host "[ERRO] Certificados nao encontrados!"
    Write-Host "Execute: python gerar_certificados.py"
    exit 1
}

Write-Host "[OK] Certificados encontrados"
Write-Host ""

# Iniciar servidor HTTP
Write-Host "Iniciando servidor HTTP (porta 8080)..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptPath'; python manage.py runserver 0.0.0.0:8080"

Start-Sleep -Seconds 2

# Iniciar servidor HTTPS
Write-Host "Iniciando servidor HTTPS (porta 8443)..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptPath'; python -m uvicorn config.asgi:application --host 0.0.0.0 --port 8443 --ssl-keyfile certs\server.key --ssl-certfile certs\server.crt"

Start-Sleep -Seconds 3

Write-Host ""
Write-Host "========================================"
Write-Host "  Servidores Iniciados!"
Write-Host "========================================"
Write-Host ""
Write-Host "HTTP (Porta 8080):"
Write-Host "  http://localhost:8080/"
Write-Host ""
Write-Host "HTTPS (Porta 8443):"
Write-Host "  https://localhost:8443/login/"
Write-Host ""
Write-Host "========================================"
Write-Host ""
Write-Host "Pressione qualquer tecla para sair..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

