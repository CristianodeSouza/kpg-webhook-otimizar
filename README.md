# KPG Webhook Otimizar Imagem - Documentação Completa

**Status**: ✅ Em Produção no Render  
**URL Produção**: https://kpg-webhook-otimizar.onrender.com  
**Última Atualização**: 2026-05-22

---

## 📋 Resumo do Projeto

Webhook Flask que:
- Recebe URLs de imagens do SIGA (sistema de gestão de imóveis)
- Otimiza imagens adicionando 77+ campos de metadados SEO
- Faz upload para Google Cloud Storage (GCS)
- Retorna URLs HTTPS públicas para integração com Make.com
- Publica automaticamente no Google Meu Negócio

---

## 🎯 Fluxo de Funcionamento

```
SIGA (imagem URL)
    ↓
Make.com (webhook trigger)
    ↓
Flask POST /otimizar_imagem
    ├─ Download da imagem
    ├─ Executa edit_metadata.py (adiciona 77 campos)
    ├─ Upload para Google Cloud Storage
    └─ Retorna URL pública HTTPS
    ↓
Make.com (processa URL)
    ↓
Google Meu Negócio (publicação automática)
```

---

## 🔧 Configuração Necessária

### 1. Secret Files (Render - CRÍTICO)

Usar a seção "Secret Files" para armazenar `.env`:

```
Nome do arquivo: .env
Conteúdo:
FLASK_ENV=production
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
GOOGLE_CREDENTIALS_B64=<Base64 da credencial - INTEIRO>
```

**Por que Secret Files?**
- Protege credenciais contra truncamento
- Evita corrupção de caracteres especiais
- Previne "Incorrect padding" errors

### 2. Google Cloud Storage (GCS)

**Bucket**: `kpg-imagens-otimizadas`

**Configurações CRÍTICAS:**
1. ✅ **DESABILITAR "Uniform bucket-level access"**
   - Permite ACL por objeto
   - Necessário para `predefined_acl='publicRead'`

2. ✅ Service Account com permissões:
   - `roles/storage.objectCreator`
   - `roles/storage.objectViewer`

3. ✅ Upload com ACL público:
   ```python
   blob.upload_from_filename(
       caminho_local,
       content_type='image/png',
       predefined_acl='publicRead'  # CRÍTICO
   )
   ```

---

## 📊 Limites API Google My Business

| Limite | Valor | Status |
|--------|-------|--------|
| QPM | 300 | Normal |
| Edições/min | 10 | HARD LIMIT |
| Posts/dia | Ilimitado* | *Sem limite específico |

### Configuração Atual (SEGURA)

```
Make Schedule: 1 post a cada 15 min (20:00-22:00)
Taxa: 0,067 posts/min
Limite: 10 posts/min
Status: ✅ 99,3% de margem
```

---

## ✅ Endpoints da API

### POST /otimizar_imagem

Request:
```json
{
  "url_imagem": "https://siga.example.com/imagens/imovel_123.jpg",
  "id_imovel": "123",
  "nome_imovel": "Apartamento Gramado"
}
```

Response (200):
```json
{
  "status": "sucesso",
  "url_otimizada": "https://storage.googleapis.com/kpg-imagens-otimizadas/imovel_123_...",
  "metadados_adicionados": 65
}
```

### GET /status

Retorna status webhook

### GET /debug

Debug info (credenciais, projeto)

---

## 🧪 Testes

**Local:**
```bash
python teste_webhook_local.py
```

**Produção:**
```bash
curl https://kpg-webhook-otimizar.onrender.com/status
```

---

## 🚨 Problemas Comuns

| Erro | Causa | Solução |
|------|-------|---------|
| 403 Forbidden | ACL não configurado | Desabilitar Uniform bucket-level access |
| Incorrect padding | Base64 truncado | Usar Secret Files, não variáveis |
| control character | JSON corrompido | Secret Files em vez de ambiente |
| storage.objects.create | Sem permissão | Adicionar Storage Object Creator role |

---

## 📁 Estrutura do Projeto

```
C:\Users\User\KPG IMAGEM METADADOS\
├── webhook_otimizar_imagem.py
├── edit_metadata.py
├── requirements.txt
├── .env (Git ignorado)
├── .gitignore
├── render.yaml
├── README.md (este)
├── SETUP.md
├── CREDENTIALS_B64.txt
└── teste_webhook_local.py
```

---

## 📚 Para Setup Completo

Ver arquivo **SETUP.md** para instruções passo a passo desde o zero.

---

**Última atualização**: 2026-05-22  
**Contato**: csrdesouza@gmail.com
