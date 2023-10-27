import time

from twocaptcha import TwoCaptcha


class Captcha:
    """
    Classe responsável por resolver captchas utilizando o serviço 2Captcha.
    """

    def __init__(self):
        """
        Inicializa uma nova instância da classe Captcha com a chave de API do 2Captcha.
        """
        self.api_key = '' # Coloque sua chave de API do 2Captcha aqui
        self.solver = TwoCaptcha(self.api_key)
        

    def solve_normal_url(self, url):
        """
        Resolve um captcha normal fornecido por uma URL.

        Args:
            url (str): URL da imagem do captcha a ser resolvida.

        Returns:
            str: Código do captcha resolvido.
        """
        result = self.solver.normal(file=url)
        return result['code']

    def solve_normal_image(self, image):
        """
        Resolve um captcha normal a partir de uma imagem.

        Args:
            image (str): Caminho do arquivo de imagem do captcha ou objeto de imagem.

        Returns:
            str: Código do captcha resolvido.
        """
        result = self.solver.normal(file=image)
        return result['code']
    
    def solve_recaptcha_v2(self, site_key, url):
        """
        Resolve um captcha reCAPTCHA v2.

        Args:
            site_key (str): Site key do captcha reCAPTCHA v2.
            url (str): URL da página onde o captcha está presente.

        Returns:
            str: Código do captcha resolvido.
        """
        result = self.solver.recaptcha(sitekey=site_key, url=url)
        return result['code']
