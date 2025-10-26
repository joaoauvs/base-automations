"""Script principal para execução do bot RPA.

Este módulo contém a classe Bot e o ponto de entrada principal
para execução da automação.
"""

import logging
from typing import Optional

from src.modules.common import attempts, time_execution
from src.modules.email import Email
from src.modules.log import LogManager
from src.web.webdriver import Browser, WebDriver


class Bot:
    """Classe principal do bot RPA.

    Attributes:
        cnpj: CNPJ a ser processado pelo bot.
        robot_name: Nome do robô/processo.
    """

    def __init__(self, cnpj: Optional[str] = None, robot_name: str = "RPABot") -> None:
        """Inicializa o bot.

        Args:
            cnpj: CNPJ a ser processado (opcional).
            robot_name: Nome do robô (padrão: "RPABot").
        """
        self.cnpj = cnpj or "00.000.000/0000-00"  # CNPJ padrão para testes
        self.robot_name = robot_name
        self.navegador = None

    @time_execution
    @attempts(max_attempts=2)
    def main(self) -> None:
        """Executa o processo principal do bot.

        Raises:
            RuntimeError: Se houver erro ao iniciar o navegador.
        """
        try:
            logging.info(f"INICIANDO O PROCESSO CNPJ: {self.cnpj}")

            # Inicializa o navegador
            self.navegador = WebDriver.get_navegador(
                Browser.UNDETECTED_CHROME,
                headless=False
            )

            # Adicione aqui a lógica do seu bot
            # Exemplo:
            # self.navegador.get("https://exemplo.com")
            # ... suas automações ...

            logging.info(f"[SUCESSO] PROCESSO CNPJ: {self.cnpj} FINALIZADO COM SUCESSO!")

        except RuntimeError as e:
            logging.error(f"[FALHA] Erro ao iniciar navegador: {type(e).__name__}: {e}")
            raise

        except Exception as e:
            logging.error(f"[FALHA] Erro durante execução: {type(e).__name__}: {e}")
            raise

        finally:
            # Garante que o navegador seja fechado
            if self.navegador:
                try:
                    self.navegador.quit()
                    logging.info("Navegador fechado com sucesso")
                except Exception as e:
                    logging.warning(f"Erro ao fechar navegador: {e}")


def main() -> None:
    """Ponto de entrada principal da aplicação."""
    try:
        # Configurar logging antes de executar
        log_manager = LogManager(path="./logs/")

        # Criar e executar o bot
        # Você pode passar um CNPJ específico aqui
        bot = Bot(cnpj="12.345.678/0001-90", robot_name="ProcessadorCNPJ")
        bot.main()

    except Exception as e:
        logging.error(f"Erro ao executar o bot: {e}")

        # Envia email de falha
        try:
            email_notifier = Email(robo="ProcessadorCNPJ")
            email_notifier.send_email_fail()
        except Exception as email_error:
            logging.error(f"Erro ao enviar email de falha: {email_error}")


if __name__ == "__main__":
    main()
