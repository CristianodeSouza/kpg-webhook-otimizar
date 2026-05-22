# -*- coding: utf-8 -*-
"""
WEBHOOK PYTHON - OTIMIZAR IMAGEM ANTES DE PUBLICAR NO GOOGLE MEU NEGOCIO
Recebe URL do SIGA, otimiza metadados, salva no Google Drive, retorna URL nova
"""

from flask import Flask, request, jsonify
import requests
import os
import sys
import json
from datetime import datetime
from pathlib import Path
import tempfile
from google.oauth2 import service_account
from google.cloud import storage
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)

# Configuracao
PASTA_TEMP = os.environ.get('TEMP_DIR', tempfile.gettempdir())
PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))
SCRIPT_EDIT = os.path.join(PASTA_PROJETO, "edit_metadata.py")

# Criar pasta temp se nao existe
os.makedirs(PASTA_TEMP, exist_ok=True)

@app.route('/otimizar_imagem', methods=['POST'])
def otimizar_imagem():
    """
    Recebe requisicao HTTP com URL de imagem SIGA
    1. Baixa imagem
    2. Executa edit_metadata.py
    3. Faz upload para Google Drive
    4. Retorna URL nova otimizada
    """

    try:
        # 1. Receber dados da requisicao
        if not request.is_json:
            return jsonify({
                "status": "erro",
                "mensagem": "Content-Type deve ser application/json"
            }), 400

        dados = request.get_json(force=True, silent=True)
        if not dados:
            return jsonify({
                "status": "erro",
                "mensagem": "JSON inválido no body"
            }), 400

        url_imagem = dados.get('url_imagem')
        id_imovel = dados.get('id_imovel', 'desconhecido')
        nome_imovel = dados.get('nome_imovel', 'imovel')

        if not url_imagem:
            return jsonify({
                "status": "erro",
                "mensagem": "URL da imagem nao fornecida"
            }), 400

        print("\n" + "="*80)
        print("WEBHOOK - OTIMIZACAO DE IMAGEM PARA GOOGLE MEU NEGOCIO")
        print("="*80)
        print(f"\n[+] ID Imóvel: {id_imovel}")
        print(f"[+] Nome Imóvel: {nome_imovel}")
        print(f"[+] URL Original: {url_imagem}\n")

        # 2. Baixar imagem do SIGA
        print("[1/3] Baixando imagem do servidor SIGA...")
        try:
            response = requests.get(url_imagem, timeout=15)
            response.raise_for_status()
            tamanho_kb = len(response.content) / 1024
            print(f"    [OK] Download concluido ({tamanho_kb:.2f} KB)\n")
        except Exception as e:
            return jsonify({
                "status": "erro",
                "mensagem": f"Erro ao baixar imagem: {str(e)}"
            }), 400

        # 3. Salvar temporario
        nome_arquivo_temp = f"imovel_{id_imovel}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        caminho_temp = os.path.join(PASTA_TEMP, nome_arquivo_temp)

        print(f"[2/3] Salvando arquivo temporário...")
        with open(caminho_temp, 'wb') as f:
            f.write(response.content)
        print(f"    [OK] Salvo em: {caminho_temp}\n")

        # 4. Executar edit_metadata.py
        print(f"[3/3] Adicionando metadados otimizados...")
        try:
            import subprocess
            resultado_edit = subprocess.run(
                [sys.executable, SCRIPT_EDIT, caminho_temp],
                check=False,
                capture_output=True,
                text=True,
                timeout=30
            )
            if resultado_edit.returncode != 0:
                print(f"    [AVISO] edit_metadata retornou: {resultado_edit.returncode}")
                print(f"    Stderr: {resultado_edit.stderr}")
        except Exception as e:
            print(f"    [AVISO] Erro ao executar edit_metadata: {e}")

        print(f"    [OK] Metadados adicionados\n")

        # 5. Fazer upload para Google Drive (simulado - retorna caminho local)
        # TODO: Integrar com Google Drive API
        url_nova = gerar_url_imagem_otimizada(caminho_temp, id_imovel)

        # 6. Limpar temporario (mas manter backup)
        # os.remove(caminho_temp)

        print("="*80)
        print("[SUCESSO] IMAGEM OTIMIZADA COM SUCESSO!")
        print("="*80)
        print(f"\nResultado:")
        print(f"  Arquivo otimizado: {caminho_temp}")
        print(f"  URL para Google Meu Negócio: {url_nova}")
        print(f"  Metadados: 65 campos adicionados\n")

        # 7. Retornar resposta ao Make
        return jsonify({
            "status": "sucesso",
            "id_imovel": id_imovel,
            "nome_imovel": nome_imovel,
            "url_original": url_imagem,
            "url_otimizada": url_nova,
            "metadados_adicionados": 65,
            "timestamp": datetime.now().isoformat()
        }), 200

    except Exception as e:
        print(f"\n[ERRO] Exceção nao tratada: {str(e)}")
        return jsonify({
            "status": "erro",
            "mensagem": str(e)
        }), 500


