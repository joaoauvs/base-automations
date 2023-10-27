import json
import logging
import re
from datetime import datetime, timedelta
from typing import Union


class Validate:
    """
    Classe responsável pela validação de diferentes tipos de dados e formatos.
    """

    @staticmethod
    def validate_dictionary(mensagem: dict) -> bool:
        """
        Valida se todos os campos do dicionário possuem valores não vazios.

        Args:
            mensagem (dict): Dicionário a ser validado.

        Returns:
            bool: Retorna True se todos os campos têm valores não vazios e False caso contrário.
        """
        return all(value for value in mensagem.values())

    @staticmethod
    def return_empty_fields(mensagem: dict) -> list:
        """
        Identifica e retorna os campos do dicionário que estão vazios.

        Args:
            mensagem (dict): Dicionário a ser verificado.

        Returns:
            list: Lista contendo as chaves dos campos vazios no dicionário.
        """
        return [key for key, value in mensagem.items() if not value]

    @staticmethod
    def is_start_date_greater_than_end_date(start_date: str, end_date: str) -> bool:
        """
        Verifica se a data de início é maior que a data de término.

        Args:
            start_date (str): Data de início no formato 'dd/mm/yyyy'.
            end_date (str): Data de término no formato 'dd/mm/yyyy'.

        Returns:
            bool: Retorna True se a data de início for menor ou igual à data de término, False caso contrário.

        Raises:
            logging.error: Registra um erro caso haja um problema ao converter as strings para objetos datetime.
        """
        try:
            start_date = datetime.strptime(start_date, '%d/%m/%Y')
            end_date = datetime.strptime(end_date, '%d/%m/%Y')
            return start_date <= end_date
        except Exception as e:
            logging.error(f'Error checking if start date is greater than end date: {e}')
            return False

    @staticmethod
    def validate_cnpj(cnpj: str) -> Union[bool, str]:
        """
        Valida um CNPJ fornecido.

        Args:
            cnpj (str): String contendo o CNPJ a ser validado.

        Returns:
            Union[bool, str]: Retorna False se o CNPJ é inválido. Retorna o CNPJ formatado se for válido.

        Raises:
            ValueError: Se a string de entrada não for um CNPJ válido.
        """
        cnpj = re.sub(r'[^0-9]', '', cnpj)

        if len(cnpj) != 14 or any(cnpj.count("{}".format(i)) == 14 for i in range(10)):
            return False

        first_digit = Validate._generate_first_digit(cnpj)
        second_digit = Validate._generate_second_digit(cnpj)

        if first_digit == cnpj[12] and second_digit == cnpj[13]:
            return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
        else:
            return False