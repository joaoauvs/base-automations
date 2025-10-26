import locale
import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

from src.core.log import Logger

locale.setlocale(locale.LC_TIME, "Portuguese_Brazil.1252")

dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)
else:
    load_dotenv()

Logger.configure_logger()

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class ExecutionMode(Enum):
    PRODUCTION = "production"
    DEVELOP = "develop"
    TEST = "test"


@dataclass(frozen=True)
class DatabricksConfig:
    """Container para credenciais do Databricks carregadas do ambiente."""

    host: str = os.getenv("DATABRICKS_HOST") or os.getenv("DATABRICKS_HOST_PATH", "")
    http_path: str = os.getenv("DATABRICKS_HTTP_PATH", "")
    access_token: str = os.getenv("DATABRICKS_ACCESS_TOKEN", "")


@dataclass(frozen=True)
class WebhookConfig:
    """URLs utilizadas para envio de status e telemetria."""

    execution_status: str = os.getenv("WEBHOOK_EXECUTION_STATUS", "")


class Settings:
    """
    Classe para gerenciar as configurações centrais do projeto sem expor
    endpoints sensíveis diretamente no código.
    """

    PROJECT_NAME = PROJECT_ROOT.name
    VERSION = os.getenv("PROJECT_VERSION", "1.0.0")
    LOG_DIR = str(Path(os.getenv("LOG_PATH", PROJECT_ROOT / "logs")).resolve())

    databricks = DatabricksConfig()
    webhook = WebhookConfig()

    # Backwards compatibility attributes -------------------------------
    DATABRICKS_HOST = databricks.host
    DATABRICKS_HTTP_PATH = databricks.http_path
    DATABRICKS_ACCESS_TOKEN = databricks.access_token
    databricks_host = databricks.host
    databricks_http_path = databricks.http_path
    databricks_access_token = databricks.access_token

    WEBHOOK_EXECUTION_STATUS = webhook.execution_status