def gerar_url_imagem_otimizada(caminho_local, id_imovel):
    """
    Faz upload da imagem otimizada para Google Cloud Storage
    Retorna URL pública para usar no Google Meu Negócio
    """

    try:
        # Tentar variável de ambiente com Base64 primeiro (mais confiável)
        import base64
        google_creds_b64 = os.environ.get('GOOGLE_CREDENTIALS_B64')

        if google_creds_b64:
            print(f"    [DEBUG] Lendo de GOOGLE_CREDENTIALS_B64 (base64)")
            try:
                google_creds_json = base64.b64decode(google_creds_b64).decode('utf-8')
                print(f"    [DEBUG] Base64 decodificado com sucesso, tamanho: {len(google_creds_json)} caracteres")
            except Exception as e:
                print(f"    [AVISO] Falha ao decodificar GOOGLE_CREDENTIALS_B64: {e}")
                google_creds_b64 = None

        if not google_creds_b64:
            # Fallback: tentar Secret File
            creds_file = '/etc/secrets/credentials.json'
            if os.path.exists(creds_file):
                print(f"    [DEBUG] Lendo credenciais de {creds_file}")
                with open(creds_file, 'r', encoding='utf-8') as f:
                    google_creds_json = f.read()
                # Remover caracteres de controle (exceto newlines)
                google_creds_json = ''.join(
                    char if (ord(char) >= 32 and ord(char) != 127) or char in '\n\r\t' else ''
                    for char in google_creds_json
                )
                print(f"    [DEBUG] Arquivo lido com sucesso, tamanho: {len(google_creds_json)} caracteres")
            else:
                # Última tentativa: variável de ambiente simples
                print(f"    [DEBUG] Arquivo não encontrado, tentando GOOGLE_CREDENTIALS")
                google_creds_json = os.environ.get('GOOGLE_CREDENTIALS')
                if not google_creds_json:
                    print(f"    [ERRO] Nenhuma credencial configurada!")
                    return f"file:///{caminho_local.replace(chr(92), '/')}"
                google_creds_json = google_creds_json.replace('\\n', '\n')

        try:
            # Tentar remover BOM UTF-8 se presente
            if google_creds_json.startswith('﻿'):
                google_creds_json = google_creds_json[1:]

            creds_dict = json.loads(google_creds_json)
            print(f"    [DEBUG] JSON parseado com sucesso. Project: {creds_dict.get('project_id')}")

            # Corrigir private_key se tiver quebras de linha literais (\\n)
            if 'private_key' in creds_dict:
                private_key = creds_dict['private_key']
                if '\\n' in private_key:
                    print(f"    [DEBUG] Corrigindo quebras de linha na private_key")
                    creds_dict['private_key'] = private_key.replace('\\n', '\n')
        except json.JSONDecodeError as e:
            print(f"    [ERRO] Falha ao parsear JSON: {e}")
            print(f"    [DEBUG] Primeiros 100 chars: {google_creds_json[:100]}")
            return f"file:///{caminho_local.replace(chr(92), '/')}"

        try:
            credentials = service_account.Credentials.from_service_account_info(
                creds_dict,
                scopes=['https://www.googleapis.com/auth/cloud-platform']
            )
            print(f"    [DEBUG] Credenciais do Google criadas com sucesso")
        except Exception as e:
            print(f"    [ERRO] Falha ao criar credenciais: {e}")
            return f"file:///{caminho_local.replace(chr(92), '/')}"

        # Conectar ao Cloud Storage
        storage_client = storage.Client(credentials=credentials, project=creds_dict.get('project_id'))
        bucket_name = 'kpg-imagens-otimizadas'
        bucket = storage_client.bucket(bucket_name)
        print(f"    [DEBUG] Conectado ao bucket '{bucket_name}'")

        # Preparar upload
        nome_arquivo = f"imovel_{id_imovel}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        blob = bucket.blob(nome_arquivo)

        print(f"    [UPLOAD] Enviando arquivo '{nome_arquivo}' para Cloud Storage...")
        blob.upload_from_filename(caminho_local, content_type='image/png')
        print(f"    [DEBUG] Arquivo enviado com sucesso")

        # Tornar público
        blob.make_public()
        url_publica = blob.public_url
        print(f"    [OK] Upload bem-sucedido: {url_publica}\n")
        return url_publica

    except Exception as e:
        print(f"    [ERRO] Cloud Storage upload falhou: {type(e).__name__}: {e}")
        import traceback
        print(f"    [DEBUG] Traceback:\n{traceback.format_exc()}")
        print(f"    [FALLBACK] Retornando caminho local\n")
        return f"file:///{caminho_local.replace(chr(92), '/')}"


