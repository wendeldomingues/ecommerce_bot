from cryptography.fernet import Fernet
import json
from pathlib import Path

def carregar_credenciais():
    config_dir = Path(__file__).parent.parent / "config"

    key_path = config_dir / "key.key"
    cred_path = config_dir / "credenciais.enc"

    if not key_path.exists() or not cred_path.exists():
        raise FileNotFoundError("Arquivos de credenciais não encontrados!")

    with open(key_path, "rb") as f:
        key = f.read()

    cipher = Fernet(key)

    with open(cred_path, "rb") as f:
        dados_criptografados = f.read()

    dados_json = cipher.decrypt(dados_criptografados)
    dados = json.loads(dados_json.decode())

    return dados["usuario"], dados["senha"]
