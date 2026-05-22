# GUIA DE USO - WEBHOOK KPG IMAGEM METADADOS

**Otimizar imagens ANTES de publicar no Google Meu Negócio**

---

## 📋 ÍNDICE

1. [Requisitos](#requisitos)
2. [Instalação de Dependências](#instalação-de-dependências)
3. [Executar o Webhook](#executar-o-webhook)
4. [Testar o Webhook](#testar-o-webhook)
5. [Integrar no Make](#integrar-no-make)
6. [Troubleshooting](#troubleshooting)

---

## 📦 REQUISITOS

- ✅ Python 3.8+
- ✅ Windows (seu computador)
- ✅ Scripts já criados:
  - `edit_metadata.py`
  - `webhook_otimizar_imagem.py`

---

## 🔧 INSTALAÇÃO DE DEPENDÊNCIAS

### Passo 1: Abrir PowerShell

```powershell
# Clique em: Windows + R
# Digite: powershell
# Pressione: Enter
```

### Passo 2: Navegar até a pasta KPG IMAGEM METADADOS

```powershell
cd "C:\Users\User\KPG IMAGEM METADADOS"
```

### Passo 3: Instalar bibliotecas necessárias

```powershell
pip install flask
pip install requests
```

**Aguarde terminar (leva ~2 minutos)**

### Verificar instalação

```powershell
python -c "import flask; import requests; print('OK - Tudo instalado')"
```

Se aparecer `OK - Tudo instalado`, está pronto! ✅

---

## 🚀 EXECUTAR O WEBHOOK

### Método 1: PowerShell (Simples)

```powershell
cd "C:\Users\User\KPG IMAGEM METADADOS"
python webhook_otimizar_imagem.py
```

**Você verá:**

```
================================================================================
WEBHOOK KPG IMAGEM METADADOS
================================================================================

[+] Iniciando servidor Flask...
[+] Escutando em: http://localhost:5000
[+] Endpoint: POST http://localhost:5000/otimizar_imagem

[!] Para parar: pressione CTRL+C
================================================================================
```

✅ **Webhook está ativo!**

### Método 2: Executar em Background (deixar rodando)

```powershell
# Abra um PowerShell NOVO (não feche o anterior)
# E deixe rodando enquanto usa Make
```

⚠️ **IMPORTANTE:** Deixe o PowerShell aberto enquanto o Make executar as automações

---

## 🧪 TESTAR O WEBHOOK

### Teste 1: Status do Webhook

**No PowerShell, abra outro terminal:**

```powershell
# Novo PowerShell ou use curl direto
curl http://localhost:5000/status
```

**Resposta esperada:**

```json
{
  "status": "ativo",
  "versao": "1.0",
  "endpoints": {
    "otimizar": "POST /otimizar_imagem",
    "status": "GET /status"
  }
}
```

✅ Webhook está respondendo!

---

### Teste 2: Enviar uma imagem real

**Copie e cole no PowerShell:**

```powershell
$url = "https://cdn.mizia.com.br/kpg/img_vendas/g1_2499_33231_1558_200526.jpeg"
$body = @{
    url_imagem = $url
    id_imovel = "TEST-001"
    nome_imovel = "Apartamento Teste"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:5000/otimizar_imagem" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body

$response.Content | ConvertFrom-Json | ConvertTo-Json
```

**Resposta esperada:**

```json
{
  "status": "sucesso",
  "id_imovel": "TEST-001",
  "nome_imovel": "Apartamento Teste",
  "url_original": "https://cdn.mizia.com.br/...",
  "url_otimizada": "file:///C:/Users/User/AppData/Local/Temp/...",
  "metadados_adicionados": 65,
  "timestamp": "2026-05-22T15:30:45.123456"
}
```

✅ Webhook processou a imagem com sucesso!

---

## 🔗 INTEGRAR NO MAKE

### Passo 1: No Make, adicionar novo módulo HTTP

```
Seu cenário atual:
[1] Google Sheets Filter
[2] AI Local Agent
[3] Google My Business Create Post  ← VOCÊ VAI INSERIR AQUI
[4] Update Row
```

**Novo fluxo:**

```
[1] Google Sheets Filter
[2] AI Local Agent
[NEW] HTTP Request (seu webhook)
[3] Google My Business Create Post
[4] Update Row
```

### Passo 2: Configurar módulo HTTP

**No Make:**

1. Clique em `+` para adicionar novo módulo
2. Busque por `HTTP`
3. Selecione `HTTP > Make a request`
4. Configure:

```
Method:         POST
URL:            http://localhost:5000/otimizar_imagem
Headers:        
  Content-Type: application/json

Body (JSON):
{
  "url_imagem": "{{2.Fotos.0.Foto_Grande}}",
  "id_imovel": "{{2.0}}",
  "nome_imovel": "{{2.19}}"
}
```

**Explicação dos campos:**
- `{{2.Fotos.0.Foto_Grande}}` = URL da imagem do SIGA (coluna BU)
- `{{2.0}}` = ID do imóvel (coluna A)
- `{{2.19}}` = Nome do imóvel (coluna T)

### Passo 3: Usar resposta no Google Meu Negócio

**No módulo "Google My Business Create Post":**

Antes estava:
```
Image URL: {{2.Fotos.0.Foto_Grande}}
```

Agora mude para:
```
Image URL: {{5.url_otimizada}}
```

(O número `5` é o ID do módulo HTTP que você adicionou - pode variar)

---

## 🛠️ TROUBLESHOOTING

### Erro: "Connection refused"

```
[ERRO] Cannot connect to http://localhost:5000
```

**Solução:**
- Verifique se o webhook está rodando no PowerShell
- Verifique se não há outro programa usando port 5000
- Reinicie o webhook

```powershell
# Matar processo na port 5000
Get-Process -Name python | Where-Object {$_.Handles -gt 0} | Stop-Process -Force
```

---

### Erro: "Module not found: flask"

```
ModuleNotFoundError: No module named 'flask'
```

**Solução:**

```powershell
pip install flask --upgrade
```

---

### Erro: "edit_metadata.py not found"

```
[ERRO] Arquivo edit_metadata.py nao existe
```

**Solução:**
- Verifique se `edit_metadata.py` está na pasta `C:\Users\User\KPG IMAGEM METADADOS\`
- Verifique o caminho no console do webhook

---

### Webhook respondendo mas Make não funciona

**Checklist:**

```
☐ Webhook está rodando (PowerShell mostra "Escutando em http://localhost:5000")
☐ Port 5000 não está bloqueada por firewall
  → Windows Defender → Firewall → Permitir app pelo firewall
  → Procure por Python e marque "Private networks"
☐ URL no Make está exato: http://localhost:5000/otimizar_imagem
☐ Body JSON está correto (sem aspas extras, sintaxe válida)
☐ Headers Content-Type = application/json
```

---

## 📊 FLUXO COMPLETO - RESUMO

```
1. Você executa webhook
   $ python webhook_otimizar_imagem.py
   ↓
2. Make dispara automação (horário agendado)
   ↓
3. Make busca imóvel não publicado
   ↓
4. Make envia URL da imagem para webhook via HTTP POST
   ↓
5. Webhook recebe, baixa, otimiza, retorna URL nova
   ↓
6. Make recebe URL otimizada
   ↓
7. Make publica no Google Meu Negócio COM METADADOS
   ↓
8. Make marca como publicado na planilha
   ↓
9. Google indexa imagem otimizada em 7-14 dias
   ↓
10. Imóvel aparece em buscas (Gramado, apartamento, etc)
```

---

## ✅ CHECKLIST DE ATIVAÇÃO

- [ ] Python 3.8+ instalado
- [ ] Flask instalado (`pip install flask`)
- [ ] Requests instalado (`pip install requests`)
- [ ] Webhook testado (status endpoint respondendo)
- [ ] Imagem de teste processada com sucesso
- [ ] Módulo HTTP adicionado no Make
- [ ] URL do webhook configurada no Make
- [ ] Body JSON configurado no Make
- [ ] Google Meu Negócio usando {{5.url_otimizada}} (ou número correto)

---

## 📞 PRÓXIMOS PASSOS

1. **Executar webhook:**
   ```powershell
   python webhook_otimizar_imagem.py
   ```

2. **Testar com Make** (deixe webhook rodando)

3. **Primeiras publicações:**
   - Faça teste manual no Make (botão de play)
   - Verifique se imagem foi otimizada
   - Confirme que apareceu no Google Meu Negócio com metadados

4. **Agendar automação:**
   - Depois de confirmar que funciona
   - Agende para rodar diariamente (ex: 06:00 AM)

---

**Versão:** 1.0  
**Criado:** 2026-05-22  
**Status:** ✅ Pronto para usar
