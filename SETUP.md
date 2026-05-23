# Setup Completo - KPG Webhook Otimizar Imagem

Este documento fornece instruções passo a passo para configurar o webhook do zero.

---

## 🎯 Objetivo Final

Ter um webhook em produção (Render) que:
1. Recebe URLs de imagens do SIGA
2. Otimiza metadados
3. Upload para Google Cloud Storage
4. Retorna URL pública para Make.com

---

## 📋 Pré-requisitos

- [ ] Conta Google Cloud
- [ ] Bucket GCS criado
- [ ] Service Account criado
- [ ] Conta Render
- [ ] Repositório GitHub
- [ ] Python 3.8+ instalado (local)

---

## FASE 1: Google Cloud Setup

### Passo 1.1: Criar Projeto Google Cloud

1. Acessar [Google Cloud Console](https://console.cloud.google.com)
2. Clicar em "Select a Project" → "New Project"
3. Nome: `kpg-webhook`
4. Deixar projeto ser criado (2-3 min)

### Passo 1.2: Ativar Google Cloud Storage API

1. No Console, ir para "APIs & Services"
2. Clicar "Enable APIs and Services"
3. Buscar por "Cloud Storage API"
4. Clicar "Enable"

### Passo 1.3: Criar Service Account

1. Ir para "APIs & Services" → "Credentials"
2. Clicar "Create Credentials" → "Service Account"
3. Preencher:
   - Service account name: `kpg-webhook`
   - Service account ID: (auto-preenchido)
4. Clicar "Create and Continue"
5. Grants (roles):
   - Adicionar role: `Storage Object Creator`
   - Adicionar role: `Storage Object Viewer`
6. Clicar "Continue"
7. Clicar "Done"

### Passo 1.4: Gerar JSON Key

1. Na página de Credentials, encontrar a Service Account `kpg-webhook`
2. Clicar em "kpg-webhook-554@kpg-webhook.iam.gserviceaccount.com"
3. Ir para aba "Keys"
4. Clicar "Add Key" → "Create new key"
5. Escolher "JSON"
6. Download automático do arquivo JSON
7. **Guardar em local seguro** (será necessário depois)

### Passo 1.5: Criar GCS Bucket

1. Ir para "Cloud Storage" → "Buckets"
2. Clicar "Create"
3. Preencher:
   - Name: `kpg-imagens-otimizadas`
   - Location: `us-central1` (ou sua região)
   - Storage class: `Standard`
   - Uniform bucket-level access: **DESABILITAR** (crítico!)
4. Avançar em todas as páginas mantendo defaults
5. Clicar "Create"

### Passo 1.6: Verificar Configurações do Bucket

1. Abrir bucket `kpg-imagens-otimizadas`
2. Ir para "Permissions" tab
3. Verificar que Service Account `kpg-webhook-554@...` tem:
   - `roles/storage.objectCreator` ✅
   - `roles/storage.objectViewer` ✅

---

## FASE 2: Converter Credenciais para Base64

### Windows PowerShell

```powershell
# Navegar para pasta do arquivo
cd "C:\Users\User\Downloads"

# Ler arquivo JSON e converter para Base64
$json = Get-Content -Raw "kpg-webhook-1234567890abcdef.json"
$bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
$base64 = [Convert]::ToBase64String($bytes)

# Copiar para clipboard
$base64 | Set-Clipboard

# Verificar tamanho (deve ter ~3000+ caracteres)
$base64.Length
```

### Salvar em arquivo local

```powershell
$base64 | Out-File -FilePath "CREDENTIALS_B64.txt" -Encoding UTF8
```

---

## FASE 3: Setup Local do Projeto

### Passo 3.1: Clonar/Preparar Repositório

```bash
# Se clonando do GitHub
git clone https://github.com/seu-user/kpg-webhook-otimizar.git
cd kpg-webhook-otimizar

# Se iniciando novo
git init
```

### Passo 3.2: Criar Arquivo .env Local

```bash
# Criar arquivo .env na raiz do projeto
cat > .env << EOF
FLASK_ENV=development
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
GOOGLE_CREDENTIALS_B64=COLE_AQUI_O_BASE64_INTEIRO
EOF
```

**Importante**: Cole o Base64 **inteiro** do Passo 2.5

### Passo 3.3: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 3.4: Testar Localmente

```bash
python teste_webhook_local.py
```

**Esperado**: Mensagem "✓ SUCESSO TOTAL"

---

## FASE 4: Deploy no Render

### Passo 4.1: Conectar GitHub ao Render

1. Acessar [Render.com](https://render.com)
2. Conectar conta GitHub
3. Autorizar acesso ao repositório

### Passo 4.2: Criar Web Service

1. Dashboard Render → "New +" → "Web Service"
2. Selecionar repositório `kpg-webhook-otimizar`
3. Preencher:
   - Name: `kpg-webhook-otimizar`
   - Environment: `Python 3`
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn webhook_otimizar_imagem:app`
4. Clicar "Create Web Service"

### Passo 4.3: Configurar Environment Variables

1. Na página do serviço, ir para "Environment"
2. Adicionar:
   ```
   FLASK_ENV=production
   FLASK_HOST=0.0.0.0
   FLASK_PORT=5000
   ```

### Passo 4.4: Adicionar Secret Files

**Crítico**: Não colar Base64 como variável de ambiente!

1. Ir para "Environment" → "Secret Files"
2. Clicar "Add Secret File"
3. Preencher:
   - Filename: `.env`
   - File contents:
     ```
     FLASK_ENV=production
     FLASK_HOST=0.0.0.0
     FLASK_PORT=5000
     GOOGLE_CREDENTIALS_B64=COLE_AQUI_BASE64_INTEIRO
     ```
4. Clicar "Save"

### Passo 4.5: Deploy

1. Render detecta push automático
2. Se não, clicar "Manual Deploy" → "Deploy latest commit"
3. Aguardar logs mostrarem "Ready"
4. URL será exibida: `https://kpg-webhook-otimizar.onrender.com`

---

## FASE 5: Validação em Produção

### Passo 5.1: Testar Endpoint /status

```bash
curl https://kpg-webhook-otimizar.onrender.com/status
```

**Esperado**: `{"status":"ativo", ...}`

### Passo 5.2: Testar Endpoint /debug

```bash
curl https://kpg-webhook-otimizar.onrender.com/debug
```

**Esperado**: JSON com informações de credenciais (project_id, client_email)

### Passo 5.3: Testar Upload Real

```bash
curl -X POST https://kpg-webhook-otimizar.onrender.com/otimizar_imagem \
  -H "Content-Type: application/json" \
  -d '{
    "url_imagem": "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png",
    "id_imovel": "teste_001",
    "nome_imovel": "Teste KPG"
  }'
```

**Esperado**: 
```json
{
  "status": "sucesso",
  "url_otimizada": "https://storage.googleapis.com/kpg-imagens-otimizadas/imovel_teste_001_...",
  ...
}
```

---

## FASE 6: Integração com Make.com

### Passo 6.1: Criar Webhook no Make

1. Acessar [Make.com](https://make.com)
2. Criar novo blueprint ou scenario
3. Adicionar trigger HTTP webhook
4. Copiar URL do webhook Make

### Passo 6.2: Configurar Rota Siga → Make → Webhook

1. No SIGA, configurar rota para Make
2. Make recebe evento
3. Make chama webhook KPG: `POST https://kpg-webhook-otimizar.onrender.com/otimizar_imagem`
4. Webhook retorna URL pública
5. Make publica no Google Meu Negócio

### Passo 6.3: Testar Fluxo Completo

1. No SIGA, criar/atualizar imóvel
2. Verificar logs Make
3. Verificar se URL pública foi recebida
4. Verificar se Google Meu Negócio foi atualizado

---

## 🔍 Verificação de Saúde

Executar regularmente:

```bash
# Status do webhook
curl https://kpg-webhook-otimizar.onrender.com/status

# Debug (credenciais, projeto)
curl https://kpg-webhook-otimizar.onrender.com/debug

# Listar objetos no bucket GCS
gsutil ls gs://kpg-imagens-otimizadas/
```

---

## 🆘 Se Algo Não Funcionar

### 1. Verificar Logs Render

- Acessar Render → Serviço → "Logs"
- Procurar por mensagens de erro
- Se vir "[FALLBACK]", há problema nas credenciais

### 2. Verificar Credenciais Render

- Ir para "Environment" → "Secret Files"
- Verificar se `.env` contém `GOOGLE_CREDENTIALS_B64`
- Verificar tamanho (deve ser ~3000+ caracteres)

### 3. Testar Localmente

```bash
python teste_webhook_local.py
```

Se funcionar local mas não em produção:
- Credenciais no Render estão truncadas/corrompidas
- Usar Secret Files em vez de variável de ambiente

### 4. Verificar GCS Bucket

```bash
# Listar objetos
gsutil ls gs://kpg-imagens-otimizadas/

# Verificar permissões da Service Account
gcloud projects get-iam-policy kpg-webhook
```

---

## ✅ Checklist Final

- [ ] Projeto Google Cloud criado
- [ ] Service Account criado com permissões
- [ ] JSON key gerado
- [ ] GCS bucket criado
- [ ] Uniform bucket-level access desabilitado
- [ ] Base64 gerado e testado
- [ ] Repositório GitHub criado
- [ ] render.yaml configurado
- [ ] .env local criado
- [ ] Teste local passou
- [ ] Render web service criado
- [ ] Secret Files adicionadas
- [ ] Deploy em produção
- [ ] Endpoints testados (/status, /debug, POST)
- [ ] Integração Make.com configurada
- [ ] Fluxo completo testado

---

**Status**: Quando todos os itens estiverem checked, webhook está pronto para produção! 🚀
