"""Módulo para conversões de datas e formatos.

Este módulo fornece utilitários para conversão e formatação de datas,
especialmente útil para processamento de datas em português brasileiro.
"""

import calendar
from datetime import datetime
from typing import Tuple


class DateConverter:
    """Conversor de formatos de data.

    Fornece métodos estáticos para converter datas entre diferentes formatos,
    com suporte para nomes de meses em português.

    Example:
        >>> DateConverter.to_first_day_of_month("Jan/2024")
        "01/01/2024"
        >>> DateConverter.to_last_day_of_month("Jan/2024")
        "31/01/2024"
    """

    # Constantes para nomes de meses
    MONTHS_FULL = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    MONTHS_ABBREV_MAP = {
        'Jan': 'Janeiro',
        'Fev': 'Fevereiro',
        'Mar': 'Março',
        'Abr': 'Abril',
        'Mai': 'Maio',
        'Jun': 'Junho',
        'Jul': 'Julho',
        'Ago': 'Agosto',
        'Set': 'Setembro',
        'Out': 'Outubro',
        'Nov': 'Novembro',
        'Dez': 'Dezembro'
    }

    @staticmethod
    def to_first_day_of_month(date_str: str, input_format: str = '%b/%Y') -> str:
        """Converte data para o primeiro dia do mês.

        Args:
            date_str: String da data no formato especificado.
            input_format: Formato da data de entrada (padrão: 'Mês/Ano').

        Returns:
            Data formatada como "01/MM/YYYY".

        Raises:
            ValueError: Se a data não puder ser parseada.

        Example:
            >>> DateConverter.to_first_day_of_month("Jan/2024")
            "01/01/2024"
        """
        try:
            date_obj = datetime.strptime(date_str.lower(), input_format)
            return date_obj.strftime("01/%m/%Y")
        except ValueError as e:
            raise ValueError(f"Erro ao converter data '{date_str}': {e}") from e

    @staticmethod
    def to_last_day_of_month(date_str: str, input_format: str = '%b/%Y') -> str:
        """Converte data para o último dia do mês.

        Args:
            date_str: String da data no formato especificado.
            input_format: Formato da data de entrada (padrão: 'Mês/Ano').

        Returns:
            Data formatada como "DD/MM/YYYY" (último dia do mês).

        Raises:
            ValueError: Se a data não puder ser parseada.

        Example:
            >>> DateConverter.to_last_day_of_month("Jan/2024")
            "31/01/2024"
        """
        try:
            date_obj = datetime.strptime(date_str.lower(), input_format)
            last_day = calendar.monthrange(date_obj.year, date_obj.month)[1]
            return date_obj.strftime(f"{last_day}/%m/%Y")
        except ValueError as e:
            raise ValueError(f"Erro ao converter data '{date_str}': {e}") from e

    @staticmethod
    def to_year_and_month_name(date_str: str, input_format: str = '%b/%Y') -> Tuple[int, str]:
        """Converte data para ano e nome do mês por extenso.

        Args:
            date_str: String da data no formato especificado.
            input_format: Formato da data de entrada (padrão: 'Mês/Ano').

        Returns:
            Tupla contendo (ano, nome_do_mês).

        Raises:
            ValueError: Se a data não puder ser parseada.

        Example:
            >>> DateConverter.to_year_and_month_name("Jan/2024")
            (2024, "Janeiro")
        """
        try:
            date_obj = datetime.strptime(date_str.lower(), input_format)
            month_name = DateConverter.MONTHS_FULL[date_obj.month - 1]
            return date_obj.year, month_name
        except ValueError as e:
            raise ValueError(f"Erro ao converter data '{date_str}': {e}") from e
        except IndexError as e:
            raise ValueError(f"Mês inválido na data '{date_str}'") from e

    @staticmethod
    def expand_month_name(date_str: str) -> str:
        """Expande abreviação de mês para nome completo.

        Args:
            date_str: Data no formato "Abr/YYYY".

        Returns:
            Data com mês por extenso "Abril/YYYY".

        Raises:
            ValueError: Se a abreviação do mês não for reconhecida.

        Example:
            >>> DateConverter.expand_month_name("Jan/2024")
            "Janeiro/2024"
        """
        try:
            month_abbrev, year = date_str.split("/")
            if month_abbrev not in DateConverter.MONTHS_ABBREV_MAP:
                raise ValueError(f"Abreviação de mês desconhecida: {month_abbrev}")
            month_full = DateConverter.MONTHS_ABBREV_MAP[month_abbrev]
            return f"{month_full}/{year}"
        except ValueError as e:
            if "not enough values" in str(e) or "too many values" in str(e):
                raise ValueError(f"Formato de data inválido: '{date_str}'. Esperado: 'Mês/Ano'") from e
            raise

    @staticmethod
    def get_month_name(month_number: int) -> str:
        """Retorna o nome do mês por extenso dado seu número.

        Args:
            month_number: Número do mês (1-12).

        Returns:
            Nome do mês por extenso.

        Raises:
            ValueError: Se o número do mês for inválido.

        Example:
            >>> DateConverter.get_month_name(1)
            "Janeiro"
        """
        if not 1 <= month_number <= 12:
            raise ValueError(f"Número de mês inválido: {month_number}. Esperado: 1-12")
        return DateConverter.MONTHS_FULL[month_number - 1]

    @staticmethod
    def get_month_number(month_abbrev: str) -> int:
        """Retorna o número do mês dada sua abreviação.

        Args:
            month_abbrev: Abreviação do mês (ex: "Jan", "Fev").

        Returns:
            Número do mês (1-12).

        Raises:
            ValueError: Se a abreviação não for reconhecida.

        Example:
            >>> DateConverter.get_month_number("Jan")
            1
        """
        if month_abbrev not in DateConverter.MONTHS_ABBREV_MAP:
            raise ValueError(f"Abreviação de mês desconhecida: {month_abbrev}")

        month_full = DateConverter.MONTHS_ABBREV_MAP[month_abbrev]
        return DateConverter.MONTHS_FULL.index(month_full) + 1


# Mantém compatibilidade com código legado
class Conversions(DateConverter):
    """Classe de compatibilidade com código legado.

    Deprecated: Use DateConverter diretamente.
    """

    @staticmethod
    def convert_date_to_string_first_day_month(data: str) -> str:
        """Método legado - use to_first_day_of_month().

        Deprecated: Use DateConverter.to_first_day_of_month() diretamente.
        """
        return DateConverter.to_first_day_of_month(data)

    @staticmethod
    def convert_date_to_string_last_day_month(data: str) -> str:
        """Método legado - use to_last_day_of_month().

        Deprecated: Use DateConverter.to_last_day_of_month() diretamente.
        """
        return DateConverter.to_last_day_of_month(data)

    @staticmethod
    def convert_date_to_year_month(data: str) -> Tuple[int, str]:
        """Método legado - use to_year_and_month_name().

        Deprecated: Use DateConverter.to_year_and_month_name() diretamente.
        """
        return DateConverter.to_year_and_month_name(data)

    @staticmethod
    def convert_month(date: str) -> str:
        """Método legado - use expand_month_name().

        Deprecated: Use DateConverter.expand_month_name() diretamente.
        """
        return DateConverter.expand_month_name(date)
