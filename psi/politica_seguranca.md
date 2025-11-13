# Política de Segurança da Informação (PSI)
## Imóvel Prime

**Versão:** 1.0  
**Data:** 2024  
**Aprovação:** Diretoria

---

## 1. OBJETIVO

Esta Política de Segurança da Informação (PSI) estabelece diretrizes, normas e procedimentos para garantir a confidencialidade, integridade e disponibilidade das informações da Imóvel Prime, protegendo os dados de clientes, imóveis e operações da empresa contra ameaças, vulnerabilidades e riscos.

## 2. ESCOPO

Esta política aplica-se a todos os colaboradores, sistemas, processos, dados e infraestrutura tecnológica da Imóvel Prime, incluindo sistemas web, bancos de dados, redes, dispositivos e informações em qualquer formato.

## 3. PRINCÍPIOS FUNDAMENTAIS

### 3.1. Confidencialidade
- Informações sensíveis devem ser acessadas apenas por pessoas autorizadas.
- Dados pessoais de clientes (CPF, e-mail, telefone) são tratados como confidenciais.
- Comunicação de dados sensíveis deve utilizar protocolos criptografados (HTTPS/TLS).
- Classificação da informação conforme nível de sensibilidade.

### 3.2. Integridade
- Garantir que as informações não sejam alteradas de forma não autorizada.
- Implementar controles de acesso e auditoria para rastreabilidade.
- Validação de dados em formulários e APIs.
- Backup regular e verificação de integridade dos dados.

### 3.3. Disponibilidade
- Sistemas críticos devem estar disponíveis conforme SLA definido.
- Implementar redundância e planos de contingência.
- Monitoramento de performance e disponibilidade.
- Manutenção preventiva e correção proativa de falhas.

## 4. CONFORMIDADE LEGAL

### 4.1. LGPD (Lei Geral de Proteção de Dados)
- Tratamento de dados pessoais conforme Lei nº 13.709/2018.
- Consentimento explícito para coleta e uso de dados.
- Direitos do titular: acesso, correção, exclusão, portabilidade, oposição.
- Nomeação de Encarregado de Proteção de Dados (DPO), se aplicável.
- Notificação de incidentes de segurança que possam causar risco aos titulares.

### 4.2. Outras Legislações
- Cumprimento de normas do Código de Defesa do Consumidor.
- Respeito à legislação imobiliária vigente.
- Proteção de dados financeiros conforme normas do Banco Central, se aplicável.

## 5. CONTROLES DE ACESSO

### 5.1. Autenticação
- Uso de credenciais únicas (usuário/senha) ou autenticação multifator (MFA) para sistemas sensíveis.
- Senhas devem seguir política de complexidade (mínimo 8 caracteres, maiúsculas, minúsculas, números, símbolos).
- Rotação periódica de senhas.
- Bloqueio de contas após tentativas falhas de login.

### 5.2. Autorização
- Princípio do menor privilégio: acesso apenas ao necessário para execução das funções.
- Revisão periódica de permissões de acesso.
- Segregação de funções (separation of duties).
- Logs de acesso e auditoria de ações críticas.

### 5.3. Rotas Sensíveis
- Rotas administrativas e de cadastro devem ser acessadas exclusivamente via HTTPS.
- Redirecionamento automático de rotas sensíveis acessadas via HTTP para HTTPS.
- Cookies de sessão e CSRF configurados como "Secure" apenas em conexões HTTPS.

## 6. CLASSIFICAÇÃO DA INFORMAÇÃO

### 6.1. Níveis de Classificação
- **Público:** Informações que podem ser divulgadas sem restrições (ex: listagem pública de imóveis).
- **Interno:** Informações para uso interno da empresa (ex: relatórios operacionais).
- **Confidencial:** Dados pessoais de clientes, informações financeiras, credenciais de acesso.
- **Restrito:** Informações altamente sensíveis (ex: dados bancários, senhas, chaves de API).

### 6.2. Tratamento por Classificação
- Dados confidenciais e restritos devem ser armazenados criptografados.
- Acesso restrito baseado em classificação.
- Rotulagem adequada de documentos e sistemas.

## 7. SEGURANÇA DE REDE E SISTEMAS

