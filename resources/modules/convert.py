import calendar
from datetime import datetime


class Conversions:

    @staticmethod
    def convert_date_to_string_first_day_month(data):
        data = data.lower()
        date_object = datetime.strptime(data, '%b/%Y')
        return date_object.strftime("01/%m/%Y")

    @staticmethod
    def convert_date_to_string_last_day_month(data):
        data = data.lower()
        date_object = datetime.strptime(data, '%b/%Y')
        last_day = calendar.monthrange(date_object.year, date_object.month)[1]
        return date_object.strftime(f"{last_day}/%m/%Y")

    @staticmethod
    def convert_date_to_year_month(data):
        data = data.lower()
        date_object = datetime.strptime(data, '%b/%Y')
        meses = [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]
        return date_object.year, meses[date_object.month - 1]

    @staticmethod
    def convert_month(date):
        months = {
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
        month, year = date.split("/")
        return f"{months[month]}/{year}"
