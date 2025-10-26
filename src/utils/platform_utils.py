"""Utilitários para compatibilidade entre diferentes sistemas operacionais.

Este módulo fornece funções e constantes para garantir que o código
funcione corretamente em Windows, Linux e macOS.
"""

import os
import platform
from pathlib import Path
from typing import Any, Dict


class PlatformUtils:
    """Classe para gerenciar compatibilidade entre plataformas."""

    @staticmethod
    def get_system() -> str:
        """Retorna o sistema operacional atual.

        Returns:
            String identificando o sistema: 'windows', 'linux', 'darwin' (macOS), ou 'unknown'
        """
        system = platform.system().lower()
        system_map = {"windows": "windows", "linux": "linux", "darwin": "macos"}
        return system_map.get(system, "unknown")

    @staticmethod
    def is_windows() -> bool:
        """Verifica se está executando no Windows."""
        return platform.system().lower() == "windows"

    @staticmethod
    def is_linux() -> bool:
        """Verifica se está executando no Linux."""
        return platform.system().lower() == "linux"

    @staticmethod
    def is_macos() -> bool:
        """Verifica se está executando no macOS."""
        return platform.system().lower() == "darwin"

    @staticmethod
    def get_null_device() -> str:
        """Retorna o dispositivo nulo apropriado para o sistema.

        Returns:
            'nul' para Windows, '/dev/null' para Unix-like systems
        """
        return "nul" if PlatformUtils.is_windows() else "/dev/null"

    @staticmethod
    def normalize_path(path: str) -> Path:
        """Normaliza um caminho para ser compatível com o sistema atual.

        Args:
            path: Caminho a ser normalizado

        Returns:
            Path object normalizado
        """
        return Path(path).resolve()

    @staticmethod
    def get_locale_settings() -> Dict[str, str]:
        """Retorna configurações de locale apropriadas para o sistema.

        Returns:
            Dicionário com configurações de locale
        """
        if PlatformUtils.is_windows():
            return {"time": "Portuguese_Brazil.1252", "encoding": "cp1252"}
        else:
            return {"time": "pt_BR.UTF-8", "encoding": "utf-8"}

    @staticmethod
    def get_chrome_args() -> list[str]:
        """Retorna argumentos específicos do Chrome para o sistema atual.

        Returns:
            Lista de argumentos para o Chrome
        """
        common_args = [
            "--disable-infobars",
            "--disable-popup-blocking",
            "--no-sandbox",
            "--disable-cache",
            "--ignore-certificate-errors",
            "--ignore-ssl-errors",
            "--disable-extensions",
            "--disable-notifications",
            "--disable-dev-shm-usage",
            "--disable-blink-features=AutomationControlled",
        ]

        if PlatformUtils.is_linux():
            # Argumentos específicos para Linux
            common_args.extend(["--disable-gpu", "--no-zygote", "--single-process"])

        return common_args

    @staticmethod
    def get_environment_info() -> Dict[str, Any]:
        """Retorna informações detalhadas sobre o ambiente de execução.

        Returns:
            Dicionário com informações do sistema
        """
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "architecture": platform.architecture(),
            "platform": platform.platform(),
            "node": platform.node(),
            "is_windows": PlatformUtils.is_windows(),
            "is_linux": PlatformUtils.is_linux(),
            "is_macos": PlatformUtils.is_macos(),
            "null_device": PlatformUtils.get_null_device(),
            "path_separator": os.sep,
            "line_separator": os.linesep,
        }


# Aliases para compatibilidade
get_system = PlatformUtils.get_system
is_windows = PlatformUtils.is_windows
is_linux = PlatformUtils.is_linux
is_macos = PlatformUtils.is_macos
get_null_device = PlatformUtils.get_null_device
normalize_path = PlatformUtils.normalize_path
