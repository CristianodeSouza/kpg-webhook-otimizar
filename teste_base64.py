#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Ler Base64 do arquivo
with open('CREDENTIALS_B64.txt', 'r') as f:
    b64_content = f.read().strip()

print(f"[1] Tamanho do Base64: {len(b64_content)} caracteres")
print(f"[2] Começa com: {b64_content[:50]}...")
print(f"[3] Termina com: ...{b64_content[-20:]}")
print()

# Testar decodificação Base64
try:
    json_str = base64.b64decode(b64_content).decode('utf-8')
    print(f"✓ Base64 decodificado com sucesso")
    print(f"  JSON tem {len(json_str)} caracteres")
except Exception as e:
    print(f"✗ Erro ao decodificar Base64: {e}")
    sys.exit(1)

print()

# Testar JSON parse
try:
    creds_dict = json.loads(json_str)
    print(f"✓ JSON parseado com sucesso")
    print(f"  Project: {creds_dict.get('project_id')}")
    print(f"  Email: {creds_dict.get('client_email')}")
except Exception as e:
    print(f"✗ Erro ao fazer parse JSON: {e}")
    sys.exit(1)

print()

# Verificar private_key
private_key = creds_dict.get('private_key', '')
print(f"[4] private_key tem {len(private_key)} caracteres")
print(f"    Começa: {private_key[:50]}...")
print(f"    Termina: ...{private_key[-50:]}")
print()

# Verificar \\n literal
if '\\n' in private_key:
    print(f"[AVISO] Encontrado \\\\n literal na private_key")
    print(f"[AVISO] Substituindo por quebra de linha real...")
    creds_dict['private_key'] = private_key.replace('\\n', '\n')
    private_key = creds_dict['private_key']
    print(f"✓ private_key corrigida, agora tem {len(private_key)} caracteres")

print()

# Tentar criar credenciais
print("[5] Tentando criar Credentials...")
try:
    from google.oauth2 import service_account

    credentials = service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )
    print(f"✓ Credentials criadas com sucesso!")
    print(f"  Service Account Email: {credentials.service_account_email}")
    print(f"  Project ID: {credentials.project_id}")
except Exception as e:
    print(f"✗ Erro ao criar Credentials: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 80)
print("✓ TODOS OS TESTES PASSARAM - Base64 está válido!")
print("=" * 80)
