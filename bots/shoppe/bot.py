from pathlib import Path
import sys
import os
import json

LOCAL       = Path(__file__).parent   # shopee/
BASE_DIR    = LOCAL.parent.parent  # ecommerce_nav/
CONFIGS_DIR  = LOCAL / "configs.json"
sys.path.append(str(BASE_DIR))

with open(CONFIGS_DIR, "r") as f:
    CONFIGS_JSON = json.load(f)
url_login = CONFIGS_JSON.get("url_login", "")

from core.navegador import Navegador


nav = Navegador(browser_type="chrome", headless=False, download_path="./downloads")
nav.abrir_site("https://shopee.com.br/")

nav.fechar_navegador()