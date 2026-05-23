# Setup GitHub para KPG Webhook Otimizar Imagem

Este arquivo documenta como enviar o código para GitHub e manter o repositório sincronizado.

---

## 📋 Repositório GitHub

**Repositório**: kpg-webhook-otimizar  
**URL**: https://github.com/seu-usuario/kpg-webhook-otimizar  
**Visibilidade**: Public (para histórico de configuração)

---

## 🚀 Enviar para GitHub (Primeira Vez)

### Passo 1: Inicializar Git

```bash
cd "C:\Users\User\KPG IMAGEM METADADOS"
git init
git config user.name "Seu Nome"
git config user.email "csrdesouza@gmail.com"
```

### Passo 2: Verificar .gitignore

Certifique-se que `.gitignore` contém:

```
credentials.json
.env
*.pyc
__pycache__/
.DS_Store
CREDENTIALS_B64.txt
```

**Importante**: Estes arquivos NÃO devem ser commitados por segurança

### Passo 3: Adicionar Arquivos

```bash
git add webhook_otimizar_imagem.py
git add edit_metadata.py
git add requirements.txt
git add .gitignore
git add render.yaml
git add README.md
git add SETUP.md
git add GITHUB_SETUP.md
git add teste_webhook_local.py
```

### Passo 4: Commit Inicial

```bash
git commit -m "Initial commit: Flask webhook for image optimization with GCS upload"
```

### Passo 5: Criar Repositório no GitHub

1. Acessar https://github.com/new
2. Nome: `kpg-webhook-otimizar`
3. Descrição: "Flask webhook for optimizing real estate images with SEO metadata and Google Cloud Storage upload"
4. Público
5. NÃO inicializar com README (já temos)
6. Create repository

### Passo 6: Push para GitHub

```bash
git branch -M main
git remote add origin https://github.com/seu-usuario/kpg-webhook-otimizar.git
git push -u origin main
```

**Seu nome de usuário GitHub**: (você escolhe)

---

## 📝 O que Documentar no GitHub

### 1. README.md (Raiz)

✅ Já criado. Contém:
- Resumo do projeto
- Fluxo de funcionamento
- Configuração necessária
- Limites API
- Endpoints
- Troubleshooting

### 2. SETUP.md

✅ Já criado. Contém:
- Instruções passo a passo completas
- Google Cloud setup
- Credenciais em Base64
- Setup local
- Deploy Render
- Validação

### 3. GITHUB_SETUP.md

Seu arquivo atual. Documenta:
- Como sincronizar com GitHub
- Processo de deploy

---

## 🔄 Manter Sincronizado

Sempre que fizer mudanças no código:

```bash
git add arquivo_modificado.py
git commit -m "Descrição breve da mudança"
git push origin main
```

**Render detecta push automático** e faz redeploy!

---

## 📦 Arquivo de Secrets (NÃO no GitHub)

Arquivos que NUNCA devem ir para GitHub:

- ❌ `.env` (variáveis de ambiente local)
- ❌ `credentials.json` (JSON Google Service Account)
- ❌ `CREDENTIALS_B64.txt` (Base64 da credencial)

Estes são gerenciados via **Secret Files no Render** ou **Environment Variables**.

---

## ✅ Checklist para GitHub

- [x] Repositório criado (públic)
- [x] .gitignore configurado
- [x] README.md escrito
- [x] SETUP.md escrito
- [x] GITHUB_SETUP.md escrito
- [x] webhook_otimizar_imagem.py commitado
- [x] edit_metadata.py commitado
- [x] requirements.txt commitado
- [x] render.yaml commitado
- [x] teste_webhook_local.py commitado
- [ ] Push para main branch
- [ ] Verificar código no GitHub
- [ ] Testar Render redeploy automático

---

## 🔐 Segurança

**Nunca**: Commitar credenciais, tokens, keys, ou .env files

**Sempre**: Usar Secret Files ou Environment Variables no Render para dados sensíveis

**Se acidentalmente commitar credenciais**:
1. Regenerar Google Service Account keys imediatamente
2. `git rm --cached .env` (remove arquivo)
3. `git commit -m "Remove .env file"`
4. `git push`

---

## 🎯 Próximos Passos

1. Executar comandos do "Passo 1-6" acima
2. Verificar no GitHub se está tudo lá
3. Fazer uma mudança de teste (ex: atualizar README)
4. Verificar se Render faz redeploy automático

---

**Documentado em**: 2026-05-22
