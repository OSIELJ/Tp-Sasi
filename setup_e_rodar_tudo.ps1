# ======================================================================
#  SCRIPT DE SETUP E EXECUÇÃO COMPLETO - IMÓVEL PRIME
# ======================================================================
# Este script assume que o Python 3.11+ e o PIP estão instalados
# e acessíveis no PATH do sistema.
# ======================================================================

# Define o diretório de trabalho para o local do script
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "========================================"
Write-Host "  Iniciando Setup Completo Imóvel Prime"
Write-Host "========================================"
Write-Host ""

# --- 1. Verificar Python ---
Write-Host "[1/6] Verificando instalação do Python..."
$pythonCheck = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCheck) {
    Write-Host "[ERRO] Python não encontrado no PATH!"
    Write-Host "Por favor, instale o Python 3.11+ e adicione-o ao PATH."
    pause
    exit 1
}
Write-Host "[OK] Python encontrado."
Write-Host ""

# --- 2. Configurar Ambiente Virtual (Venv) ---
$VenvDir = ".\.venv"
$VenvPython = ".\.venv\Scripts\python.exe"
$VenvPip = ".\.venv\Scripts\pip.exe"

Write-Host "[2/6] Configurando ambiente virtual (.venv)..."
if (-not (Test-Path $VenvDir)) {
    Write-Host "   Criando .venv..."
    python -m venv .venv
    Write-Host "[OK] Ambiente virtual criado."
} else {
    Write-Host "[OK] Ambiente virtual .venv já existe."
}
Write-Host ""

# --- 3. Instalar Dependências ---
Write-Host "[3/6] Instalando dependências do requirements.txt..."
# Usamos & para executar o pip de dentro do venv
& $VenvPip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERRO] Falha ao instalar dependências."
    pause
    exit 1
}
Write-Host "[OK] Dependências instaladas."
Write-Host ""

# --- 4. Gerar Certificados ---
Write-Host "[4/6] Gerando certificados SSL..."
# Usamos & para executar o python de dentro do venv
& $VenvPython gerar_certificados.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERRO] Falha ao gerar certificados."
    pause
    exit 1
}
Write-Host "[OK] Certificados gerados."
Write-Host ""

# --- 5. Executar Migrações do Banco de Dados ---
Write-Host "[5/6] Executando migrações (python manage.py migrate)..."
& $VenvPython manage.py migrate
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERRO] Falha ao executar migrações."
    pause
    exit 1
}
Write-Host "[OK] Banco de dados migrado."
Write-Host ""

# --- 6. Iniciar Servidores ---
Write-Host "[6/6] Iniciando servidores (HTTP e HTTPS)..."
Write-Host ""

# Iniciar servidor HTTP (porta 8080)
Write-Host "Iniciando servidor HTTP (porta 8080) em uma nova janela..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptPath'; Write-Host 'Servidor HTTP Rodando...'; & $VenvPython manage.py runserver 0.0.0.0:8080"

Start-Sleep -Seconds 2

# Iniciar servidor HTTPS (porta 8443)
Write-Host "Iniciando servidor HTTPS (porta 8443) em uma nova janela..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptPath'; Write-Host 'Servidor HTTPS Rodando...'; & $VenvPython -m uvicorn config.asgi:application --host 0.0.0.0 --port 8443 --ssl-keyfile certs\server.key --ssl-certfile certs\server.crt"

Start-Sleep -Seconds 3

Write-Host ""
Write-Host "========================================"
Write-Host "  SETUP E EXECUÇÃO CONCLUÍDOS!"
Write-Host "========================================"
Write-Host "Dois novos terminais foram abertos para os servidores."
Write-Host ""
Write-Host "HTTP (Porta 8080):"
Write-Host "  http://localhost:8080/"
Write-Host ""
Write-Host "HTTPS (Porta 8443):"
Write-Host "  https://localhost:8443/login/"
Write-Host ""
Write-Host "========================================"
Write-Host ""
Write-Host "Pressione qualquer tecla para fechar este script de setup..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")