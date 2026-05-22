# -*- coding: utf-8 -*-
"""
ANALISE DE METADADOS - IMAGEM DO CRM SIGA
Baixa imagem do servidor SIGA e analisa todos os metadados presentes
"""

from PIL import Image
import sys
import requests
import json
from io import BytesIO

sys.stdout.reconfigure(encoding='utf-8')

def analisar_metadados_crm(url_imagem):
    """
    Baixa imagem de URL e analisa todos os metadados presentes
    """

    print("\n" + "="*80)
    print("ANALISE DE METADADOS - IMAGEM DO CRM SIGA")
    print("="*80 + "\n")

    print(f"[+] URL: {url_imagem}")
    print("[+] Baixando imagem do servidor...\n")

    try:
        # Baixar imagem
        response = requests.get(url_imagem, timeout=10)
        response.raise_for_status()

        print(f"[OK] Download concluido ({len(response.content) / 1024:.2f} KB)\n")

        # Abrir imagem
        img = Image.open(BytesIO(response.content))

        print(f"[+] Dimensoes: {img.size[0]} x {img.size[1]} pixels")
        print(f"[+] Formato: {img.format}")
        print(f"[+] Modo: {img.mode}\n")

        # Analisar EXIF
        print("="*80)
        print("METADADOS EXIF")
        print("="*80 + "\n")

        exif_data = None
        if hasattr(img, 'getexif'):
            try:
                exif_data = img.getexif()
                if exif_data:
                    print(f"[OK] {len(exif_data)} tags EXIF encontradas:\n")
                    for tag_id, valor in sorted(exif_data.items()):
                        valor_str = str(valor)
                        if len(valor_str) > 80:
                            print(f"  Tag {tag_id}: {valor_str[:80]}...")
                        else:
                            print(f"  Tag {tag_id}: {valor_str}")
                else:
                    print("[!] Nenhum dado EXIF encontrado\n")
            except Exception as e:
                print(f"[!] Erro ao ler EXIF: {e}\n")

        # Analisar Info (metadados PNG/outros)
        print("\n" + "="*80)
        print("METADADOS PNG INFO (Text Chunks)")
        print("="*80 + "\n")

        if hasattr(img, 'info') and img.info:
            print(f"[OK] {len(img.info)} campos de metadados encontrados:\n")
            for chave, valor in sorted(img.info.items()):
                valor_str = str(valor)
                if len(valor_str) > 80:
                    print(f"  {chave}: {valor_str[:80]}...")
                else:
                    print(f"  {chave}: {valor_str}")
        else:
            print("[!] Nenhum metadado PNG customizado encontrado\n")

        # Analisar IFD (JPEG specific)
        print("\n" + "="*80)
        print("METADADOS IPTC/IFD DETALHADOS")
        print("="*80 + "\n")

        if hasattr(img, 'tag_v2'):
            print("[OK] Dados IFD encontrados:")
            for tag, valor in sorted(img.tag_v2.items()):
                print(f"  Tag {tag}: {valor}")
        else:
            print("[!] Nenhum dado IFD encontrado\n")

        # RESUMO
        print("\n" + "="*80)
        print("RESUMO DE METADADOS PRESENTES")
        print("="*80 + "\n")

        total_metadados = 0
        if exif_data:
            total_metadados += len(exif_data)
        if hasattr(img, 'info') and img.info:
            total_metadados += len(img.info)

        print(f"TOTAL DE METADADOS ENCONTRADOS: {total_metadados} campos\n")

        if total_metadados == 0:
            print("[!] NENHUM METADADO ENCONTRADO NA IMAGEM DO CRM SIGA")
            print("\nIsso significa:")
            print("  • A imagem vem SEM metadados customizados")
            print("  • O CRM SIGA nao adiciona metadados automaticamente")
            print("  • Metadados precisam ser ADICIONADOS no Make ou aqui")
            print("  • Use nosso projeto KPG IMAGEM METADADOS para otimizar\n")
        else:
            print("[OK] A imagem contem metadados nativos (EXIF/IFD)")
            print("\nIsso significa:")
            print("  • A imagem tem dados basicos de câmera/data")
            print("  • MAS faltam metadados otimizados para SEO")
            print("  • Recomendado: Adicionar 65+ metadados no projeto\n")

        # Salvar relatorio
        relatorio = {
            "url": url_imagem,
            "dimensoes": f"{img.size[0]}x{img.size[1]}",
            "formato": img.format,
            "modo_cor": img.mode,
            "total_metadados": total_metadados,
            "exif_presente": bool(exif_data),
            "info_png_presente": bool(hasattr(img, 'info') and img.info),
        }

        if exif_data:
            relatorio["exif_tags"] = {str(k): str(v)[:100] for k, v in exif_data.items()}
        if hasattr(img, 'info') and img.info:
            relatorio["info_campos"] = {k: str(v)[:100] for k, v in img.info.items()}

        print("="*80)
        print("RELATORIO EM JSON")
        print("="*80 + "\n")
        print(json.dumps(relatorio, indent=2, ensure_ascii=False))
        print("\n" + "="*80)

        return relatorio

    except requests.exceptions.RequestException as e:
        print(f"\n[ERRO] Nao foi possivel baixar a imagem: {e}")
        print("Verifique:")
        print("  • URL esta correta?")
        print("  • Voce tem acesso ao servidor?")
        print("  • Link esta vivo?")
        return None
    except Exception as e:
        print(f"\n[ERRO] Erro ao analisar imagem: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUso: python analisar_metadados_crm_siga.py <URL_da_imagem>")
        print("\nExemplo:")
        print('  python analisar_metadados_crm_siga.py "https://cdn.mizia.com.br/kpg/img_vendas/g1_2499_33231_1558_200526.jpeg"')
        sys.exit(1)

    url = sys.argv[1]
    analisar_metadados_crm(url)