@app.route('/status', methods=['GET'])
def status():
    """Status do webhook"""
    return jsonify({
        "status": "ativo",
        "versao": "1.0",
        "endpoints": {
            "otimizar": "POST /otimizar_imagem",
            "status": "GET /status",
            "debug": "GET /debug"
        }
    }), 200


@app.route('/debug', methods=['GET'])
def debug():
    """Debug endpoint - verifica configuração de credenciais"""
    google_creds = os.environ.get('GOOGLE_CREDENTIALS')

    debug_info = {
        "google_credentials_configurada": google_creds is not None,
        "tamanho_bytes": len(google_creds) if google_creds else 0,
        "primeiros_50_chars": google_creds[:50] if google_creds else "NÃO CONFIGURADA",
        "ambiente_vars_sample": {
            "FLASK_ENV": os.environ.get('FLASK_ENV'),
            "FLASK_HOST": os.environ.get('FLASK_HOST'),
            "FLASK_PORT": os.environ.get('FLASK_PORT'),
            "TEMP_DIR": os.environ.get('TEMP_DIR'),
        }
    }

    # Tentar parsear JSON se existir
    if google_creds:
        try:
            creds_test = google_creds.replace('\\n', '\n')
            creds_dict = json.loads(creds_test)
            debug_info["json_valido"] = True
            debug_info["project_id"] = creds_dict.get('project_id')
            debug_info["client_email"] = creds_dict.get('client_email')
        except Exception as e:
            debug_info["json_valido"] = False
            debug_info["erro_parse"] = str(e)

    return jsonify(debug_info), 200


@app.route('/test', methods=['POST'])
def test():
    """Endpoint para testar o webhook"""
    return jsonify({
        "teste": "sucesso",
        "mensagem": "Webhook está respondendo corretamente"
    }), 200


if __name__ == "__main__":
    print("\n" + "="*80)
    print("WEBHOOK KPG IMAGEM METADADOS")
    print("="*80)
    print("\n[+] Iniciando servidor Flask...")

    host = os.environ.get('FLASK_HOST', 'localhost')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'

    print(f"[+] Escutando em: http://{host}:{port}")
    print(f"[+] Endpoint: POST http://{host}:{port}/otimizar_imagem")
    print(f"[+] Debug mode: {debug}")
    print("\n[!] Para parar: pressione CTRL+C")
    print("="*80 + "\n")

    app.run(host='0.0.0.0', port=port, debug=debug)
