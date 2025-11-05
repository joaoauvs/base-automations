"""Módulo para integração com Azure Key Vault.

Este módulo fornece funcionalidades para buscar credenciais e segredos
do Azure Key Vault de forma segura, substituindo o uso de variáveis de
ambiente do arquivo .env.
"""

import logging
import os
from typing import Dict, Optional

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


class KeyVaultClient:
    """Cliente para gerenciar acesso ao Azure Key Vault.

    Esta classe fornece métodos para buscar segredos do Azure Key Vault
    usando autenticação via DefaultAzureCredential (suporta Managed Identity,
    Service Principal, Azure CLI, etc).

    Attributes:
        vault_url: URL do Key Vault (ex: https://meu-keyvault.vault.azure.net/).
        client: Cliente do Azure Key Vault.
        _cache: Cache local de segredos para evitar múltiplas requisições.

    Example:
        >>> kv_client = KeyVaultClient()
        >>> email_password = kv_client.get_secret("EMAIL-PASSWORD")
        >>> all_secrets = kv_client.get_all_secrets(["EMAIL-SENDER", "EMAIL-PASSWORD"])
    """

    def __init__(self, vault_url: Optional[str] = None) -> None:
        """Inicializa o cliente do Key Vault.

        Args:
            vault_url: URL do Azure Key Vault. Se None, busca da variável
                      de ambiente AZURE_KEYVAULT_URL.

        Raises:
            ValueError: Se a URL do Key Vault não for fornecida.
        """
        self.vault_url = vault_url or os.getenv("AZURE_KEYVAULT_URL")

        if not self.vault_url:
            raise ValueError(
                "URL do Azure Key Vault não fornecida. "
                "Configure a variável de ambiente AZURE_KEYVAULT_URL ou "
                "passe o parâmetro vault_url ao inicializar o KeyVaultClient."
            )

        try:
            # DefaultAzureCredential tenta múltiplos métodos de autenticação:
            # 1. Environment variables (AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET)
            # 2. Managed Identity (se rodando no Azure)
            # 3. Azure CLI (se autenticado via 'az login')
            # 4. Visual Studio Code
            # 5. Azure PowerShell
            credential = DefaultAzureCredential()
            self.client = SecretClient(vault_url=self.vault_url, credential=credential)
            self._cache: Dict[str, str] = {}

            logging.info(f"Cliente Key Vault inicializado com sucesso: {self.vault_url}")

        except Exception as e:
            logging.error(f"Erro ao inicializar cliente do Key Vault: {e}")
            raise

    def get_secret(self, secret_name: str, use_cache: bool = True) -> Optional[str]:
        """Busca um segredo do Key Vault.

        Args:
            secret_name: Nome do segredo no Key Vault.
            use_cache: Se True, usa cache local para evitar múltiplas requisições.

        Returns:
            O valor do segredo ou None se não encontrado.

        Example:
            >>> client = KeyVaultClient()
            >>> password = client.get_secret("DATABASE-PASSWORD")
        """
        # Verifica cache primeiro
        if use_cache and secret_name in self._cache:
            logging.debug(f"Segredo '{secret_name}' obtido do cache")
            return self._cache[secret_name]

        try:
            secret = self.client.get_secret(secret_name)
            secret_value = secret.value

            # Armazena no cache
            if use_cache:
                self._cache[secret_name] = secret_value

            logging.info(f"Segredo '{secret_name}' obtido com sucesso do Key Vault")
            return secret_value

        except Exception as e:
            logging.error(f"Erro ao buscar segredo '{secret_name}' do Key Vault: {e}")
            return None

    def get_all_secrets(self, secret_names: list, use_cache: bool = True) -> Dict[str, Optional[str]]:
        """Busca múltiplos segredos do Key Vault.

        Args:
            secret_names: Lista de nomes de segredos a buscar.
            use_cache: Se True, usa cache local para evitar múltiplas requisições.

        Returns:
            Dicionário com os nomes dos segredos como chaves e seus valores.

        Example:
            >>> client = KeyVaultClient()
            >>> secrets = client.get_all_secrets([
            ...     "EMAIL-SENDER",
            ...     "EMAIL-PASSWORD",
            ...     "TWOCAPTCHA-API-KEY"
            ... ])
            >>> email_sender = secrets.get("EMAIL-SENDER")
        """
        secrets = {}
        for secret_name in secret_names:
            secrets[secret_name] = self.get_secret(secret_name, use_cache)

        return secrets

    def refresh_cache(self) -> None:
        """Limpa o cache de segredos, forçando nova busca no próximo acesso."""
        self._cache.clear()
        logging.info("Cache de segredos do Key Vault limpo")

    def get_secret_with_fallback(
        self,
        secret_name: str,
        env_var_name: Optional[str] = None,
        default: str = ""
    ) -> str:
        """Busca um segredo do Key Vault com fallback para variável de ambiente.

        Útil durante migração do .env para Key Vault, permitindo que o sistema
        continue funcionando se o Key Vault não estiver configurado.

        Args:
            secret_name: Nome do segredo no Key Vault.
            env_var_name: Nome da variável de ambiente (fallback). Se None, usa secret_name.
            default: Valor padrão se não encontrado em nenhum lugar.

        Returns:
            O valor do segredo, variável de ambiente ou valor padrão.

        Example:
            >>> client = KeyVaultClient()
            >>> # Tenta Key Vault primeiro, depois EMAIL_SENDER do .env
            >>> email = client.get_secret_with_fallback("EMAIL-SENDER", "EMAIL_SENDER")
        """
        # Tenta buscar do Key Vault primeiro
        secret_value = self.get_secret(secret_name)

        if secret_value:
            return secret_value

        # Fallback para variável de ambiente
        env_name = env_var_name or secret_name.replace("-", "_")
        env_value = os.getenv(env_name)

        if env_value:
            logging.warning(
                f"Segredo '{secret_name}' não encontrado no Key Vault. "
                f"Usando variável de ambiente '{env_name}' como fallback."
            )
            return env_value

        logging.warning(
            f"Segredo '{secret_name}' não encontrado no Key Vault nem em variáveis de ambiente. "
            f"Usando valor padrão."
        )
        return default

    def __repr__(self) -> str:
        """Representação em string do objeto KeyVaultClient."""
        return f"KeyVaultClient(vault_url='{self.vault_url}')"


# Instância global singleton (lazy loading)
_global_client: Optional[KeyVaultClient] = None


def get_keyvault_client(vault_url: Optional[str] = None) -> KeyVaultClient:
    """Retorna uma instância singleton do KeyVaultClient.

    Args:
        vault_url: URL do Azure Key Vault. Se None, usa a instância global existente
                  ou cria uma nova usando AZURE_KEYVAULT_URL do ambiente.

    Returns:
        Instância do KeyVaultClient.

    Example:
        >>> client = get_keyvault_client()
        >>> password = client.get_secret("DATABASE-PASSWORD")
    """
    global _global_client

    if _global_client is None or (vault_url and vault_url != _global_client.vault_url):
        _global_client = KeyVaultClient(vault_url)

    return _global_client
