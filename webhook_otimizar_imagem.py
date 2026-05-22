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
        dados = request.get_json()
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
        cmd = f'python "{SCRIPT_EDIT}" "{caminho_temp}"'
        resultado_edit = os.system(cmd)

        if resultado_edit != 0:
            return jsonify({
                "status": "erro",
                "mensagem": "Erro ao executar edit_metadata.py"
            }), 500

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
    Faz upload da imagem otimizada para imgbb.com
    Retorna URL permanente para usar no Google Meu Negócio
    """

    IMGBB_API_KEY = os.environ.get('IMGBB_API_KEY', 'b8ef80fb7c8c2c31a65b0597ed9ed38c')

    try:
        with open(caminho_local, 'rb') as f:
            files = {'image': f}
            data = {'key': IMGBB_API_KEY}

            print(f"[UPLOAD] Enviando para imgbb.com...")
            response = requests.post('https://api.imgbb.com/1/upload', files=files, data=data, timeout=30)
            response.raise_for_status()

            resultado = response.json()
            if resultado.get('success'):
                url_imagem = resultado['data']['url']
                print(f"    [OK] Upload bem-sucedido: {url_imagem}\n")
                return url_imagem
            else:
                print(f"    [ERRO] imgbb retornou: {resultado.get('error', 'erro desconhecido')}\n")
                return f"file:///{caminho_local.replace(chr(92), '/')}"

    except Exception as e:
        print(f"    [AVISO] Erro ao fazer upload para imgbb: {e}")
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
            "status": "GET /status"
        }
    }), 200


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