### 7.1. Criptografia
- Uso de TLS/SSL para comunicação de dados sensíveis (HTTPS na porta 8443).
- Certificados digitais válidos e renovados regularmente.
- Criptografia de dados em repouso para informações sensíveis.

### 7.2. Firewall e Proteção de Perímetro
- Configuração de firewall para bloquear tráfego não autorizado.
- Segmentação de rede quando aplicável.
- Monitoramento de tráfego suspeito.

### 7.3. Atualização e Patches
- Aplicação regular de patches de segurança em sistemas operacionais e aplicações.
- Manutenção de inventário de software e versões.
- Testes de patches em ambiente de homologação antes da produção.

## 8. BACKUP E RECUPERAÇÃO

### 8.1. Backup
- Backup diário automático do banco de dados (SQLite ou equivalente).
- Retenção de backups conforme política de retenção (mínimo 30 dias).
- Armazenamento de backups em local seguro e separado do ambiente de produção.
- Testes periódicos de restauração de backup.

### 8.2. Plano de Continuidade
- Documentação de procedimentos de recuperação de desastres (DRP).
- Definição de RTO (Recovery Time Objective) e RPO (Recovery Point Objective).
- Exercícios de simulação de desastres.

## 9. E-MAIL E COMUNICAÇÃO

### 9.1. Uso Seguro de E-mail
- Não enviar dados sensíveis (CPF, senhas) por e-mail sem criptografia.
- Verificação de remetentes suspeitos (phishing).
- Uso de assinatura digital para comunicações oficiais, quando aplicável.

### 9.2. Comunicação Interna
- Canais seguros para comunicação de informações confidenciais.
- Treinamento sobre engenharia social e phishing.

## 10. VPN E ACESSO REMOTO

### 10.1. Acesso Remoto
- Uso de VPN (Virtual Private Network) para acesso remoto a sistemas internos.
- Autenticação forte para conexões VPN.
- Logs de conexões VPN e monitoramento de atividades.

## 11. TREINAMENTO E CONSCIENTIZAÇÃO

### 11.1. Treinamento de Segurança
- Treinamento inicial e periódico sobre segurança da informação para todos os colaboradores.
- Conscientização sobre phishing, engenharia social e boas práticas.
- Simulações de incidentes de segurança.

### 11.2. Cultura de Segurança
- Promoção de cultura onde segurança é responsabilidade de todos.
- Canal de reporte de incidentes e vulnerabilidades.
- Reconhecimento de boas práticas de segurança.

## 12. AUDITORIA E MONITORAMENTO

### 12.1. Logs e Monitoramento
- Registro de logs de acesso, autenticação, alterações críticas e erros.
- Retenção de logs conforme política (mínimo 90 dias).
- Monitoramento proativo de atividades suspeitas.
- Alertas automáticos para eventos de segurança.

### 12.2. Auditoria
- Auditorias internas periódicas de segurança.
- Revisão de logs e permissões de acesso.
- Avaliação de conformidade com esta PSI e legislação aplicável.

## 13. GESTÃO DE INCIDENTES

### 13.1. Procedimento de Incidentes
- Plano de resposta a incidentes de segurança (IRP).
- Equipe de resposta a incidentes designada.
- Notificação imediata de incidentes críticos à diretoria e autoridades, se necessário (LGPD).
- Documentação e análise pós-incidente (lessons learned).

## 14. RESPONSABILIDADES

### 14.1. Diretoria
- Aprovação e suporte à PSI.
- Alocação de recursos para segurança.

### 14.2. TI/Segurança
- Implementação e manutenção de controles de segurança.
- Monitoramento e resposta a incidentes.
- Atualização desta PSI conforme necessário.

### 14.3. Colaboradores
- Cumprimento desta PSI.
- Reporte de incidentes e vulnerabilidades.
- Uso seguro de sistemas e informações.

## 15. REVISÃO E ATUALIZAÇÃO

Esta PSI deve ser revisada anualmente ou sempre que houver mudanças significativas no ambiente, legislação ou riscos. Alterações devem ser comunicadas a todos os colaboradores.

---

**Aprovação:**  
Diretoria Imóvel Prime  
Data: 2024

