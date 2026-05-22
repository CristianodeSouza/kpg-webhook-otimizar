#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste simulando exatamente o fluxo do webhook para GCS
"""
import os
import sys
import base64
import json
from datetime import datetime
import tempfile

sys.stdout.reconfigure(encoding='utf-8')

print("\n" + "="*80)
print("TESTE LOCAL DO WEBHOOK - SIMULAR GCS UPLOAD")
print("="*80)

# 1. Carregar Base64 do arquivo
print("\n[1] Carregando Base64 do arquivo...")
with open('CREDENTIALS_B64.txt', 'r') as f:
    google_creds_b64 = f.read().strip()

print(f"    Lido: {len(google_creds_b64)} caracteres")

# 2. Decodificar (igual ao webhook)
print("\n[2] Decodificando Base64...")
try:
    google_creds_json = base64.b64decode(google_creds_b64).decode('utf-8')
    print(f"    ✓ Sucesso, JSON tem {len(google_creds_json)} caracteres")
except Exception as e:
    print(f"    ✗ ERRO: {e}")
    sys.exit(1)

# 3. Parse JSON (igual ao webhook)
print("\n[3] Fazendo parse do JSON...")
try:
    if google_creds_json.startswith('﻿'):
        google_creds_json = google_creds_json[1:]

    creds_dict = json.loads(google_creds_json)
    print(f"    ✓ JSON parseado com sucesso")
    print(f"    Project: {creds_dict.get('project_id')}")

    # Corrigir private_key
    if 'private_key' in creds_dict:
        private_key = creds_dict['private_key']
        if '\\n' in private_key:
            print(f"    ✓ Corrigindo \\n na private_key")
            creds_dict['private_key'] = private_key.replace('\\n', '\n')
except Exception as e:
    print(f"    ✗ ERRO ao parse JSON: {e}")
    sys.exit(1)

# 4. Criar credenciais (igual ao webhook)
print("\n[4] Criando Credentials do Google...")
try:
    from google.oauth2 import service_account
    from google.cloud import storage

    credentials = service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )
    print(f"    ✓ Credentials criadas com sucesso")
    print(f"    Email: {credentials.service_account_email}")
except Exception as e:
    print(f"    ✗ ERRO ao criar Credentials: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 5. Conectar ao Cloud Storage
print("\n[5] Conectando ao Cloud Storage...")
try:
    storage_client = storage.Client(
        credentials=credentials,
        project=creds_dict.get('project_id')
    )
    bucket_name = 'kpg-imagens-otimizadas'
    bucket = storage_client.bucket(bucket_name)
    print(f"    ✓ Conectado ao bucket '{bucket_name}'")
except Exception as e:
    print(f"    ✗ ERRO ao conectar GCS: {e}")
    sys.exit(1)

# 6. Criar arquivo de teste e fazer upload
print("\n[6] Testando upload de arquivo...")
try:
    # Criar arquivo de teste
    test_dir = tempfile.gettempdir()
    test_file = os.path.join(test_dir, f"teste_kpg_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(f"Teste de upload para GCS - {datetime.now().isoformat()}\n")
        f.write(f"Este arquivo foi criado em: {test_file}\n")

    print(f"    Arquivo criado: {test_file}")

    # Upload
    nome_blob = f"teste_kpg_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    blob = bucket.blob(nome_blob)

    print(f"    Enviando: {nome_blob}")
    blob.upload_from_filename(test_file, content_type='text/plain')
    print(f"    ✓ Upload concluído")

    # Tornar público
    try:
        blob.make_public()
        print(f"    ✓ Arquivo tornado público")
    except Exception as e:
        print(f"    ⚠ make_public falhou: {e}")

    # Obter URL pública
    url_publica = blob.public_url
    print(f"    ✓ URL pública: {url_publica}")

    # Limpeza
    os.remove(test_file)

except Exception as e:
    print(f"    ✗ ERRO durante upload: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*80)
print("✓ SUCESSO TOTAL - WEBHOOK FUNCIONA CORRETAMENTE COM BASE64!")
print("="*80)
print(f"\n📍 URL DE TESTE GERADA: {url_publica}")
print("\n[CONCLUSÃO]")
print("- Base64 é válido")
print("- Credenciais são criadas corretamente")
print("- Conexão ao GCS funciona")
print("- Upload funciona")
print("- URLs públicas são geradas")
print("\n[PRÓXIMO PASSO]")
print("Verificar valor exato que o Render tem em GOOGLE_CREDENTIALS_B64")
print("(Pode estar truncado ou com espaços extras)")
