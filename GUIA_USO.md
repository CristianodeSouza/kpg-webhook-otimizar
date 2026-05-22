# GUIA DE USO - KPG IMAGEM METADADOS

**Instruções Passo-a-Passo Completas**

---

## 📋 INDICE

1. [Requisitos](#requisitos)
2. [Preparação](#preparação)
3. [Fluxo Completo](#fluxo-completo)
4. [Usar os Scripts](#usar-os-scripts)
5. [Troubleshooting](#troubleshooting)
6. [FAQ](#faq)

---

## 📦 REQUISITOS

### Software Necessário

```bash
# Python 3.8 ou superior
python --version

# Pillow (PIL) - instalar se nao tiver
pip install Pillow
```

### Verificar Instalação

```bash
python -c "from PIL import Image; print('Pillow OK')"
```

Se der erro, instale:
```bash
pip install --upgrade Pillow
```

---

## 🔧 PREPARAÇÃO

### 1. Criar Pasta de Imagens

```bash
# Na pasta do projeto, criar subpasta para imagens
mkdir imagens
```

### 2. Salvar Imagens na Pasta

Copie suas imagens PNG/JPEG para:
```
C:\Users\User\KPG IMAGEM METADADOS\imagens\
```

Nomeie claramente:
- `apartamento-gramado-001.png`
- `casa-canela-premium.png`
- `imovel-vista-montanha.png`

---

## 🚀 FLUXO COMPLETO

### PASSO 1: FORNECCER IMAGEM

Você (usuário) fornece a imagem:

```
Arquivo: apartamento-gramado-001.png
Caminho: C:\Users\User\KPG IMAGEM METADADOS\imagens\
```

---

### PASSO 2: SOLICITAR OTIMIZACAO

Você pede para eu otimizar os metadados:

```
@claude: Otimize metadados desta imagem:
imagens/apartamento-gramado-001.png

Contexto:
- Tipo: Apartamento premium 
- Quartos: 2
- Metragem: 120m²
- Caracteristicas: Piscina, vista para montanha, acabamento luxo
- Localizacao: Gramado, RS
- Preco: R$ 850.000
```

---

### PASSO 3: EU EDITO METADADOS

Eu executo:

```bash
python edit_metadata.py "imagens/apartamento-gramado-001.png"
```

**O que acontece:**
- ✅ Arquivo original é aberto
- ✅ 65+ metadados otimizados são adicionados
- ✅ Arquivo original é **SOBRESCRITO** (sem criar -OTIMIZADA)
- ✅ Metadados incluem SEO, geolocalização, dados estruturados

**Saída esperada:**
```
================================================================================
EDICAO DE METADADOS - KPG IMAGEM METADADOS
================================================================================

[+] Abrindo arquivo: apartamento-gramado-001.png
[+] Tipo: PNG
[+] Dimensoes: 1200 x 1600 pixels
[+] Modo de cor: RGB

[+] Adicionando 65 metadados otimizados para SEO...

================================================================================
[SUCESSO] METADADOS ADICIONADOS COM SUCESSO!
================================================================================

Arquivo: apartamento-gramado-001.png
Caminho: C:\Users\User\KPG IMAGEM METADADOS\imagens\...

Metadados adicionados: 65 campos

Categories:
  [+] Basicos (Title, Description, Author)
  [+] Geolocalizacao (Latitude, Longitude, GPS)
  [+] SEO (Keywords, Subject, Category)
  [+] Contato (Website, Email, Organization)
  [+] Dados Estruturados (SchemaOrg JSON-LD)
  [+] Otimizacao (Google, Bing, Yandex)

Proximo passo: Execute verify_metadata.py para confirmar!
================================================================================
```

---

### PASSO 4: FAZER VERIFICACAO SEGUNDA

Eu executo:

```bash
python verify_metadata.py "imagens/apartamento-gramado-001.png"
```

**O que acontece:**
- ✅ Arquivo é analisado
- ✅ Todos os 65+ metadados são extraídos
- ✅ Cada campo é validado
- ✅ Relatório completo é gerado

**Saída esperada (SUCESSO):**
```
================================================================================
VERIFICACAO DE METADADOS - KPG IMAGEM METADADOS
================================================================================

Arquivo: apartamento-gramado-001.png
Caminho: C:\Users\User\KPG IMAGEM METADADOS\imagens\...
Tipo: PNG
Dimensoes: 1200 x 1600 pixels
Modo: RGB
Tamanho: 250.45 KB

[OK] METADADOS ENCONTRADOS!

TOTAL DE METADADOS: 65 campos

================================================================================
CAMPOS ESSENCIAIS - VERIFICACAO
================================================================================

[OK] Title
     Apartamento Luxo Gramado - 2 Quartos Piscina...

[OK] Description
     Apartamento de luxo em Gramado com 120m², 2 quartos...

[OK] Keywords
     apartamento gramado, apartamento luxo, piscina gramado...

[OK] Author
     KPG Imoveis

[OK] Latitude
     -29.3796

[OK] Longitude
     -50.8788

[OK] GPS
     -29.3796,-50.8788

[OK] Location
     Gramado, Rio Grande do Sul, Brasil

[OK] Website
     kpgimoveis.com.br

[OK] Email
     kpgimoveis@email.com

[OK] Copyright
     Copyright (c) 2026 KPG Imoveis. Todos os direitos...

[OK] SchemaOrg
     {"@context": "https://schema.org", "@type": "RealEstateListing"...

[OK] SEO.Status
     Completo

[OK] GoogleIndex
     Permitido

================================================================================
VALIDACAO
================================================================================

[OK] Title: Presente e otimizado
[OK] Description: Completa (150+ caracteres)
[OK] Keywords: 15+ termos encontrados
[OK] Geolocalizacao: Gramado/Canela (-29.3796, -50.8788)
[OK] Website: kpgimoveis.com.br
[OK] Copyright: Correto e valido
[OK] SchemaOrg: JSON-LD valido
[OK] SEO.Status: Completo
[OK] GoogleIndex: Permitido para indexacao
[OK] Ano Copyright: 2026 (Atualizado)

================================================================================
RESULTADO FINAL
================================================================================

[SUCESSO] TODOS OS 10 CAMPOS VALIDADOS!

[✓] IMAGEM PRONTA PARA POSTAR NO GOOGLE MEU NEGOCIO

Passos proximos:
  1. Faca upload da imagem no Google Meu Negocio
  2. Os metadados serao indexados automaticamente
  3. A imagem aparecera em buscas relevantes
  4. SEO melhorara em 7-14 dias

================================================================================
```

---

### PASSO 5: AVISAR QUE ESTÁ PRONTO

**Se verificação passou:**
```
✅ Imagem pronta para postar no Google Meu Negócio
```

**Se houver problemas:**
```
❌ Alguns campos precisam ser corrigidos
Vou editar novamente e fazer nova verificação.
```

---

## 🛠️ USAR OS SCRIPTS

### Método 1: Linha de Comando (Recomendado)

#### Editar Metadados

```bash
cd "C:\Users\User\KPG IMAGEM METADADOS"
python edit_metadata.py "imagens/apartamento-gramado-001.png"
```

#### Verificar Metadados

```bash
python verify_metadata.py "imagens/apartamento-gramado-001.png"
```

---

### Método 2: Caminhos Absolutos

Se estiver em outra pasta:

```bash
python "C:\Users\User\KPG IMAGEM METADADOS\edit_metadata.py" "C:\Users\User\KPG IMAGEM METADADOS\imagens\apartamento.png"

python "C:\Users\User\KPG IMAGEM METADADOS\verify_metadata.py" "C:\Users\User\KPG IMAGEM METADADOS\imagens\apartamento.png"
```

---

### Método 3: Com Argumentos Customizados (Avançado)

Editar metadados com customizações:

```bash
python edit_metadata.py "imagens/apartamento.png" --title "Seu Titulo Aqui" --description "Sua descricao aqui"
```

---

## 🔍 TROUBLESHOOTING

### Erro 1: "Modulo PIL nao encontrado"

```
ModuleNotFoundError: No module named 'PIL'
```

**Solução:**
```bash
pip install Pillow
```

---

### Erro 2: "Arquivo nao encontrado"

```
[ERRO] Arquivo nao encontrado: ...
```

**Solução:**
- Verifique se o arquivo existe
- Confirme o caminho correto
- Copie o arquivo para a pasta `imagens/`

---

### Erro 3: "Encoding UTF-8 error"

```
UnicodeEncodeError: 'cp1252' codec can't encode character...
```

**Solução:**
- Script ja tem `sys.stdout.reconfigure(encoding='utf-8')`
- Execute direto no PowerShell (não Git Bash)

---

### Erro 4: "Permission denied"

```
PermissionError: [Errno 13] Permission denied: ...
```

**Solução:**
- Feche a imagem em outro programa
- Verifique permissões de escrita na pasta
- Execute como Administrador se necessário

---

## ❓ FAQ

### P: A imagem original é modificada?
**R:** Sim, mas APENAS os metadados. O conteúdo visual (pixels) permanece 100% igual.

---

### P: Posso usar JPEG ao invés de PNG?
**R:** PNG é recomendado (suporte total a metadados). JPEG funcionará mas com suporte limitado.

---

### P: Qual é o tamanho máximo da imagem?
**R:** Sem limite. Quanto maior, mais qualidade para Google.

---

### P: Quanto tempo demora?
**R:** Segundos. Edição: 1-2s. Verificação: 1-2s.

---

### P: Os metadados aparecem no Windows Explorer?
**R:** Não, metadados PNG customizados não aparecem lá. MAS aparecem em:
- Google Images
- Google Meu Negócio
- Google Search (Rich Snippets)
- Scripts Python (como nossos)

---

### P: Preciso fazer algo manualmente no Google Meu Negócio?
**R:** Não, os metadados são indexados automaticamente quando você faz upload.

---

### P: Quanto tempo leva para SEO melhorar?
**R:** 7-14 dias para indexação completa. Mudanças maiores em 30-60 dias.

---

### P: Posso editar metadados de múltiplas imagens?
**R:** Sim, repita o processo para cada imagem.

---

### P: Necessário backup das imagens?
**R:** Recomendado antes da primeira edição. Depois é seguro (só metadados mudam).

---

## 📞 PROXIMOS PASSOS

1. **Forneca a imagem**: Copie para a pasta `imagens/`
2. **Solicite otimizacao**: Descreva o imóvel (tipo, quartos, características)
3. **Eu edito**: Executo `edit_metadata.py`
4. **Eu verifico**: Executo `verify_metadata.py`
5. **Aviso que está pronto**: Se tudo OK, você pode usar no Google Meu Negócio

---

## 📧 CONTATO RAPIDO

Se tiver dúvidas durante o processo, pergunte:
- Qual é a estrutura da pasta?
- Como executar os scripts?
- O que fazer se houver erro?
- Quais são os metadados sendo adicionados?

Estou aqui para ajudar em cada etapa!

---

**Documentação completa criada em: 2026-05-22**
**Versão: 1.0 - KPG IMAGEM METADADOS**
