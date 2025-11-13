#!/usr/bin/env python
"""
Script para verificar se a instalação do projeto está correta.
"""
import os
import sys
from pathlib import Path

def verificar_estrutura():
    """Verifica se a estrutura de pastas está correta."""
    print("🔍 Verificando estrutura de pastas...")
    
    pastas_necessarias = [
        'config',
        'core',
        'core/templates/core',
        'certs',
        'psi',
    ]
    
    arquivos_necessarios = [
        'manage.py',
        'requirements.txt',
        'config/settings.py',
        'config/urls.py',
        'config/asgi.py',
        'config/middleware.py',
        'core/models.py',
        'core/views.py',
        'core/forms.py',
        'core/urls.py',
        'README.md',
        'tutorial_openssl.md',
    ]
    
    erros = []
    
    for pasta in pastas_necessarias:
        if not os.path.exists(pasta):
            erros.append(f"❌ Pasta não encontrada: {pasta}")
        else:
            print(f"✅ Pasta encontrada: {pasta}")
    
    for arquivo in arquivos_necessarios:
        if not os.path.exists(arquivo):
            erros.append(f"❌ Arquivo não encontrado: {arquivo}")
        else:
            print(f"✅ Arquivo encontrado: {arquivo}")
    
    return erros

def verificar_certificados():
    """Verifica se os certificados SSL foram gerados."""
    print("\n🔐 Verificando certificados SSL...")
    
    certificados = [
        'certs/ca.key',
        'certs/ca.crt',
        'certs/server.key',
        'certs/server.crt',
    ]
    
    erros = []
    
    for cert in certificados:
        if not os.path.exists(cert):
            erros.append(f"❌ Certificado não encontrado: {cert}")
            print(f"⚠️  {cert} não encontrado - execute os comandos OpenSSL do tutorial")
        else:
            tamanho = os.path.getsize(cert)
            print(f"✅ {cert} encontrado ({tamanho} bytes)")
    
    return erros

def verificar_dependencias():
    """Verifica se as dependências estão instaladas."""
    print("\n📦 Verificando dependências Python...")
    
    try:
        import django
        print(f"✅ Django {django.get_version()} instalado")
    except ImportError:
        print("❌ Django não instalado - execute: pip install -r requirements.txt")
        return False
    
    try:
        import uvicorn
        print(f"✅ Uvicorn instalado")
    except ImportError:
        print("❌ Uvicorn não instalado - execute: pip install -r requirements.txt")
        return False
    
    return True

def verificar_banco():
    """Verifica se o banco de dados foi criado."""
    print("\n💾 Verificando banco de dados...")
    
    if os.path.exists('db.sqlite3'):
        tamanho = os.path.getsize('db.sqlite3')
        print(f"✅ db.sqlite3 encontrado ({tamanho} bytes)")
        print("   Execute 'python manage.py migrate' se ainda não executou")
        return True
    else:
        print("⚠️  db.sqlite3 não encontrado")
        print("   Execute: python manage.py migrate")
        return False

def main():
    print("=" * 60)
    print("VERIFICAÇÃO DA INSTALAÇÃO - IMÓVEL PRIME")
    print("=" * 60)
    
    erros_estrutura = verificar_estrutura()
    erros_certificados = verificar_certificados()
    deps_ok = verificar_dependencias()
    banco_ok = verificar_banco()
    
    print("\n" + "=" * 60)
    print("RESUMO")
    print("=" * 60)
    
    if erros_estrutura:
        print("\n❌ ERROS DE ESTRUTURA:")
        for erro in erros_estrutura:
            print(f"   {erro}")
    else:
        print("\n✅ Estrutura de pastas: OK")
    
    if erros_certificados:
        print("\n⚠️  CERTIFICADOS FALTANDO:")
        for erro in erros_certificados:
            print(f"   {erro}")
        print("\n   Execute os comandos OpenSSL do tutorial_openssl.md")
    else:
        print("\n✅ Certificados SSL: OK")
    
    if not deps_ok:
        print("\n❌ Dependências: FALTANDO")
    else:
        print("\n✅ Dependências: OK")
    
    if not banco_ok:
        print("\n⚠️  Banco de dados: Execute migrações")
    else:
        print("\n✅ Banco de dados: OK")
    
    print("\n" + "=" * 60)
    print("PRÓXIMOS PASSOS:")
    print("=" * 60)
    print("1. Se certificados faltando: execute comandos OpenSSL")
    print("2. Se banco não criado: python manage.py migrate")
    print("3. Criar superuser: python manage.py createsuperuser")
    print("4. Iniciar servidores:")
    print("   Terminal 1: python manage.py runserver 0.0.0.0:8080")
    print("   Terminal 2: uvicorn config.asgi:application --host 0.0.0.0 --port 8443 --ssl-keyfile certs/server.key --ssl-certfile certs/server.crt")
    print("=" * 60)

if __name__ == '__main__':
    main()

