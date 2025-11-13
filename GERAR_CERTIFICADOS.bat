@echo off
echo ========================================
echo Gerando Certificados SSL/TLS
echo ========================================
echo.

cd /d "%~dp0"

if not exist "certs" (
    echo Criando pasta certs...
    mkdir certs
)

echo.
echo [1/5] Gerando chave privada da CA...
openssl genrsa -out certs\ca.key 4096
if errorlevel 1 goto erro

echo [2/5] Gerando certificado da CA...
openssl req -x509 -new -nodes -key certs\ca.key -sha256 -days 365 -subj "/C=BR/ST=MG/L=Diamantina/O=ImovelPrime/OU=TI/CN=ImovelPrime-CA" -out certs\ca.crt
if errorlevel 1 goto erro

echo [3/5] Gerando chave privada do servidor...
openssl genrsa -out certs\server.key 2048
if errorlevel 1 goto erro

echo [4/5] Gerando Certificate Signing Request...
openssl req -new -key certs\server.key -subj "/C=BR/ST=MG/L=Diamantina/O=ImovelPrime/OU=TI/CN=localhost" -out certs\server.csr
if errorlevel 1 goto erro

echo [5/5] Assinando certificado do servidor...
openssl x509 -req -in certs\server.csr -CA certs\ca.crt -CAkey certs\ca.key -CAcreateserial -out certs\server.crt -days 365 -sha256
if errorlevel 1 goto erro

echo.
echo ========================================
echo Certificados gerados com sucesso!
echo ========================================
echo.
echo IMPORTANTE: Importe o arquivo certs\ca.crt no seu navegador
echo para evitar avisos de "Nao seguro".
echo.
echo Veja o tutorial_openssl.md para instrucoes detalhadas.
echo.
pause
goto fim

:erro
echo.
echo ERRO: Falha ao gerar certificados!
echo Verifique se o OpenSSL esta instalado.
echo.
pause
exit /b 1

:fim

