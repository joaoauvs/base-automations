"""Módulo para criação e gerenciamento de arquivos de log.

Este módulo fornece uma classe para configurar e gerenciar arquivos de log
de forma estruturada e padronizada.
"""

import logging
from datetime import datetime
from pathlib import Path


class LogManager:
    """Gerenciador de arquivos de log.

    Configura e gerencia arquivos de log diários com formatação padronizada.
    Suporta criação automática de diretórios e limpeza de logs antigos.

    Attributes:
        log_dir: Diretório onde os arquivos de log são armazenados.
        current_date: Data atual no formato "dd-mm-yyyy".
        filename: Nome do arquivo de log baseado na data atual.
        log_path: Caminho completo do arquivo de log.

    Example:
        >>> log_manager = LogManager(path="/var/logs/app")
        >>> # Logs serão criados em /var/logs/app/DD-MM-YYYY.log
    """

    DEFAULT_FORMAT = "{asctime} - {levelname} - {funcName}:{lineno} - {message}"
    DEFAULT_DATE_FORMAT = "%d/%m/%Y %H:%M:%S"
    DEFAULT_LEVEL = logging.INFO

    def __init__(
        self,
        path: str = "logs",
        level: int = DEFAULT_LEVEL,
        file_mode: str = 'a',
        encoding: str = 'utf-8'
    ) -> None:
        """Inicializa o gerenciador de logs.

        Args:
            path: Caminho do diretório onde os logs serão armazenados (padrão: "logs").
            level: Nível mínimo de log (padrão: INFO).
            file_mode: Modo de abertura do arquivo ('a' = append, 'w' = overwrite).
            encoding: Codificação do arquivo de log (padrão: utf-8).

        Raises:
            ValueError: Se o path fornecido for inválido.
        """
        if not path:
            raise ValueError("O caminho do diretório de log não pode ser vazio")

        self.log_dir = Path(path)
        self.current_date = datetime.now().strftime("%d-%m-%Y")
        self.filename = f"{self.current_date}.log"
        self.log_path = self.log_dir / self.filename

        self._level = level
        self._file_mode = file_mode
        self._encoding = encoding

        self._setup_logging()

    def _setup_logging(self) -> None:
        """Configura o sistema de logging.

        Cria o diretório de logs se não existir e configura o logging básico.
        """
        try:
            # Cria o diretório se não existir
            self.log_dir.mkdir(parents=True, exist_ok=True)

            # Remove handlers existentes para evitar duplicação
            for handler in logging.root.handlers[:]:
                logging.root.removeHandler(handler)

            # Configura o logging
            logging.basicConfig(
                filename=str(self.log_path),
                filemode=self._file_mode,
                encoding=self._encoding,
                level=self._level,
                format=self.DEFAULT_FORMAT,
                datefmt=self.DEFAULT_DATE_FORMAT,
                style='{'
            )

            logging.info(f"Sistema de log iniciado - Arquivo: {self.log_path}")

        except OSError as e:
            raise OSError(f"Erro ao criar diretório de log '{self.log_dir}': {e}") from e
        except Exception as e:
            raise RuntimeError(f"Erro ao configurar sistema de log: {e}") from e

    def delete_log(self) -> None:
        """Remove o arquivo de log atual.

        Raises:
            FileNotFoundError: Se o arquivo de log não existir.
            OSError: Se houver erro ao deletar o arquivo.
        """
        try:
            if self.log_path.exists():
                self.log_path.unlink()
                logging.info(f"Arquivo de log removido: {self.log_path}")
            else:
                raise FileNotFoundError(f"Arquivo de log não encontrado: {self.log_path}")
        except OSError as e:
            raise OSError(f"Erro ao deletar arquivo de log '{self.log_path}': {e}") from e

    def delete_old_logs(self, days: int = 30) -> int:
        """Remove arquivos de log mais antigos que o número de dias especificado.

        Args:
            days: Número de dias. Logs mais antigos que isso serão removidos.

        Returns:
            Número de arquivos removidos.

        Raises:
            ValueError: Se days for negativo.
        """
        if days < 0:
            raise ValueError("O número de dias deve ser positivo")

        removed_count = 0
        current_time = datetime.now()

        try:
            for log_file in self.log_dir.glob("*.log"):
                if log_file.is_file():
                    file_age = current_time - datetime.fromtimestamp(log_file.stat().st_mtime)
                    if file_age.days > days:
                        log_file.unlink()
                        removed_count += 1
                        logging.info(f"Log antigo removido: {log_file.name}")

            logging.info(f"Limpeza de logs concluída: {removed_count} arquivo(s) removido(s)")
            return removed_count

        except OSError as e:
            logging.error(f"Erro ao deletar logs antigos: {e}")
            raise

    def get_log_size(self) -> int:
        """Retorna o tamanho do arquivo de log atual em bytes.

        Returns:
            Tamanho do arquivo em bytes, ou 0 se o arquivo não existir.
        """
        if self.log_path.exists():
            return self.log_path.stat().st_size
        return 0

    def __repr__(self) -> str:
        """Representação em string do objeto LogManager."""
        return f"LogManager(path='{self.log_dir}', filename='{self.filename}')"


# Mantém compatibilidade com código legado
Log = LogManager