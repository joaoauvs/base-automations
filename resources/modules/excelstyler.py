import openpyxl
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Side
from openpyxl.utils import get_column_letter


class ExcelStyler:
    
    @staticmethod
    def adjust_column_width(worksheet):
        """
        Ajusta a largura das colunas de uma planilha do Excel baseado no tamanho do conteúdo das células.
        
        Args:
        - worksheet: A planilha do Excel a ser ajustada.
        """
        for column in worksheet.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    cell_value_length = len(str(cell.value))
                    if cell_value_length > max_length:
                        max_length = cell_value_length
                except:
                    pass
            adjusted_width = (max_length + 2)
            worksheet.column_dimensions[column[0].column_letter].width = adjusted_width

    @staticmethod
    def adjust_alignment_in_column(worksheet, column_letter, horizontal='center', vertical='center'):
        """
        Ajusta o alinhamento das células em uma coluna específica de uma planilha do Excel.
        
        Args:
        - worksheet: A planilha do Excel a ser ajustada.
        - column_letter: A letra da coluna a ser ajustada.
        - alignment: O alinhamento desejado (padrão é centralizado horizontal e verticalmente).
        """
        for row in worksheet.iter_rows():
            for cell in row:
                if cell.column_letter == column_letter:
                    cell.alignment = Alignment(horizontal=horizontal, vertical=vertical, wrap_text=True)

    @staticmethod
    def center_text_in_cells_except(worksheet, exclude_columns=[]):
        """
        Centraliza o texto em todas as células de uma planilha do Excel, exceto nas colunas excluídas.
        
        Args:
        - worksheet: A planilha do Excel a ser ajustada.
        - exclude_columns: Lista de colunas que não devem ser ajustadas.
        """
        for row in worksheet.iter_rows():
            for cell in row:
                if cell.column_letter not in exclude_columns:
                    cell.alignment = Alignment(horizontal='center', vertical='center')
    
    @staticmethod
    def center_text_in_cells(worksheet):
        """
        Centraliza o texto em todas as células de uma planilha do Excel.
        
        Args:
        - worksheet: A planilha do Excel a ser ajustada.
        """
        for row in worksheet.iter_rows():
            for cell in row:
                cell.alignment = Alignment(horizontal='center', vertical='center')
    
    @staticmethod
    def add_borders_to_cells(worksheet):
        """
        Adiciona bordas a todas as células de uma planilha do Excel.
        
        Args:
        - worksheet: A planilha do Excel a ser ajustada.
        """
        border = Border(left=Side(style='thin'),
                        right=Side(style='thin'),
                        top=Side(style='thin'),
                        bottom=Side(style='thin'))
        
        for row in worksheet.iter_rows():
            for cell in row:
                cell.border = border