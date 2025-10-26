import logging
from pathlib import Path


class Logger:
    _is_configured = False  # Flag para evitar configuração duplicada

    @staticmethod
    def configure_logger(log_path: str = None, console: bool = True, filemode: str = "a"):
        """
        Configura o logging globalmente para todos os arquivos usando logging.basicConfig.

        Args:
            log_path (str, optional): Caminho do diretório onde o arquivo de log será salvo.
                                      Se não fornecido, usará 'logs/processamento.log'.
            console (bool, optional): Se True, também exibe logs no console (stdout).
            filemode (str, optional): Modo de abertura do arquivo ('a' para append, 'w' para sobrescrever).
        """
        if Logger._is_configured:
            return

        # Define diretório padrão
        project_root_path = Path(__file__).resolve().parent.parent.parent / "logs"
        log_dir = Path(log_path) if log_path else project_root_path
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "processamento.log"

        # Formato base
        log_format = "{asctime} - {levelname} - {funcName}:{lineno} - {message}"
        date_format = "%d/%m/%Y %H:%M:%S"

        # Configuração do handler de arquivo
        handlers = [
            logging.FileHandler(log_file, mode=filemode, encoding="utf-8")
        ]

        # Adiciona saída no console se habilitado
        if console:
            handlers.append(logging.StreamHandler())

        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            datefmt=date_format,
            style="{",
            handlers=handlers,
        )

        Logger._is_configured = True
