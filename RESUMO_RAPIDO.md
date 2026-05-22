# RESUMO RÁPIDO - KPG IMAGEM METADADOS

**Referência Rápida do Projeto**

---

## 📂 ESTRUTURA DO PROJETO

```
C:\Users\User\KPG IMAGEM METADADOS\
│
├─ README.md                    ← Visão geral do projeto
├─ FLUXO_TRABALHO.md           ← Processo completo (passo-a-passo)
├─ TEMPLATE_METADADOS.md       ← 65+ metadados disponíveis
├─ GUIA_USO.md                 ← Instruções detalhadas + Troubleshooting
├─ RESUMO_RAPIDO.md            ← Este arquivo (referência rápida)
│
├─ edit_metadata.py            ← Script para EDITAR metadados
├─ verify_metadata.py          ← Script para VERIFICAR metadados
│
└─ imagens/                    ← Pasta para salvar imagens PNG/JPEG
   ├─ apartamento-001.png
   ├─ casa-premium.png
   └─ ...
```

---

## ⚡ PROCESSO EM 5 MINUTOS

### 1️⃣ VOCÊ FORNECE IMAGEM
```
Copie arquivo PNG/JPEG para: imagens/
```

### 2️⃣ VOCÊ PEDE PARA OTIMIZAR
```
"@claude: Otimize metadados desta imagem:
imagens/seu-imovel.png

Tipo: Apartamento em Gramado
Características: 2 quartos, piscina, etc."
```

### 3️⃣ EU EDITO METADADOS
```bash
python edit_metadata.py "imagens/seu-imovel.png"
```

### 4️⃣ EU VERIFICO METADADOS
```bash
python verify_metadata.py "imagens/seu-imovel.png"
```

### 5️⃣ RESULTADO
```
✅ Imagem pronta para postar no Google Meu Negócio
```

---

## 🎯 METADADOS ADICIONADOS (65+)

**Categoria Básica (8)**
- Title, Description, Author, Creator, Producer, Copyright, Rights, Software

**Geolocalização (16)**
- Latitude, Longitude, GPS, Location, City, Municipality, State, StateAbbr, Country, CountryCode, Region, GeographicArea, GPSMapDatum, Altitude, LocaleName, LocaleID

**SEO (7)**
- Keywords, Subject, Category, Type, Genre, Comment, Narrative

**Contato (9)**
- URL, Website, Website.pt, Contact, Email, ContactType, BusinessType, Organization, CompanyName

**Conteúdo (6)**
- Content.Type, Content.Topic, Content.Purpose, Content.Language, Language, LanguageCode

**Qualidade (8)**
- ImageQuality, ImageWidth, ImageHeight, Dimensions, AspectRatio, Resolution, ResolutionDPI, ColorMode, ColorDepth

**Data/Versão (5)**
- CreationTime, DateCreated, DateModified, Version, Revision

**Origem (8)**
- Source, SourceWebsite, SourceApp, SourceType, Distribution, Usage, License, Attribution

**SEO Avançado (9)**
- SearchEngine.Google, SearchEngine.Bing, SearchEngine.Yandex, SEO.Status, SEO.Priority, SEO.Importance, SearchEngineOptimization, GoogleIndex, RobotsIndex

**Dados Estruturados (1 + JSON-LD)**
- SchemaOrg (JSON-LD com RealEstateListing)

---

## 🚀 COMANDOS PRINCIPAIS

### Editar Metadados
```bash
cd "C:\Users\User\KPG IMAGEM METADADOS"
python edit_metadata.py "imagens/sua-imagem.png"
```

### Verificar Metadados
```bash
python verify_metadata.py "imagens/sua-imagem.png"
```

### Com Caminho Absoluto
```bash
python "C:\Users\User\KPG IMAGEM METADADOS\edit_metadata.py" "C:\Users\User\...\imagem.png"
```

---

## ✅ CHECKLIST ANTES DE USAR NO GOOGLE

