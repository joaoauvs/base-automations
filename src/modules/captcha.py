"""Módulo para resolução de captchas usando o serviço 2Captcha.

Este módulo fornece uma interface para resolver diferentes tipos de captchas
utilizando a API do serviço 2Captcha.
"""

import logging
import os
from typing import Dict, Optional

from twocaptcha import TwoCaptcha
from twocaptcha.api import ApiException, NetworkException, TimeoutException


class CaptchaSolver:
    """Resolvedor de captchas usando o serviço 2Captcha.

    Fornece métodos para resolver diferentes tipos de captchas incluindo
    captchas normais de imagem e reCAPTCHA v2/v3.

    Attributes:
        api_key: Chave de API do serviço 2Captcha.
        solver: Instância do TwoCaptcha para resolução.

    Example:
        >>> solver = CaptchaSolver()
        >>> code = solver.solve_image("captcha.png")
        >>> print(f"Captcha resolvido: {code}")
    """

    def __init__(self, api_key: Optional[str] = None) -> None:
        """Inicializa o resolvedor de captchas.

        Args:
            api_key: Chave de API do 2Captcha. Se None, busca de variável de ambiente.

        Raises:
            ValueError: Se a API key não for fornecida nem encontrada em variáveis de ambiente.
        """
        self.api_key = api_key or os.getenv("TWOCAPTCHA_API_KEY", "")

        if not self.api_key:
            raise ValueError(
                "API key do 2Captcha não configurada. "
                "Forneça via parâmetro ou configure a variável de ambiente TWOCAPTCHA_API_KEY"
            )

        try:
            self.solver = TwoCaptcha(self.api_key)
            logging.info("CaptchaSolver inicializado com sucesso")
        except Exception as e:
            logging.error(f"Erro ao inicializar CaptchaSolver: {e}")
            raise

    def solve_image_from_url(self, url: str, **kwargs) -> str:
        """Resolve um captcha de imagem a partir de uma URL.

        Args:
            url: URL da imagem do captcha.
            **kwargs: Parâmetros adicionais para o solver.

        Returns:
            Código do captcha resolvido.

        Raises:
            ApiException: Se houver erro na API do 2Captcha.
            NetworkException: Se houver erro de rede.
            TimeoutException: Se o tempo limite for excedido.

        Example:
            >>> solver.solve_image_from_url("https://site.com/captcha.png")
            "ABC123"
        """
        try:
            logging.info(f"Resolvendo captcha da URL: {url}")
            result = self.solver.normal(file=url, **kwargs)
            code = result.get('code', '')
            logging.info(f"Captcha resolvido com sucesso: {code}")
            return code
        except ApiException as e:
            logging.error(f"Erro na API do 2Captcha: {e}")
            raise
        except NetworkException as e:
            logging.error(f"Erro de rede ao resolver captcha: {e}")
            raise
        except TimeoutException as e:
            logging.error(f"Timeout ao resolver captcha: {e}")
            raise
        except Exception as e:
            logging.error(f"Erro inesperado ao resolver captcha: {e}")
            raise

    def solve_image_from_file(self, image_path: str, **kwargs) -> str:
        """Resolve um captcha de imagem a partir de um arquivo local.

        Args:
            image_path: Caminho do arquivo de imagem do captcha.
            **kwargs: Parâmetros adicionais para o solver.

        Returns:
            Código do captcha resolvido.

        Raises:
            FileNotFoundError: Se o arquivo não existir.
            ApiException: Se houver erro na API do 2Captcha.

        Example:
            >>> solver.solve_image_from_file("/path/to/captcha.png")
            "ABC123"
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Arquivo de captcha não encontrado: {image_path}")

        try:
            logging.info(f"Resolvendo captcha do arquivo: {image_path}")
            result = self.solver.normal(file=image_path, **kwargs)
            code = result.get('code', '')
            logging.info(f"Captcha resolvido com sucesso: {code}")
            return code
        except ApiException as e:
            logging.error(f"Erro na API do 2Captcha: {e}")
            raise
        except Exception as e:
            logging.error(f"Erro ao resolver captcha: {e}")
            raise

    def solve_recaptcha_v2(
        self,
        site_key: str,
        url: str,
        invisible: bool = False,
        **kwargs
    ) -> str:
        """Resolve um reCAPTCHA v2.

        Args:
            site_key: Site key do reCAPTCHA.
            url: URL da página onde o captcha está presente.
            invisible: Se True, resolve reCAPTCHA invisível.
            **kwargs: Parâmetros adicionais para o solver.

        Returns:
            Token do reCAPTCHA resolvido.

        Raises:
            ApiException: Se houver erro na API do 2Captcha.

        Example:
            >>> solver.solve_recaptcha_v2("6Le-wvkSAAAAAPBMRTvw...", "https://site.com")
            "03AGdBq25..."
        """
        try:
            logging.info(f"Resolvendo reCAPTCHA v2 para URL: {url}")
            result = self.solver.recaptcha(
                sitekey=site_key,
                url=url,
                invisible=1 if invisible else 0,
                **kwargs
            )
            code = result.get('code', '')
            logging.info("reCAPTCHA v2 resolvido com sucesso")
            return code
        except ApiException as e:
            logging.error(f"Erro na API do 2Captcha: {e}")
            raise
        except Exception as e:
            logging.error(f"Erro ao resolver reCAPTCHA v2: {e}")
            raise

    def solve_recaptcha_v3(
        self,
        site_key: str,
        url: str,
        action: str = "verify",
        min_score: float = 0.3,
        **kwargs
    ) -> str:
        """Resolve um reCAPTCHA v3.

        Args:
            site_key: Site key do reCAPTCHA.
            url: URL da página onde o captcha está presente.
            action: Ação do reCAPTCHA.
            min_score: Score mínimo desejado (0.1 a 0.9).
            **kwargs: Parâmetros adicionais para o solver.

        Returns:
            Token do reCAPTCHA resolvido.

        Raises:
            ApiException: Se houver erro na API do 2Captcha.

        Example:
            >>> solver.solve_recaptcha_v3("6Le-wvkSAAAAAPBMRTvw...", "https://site.com")
            "03AGdBq25..."
        """
        try:
            logging.info(f"Resolvendo reCAPTCHA v3 para URL: {url}")
            result = self.solver.recaptcha(
                sitekey=site_key,
                url=url,
                version='v3',
                action=action,
                score=min_score,
                **kwargs
            )
            code = result.get('code', '')
            logging.info("reCAPTCHA v3 resolvido com sucesso")
            return code
        except ApiException as e:
            logging.error(f"Erro na API do 2Captcha: {e}")
            raise
        except Exception as e:
            logging.error(f"Erro ao resolver reCAPTCHA v3: {e}")
            raise

    def get_balance(self) -> float:
        """Retorna o saldo disponível na conta do 2Captcha.

        Returns:
            Saldo em USD.

        Raises:
            ApiException: Se houver erro ao consultar o saldo.

        Example:
            >>> solver.get_balance()
            10.50
        """
        try:
            balance = self.solver.balance()
            logging.info(f"Saldo atual: ${balance}")
            return float(balance)
        except Exception as e:
            logging.error(f"Erro ao consultar saldo: {e}")
            raise

    def __repr__(self) -> str:
        """Representação em string do objeto CaptchaSolver."""
        masked_key = f"{self.api_key[:8]}..." if len(self.api_key) > 8 else "***"
        return f"CaptchaSolver(api_key='{masked_key}')"


# Mantém compatibilidade com código legado
class Captcha(CaptchaSolver):
    """Classe de compatibilidade com código legado.

    Deprecated: Use CaptchaSolver diretamente.
    """

    def __init__(self, api_key: Optional[str] = None) -> None:
        """Inicializa Captcha (compatibilidade legado).

        Args:
            api_key: Chave de API do 2Captcha.
        """
        # Se não fornecido, tenta pegar de env, se não existir usa string vazia
        if api_key is None:
            api_key = os.getenv("TWOCAPTCHA_API_KEY")
            if not api_key:
                logging.warning(
                    "API key do 2Captcha não configurada. "
                    "Configure a variável de ambiente TWOCAPTCHA_API_KEY"
                )
                api_key = ""  # Mantém comportamento legado

        # Inicializa solver mesmo com key vazia para compatibilidade
        self.api_key = api_key
        if api_key:
            self.solver = TwoCaptcha(api_key)
        else:
            self.solver = None
            logging.warning("CaptchaSolver inicializado sem API key válida")

    def solve_normal_url(self, url: str) -> str:
        """Método legado - use solve_image_from_url().

        Deprecated: Use CaptchaSolver.solve_image_from_url() diretamente.
        """
        if not self.solver:
            raise ValueError("API key não configurada")
        return self.solve_image_from_url(url)

    def solve_normal_image(self, image: str) -> str:
        """Método legado - use solve_image_from_file().

        Deprecated: Use CaptchaSolver.solve_image_from_file() diretamente.
        """
        if not self.solver:
            raise ValueError("API key não configurada")
        return self.solve_image_from_file(image)

    def solve_recaptcha_v2(self, site_key: str, url: str) -> str:
        """Método legado mantido para compatibilidade.

        Deprecated: Use CaptchaSolver.solve_recaptcha_v2() diretamente.
        """
        if not self.solver:
            raise ValueError("API key não configurada")
        return super().solve_recaptcha_v2(site_key, url)
