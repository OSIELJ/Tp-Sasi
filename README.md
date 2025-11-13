# 🏠 Imóvel Prime – Sistema Web com Segurança Seletiva (TPIV_SASI)

## 👥 Grupo
- Osiel Junior  
- Maicon Douglas  
- Raul Rodriguês  
- Fernando Maia  

---

## 📌 1. Visão Geral

O **Imóvel Prime** é um sistema web desenvolvido para o **TPIV_SASI** com foco em **segurança seletiva**, utilizando:

- **HTTP** para páginas públicas  
- **HTTPS** para páginas sensíveis (login, cadastro, dashboard, admin)

A aplicação roda simultaneamente em:

- 🔵 **HTTP – Porta 8080** → Rotas públicas  
- 🟢 **HTTPS – Porta 8443** → Rotas sensíveis  

---

## 🔐 2. Segurança Seletiva (HTTP/HTTPS)

A segurança foi implementada com:

### ✔ Divisão de URLs
No arquivo **`core/urls.py`**, existem duas listas:

- `urlpatterns_publicas` → HTTP  
- `urlpatterns_seguras` → HTTPS  

### ✔ Middleware de Redirecionamento
Arquivo: `config/middleware.py`  
Classe: **ForceHTTPSSelective**

Função:

- Identifica quando o usuário acessa rota sensível pelo HTTP  
- Executa redirecionamento **301 Permanent Redirect** para HTTPS (porta 8443)

Middleware habilitado em `config/settings.py`.

### ✔ Servidores
- `python manage.py runserver` → HTTP :8080  
- `uvicorn` + SSL → HTTPS :8443  

---

## 🔑 3. Geração dos Certificados Digitais

Você pode gerar os certificados de duas formas:

---

### 🔹 Método A — Via OpenSSL (Requisito do Trabalho)

Necessário ter **OpenSSL** instalado.

```powershell
.\GERAR_CERTIFICADOS.bat
O script gera:

- `certs/ca.key` → chave privada da CA  
- `certs/ca.crt` → certificado raiz  
- `certs/server.key` → chave privada do servidor  
- `certs/server.csr` → CSR (Certificate Signing Request)  
- `certs/server.crt` → certificado final usado pelo HTTPS  

---

### 🔹 Método B — Via Python (Automático)

Não requer OpenSSL instalado no sistema, pois utiliza a biblioteca **cryptography**.

python gerar_certificados.py

Esse método:

- Gera automaticamente a CA  
- Gera chave e certificado do servidor  
- Salva tudo na pasta `certs/`  
- Reduz dependências externas (não exige OpenSSL)  

---

## ⚙️ 4. Como Executar o Projeto

### ✔ Pré-requisitos

- **Python 3.11+**
- **Git**
- **PowerShell (Windows é recomendado)**
- **OpenSSL (opcional, apenas para o Método A)**

---

## 🚀 Método 1 – Execução Automatizada (Recomendado)

No PowerShell:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

.\setup_e_rodar_tudo.ps1

Esse script executa automaticamente:

- Criação do ambiente virtual  
- Instalação das dependências  
- Geração dos certificados SSL  
- Execução das migrações do banco de dados  
- Inicialização do servidor HTTP (8080)  
- Inicialização do servidor HTTPS (8443)  

Ideal para testes rápidos e execução imediata do sistema.

---

## 🧩 Método 2 – Execução Manual

### 1️⃣ Clonar o repositório


git clone https://github.com/OSIELJ/Tp-Sasi.git
cd imovel-prime

### 2️⃣ Criar o ambiente virtual


python -m venv .venv

.\.venv\Scripts\Activate.ps1

3️⃣ Instalar dependências

pip install -r requirements.txt

4️⃣ Gerar os certificados SSL

python gerar_certificados.py

5️⃣ Executar as migrações do banco

python manage.py migrate

6️⃣ Subir os servidores

🔵 Terminal 1 — HTTP (8080)

python manage.py runserver 0.0.0.0:8080

🟢 Terminal 2 — HTTPS (8443)

python -m uvicorn config.asgi:application --host 0.0.0.0 --port 8443 --ssl-keyfile certs/server.key --ssl-certfile certs/server.crt

🌐 5. Acesso ao Sistema

🔵 Página Pública (HTTP)

http://localhost:8080/

🟢 Página Segura (HTTPS — Login, Dashboard)

https://localhost:8443/login/

⚠️ IMPORTANTE:
Para evitar alertas de site inseguro no navegador, importe o certificado:


certs/ca.crt
como Autoridade Certificadora Raiz Confiável.

🔒 6. Política de Segurança da Informação (PSI)
Arquivo localizado em:

psi/politica_seguranca.md

O documento descreve:

Confidencialidade dos dados

Integridade e prevenção de alterações indevidas

Conformidade com a LGPD

Identificação e mitigação de riscos

Autenticação e controles de acesso

Segurança no armazenamento e na transmissão

📁 Estrutura Simplificada do Projeto

imovel-prime/
│
├── certs/                   # Certificados gerados automaticamente
├── config/                  # Configurações (ASGI, settings, middleware)
├── core/                    # URLs públicas e protegidas
├── psi/                     # Política de Segurança da Informação
├── gerar_certificados.py    # Script de geração de certificados via Python
├── GERAR_CERTIFICADOS.bat   # Script de geração via OpenSSL
├── setup_e_rodar_tudo.ps1   # Setup geral automatizado
├── manage.py
└── requirements.txt

📝 Licença
Projeto acadêmico desenvolvido para o TPIV_SASI.
Uso permitido apenas para fins educacionais.
