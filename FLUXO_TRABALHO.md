# FLUXO DE TRABALHO - KPG IMAGEM METADADOS

---

## 🔄 Processo Completo

### ETAPA 1: RECEBER IMAGEM
```
Usuário fornece imagem (PNG ou JPEG)
↓
Salva em: C:\Users\User\KPG IMAGEM METADADOS\imagens\nome_da_imagem.png
```

**Formato esperado:**
- PNG ou JPEG
- Qualidade mínima: 1000x1000 pixels
- Nomeação clara: ex. `apartamento-gramado-001.png`

---

### ETAPA 2: SOLICITAR OTIMIZAÇÃO DE METADADOS

**Padrão de requisição do usuário:**
```
@claude: Otimize metadados desta imagem:
imagens/apartamento-gramado-001.png

Contexto:
- Tipo: Apartamento premium em Gramado
- Localização: Gramado, RS
- Características: Piscina, sala de estar, vista para montanha
- Preço: R$ 850.000
```

---

### ETAPA 3: EDITAR METADADOS NO ARQUIVO ORIGINAL

Eu vou:
1. Analisar a imagem e contexto fornecido
2. Extrair informações relevantes (tipo de imóvel, localização, características)
3. Otimizar metadados usando **TEMPLATE_METADADOS.md**
4. Executar script: `python edit_metadata.py "caminho_imagem.png"`
5. **Sobrescrever o arquivo original** com os metadados editados

**Metadados que serão otimizados:**
- Title: Título SEO otimizado
- Description: Descrição completa e detalhada
- Keywords: 15+ palavras-chave relacionadas
- Latitude/Longitude: Coordenadas exatas de Gramado/Canela
- SchemaOrg: Dados estruturados em JSON-LD para Google

---

### ETAPA 4: VERIFICAÇÃO SEGUNDA (VALIDAÇÃO)

Eu vou executar:
```bash
python verify_metadata.py "caminho_imagem.png"
```

O script vai:
1. ✅ Abrir arquivo original
2. ✅ Extrair TODOS os metadados
3. ✅ Verificar campos esperados
4. ✅ Validar se foram alterados
5. ✅ Gerar relatório completo

**Exemplo de saída:**
```
================================================================================
VERIFICACAO DE METADADOS - apartamento-gramado-001.png
================================================================================

[✓] Title: ENCONTRADO
    "Apartamento Luxo Gramado - 2 Quartos Piscina | Imóveis Premium"

[✓] Description: ENCONTRADO
    "Apartamento de luxo em Gramado com 120m², 2 quartos, piscina e vista..."

[✓] Keywords: ENCONTRADO
    "apartamento gramado, apartamento luxo gramado, imóvel gramado..."

[✓] Latitude: ENCONTRADO (-29.3796)
[✓] Longitude: ENCONTRADO (-50.8788)
[✓] Location: ENCONTRADO (Gramado, Rio Grande do Sul, Brasil)

[✓] SchemaOrg: ENCONTRADO (JSON-LD estruturado)

================================================================================
TOTAL DE METADADOS: 65 campos
STATUS: ✓ TUDO CORRETO E OTIMIZADO
================================================================================
```

---

### ETAPA 5: AUTORIZAÇÃO PARA USO

Se tudo estiver correto:
```
✅ Imagem pronta para postar no Google Meu Negócio
```

Se houver problema:
```
❌ Erro encontrado: [descrição do problema]
Vou corrigir e fazer nova verificação.
```

---

## 📋 Checklist de Verificação

Antes de avisar que está pronto, confirmo:

- [x] Arquivo original foi sobrescrito (não há -OTIMIZADA)
- [x] Todos os 65+ metadados estão presentes
- [x] Title é otimizado para SEO
- [x] Description é completa (150+ caracteres)
- [x] Keywords incluem termos principais de busca
- [x] Geolocalização (Lat/Long) está correta
- [x] SchemaOrg está formatado como JSON válido
- [x] Email, Website e Copyright estão presentes
- [x] Arquivo é PNG ou JPEG válido
- [x] Imagem está pronta para Google Meu Negócio

---

## 🎯 Otimizações Aplicadas Automaticamente

Cada imagem receberá:

1. **Otimização SEO**
   - Keywords expandidas (15+ termos)
   - Title com palavras-chave principais
   - Description com 150+ caracteres

2. **Geolocalização**
   - GPS precisos de Gramado (-29.3796, -50.8788) ou Canela
   - City, State, Country preenchidos
   - Location com informações completas

3. **Dados Estruturados**
   - SchemaOrg em JSON-LD
   - Type: RealEstateListing ou RealEstateAgent
   - Compatível com Google Rich Snippets

4. **Informações Corporativas**
   - Author: KPG Imóveis
   - Website: kpgimoveis.com.br
   - Contact: email@kpgimoveis.com.br
   - Copyright: KPG Imóveis 2026

5. **Qualidade e Padrões**
   - Version: 2.0
   - SEO.Status: Completo
   - GoogleIndex: Permitido

---

## 💾 Resultado Final

Arquivo original recebe todos os metadados e fica pronto para:
- ✅ Google Meu Negócio
- ✅ Google Images
- ✅ Google Search (Rich Snippets)
- ✅ Bing Images
- ✅ Redes sociais com metadados abertos (Open Graph)

---

## 🚨 Importante

- **NÃO** será criado arquivo com sufixo -OTIMIZADA
- **SEMPRE** editar o arquivo original
- **SEMPRE** fazer verificação segunda
- **SEMPRE** confirmar antes de usar em produção
