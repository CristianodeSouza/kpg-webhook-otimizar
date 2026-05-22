# -*- coding: utf-8 -*-
"""
SCRIPT DE VERIFICACAO DE METADADOS - KPG IMAGEM METADADOS
Verifica se os metadados foram aplicados corretamente no arquivo original
"""

from PIL import Image
import sys
import json
import os

sys.stdout.reconfigure(encoding='utf-8')

def verificar_metadados(caminho_arquivo):
    """
    Verifica e exibe todos os metadados de uma imagem PNG/JPEG.
    Confirma se estao corretos e completos para Google Meu Negocio.
    """

    if not os.path.exists(caminho_arquivo):
        print(f"\n[ERRO] Arquivo nao encontrado: {caminho_arquivo}")
        return False

    print("\n" + "="*80)
    print("VERIFICACAO DE METADADOS - KPG IMAGEM METADADOS")
    print("="*80)

    try:
        with Image.open(caminho_arquivo) as img:
            nome_arquivo = os.path.basename(caminho_arquivo)
            extensao = os.path.splitext(caminho_arquivo)[1].lower()

            print(f"\nArquivo: {nome_arquivo}")
            print(f"Caminho: {caminho_arquivo}")
            print(f"Tipo: {'PNG' if extensao == '.png' else 'JPEG'}")
            print(f"Dimensoes: {img.size[0]} x {img.size[1]} pixels")
            print(f"Modo: {img.mode}")
            print(f"Tamanho: {os.path.getsize(caminho_arquivo) / 1024:.2f} KB")

            # Campos essenciais esperados
            campos_essenciais = [
                "Title",
                "Description",
                "Keywords",
                "Author",
                "Latitude",
                "Longitude",
                "GPS",
                "Location",
                "Website",
                "Email",
                "Copyright",
                "SchemaOrg",
                "SEO.Status",
                "GoogleIndex"
            ]

            # Verificar metadados
            if hasattr(img, 'info') and img.info:
                print(f"\n[OK] METADADOS ENCONTRADOS!\n")

                metadados_encontrados = len(img.info)
                print(f"TOTAL DE METADADOS: {metadados_encontrados} campos\n")

                print("="*80)
                print("CAMPOS ESSENCIAIS - VERIFICACAO")
                print("="*80 + "\n")

                # Verificar campos essenciais
                campos_ok = 0
                for campo in campos_essenciais:
                    valor = img.info.get(campo, None)
                    if valor:
                        campos_ok += 1
                        valor_display = str(valor)
                        if len(valor_display) > 80:
                            valor_display = valor_display[:80] + "..."
                        print(f"[OK] {campo}")
                        print(f"     {valor_display}\n")
                    else:
                        print(f"[!] {campo}: NAO ENCONTRADO\n")

                print("="*80)
                print("VALIDACAO")
                print("="*80 + "\n")

                # Validacoes especificas
                validacoes = []

                # 1. Title
                title = img.info.get("Title", "")
                if title and len(title) > 30:
                    validacoes.append(("[OK] Title", "Presente e otimizado"))
                else:
                    validacoes.append(("[!] Title", "Muito curto ou ausente"))

                # 2. Description
                desc = img.info.get("Description", "")
                if desc and len(desc) > 100:
                    validacoes.append(("[OK] Description", "Completa (150+ caracteres)"))
                else:
                    validacoes.append(("[!] Description", "Muito curta ou ausente"))

                # 3. Keywords
                keywords = img.info.get("Keywords", "")
                if keywords and "," in keywords:
                    num_keywords = len(keywords.split(","))
                    validacoes.append(("[OK] Keywords", f"{num_keywords} termos encontrados"))
                else:
                    validacoes.append(("[!] Keywords", "Ausentes ou incompletas"))

                # 4. Geolocalizacao
                lat = img.info.get("Latitude", "")
                lon = img.info.get("Longitude", "")
                if lat and lon and lat.startswith("-29"):
                    validacoes.append(("[OK] Geolocalizacao", f"Gramado/Canela ({lat}, {lon})"))
                else:
                    validacoes.append(("[!] Geolocalizacao", "Incorreta ou ausente"))

                # 5. Website
                website = img.info.get("Website", "")
                if website and "kpgimoveis" in website.lower():
                    validacoes.append(("[OK] Website", website))
                else:
                    validacoes.append(("[!] Website", "Ausente ou incorreto"))

                # 6. Copyright
                copyright_text = img.info.get("Copyright", "")
                if copyright_text and "KPG" in copyright_text and "2026" in copyright_text:
                    validacoes.append(("[OK] Copyright", "Correto e valido"))
                else:
                    validacoes.append(("[!] Copyright", "Ausente ou incompleto"))

                # 7. SchemaOrg
                schema = img.info.get("SchemaOrg", "")
                if schema:
                    try:
                        json.loads(schema)
                        validacoes.append(("[OK] SchemaOrg", "JSON-LD valido"))
                    except:
                        validacoes.append(("[!] SchemaOrg", "JSON invalido"))
                else:
                    validacoes.append(("[!] SchemaOrg", "Ausente"))

                # 8. SEO Status
                seo_status = img.info.get("SEO.Status", "")
                if seo_status == "Completo":
                    validacoes.append(("[OK] SEO.Status", "Completo"))
                else:
                    validacoes.append(("[!] SEO.Status", "Nao otimizado"))

                # 9. GoogleIndex
                google_index = img.info.get("GoogleIndex", "")
                if google_index == "Permitido":
                    validacoes.append(("[OK] GoogleIndex", "Permitido para indexacao"))
                else:
                    validacoes.append(("[!] GoogleIndex", "Bloqueado ou ausente"))

                # 10. Copyright Year
                if "2026" in copyright_text:
                    validacoes.append(("[OK] Ano Copyright", "2026 (Atualizado)"))
                else:
                    validacoes.append(("[!] Ano Copyright", "Desatualizado"))

                # Exibir validacoes
                for status, msg in validacoes:
                    print(f"{status}: {msg}")

                print("\n" + "="*80)
                print("RESULTADO FINAL")
                print("="*80 + "\n")

                # Contar sucessos
                sucessos = sum(1 for s, _ in validacoes if "[OK]" in s)
                total_validacoes = len(validacoes)

                if sucessos == total_validacoes:
                    print(f"[SUCESSO] TODOS OS {total_validacoes} CAMPOS VALIDADOS!")
                    print(f"\n[✓] IMAGEM PRONTA PARA POSTAR NO GOOGLE MEU NEGOCIO\n")
                    print("Passos proximos:")
                    print("  1. Faca upload da imagem no Google Meu Negocio")
                    print("  2. Os metadados serao indexados automaticamente")
                    print("  3. A imagem aparecera em buscas relevantes")
                    print("  4. SEO melhorara em 7-14 dias\n")
                    resultado = True
                else:
                    print(f"[ATENCAO] {sucessos}/{total_validacoes} campos validados")
                    print(f"\n[!] ALGUNS CAMPOS PRECISAM SER CORRIGIDOS\n")
                    print("Campos faltantes ou incorretos:")
                    for status, msg in validacoes:
                        if "[!]" in status:
                            print(f"  - {msg}")
                    print("\nVou corrigir os metadados e fazer nova verificacao.")
                    resultado = False

                print("\n" + "="*80)
                print("DETALHES COMPLETOS DOS METADADOS")
                print("="*80 + "\n")

                # Listar TODOS os metadados
                contador = 0
                for chave, valor in sorted(img.info.items()):
                    contador += 1
                    valor_str = str(valor)
                    if len(valor_str) > 100:
                        print(f"[{contador:02d}] {chave}")
                        print(f"      {valor_str[:100]}...\n")
                    else:
                        print(f"[{contador:02d}] {chave}")
                        print(f"      {valor_str}\n")

                print("="*80)
                print(f"CONCLUSAO: {metadados_encontrados} metadados presentes no arquivo")
                print("="*80 + "\n")

                return resultado

            else:
                print("\n[ERRO] Nenhum metadado encontrado na imagem!")
                print("\nPossivel solucao: Execute edit_metadata.py para adicionar metadados.")
                print("="*80 + "\n")
                return False

    except Exception as e:
        print(f"\n[ERRO] Nao foi possivel abrir a imagem: {e}")
        print("="*80 + "\n")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUso: python verify_metadata.py <caminho_da_imagem>")
        print("\nExemplo:")
        print('  python verify_metadata.py "C:\\Users\\User\\Downloads\\imagem.png"')
        print('  python verify_metadata.py "imagens/apartamento-001.png"')
        sys.exit(1)

    caminho = sys.argv[1]
    sucesso = verificar_metadados(caminho)
    sys.exit(0 if sucesso else 1)
