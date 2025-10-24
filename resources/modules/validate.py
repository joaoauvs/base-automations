"""Módulo para validação de dados e documentos.

Este módulo fornece funções de validação para diferentes tipos de dados,
incluindo dicionários, datas e documentos brasileiros (CNPJ, CPF).
"""

import logging
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Union


class Validator:
    """Validador de dados e documentos.

    Fornece métodos estáticos para validação de diferentes tipos de dados
    como dicionários, datas, CNPJ e CPF.

    Example:
        >>> Validator.validate_cnpj("12.345.678/0001-90")
        "12.345.678/0001-90"  # Se válido
        >>> Validator.validate_cpf("123.456.789-09")
        "123.456.789-09"  # Se válido
    """

    @staticmethod
    def validate_dictionary(data: Dict[str, Any], required_fields: Optional[List[str]] = None) -> bool:
        """Valida se todos os campos obrigatórios do dicionário possuem valores não vazios.

        Args:
            data: Dicionário a ser validado.
            required_fields: Lista de campos obrigatórios. Se None, valida todos os campos.

        Returns:
            True se todos os campos obrigatórios têm valores não vazios.

        Example:
            >>> Validator.validate_dictionary({"nome": "João", "idade": 30})
            True
            >>> Validator.validate_dictionary({"nome": "", "idade": 30})
            False
        """
        if required_fields is None:
            return all(value for value in data.values())

        return all(data.get(field) for field in required_fields)

    @staticmethod
    def return_empty_fields(data: Dict[str, Any]) -> List[str]:
        """Identifica e retorna os campos do dicionário que estão vazios.

        Args:
            data: Dicionário a ser verificado.

        Returns:
            Lista contendo as chaves dos campos vazios.

        Example:
            >>> Validator.return_empty_fields({"nome": "João", "email": ""})
            ["email"]
        """
        return [key for key, value in data.items() if not value]

    @staticmethod
    def is_valid_date_range(start_date: str, end_date: str, date_format: str = '%d/%m/%Y') -> bool:
        """Verifica se a data de início é menor ou igual à data de término.

        Args:
            start_date: Data de início.
            end_date: Data de término.
            date_format: Formato das datas (padrão: 'dd/mm/yyyy').

        Returns:
            True se o intervalo de datas for válido.

        Raises:
            ValueError: Se as datas não puderem ser parseadas.

        Example:
            >>> Validator.is_valid_date_range("01/01/2024", "31/12/2024")
            True
        """
        try:
            start = datetime.strptime(start_date, date_format)
            end = datetime.strptime(end_date, date_format)
            return start <= end
        except ValueError as e:
            logging.error(f'Erro ao validar intervalo de datas: {e}')
            raise ValueError(f"Formato de data inválido. Esperado: {date_format}") from e

    @staticmethod
    def _calculate_cnpj_digit(cnpj: str, weights: List[int]) -> str:
        """Calcula um dígito verificador do CNPJ.

        Args:
            cnpj: String do CNPJ (apenas números).
            weights: Lista de pesos para o cálculo.

        Returns:
            Dígito verificador calculado.
        """
        total = sum(int(cnpj[i]) * weights[i] for i in range(len(weights)))
        remainder = total % 11
        return '0' if remainder < 2 else str(11 - remainder)

    @staticmethod
    def validate_cnpj(cnpj: str) -> Union[bool, str]:
        """Valida um CNPJ brasileiro.

        Args:
            cnpj: String contendo o CNPJ (com ou sem formatação).

        Returns:
            CNPJ formatado se válido, False caso contrário.

        Example:
            >>> Validator.validate_cnpj("12345678000190")
            "12.345.678/0001-90"
            >>> Validator.validate_cnpj("00000000000000")
            False
        """
        # Remove caracteres não numéricos
        cnpj_clean = re.sub(r'[^0-9]', '', cnpj)

        # Verifica se tem 14 dígitos e não é sequência repetida
        if len(cnpj_clean) != 14 or len(set(cnpj_clean)) == 1:
            return False

        # Calcula primeiro dígito verificador
        weights_first = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        first_digit = Validator._calculate_cnpj_digit(cnpj_clean, weights_first)

        # Calcula segundo dígito verificador
        weights_second = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        second_digit = Validator._calculate_cnpj_digit(cnpj_clean, weights_second)

        # Verifica se os dígitos calculados conferem
        if first_digit == cnpj_clean[12] and second_digit == cnpj_clean[13]:
            return f"{cnpj_clean[:2]}.{cnpj_clean[2:5]}.{cnpj_clean[5:8]}/{cnpj_clean[8:12]}-{cnpj_clean[12:]}"

        return False

    @staticmethod
    def _calculate_cpf_digit(cpf: str, weights: List[int]) -> str:
        """Calcula um dígito verificador do CPF.

        Args:
            cpf: String do CPF (apenas números).
            weights: Lista de pesos para o cálculo.

        Returns:
            Dígito verificador calculado.
        """
        total = sum(int(cpf[i]) * weights[i] for i in range(len(weights)))
        remainder = total % 11
        return '0' if remainder < 2 else str(11 - remainder)

    @staticmethod
    def validate_cpf(cpf: str) -> Union[bool, str]:
        """Valida um CPF brasileiro.

        Args:
            cpf: String contendo o CPF (com ou sem formatação).

        Returns:
            CPF formatado se válido, False caso contrário.

        Example:
            >>> Validator.validate_cpf("12345678909")
            "123.456.789-09"
            >>> Validator.validate_cpf("00000000000")
            False
        """
        # Remove caracteres não numéricos
        cpf_clean = re.sub(r'[^0-9]', '', cpf)

        # Verifica se tem 11 dígitos e não é sequência repetida
        if len(cpf_clean) != 11 or len(set(cpf_clean)) == 1:
            return False

        # Calcula primeiro dígito verificador
        weights_first = list(range(10, 1, -1))
        first_digit = Validator._calculate_cpf_digit(cpf_clean, weights_first)

        # Calcula segundo dígito verificador
        weights_second = list(range(11, 1, -1))
        second_digit = Validator._calculate_cpf_digit(cpf_clean, weights_second)

        # Verifica se os dígitos calculados conferem
        if first_digit == cpf_clean[9] and second_digit == cpf_clean[10]:
            return f"{cpf_clean[:3]}.{cpf_clean[3:6]}.{cpf_clean[6:9]}-{cpf_clean[9:]}"

        return False

    @staticmethod
    def validate_email(email: str) -> bool:
        """Valida um endereço de email.

        Args:
            email: String contendo o email.

        Returns:
            True se o email for válido.

        Example:
            >>> Validator.validate_email("usuario@exemplo.com")
            True
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_phone(phone: str, require_ddd: bool = True) -> Union[bool, str]:
        """Valida um número de telefone brasileiro.

        Args:
            phone: String contendo o telefone.
            require_ddd: Se True, exige DDD no telefone.

        Returns:
            Telefone formatado se válido, False caso contrário.

        Example:
            >>> Validator.validate_phone("11987654321")
            "(11) 98765-4321"
        """
        # Remove caracteres não numéricos
        phone_clean = re.sub(r'[^0-9]', '', phone)

        # Telefone com DDD (11 dígitos para celular, 10 para fixo)
        if require_ddd:
            if len(phone_clean) == 11:  # Celular
                return f"({phone_clean[:2]}) {phone_clean[2:7]}-{phone_clean[7:]}"
            elif len(phone_clean) == 10:  # Fixo
                return f"({phone_clean[:2]}) {phone_clean[2:6]}-{phone_clean[6:]}"
            return False
        else:
            # Telefone sem DDD
            if len(phone_clean) == 9:  # Celular
                return f"{phone_clean[:5]}-{phone_clean[5:]}"
            elif len(phone_clean) == 8:  # Fixo
                return f"{phone_clean[:4]}-{phone_clean[4:]}"
            return False


# Mantém compatibilidade com código legado
class Validate(Validator):
    """Classe de compatibilidade com código legado.

    Deprecated: Use Validator diretamente.
    """

    @staticmethod
    def is_start_date_greater_than_end_date(start_date: str, end_date: str) -> bool:
        """Método legado - use is_valid_date_range().

        Deprecated: Use Validator.is_valid_date_range() diretamente.
        """
        return Validator.is_valid_date_range(start_date, end_date)

    @staticmethod
    def _generate_first_digit(cnpj: str) -> str:
        """Método legado para compatibilidade."""
        weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        return Validator._calculate_cnpj_digit(cnpj, weights)

    @staticmethod
    def _generate_second_digit(cnpj: str) -> str:
        """Método legado para compatibilidade."""
        weights = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        return Validator._calculate_cnpj_digit(cnpj, weights)
