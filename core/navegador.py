import os
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

class Navegador:
    def __init__(self, browser_type="chrome", headless=True, download_path=None):
        self.browser_type = browser_type.lower()
        self.headless = headless
        self.download_path = download_path or os.getcwd()
        self.driver = self._init_driver()
        self.wait = WebDriverWait(self.driver, 15)
        self.keys = Keys

    def _init_driver(self):
        if self.browser_type == "chrome":
            options = webdriver.ChromeOptions()
            options.headless = self.headless
            prefs = {
                "download.default_directory": self.download_path,
                "download.prompt_for_download": False,
                "plugins.always_open_pdf_externally": True,
            }
            options.add_experimental_option("prefs", prefs)
            service = ChromeService(ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=options)

        elif self.browser_type == "firefox":
            options = webdriver.FirefoxOptions()
            options.headless = self.headless
            profile = webdriver.FirefoxProfile()
            profile.set_preference("browser.download.folderList", 2)
            profile.set_preference("browser.download.dir", self.download_path)
            profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf,text/csv,application/octet-stream")
            service = FirefoxService(GeckoDriverManager().install())
            return webdriver.Firefox(service=service, options=options, firefox_profile=profile)
        else:
            raise ValueError("Browser não suportado: use 'chrome' ou 'firefox'")

    # ------------------- Navegação -------------------
    def abrir_site(self, url):
        self.driver.get(url)
        self._esperar_carregamento()

    def _esperar_carregamento(self):
        sleep(1)
        while self.driver.execute_script("return document.readyState") != "complete":
            sleep(0.5)

    def mudar_janela(self, index=-1):
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[index])

    # ------------------- Interação -------------------
    def click(self, xpath):
        elem = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        elem.click()

    def escrever(self, xpath, texto):
        elem = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        elem.clear()
        elem.send_keys(texto)

    def ler(self, xpath):
        elem = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        return elem.text

    def selecionar_option(self, xpath, valor, por="value"):
        select_elem = Select(self.wait.until(EC.presence_of_element_located((By.XPATH, xpath))))
        if por == "value":
            select_elem.select_by_value(valor)
        else:
            select_elem.select_by_visible_text(valor)

    def alerta_aceitar(self):
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except:
            pass

    # ------------------- Cookies -------------------
    def salvar_cookies(self, arquivo="cookies.json"):
        with open(arquivo, "w") as f:
            json.dump(self.driver.get_cookies(), f)

    def carregar_cookies(self, arquivo="cookies.json"):
        with open(arquivo, "r") as f:
            cookies = json.load(f)
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()

    # ------------------- Finalização -------------------
    def fechar_navegador(self):
        self.driver.quit()
