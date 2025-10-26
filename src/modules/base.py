import asyncio
import os
import time
from typing import Optional, Tuple, Union

import pyautogui
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    NoSuchFrameException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Web:
    def __init__(self, driver: webdriver.Chrome, timeout: int = 15):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def navigate(self, url: str):
        """Navega até a URL fornecida e maximiza a janela do navegador.

        Args:
            url (str): A URL para navegar.
        """
        self.driver.get(url)
        self.driver.maximize_window()

    def assert_element_exists(self, locator: Tuple[str, str], ensure_visible: bool = True) -> bool:
        """
        Verifica se o elemento existe e é visível (se especificado) na página.

        Args:
            locator (Tuple[str, str]): Uma tupla contendo o tipo de localizador e o valor do localizador.
            ensure_visible (bool, opcional): Se True, verifica a visibilidade do elemento. Por padrão é True.

        Returns:
            bool: Retorna True se o elemento for encontrado e visível (se especificado), caso contrário, retorna False.
        """
        try:
            return bool(self.wait.until(EC.visibility_of_element_located(locator) if ensure_visible else EC.presence_of_element_located(locator)))
        except (NoSuchElementException, TimeoutException):
            return False

    def click_element(self, locator: Tuple[By, str]):
        """Clica em um elemento dado um localizador.

        Args:
            locator (Tuple[By, str]): O localizador do elemento a ser clicado.

        Raises:
            NoSuchElementException: Se o elemento não for encontrado.
        """
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def set_text(self, locator: Tuple[By, str], text: str):
        """Define o texto de um elemento dado um localizador.

        Args:
            locator (Tuple[By, str]): O localizador do elemento.
            text (str): O texto a ser definido no elemento.

        Raises:
            NoSuchElementException: Se o elemento não for encontrado.
        """
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: Tuple[By, str]) -> str:
        """Obtém o texto de um elemento dado um localizador.

        Args:
            locator (Tuple[By, str]): O localizador do elemento.

        Returns:
            str: O texto do elemento.

        Raises:
            NoSuchElementException: Se o elemento não for encontrado.
        """
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.text

    def wait_for_element(self, locator: Tuple[By, str], condition, timeout: int = 15):
        """Espera por uma condição específica em um elemento.

        Args:
            locator (Tuple[By, str]): O localizador do elemento.
            condition: A condição esperada (EC.condition).
            timeout (int, opcional): Tempo de espera em segundos.

        Raises:
            TimeoutException: Se o tempo limite for excedido.
        """
        WebDriverWait(self.driver, timeout).until(condition(locator))

    ###### JavaScript ######

    def execute_js(self, script: str):
        """Executa um script JavaScript no navegador.

        Args:
            script (str): O script JavaScript a ser executado.
        """
        return self.driver.execute_script(script)

    def set_text_js(self, selector: str, value: str):
        """Define o texto de um elemento usando JavaScript.

        Args:
            selector (str): O seletor CSS do elemento.
            value (str): O valor a ser definido no elemento.
        """
        script = f"document.querySelector('{selector}').value = '{value}';"
        self.execute_js(script)

    def get_text_js(self, selector: str) -> str:
        """Obtém o texto de um elemento usando JavaScript.

        Args:
            selector (str): O seletor CSS do elemento.

        Returns:
            str: O texto do elemento.
        """
        script = f"return document.querySelector('{selector}').textContent;"
        return self.execute_js(script)

    def click_js(self, selector: str):
        """Clica em um elemento utilizando JavaScript.

        Args:
            selector (str): O seletor CSS do elemento a ser clicado.
        """
        script = f"document.querySelector('{selector}').click();"
        self.execute_js(script)

    ###### Pyautogui ######

    def click_on_image(self, image_path: str, confidence: float = 0.8) -> bool:
        """Tenta clicar em uma imagem na tela usando PyAutoGUI.

        Args:
            image_path (str): Caminho da imagem a ser clicada.
            confidence (float, opcional): Nível de confiança para a correspondência da imagem.

        Returns:
            bool: True se o clique for bem-sucedido, False caso contrário.
        """
        location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        if location:
            pyautogui.click(location)
            return True
        return False

    async def click_on_image_async(self, image_path: str, confidence: float = 0.8) -> bool:
        """Versão assíncrona de click_on_image usando asyncio."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.click_on_image, image_path, confidence)

    async def find_and_click_any(self, image_paths: list, confidence: float = 0.7, timeout: int = 10) -> bool:
        """Tenta clicar em qualquer uma das imagens fornecidas até que uma delas funcione.

        Args:
            image_paths (list of str): Lista de caminhos de imagem para tentar clicar.
            confidence (float, opcional): Nível de confiança para a correspondência de imagem.
            timeout (int, opcional): Tempo limite total em segundos para tentar clicar nas imagens.

        Returns:
            bool: Retorna True se pelo menos uma das imagens for clicada com sucesso, False caso contrário.
        """
        tasks = [self.click_on_image_async(path, confidence) for path in image_paths]
        done, pending = await asyncio.wait(tasks, timeout=timeout, return_when=asyncio.FIRST_COMPLETED)

        for task in pending:
            task.cancel()

        return any(task.result() for task in done if task.done())
