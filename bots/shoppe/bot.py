from pathlib import Path
import sys
import json
import time

# -----------------------------------
# Função de Login
# -----------------------------------
def login(nav, usuario, senha):
    """
    Realiza login na Shopee com verificações mais robustas.
    """

    # Preencher username
    if not nav.escrever("//input[@placeholder='Número de telefone/Nome do usuário/Email']", usuario):
        print("Campo de usuário não encontrado.")
        return False
    time.sleep(1)

    # Preencher senha
    if not nav.escrever("//input[@placeholder='Senha']", senha):
        print("Campo de senha não encontrado.")
        return False
    time.sleep(1)

    # Clicar no botão Entrar
    if not nav.click("//button[normalize-space()='Entre']"):
        print("Botão de entrar não encontrado.")
        return False

    time.sleep(3)  # dar tempo para Shopee validar

    # Verifica erro de login
    erro_login_incorreto = nav.ler("//div[normalize-space()='Sua conta e/ou senha estão incorretas, tente novamente']")

    if erro_login_incorreto:
        print("Login incorreto. Verifique suas credenciais.")
        return False

    print("Login realizado com sucesso.")
    return True


# -----------------------------------
# Configurações e Caminhos
# -----------------------------------
LOCAL    = Path(__file__).parent              # .../bots/shopee/
BASE_DIR = LOCAL.parent.parent                # .../ecommerce_bot/
CONFIGS_DIR = LOCAL / "configs.json"          # .../bots/shopee/configs.json

# Adicionar ecommerce_bot/ ao sys.path
sys.path.append(str(BASE_DIR))

# Carregar arquivo de configuração JSON
with open(CONFIGS_DIR, "r") as f:
    CONFIGS_JSON = json.load(f)

url_login = CONFIGS_JSON.get("url_login", "")

# -----------------------------------
# Imports do Core
# -----------------------------------
from core.navegador import Navegador
from core.seguranca import carregar_credenciais


# -----------------------------------
# Execução
# -----------------------------------
usuario, senha = carregar_credenciais()

nav = Navegador(browser_type="chrome", headless=False, download_path="./downloads")
nav.abrir_site(url_login)
nav.maximizar_janela()

if not login(nav, usuario, senha):
    print("Encerrando o bot devido a falha no login.")
    nav.fechar_navegador()
    raise SystemExit

print("Bot finalizado com sucesso.")
nav.fechar_navegador()