- [x] Arquivo PNG ou JPEG
- [x] Nomeado claramente (ex: apartamento-gramado-001.png)
- [x] Dimensões mínimo 1000x1000 pixels
- [x] Qualidade adequada (não comprimida demais)
- [x] edit_metadata.py foi executado
- [x] verify_metadata.py confirmou sucesso
- [x] Mensagem "✅ Imagem pronta" foi exibida

---

## 🔴 SE HOUVER ERRO

**edit_metadata.py não executa:**
- Instale: `pip install Pillow`
- Use Python 3.8+
- Confirme caminho do arquivo

**verify_metadata.py mostra campos faltantes:**
- Rode `edit_metadata.py` novamente
- Confirme que o arquivo está em PNG
- Se persistir, avise para novo diagnóstico

**Metadados não aparecem no Windows Explorer:**
- NORMAL! Metadados PNG customizados não aparecem lá
- Aparecem em: Google Images, Google Meu Negócio, Google Search

---

## 📞 PADRÃO DE REQUISIÇÃO

Quando fornecedor imagem, use este padrão:

```
@claude: Otimize metadados desta imagem:
imagens/[nome-do-arquivo]

Tipo de imóvel: [Apartamento/Casa/Terreno/etc]
Quartos: [número]
Metragem: [m²]
Características principais: [lista]
Localização: [bairro/cidade]
Preço (opcional): [valor]
Outras info: [se houver]
```

---

## 📊 RESULTADO ESPERADO

Após edição e verificação:

✅ **65+ campos de metadados** embutidos
✅ **Otimizado para Google** Images, Search, Meu Negócio
✅ **Dados estruturados** em JSON-LD
✅ **Geolocalização precisa** (Gramado/Canela)
✅ **Keywords completos** para SEO
✅ **Arquivo original sobrescrito** (sem cópia -OTIMIZADA)
✅ **Verificação segunda confirmada**
✅ **Pronto para publicação** no Google

---

## 📈 IMPACTO NO SEO

Após publicar no Google Meu Negócio:

**7-14 dias:**
- Indexação completa
- Aparece em buscas de "imóvel Gramado"
- Aparece em buscas geolocalizadas

**30-60 dias:**
- Ranqueamento melhor
- Aparece em buscas de concorrentes
- Melhor click-through rate

**60+ dias:**
- Estabilização do posicionamento
- Mais conversões de leads
- Mais visualizações em Google Images

---

## 🎓 REFERÊNCIAS RÁPIDAS

**Ler primeiro:**
1. README.md - Visão geral
2. FLUXO_TRABALHO.md - Entender o processo

**Para usar:**
1. GUIA_USO.md - Passo-a-passo
2. TEMPLATE_METADADOS.md - Consultar campos

**Para troubleshoot:**
1. GUIA_USO.md (seção Troubleshooting)
2. FAQ do GUIA_USO.md

---

## 📝 NOTAS IMPORTANTES

- ✅ Arquivo original é SOBRESCRITO (sem -OTIMIZADA)
- ✅ Conteúdo visual NUNCA muda (apenas metadados)
- ✅ Sempre fazer verificação segunda ANTES de usar
- ✅ Metadados PNG não aparecem no Windows Explorer (NORMAL)
- ✅ Google indexa automaticamente quando faz upload
- ✅ Suporta PNG e JPEG (PNG é recomendado)

---

## 🎯 PRÓXIMOS PASSOS

1. Copie suas imagens para pasta `imagens/`
2. Solicite otimização aqui (use padrão de requisição acima)
3. Eu executo edit_metadata.py + verify_metadata.py
4. Quando pronto, aviso: "✅ Imagem pronta para Google Meu Negócio"
5. Você faz upload no Google Meu Negócio
6. SEO melhora em 7-14 dias

---

**Projeto criado:** 2026-05-22
**Versão:** 1.0
**Status:** ✅ Pronto para usar
