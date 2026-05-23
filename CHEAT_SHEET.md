# KPG Webhook — Cheat Sheet Rápido

Referência rápida de tudo que foi feito e como usar.

---

## 🎯 O que é

Webhook Flask em **https://kpg-webhook-otimizar.onrender.com** que:
- Recebe imagens do SIGA
- Adiciona metadados SEO (77 campos)
- Upload para Google Cloud Storage
- Retorna URL pública

---

## 🔗 URL Principal

```
POST https://kpg-webhook-otimizar.onrender.com/otimizar_imagem
```

**Body JSON**:
```json
{
  "url_imagem": "https://...",
  "id_imovel": "123",
  "nome_imovel": "Apartamento"
}
```

**Response**:
```json
{
  "status": "sucesso",
  "url_otimizada": "https://storage.googleapis.com/kpg-imagens-otimizadas/..."
}
```

---

## 🔧 Configuração Render

### Environment Variables
```
FLASK_ENV=production
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

### Secret Files (.env)
```
FLASK_ENV=production
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
GOOGLE_CREDENTIALS_B64=<inteiro>
```

---

## 📋 Google Cloud

**Bucket**: `kpg-imagens-otimizadas`

**CRÍTICO**:
- ✅ Desabilitar Uniform bucket-level access
- ✅ Service Account com Storage Object Creator/Viewer
- ✅ Upload com `predefined_acl='publicRead'`

---

## 📊 Limites API

| Limite | Valor |
|--------|-------|
| QPM | 300 |
| Edições/min | 10 |
| Posts/dia | Ilimitado |

**Atual**: 1 post a cada 15 min = 99,3% de margem ✅

---

## 🆘 Problemas

| Erro | Fix |
|------|-----|
| 403 Forbidden | Desabilitar Uniform access, usar predefined_acl |
| Incorrect padding | Base64 truncado, usar Secret Files |
| control character | JSON corrompido, usar Secret Files |
| storage.objects.create | Adicionar Storage Object Creator role |

---

## ✅ Testes

**Local**:
```bash
python teste_webhook_local.py
```

**Produção**:
```bash
curl https://kpg-webhook-otimizar.onrender.com/status
```

---

## 📁 Arquivos Principais

```
webhook_otimizar_imagem.py  → Flask app
edit_metadata.py            → Adiciona metadados
requirements.txt            → Dependências
.env                        → Local (Git ignorado)
.gitignore                  → O que não commitar
render.yaml                 → Config Render
README.md                   → Referência completa
SETUP.md                    → Passo a passo
GITHUB_SETUP.md             → Como usar GitHub
CHEAT_SHEET.md              → Este arquivo
```

---

## 🚀 Deploy

```bash
git push origin main
# Render detecta e redeploy automático
```

---

## 📞 Endpoints

| Endpoint | Método | Função |
|----------|--------|--------|
| /otimizar_imagem | POST | Otimizar e fazer upload |
| /status | GET | Health check |
| /debug | GET | Info credenciais |
| /test | POST | Teste conectividade |

---

## 🔐 Segurança

**NUNCA commitar**:
- .env
- credentials.json
- CREDENTIALS_B64.txt

**Usar**:
- Secret Files (Render)
- Environment Variables

---

## 💡 Lições Aprendidas

1. **Secret Files > Variáveis de Ambiente** para dados grandes
2. **Desabilitar Uniform bucket-level access** para ACL por objeto
3. **predefined_acl='publicRead'** na hora do upload, não depois
4. **Service Account precisa de Storage Object Creator** para upload

---

**Status**: ✅ Produção  
**Última Atualização**: 2026-05-22
