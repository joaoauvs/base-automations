import asyncio
import logging
from math import log

from login_gov import Gov
from resources.modules.common import attempts, time_execution
from resources.modules.email import Email
from resources.modules.log import Log
from resources.web.webdriver import Browser, WebDriver

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Bot:

    @time_execution
    @attempts(max_attempts=2)
    def main(self):
        """Executa o bot."""
        try:
            logging.info(f"📝 INICIANDO O PROCESSO CNPJ: {self.cnpj}")

            navegador = WebDriver.get_navegador(Browser.UNDETECTED_CHROME, headless=False)

            logging.info(f"[✔] PROCESSO CNPJ: {self.cnpj} FINALIZADO COM SUCESSO!")
        except RuntimeError as e:
            logging.warning(f"[FALHA START NAVEGADOR]: {type(e).__name__}, {e.args[0]}")
        finally:
            navegador.quit()


if __name__ == "__main__":
    try:
        asyncio.run(Bot().main())
    except Exception as e:
        logging.warning("Erro ao executar o bot: " + str(e))
        Email().send_email_fail()
