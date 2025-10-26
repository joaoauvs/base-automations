"""Script principal para execução do bot RPA focado em automações web.

Este módulo contém a classe BotWeb e o ponto de entrada principal
para execução de automações web específicas.
"""

import logging
from typing import Optional

from src.modules.common import attempts, time_execution
from src.modules.email import Email
from src.modules.log import LogManager
from src.modules.web.webdriver import Browser, WebDriver


class BotWeb:
    """Classe principal do bot RPA para automações web.

    Attributes:
        cnpj: CNPJ a ser processado pelo bot.
        robot_name: Nome do robô/processo.
        url: URL alvo para automação.
    """

    def __init__(self, cnpj: Optional[str] = None, robot_name: str = "RPABotWeb", url: Optional[str] = None) -> None:
        """Inicializa o bot web.

        Args:
            cnpj: CNPJ a ser processado (opcional).
            robot_name: Nome do robô (padrão: "RPABotWeb").
            url: URL alvo para automação (opcional).
        """
        self.cnpj = cnpj or "00.000.000/0000-00"  # CNPJ padrão para testes
        self.robot_name = robot_name
        self.url = url or "https://exemplo.com"
        self.navegador = None

    @time_execution
    @attempts(max_attempts=3)
    def executar_automacao_web(self) -> None:
        """Executa o processo principal de automação web.

        Raises:
            RuntimeError: Se houver erro ao iniciar o navegador.
        """
        try:
            logging.info(f"INICIANDO AUTOMAÇÃO WEB - CNPJ: {self.cnpj}")
            logging.info(f"URL ALVO: {self.url}")

            # Inicializa o navegador
            self.navegador = WebDriver.get_navegador(
                Browser.UNDETECTED_CHROME,
                headless=False
            )

            # Navega para a URL
            self.navegador.get(self.url)
            logging.info(f"Navegando para: {self.url}")

            # Adicione aqui a lógica específica de automação web
            # Exemplos:
            # - Preenchimento de formulários
            # - Extração de dados
            # - Interação com elementos da página
            # - Screenshots
            # - Downloads

            logging.info(f"[SUCESSO] AUTOMAÇÃO WEB CNPJ: {self.cnpj} FINALIZADA COM SUCESSO!")

        except RuntimeError as e:
            logging.error(f"[FALHA] Erro ao iniciar navegador: {type(e).__name__}: {e}")
            raise

        except Exception as e:
            logging.error(f"[FALHA] Erro durante automação web: {type(e).__name__}: {e}")
            raise

        finally:
            # Garante que o navegador seja fechado
            if self.navegador:
                try:
                    self.navegador.quit()
                    logging.info("Navegador fechado com sucesso")
                except Exception as e:
                    logging.warning(f"Erro ao fechar navegador: {e}")

    def processar_lista_cnpjs(self, lista_cnpjs: list[str], url: Optional[str] = None) -> None:
        """Processa uma lista de CNPJs em automação web.

        Args:
            lista_cnpjs: Lista de CNPJs para processar.
            url: URL específica (opcional, usa a URL da instância se não fornecida).
        """
        url_processamento = url or self.url
        
        for cnpj in lista_cnpjs:
            try:
                logging.info(f"Processando CNPJ: {cnpj}")
                self.cnpj = cnpj
                self.url = url_processamento
                self.executar_automacao_web()
            except Exception as e:
                logging.error(f"Erro ao processar CNPJ {cnpj}: {e}")
                continue


def main() -> None:
    """Ponto de entrada principal da aplicação web."""
    try:
        # Configurar logging antes de executar
        LogManager()

        # Criar e executar o bot web
        # Exemplo de uso com URL específica
        bot_web = BotWeb(
            cnpj="12.345.678/0001-90", 
            robot_name="AutomacaoWeb",
            url="https://www.receita.fazenda.gov.br/"
        )
        bot_web.executar_automacao_web()

        # Exemplo de processamento em lote
        # lista_cnpjs = ["12.345.678/0001-90", "98.765.432/0001-10"]
        # bot_web.processar_lista_cnpjs(lista_cnpjs)

    except Exception as e:
        logging.error(f"Erro ao executar o bot web: {e}")

        # Envia email de falha
        try:
            email_notifier = Email(robo="AutomacaoWeb")
            email_notifier.send_email_fail()
        except Exception as email_error:
            logging.error(f"Erro ao enviar email de falha: {email_error}")


if __name__ == "__main__":
    main()