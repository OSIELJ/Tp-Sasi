#!/usr/bin/env python
"""
Script para gerar certificados SSL/TLS usando Python (sem precisar do OpenSSL instalado).
"""
import os
import ipaddress
from pathlib import Path
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta

def gerar_certificados():
    """Gera os certificados SSL/TLS necessários."""
    
    # Criar pasta certs se não existir
    certs_dir = Path("certs")
    certs_dir.mkdir(exist_ok=True)
    
    print("Gerando certificados SSL/TLS...")
    print()
    
    # 1. Gerar chave privada da CA
    print("[1/5] Gerando chave privada da CA...")
    ca_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
    )
    ca_key_path = certs_dir / "ca.key"
    try:
        with open(ca_key_path, "wb") as f:
            key_bytes = ca_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
            f.write(key_bytes)
        print(f"[OK] {ca_key_path} criado")
    except Exception as e:
        print(f"[ERRO] Falha ao criar {ca_key_path}: {e}")
        raise
    
    # 2. Gerar certificado da CA
    print("[2/5] Gerando certificado da CA...")
    ca_subject = ca_issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "BR"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "MG"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Diamantina"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "ImovelPrime"),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "TI"),
        x509.NameAttribute(NameOID.COMMON_NAME, "ImovelPrime-CA"),
    ])
    
    ca_cert = x509.CertificateBuilder().subject_name(
        ca_subject
    ).issuer_name(
        ca_issuer
    ).public_key(
        ca_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=365)
    ).add_extension(
        x509.BasicConstraints(ca=True, path_length=None), critical=True,
    ).sign(ca_key, hashes.SHA256())
    
    ca_cert_path = certs_dir / "ca.crt"
    with open(ca_cert_path, "wb") as f:
        f.write(ca_cert.public_bytes(serialization.Encoding.PEM))
    print(f"[OK] {ca_cert_path} criado")
    
    # 3. Gerar chave privada do servidor
    print("[3/5] Gerando chave privada do servidor...")
    server_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    server_key_path = certs_dir / "server.key"
    with open(server_key_path, "wb") as f:
        key_bytes = server_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        f.write(key_bytes)
    print(f"[OK] {server_key_path} criado")
    
    # 4. Gerar CSR do servidor (opcional, mas vamos criar)
    print("[4/5] Gerando Certificate Signing Request...")
    server_csr = x509.CertificateSigningRequestBuilder().subject_name(
        x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "BR"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "MG"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Diamantina"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "ImovelPrime"),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "TI"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
    ).sign(server_key, hashes.SHA256())
    
    server_csr_path = certs_dir / "server.csr"
    with open(server_csr_path, "wb") as f:
        f.write(server_csr.public_bytes(serialization.Encoding.PEM))
    print(f"[OK] {server_csr_path} criado")
    
    # 5. Assinar certificado do servidor com a CA
    print("[5/5] Assinando certificado do servidor...")
    server_cert = x509.CertificateBuilder().subject_name(
        x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "BR"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "MG"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Diamantina"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "ImovelPrime"),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "TI"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
    ).issuer_name(
        ca_issuer
    ).public_key(
        server_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName("localhost"),
            x509.DNSName("127.0.0.1"),
            x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
        ]),
        critical=False,
    ).sign(ca_key, hashes.SHA256())
    
    server_cert_path = certs_dir / "server.crt"
    with open(server_cert_path, "wb") as f:
        f.write(server_cert.public_bytes(serialization.Encoding.PEM))
    print(f"[OK] {server_cert_path} criado")
    
    print()
    print("=" * 60)
    print("[OK] Certificados gerados com sucesso!")
    print("=" * 60)
    print()
    print("Arquivos criados em: certs/")
    print("   - ca.key (chave privada da CA)")
    print("   - ca.crt (certificado da CA - importar no navegador)")
    print("   - server.key (chave privada do servidor)")
    print("   - server.csr (Certificate Signing Request)")
    print("   - server.crt (certificado do servidor)")
    print()
    print("IMPORTANTE:")
    print("   Importe o arquivo certs/ca.crt no seu navegador")
    print("   para evitar avisos de 'Nao seguro'.")
    print()
    print("   Veja o tutorial_openssl.md para instrucoes detalhadas.")
    print()

if __name__ == "__main__":
    try:
        gerar_certificados()
    except ImportError:
        print("[ERRO] Biblioteca 'cryptography' nao instalada!")
        print()
        print("Instale com:")
        print("   pip install cryptography")
        print()
        print("Ou adicione ao requirements.txt e execute:")
        print("   pip install -r requirements.txt")
        exit(1)
    except Exception as e:
        print(f"[ERRO] {e}")
        exit(1)

