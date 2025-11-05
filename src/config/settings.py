import locale
import logging
import os
import platform
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional

from dotenv import find_dotenv, load_dotenv

from src.core.log import Logger

# Configuração de locale compatível com Windows e Linux
try:
    if platform.system() == "Windows":
        locale.setlocale(locale.LC_TIME, "Portuguese_Brazil.1252")
    else:
        # Linux/Unix
        try:
            locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
        except locale.Error:
            # Fallback para sistemas que não têm pt_BR
            try:
                locale.setlocale(locale.LC_TIME, "C.UTF-8")
            except locale.Error:
                # Último fallback
                locale.setlocale(locale.LC_TIME, "C")
except locale.Error:
    # Se não conseguir configurar nenhum locale, usa o padrão do sistema
    pass

dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)
else:
    load_dotenv()

Logger.configure_logger()

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Inicializa Key Vault client (se configurado)
_keyvault_client: Optional[object] = None
USE_KEYVAULT = os.getenv("USE_AZURE_KEYVAULT", "false").lower() in ("true", "1", "yes")

if USE_KEYVAULT:
    try:
        from src.config.keyvault import get_keyvault_client
        _keyvault_client = get_keyvault_client()
        logging.info("Azure Key Vault configurado e pronto para uso")
    except Exception as e:
        logging.warning(f"Não foi possível inicializar Azure Key Vault: {e}")
        logging.warning("Usando variáveis de ambiente do .env como fallback")
        _keyvault_client = None


def get_config_value(key: str, keyvault_name: Optional[str] = None, default: str = "") -> str:
    """Busca um valor de configuração, primeiro do Key Vault, depois do .env.

    Args:
        key: Nome da variável de ambiente (ex: "EMAIL_SENDER").
        keyvault_name: Nome do segredo no Key Vault (ex: "EMAIL-SENDER").
                      Se None, converte key (underscores para hyphens).
        default: Valor padrão se não encontrado.

    Returns:
        O valor da configuração.

    Example:
        >>> email = get_config_value("EMAIL_SENDER")
        >>> # Busca "EMAIL-SENDER" no Key Vault, depois EMAIL_SENDER do .env
    """
    # Se Key Vault estiver habilitado e configurado, tenta buscar de lá primeiro
    if USE_KEYVAULT and _keyvault_client:
        kv_name = keyvault_name or key.replace("_", "-")
        try:
            secret_value = _keyvault_client.get_secret(kv_name)
            if secret_value:
                return secret_value
        except Exception as e:
            logging.debug(f"Erro ao buscar '{kv_name}' do Key Vault: {e}")

    # Fallback para variável de ambiente
    return os.getenv(key, default)


class ExecutionMode(Enum):
    PRODUCTION = "production"
    DEVELOP = "develop"
    TEST = "test"


@dataclass(frozen=True)
class DatabricksConfig:
    """Container para credenciais do Databricks carregadas do ambiente ou Key Vault."""

    host: str = (
        get_config_value("DATABRICKS_HOST", "DATABRICKS-HOST") or
        get_config_value("DATABRICKS_HOST_PATH", "DATABRICKS-HOST-PATH")
    )
    http_path: str = get_config_value("DATABRICKS_HTTP_PATH", "DATABRICKS-HTTP-PATH")
    access_token: str = get_config_value("DATABRICKS_ACCESS_TOKEN", "DATABRICKS-ACCESS-TOKEN")


@dataclass(frozen=True)
class WebhookConfig:
    """URLs utilizadas para envio de status e telemetria."""

    execution_status: str = get_config_value("WEBHOOK_EXECUTION_STATUS", "WEBHOOK-EXECUTION-STATUS")


class Settings:
    """
    Classe para gerenciar as configurações centrais do projeto sem expor
    endpoints sensíveis diretamente no código.
    """

    PROJECT_NAME = PROJECT_ROOT.name
    VERSION = get_config_value("PROJECT_VERSION", default="1.0.0")
    LOG_DIR = str(Path(get_config_value("LOG_PATH", default=str(PROJECT_ROOT / "logs"))).resolve())

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
