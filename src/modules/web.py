import asyncio
import logging
import os
import time
from typing import Optional, Tuple, Union

import pyautogui
from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    NoSuchFrameException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Web:
    """
    Classe base para interações com a web.

    Args:
        driver (webdriver.Chrome): Instância do WebDriver.
        timeout (int, opcional): Tempo limite para esperar por elementos.
    """

    def __init__(self, driver: webdriver.Chrome, timeout: int = 15):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def navigate(self, url: str) -> None:
        """
        Navega até a URL fornecida e maximiza a janela do navegador.

        Args:
            url (str): URL para navegar.
        """
        self.driver.get(url)
        self.driver.maximize_window()

    def find_element(self, by_locator: Tuple[str, str], ensure_visible: bool = True) -> Union[webdriver.remote.webelement.WebElement, bool]:
        """
        Verifica e retorna se o elemento existe e é visível, ou retorna o próprio elemento.

        Args:
            by_locator (Tuple[str, str]): Localizador do elemento.
            ensure_visible (bool, opcional): Se True, verifica a visibilidade do elemento.

        Returns:
            WebElement | bool: Retorna o elemento se encontrado, ou False se não for encontrado.
        """
        try:
            if ensure_visible:
                return self.wait.until(EC.visibility_of_element_located(by_locator))
            return self.wait.until(EC.presence_of_element_located(by_locator))
        except (NoSuchElementException, TimeoutException):
            return False

    def wait_for_element(self, by_locator: Tuple[By, str], condition: Optional[callable] = None) -> None:
        """
        Espera até que um elemento atenda a uma condição específica ou a condição padrão (visibilidade).

        Args:
            by_locator (Tuple[By, str]): Localizador do elemento.
            condition (callable, opcional): Condição a ser atendida pelo elemento. Se None, usa EC.visibility_of_element_located.
        """
        if condition is None:
            condition = EC.visibility_of_element_located
        self.wait.until(condition(by_locator))

    def click_js(self, selector: str):
        """Clica em um elemento utilizando JavaScript.

        Args:
            selector (str): O seletor CSS do elemento a ser clicado.
        """
        script = f"document.querySelector('{selector}').click();"
        self.execute_js(script)

    def scroll_to_element(self, by_locator: Tuple[By, str]) -> None:
        """
        Rola a página até o elemento especificado.

        Args:
            by_locator (Tuple[By, str]): Localizador do elemento.
        """
        element = self.find_element(by_locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def click_element(self, by_locator: Tuple[By, str], use_js: bool = False) -> None:
        """Clica em um elemento dado um localizador, com a opção de usar JavaScript.

        Args:
            by_locator (Tuple[By, str]): O localizador do elemento.
            use_js (bool, opcional): Se True, utiliza JavaScript para clicar.
        """
        try:
            element = self.find_element(by_locator)
            if not element:
                raise NoSuchElementException(f"Elemento não encontrado: {by_locator}")

            if use_js:
                self.driver.execute_script("arguments[0].click();", element)
            else:
                self.wait.until(EC.element_to_be_clickable(by_locator)).click()
        except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
            raise NoSuchElementException(f"Falha ao tentar clicar no elemento: {by_locator}. Detalhes: {e}")

    def set_text(self, by_locator: Tuple[By, str], text: str) -> None:
        """
        Define o texto de um elemento.

        Args:
            by_locator (Tuple[By, str]): Localizador do elemento.
            text (str): Texto a ser definido.
        """
        element = self.find_element(by_locator)
        if element:
            element.clear()
            element.send_keys(text)
        else:
            raise NoSuchElementException(f"Elemento não encontrado: {by_locator}")

    def get_text(self, by_locator: Tuple[By, str]) -> str:
        """
        Obtém o texto de um elemento.

        Args:
            by_locator (Tuple[By, str]): Localizador do elemento.

        Returns:
            str: Texto do elemento.
        """
        element = self.find_element(by_locator)
        if element:
            return element.text
        raise NoSuchElementException(f"Elemento não encontrado: {by_locator}")

    def get_elements(self, by_locator: Tuple[By, str]) -> list:
        """
        Obtém uma lista de elementos.

        Args:
            by_locator (Tuple[By, str]): Localizador do elemento.

        Returns:
            list: Lista de elementos.
        """
        return self.wait.until(EC.presence_of_all_elements_located(by_locator))

    def interact_with_tag(self, by_locator: Tuple[str, str], tag: str, text: Optional[str] = None, click: bool = False) -> Union[list, bool]:
        """
        Interage com elementos de uma tag específica, opcionalmente clicando ou retornando uma lista de elementos.

        Args:
            by_locator (Tuple[str, str]): Localizador do elemento pai.
            tag (str): Nome da tag do elemento filho.
            text (str, opcional): Texto do elemento a ser encontrado.
            click (bool, opcional): Se True, clica no elemento encontrado.

        Returns:
            list | bool: Retorna uma lista de elementos encontrados, ou True se um clique for bem-sucedido.
        """
        element = self.find_element(by_locator)
        if element:
            tag_elements = element.find_elements(By.TAG_NAME, tag)
            if text:
                for el in tag_elements:
                    if el.text == text:
                        if click:
                            el.click()
                        return True
            return tag_elements
        return False

    def assert_element_exists(self, by_locator: Tuple[str, str], ensure_visible: bool = True) -> bool:
        """Verifica se o elemento existe e é visível (se especificado) na página.

        Args:
            by_locator (Tuple[str, str]): O localizador do elemento.
            ensure_visible (bool, opcional): Se True, verifica a visibilidade do elemento.

        Returns:
            bool: Retorna True se o elemento for encontrado, False caso contrário.
        """
        return bool(self.find_element(by_locator, ensure_visible=ensure_visible))

    def execute_js(self, script: str, element: Optional[webdriver.remote.webelement.WebElement] = None) -> any:
        """
        Executa um script JavaScript no navegador.

        Args:
            script (str): Script JavaScript a ser executado.
            element (WebElement, opcional): Elemento a ser passado para o script.

        Returns:
            any: Resultado da execução do script.
        """
        return self.driver.execute_script(script, element) if element else self.driver.execute_script(script)

    # Verificar se o javascrit existe e não está vazio
    def js_exists(self, script: str) -> bool:
        """
        Verifica se um script JavaScript existe e não está vazio.

        Args:
            script (str): Script JavaScript a ser verificado.

        Returns:
            bool: True se o script existir e não estiver vazio, False caso contrário.
        """
        try:
            response = self.driver.execute_script(f"return !!({script});")
            return bool(response)
        except Exception as e:
            logging.error(f"Erro ao verificar script JavaScript: {e}")
            return False
    
    def access_iframe(self, by_locator: Tuple[str, str]) -> None:
        """
        Acessa um iframe utilizando o localizador especificado.
        """
        iframe = EC.visibility_of_element_located(by_locator)
        self.driver.switch_to.frame(self.wait.until(iframe))

    def close_iframe(self) -> None:
        """
        Sai do iframe atual e retorna ao contexto principal.
        """
        self.driver.switch_to.default_content()

    ###### Pyautogui ######

    def click_on_image(self, image_path: str, confidence: float = 0.8) -> bool:
        """
        Tenta clicar em uma imagem na tela usando PyAutoGUI.

        Args:
            image_path (str): Caminho para a imagem.
            confidence (float, opcional): Confiança da correspondência da imagem.

        Returns:
            bool: True se a imagem for encontrada e clicada, False caso contrário.
        """
        location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        if location:
            pyautogui.click(location)
            return True
        return False

    async def click_on_image_async(self, image_path: str, confidence: float = 0.8) -> bool:
        """
        Versão assíncrona de click_on_image usando asyncio.

        Args:
            image_path (str): Caminho para a imagem.
            confidence (float, opcional): Confiança da correspondência da imagem.

        Returns:
            bool: True se a imagem for encontrada e clicada, False caso contrário.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.click_on_image, image_path, confidence)

    async def find_and_click_any(self, image_paths: list, confidence: float = 0.7, timeout: int = 10) -> bool:
        """
        Tenta clicar em qualquer uma das imagens fornecidas até que uma delas funcione.

        Args:
            image_paths (list): Lista de caminhos para as imagens.
            confidence (float, opcional): Confiança da correspondência da imagem.
            timeout (int, opcional): Tempo limite em segundos.

        Returns:
            bool: True se uma das imagens for encontrada e clicada, False caso contrário.
        """
        tasks = [self.click_on_image_async(path, confidence) for path in image_paths]
        done, pending = await asyncio.wait(tasks, timeout=timeout, return_when=asyncio.FIRST_COMPLETED)

        for task in pending:
            task.cancel()

        return any(task.result() for task in done if task.done())
