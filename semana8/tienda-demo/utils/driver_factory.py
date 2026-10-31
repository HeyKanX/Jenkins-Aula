"""
DriverFactory: crea y configura instancias del navegador para los tests.

Centraliza la configuración del driver Chrome para que los archivos de test
mantengan un único punto de creación del navegador.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class DriverFactory:
    # Crea un driver Chrome configurado para pruebas.
    #
    # El modo headless permite ejecutar los tests sin abrir una ventana
    # visible del navegador, lo cual es útil para entornos de CI o ejecución rápida.
    @staticmethod
    def create_chrome(headless=True):
        options = Options()
        if headless:
            options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        return driver
