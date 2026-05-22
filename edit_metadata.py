# -*- coding: utf-8 -*-
"""
SCRIPT DE EDICAO DE METADADOS - KPG IMAGEM METADADOS
Edita metadados de imagem PNG/JPEG e sobrescreve arquivo original
"""

from PIL import Image
from PIL.PngImagePlugin import PngInfo
from datetime import datetime
import sys
import json
import os

sys.stdout.reconfigure(encoding='utf-8')

def editar_metadados_imagem(caminho_arquivo, metadados_customizados=None):
    """
    Edita metadados de uma imagem PNG/JPEG e sobrescreve o arquivo original.

    Args:
        caminho_arquivo: Caminho completo da imagem
        metadados_customizados: Dicionário com metadados personalizados (opcional)
    """

    if not os.path.exists(caminho_arquivo):
        print(f"\n[ERRO] Arquivo nao encontrado: {caminho_arquivo}")
        return False

    print("\n" + "="*80)
    print("EDICAO DE METADADOS - KPG IMAGEM METADADOS")
    print("="*80 + "\n")

    # Determinar se é PNG ou JPEG
    extensao = os.path.splitext(caminho_arquivo)[1].lower()
    is_png = extensao == '.png'

    print(f"[+] Abrindo arquivo: {os.path.basename(caminho_arquivo)}")
    print(f"[+] Tipo: {'PNG' if is_png else 'JPEG'}")

    # Carregar imagem original
    img = Image.open(caminho_arquivo)
    img_copy = img.copy()

    print(f"[+] Dimensoes: {img.size[0]} x {img.size[1]} pixels")
    print(f"[+] Modo de cor: {img.mode}\n")

    # Metadados padrao (BASE)
    metadados_base = {
        "Title": "Imovel em Gramado e Canela - KPG Imoveis",
        "Description": "Propriedade imobiliaria especializada em compra, venda e locacao em Gramado e Canela. Imobiliaria profissional com consultoria completa.",
        "Author": "KPG Imoveis",
        "Creator": "KPG Imoveis Marketing",
        "Producer": "KPG Imoveis - Marketing Digital Professional",
        "Copyright": "Copyright (c) 2026 KPG Imoveis. Todos os direitos reservados.",
        "Rights": "Propriedade intelectual de KPG Imoveis",
        "Software": "KPG Imoveis SEO Optimization Engine v2.0",
        "Latitude": "-29.3796",
        "Longitude": "-50.8788",
        "Location": "Gramado, Rio Grande do Sul, Brasil",
        "City": "Gramado",
        "Municipality": "Gramado",
        "State": "Rio Grande do Sul",
        "StateAbbr": "RS",
        "Country": "Brasil",
        "CountryCode": "BR",
        "Region": "Serra Gaucha",
        "GeographicArea": "Sul do Brasil",
        "GPS": "-29.3796,-50.8788",
        "GPSMapDatum": "WGS-84",
        "Altitude": "800-1200",
        "LocaleName": "Gramado",
        "LocaleID": "gramado_rs_br",
        "Keywords": "imobiliaria gramado, imobiliaria canela, apartamentos gramado, casas canela, imoveis serra gaucha, investimento imobiliario gramado, kpg imoveis, imobiliaria gramado rs, imoveis canela rs, propriedades gramado, consultoria imobiliaria, compra venda imoveis, locacao imoveis, imobiliaria profissional",
        "Subject": "Imoveis | Imobiliaria | Consultoria Imobiliaria | Compra Venda Locacao",
        "Category": "Real Estate | Imobiliaria | Propriedades",
        "Type": "RealEstateListing | ResidentialProperty",
        "Genre": "Comercial | Negocio | Imobiliario",
        "Comment": "Imagem otimizada para indexacao em Google Images e Google Meu Negocio",
        "URL": "https://www.kpgimoveis.com.br",
        "Website": "kpgimoveis.com.br",
        "Website.pt": "www.kpgimoveis.com.br",
        "Contact": "contato@kpgimoveis.com.br",
        "Email": "kpgimoveis@email.com",
        "ContactType": "Business",
        "BusinessType": "RealEstateAgency",
        "Organization": "KPG Imoveis Ltda",
        "CompanyName": "KPG Imoveis",
        "Content.Type": "Marketing Image - Real Estate",
        "Content.Topic": "Imoveis Gramado Canela",
        "Content.Purpose": "SEO Optimization for Google Images",
        "Content.Language": "pt-BR",
        "Language": "Portuguese",
        "LanguageCode": "pt",
        "ImageQuality": "Professional",
        "ImageWidth": str(img.size[0]),
        "ImageHeight": str(img.size[1]),
        "Dimensions": f"{img.size[0]}x{img.size[1]}",
        "AspectRatio": f"{img.size[0]}:{img.size[1]}",
        "Resolution": "96 DPI",
        "ResolutionDPI": "96",
        "ColorMode": img.mode,
        "ColorDepth": "24-bit" if img.mode == "RGB" else "8-bit",
        "CreationTime": datetime.now().isoformat(),
        "DateCreated": datetime.now().strftime("%Y-%m-%d"),
        "DateModified": datetime.now().strftime("%Y-%m-%d"),
        "Version": "2.0",
        "Revision": "SEO-Optimized",
        "Source": "KPG Imoveis Marketing Department",
        "SourceWebsite": "https://www.kpgimoveis.com.br",
        "SourceApp": "KPG Imoveis Content Creator",
        "SourceType": "Professional Marketing Material",
        "Distribution": "Web | Google Images | Google Meu Negocio",
        "Usage": "Commercial - Website and Marketing",
        "License": "Copyright License - KPG Imoveis",
        "Attribution": "KPG Imoveis Gramado",
        "SearchEngine.Google": "Otimizado para indexacao em Google Images e Google Search",
        "SearchEngine.Bing": "Compativel com Bing Images",
        "SearchEngine.Yandex": "Otimizado para Yandex Images",
        "SEO.Status": "Completo",
        "SEO.Priority": "Alta",
        "SEO.Importance": "Critica para visibilidade online",
        "SearchEngineOptimization": "Otimizado para Google Images, Google Search, Bing, Yandex, Google Meu Negocio",
        "GoogleIndex": "Permitido",
        "RobotsIndex": "index, follow",
    }

    # Sobrescrever com customizacoes se fornecidas
    if metadados_customizados:
        metadados_base.update(metadados_customizados)

    # Gerar dados estruturados SchemaOrg
    schema_data = {
        "@context": "https://schema.org",
        "@type": "RealEstateListing",
        "name": metadados_base.get("Title", "Imovel em Gramado"),
        "description": metadados_base.get("Description", ""),
        "url": metadados_base.get("URL", "https://www.kpgimoveis.com.br"),
        "image": "https://www.kpgimoveis.com.br/images/propriedade.png",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Gramado",
            "addressRegion": "Rio Grande do Sul",
            "addressCountry": "BR"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": "-29.3796",
            "longitude": "-50.8788"
        },
        "agent": {
            "@type": "RealEstateAgent",
            "name": "KPG Imoveis",
            "url": "https://www.kpgimoveis.com.br"
        },
        "areaServed": ["Gramado", "Canela", "Serra Gaucha"]
    }

    metadados_base["SchemaOrg"] = json.dumps(schema_data, ensure_ascii=False)

    print(f"[+] Adicionando {len(metadados_base)} metadados otimizados para SEO...\n")

    # Aplicar metadados conforme tipo de arquivo
    if is_png:
        pnginfo = PngInfo()
        for chave, valor in metadados_base.items():
            pnginfo.add_text(chave, str(valor))

        # Salvar PNG com metadados (sobrescrever original)
        img_copy.save(caminho_arquivo, "PNG", pnginfo=pnginfo)
    else:
        # JPEG nao suporta metadados customizados de forma nativa
        # Salvar apenas para manter compatibilidade
        img_copy.save(caminho_arquivo, "JPEG", quality=95)
        print("[!] Aviso: JPEG nao suporta metadados PNG. Use PNG para maximo suporte.")

    print("="*80)
    print("[SUCESSO] METADADOS ADICIONADOS COM SUCESSO!")
    print("="*80)
    print(f"\nArquivo: {os.path.basename(caminho_arquivo)}")
    print(f"Caminho: {caminho_arquivo}")
    print(f"Tamanho: {os.path.getsize(caminho_arquivo) / 1024:.2f} KB")
    print(f"\nMetadados adicionados: {len(metadados_base)} campos")
    print(f"\nCategories:")
    print(f"  [+] Basicos (Title, Description, Author)")
    print(f"  [+] Geolocalizacao (Latitude, Longitude, GPS)")
    print(f"  [+] SEO (Keywords, Subject, Category)")
    print(f"  [+] Contato (Website, Email, Organization)")
    print(f"  [+] Dados Estruturados (SchemaOrg JSON-LD)")
    print(f"  [+] Otimizacao (Google, Bing, Yandex)")
    print(f"\nProximo passo: Execute verify_metadata.py para confirmar!")
    print("="*80 + "\n")

    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUso: python edit_metadata.py <caminho_da_imagem>")
        print("\nExemplo:")
        print('  python edit_metadata.py "C:\\Users\\User\\Downloads\\imagem.png"')
        print('  python edit_metadata.py "imagens/apartamento-001.png"')
        sys.exit(1)

    caminho = sys.argv[1]

    # Opcional: metadados customizados como argumentos
    metadados_custom = {}
    if len(sys.argv) > 2:
        # Exemplo: --title "Meu Titulo" --description "Minha descricao"
        for i in range(2, len(sys.argv), 2):
            if i+1 < len(sys.argv):
                chave = sys.argv[i].replace("--", "")
                valor = sys.argv[i+1]
                metadados_custom[chave] = valor

    editar_metadados_imagem(caminho, metadados_custom)
